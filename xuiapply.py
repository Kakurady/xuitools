#!/usr/bin/env python2.7

import xml.dom
#import re
from xml.dom.minidom import parse, parseString
import sys, os.path
import re

#patch up minidom
if not hasattr( xml.dom.minidom.NamedNodeMap, '__contains__' ):
	xml.dom.minidom.NamedNodeMap.__contains__ = xml.dom.minidom.NamedNodeMap.has_key


infile = "/home/nekoyasha/wget.po"
infile2 = "/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/zh/floater_env_settings.xml"

messages = {}
def read_catalog(filename):
	with open(filename) as f:
		lines = []
		msgid = ""
		msgstr = ""
		fuzzy = False
		next_fuzzy = False
		for line in f:
			filt = line.decode('utf_8').strip()
			try:
				if filt[0] == u'"': 
					#print "continuation", filt
					lines.extend(filt[1:-1])
					pass
				elif filt[0:2] == u'#,': 
					#print "flags", filt
					if u"fuzzy" in filt:
						next_fuzzy = True
						#sys.stderr.write("fuzzy!\n")
					else:
						pass
						#sys.stderr.write("not fuzzy.\n")
					pass
				elif filt[0:5] == u'msgid': 
					if not fuzzy:
						msgstr = "".join(lines).replace(u'\\n', u'\n').strip()
						lower = msgid.lower()
						messages[lower] = msgstr
						
						#also put in variations
						try:
							if lower[-1:] == ":":
								if lower[0:-1] not in messages:
									#sys.stderr.write("found colon {0} \n".format(lower))
									if msgstr[-1:] == ":":
										messages[lower[0:-1]] = msgstr[0:-1]
									else:
										messages[lower[0:-1]] = msgstr										
							elif lower[-3:] == "...":
								if lower[0:-3] not in messages:
									#sys.stderr.write("found dot dot dot {0} \n".format(lower))
									if msgstr[-3:] == "...":
										messages[lower[0:-3]] = msgstr[0:-3]
									else:
										messages[lower[0:-3]] = msgstr
							if len(lower) > 40:
								nowhite = re.sub(ur'\s+', u" ", lower, flags=re.MULTILINE)
								if nowhite not in messages:
									#sys.stderr.write("found dot dot dot {0} \n".format(lower))
									messages[nowhite] = msgstr
						except IndexError:
							pass
					fuzzy = next_fuzzy
					next_fuzzy = False
					lines = []
					lines.extend(filt[7:-1])
					pass
				elif filt[0:6] == u'msgstr': 
					msgid = "".join(lines).replace(u'\\n', u'\n').strip()
					lines = []
					lines.extend(filt[8:-1])
#					print "msgstr", filt
					pass
				else :
					pass
			except IndexError:
				pass

def scan_translation (Node, document, props):
	my_name = ""
	text = ""
	if Node.hasAttributes():
		for name, value in Node.attributes.items():
			if name == "name":
				continue
			if value.lower() in props.keys():
				Node.attributes[name].value = props[value.lower()]
#		if 'name' in Node.attributes:
#			my_name = Node.attributes['name'].value 
#		else:
#			my_name =  Node.nodeName + some_integer
#			some_integer += 1
	if Node.hasChildNodes():
		Node.normalize()		
		for i in Node.childNodes:
			try:
				if i.nodeType in [xml.dom.Node.TEXT_NODE, xml.dom.Node.CDATA_SECTION_NODE]:
					text = text + i.data
				elif i.nodeType in [xml.dom.Node.COMMENT_NODE]:
					continue
				#Despite being a Node, Text does not have hasAttributes()
				elif i.hasAttributes() and 'name' in i.attributes:
					scan_translation(i, document, props)
			except (AttributeError):
				pass
		text = text.strip()
		if text != "":
			lower = text.lower();
			if lower in props.keys():
#				print text.lower().encode("utf_8"),  props[text.lower()].encode("utf_8")
#				print document.createTextNode(props[text.lower()])
				Node.replaceChild(document.createTextNode(props[lower]), Node.firstChild)
			else:
				if len(lower) > 40:
					nowhite = re.sub(ur'\s+', u" ", lower, flags=re.MULTILINE)
					if nowhite in messages:
						#sys.stderr.write("found dot dot dot {0} \n".format(lower))
						Node.replaceChild(document.createTextNode(props[nowhite]), Node.firstChild)
	
		
if __name__ == "__main__":
	if len(sys.argv) > 1:
		infile  = sys.argv[1]
		infile2  = sys.argv[2]
		read_catalog(infile)
		messages[""] = ""
		#print messages
		dom2 = parse(infile2)
		scan_translation(dom2.documentElement, dom2, messages)
		#print dom2.createTextNode('utf_8')
		print dom2.documentElement.toxml(encoding='utf_8')
#		print dom2.documentElement.toprettyxml(encoding='utf_8')
