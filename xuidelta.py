#!/usr/bin/env python

import xml.dom
#import re
from xml.dom.minidom import parse, parseString
import sys, os.path
import re

#patch up minidom
if not hasattr( xml.dom.minidom.NamedNodeMap, '__contains__' ):
	xml.dom.minidom.NamedNodeMap.__contains__ = xml.dom.minidom.NamedNodeMap.has_key


infile = "/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/en-us/floater_env_settings.xml"
infile2 = "/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/zh/floater_env_settings.xml"

some_integer = 0

def iterDOM (Node):
	attlist = {}
	childlist = {}
	my_name = ""
	text = ""
	if Node.hasAttributes():
		attlist.update(Node.attributes.items())
		if 'name' in Node.attributes:
			my_name = Node.attributes['name'].value 
		else:
			my_name =  Node.nodeName + some_integer
			some_integer += 1
	if Node.hasChildNodes():
		Node.normalize()
		for i in Node.childNodes:
			try:
				if i.nodeType in [xml.dom.Node.TEXT_NODE, xml.dom.Node.CDATA_SECTION_NODE]:
					text = text + i.data
				#Despite being a Node, Text does not have hasAttributes()
				elif i.hasAttributes() and 'name' in i.attributes:
					childlist.update(iterDOM (i))
			except (AttributeError):
				pass
	text = text.strip()
	return {my_name: {'attr': attlist, 'children': childlist, 'text': text}}

def emitPair(msgid, msgstr, comments = "", path=None):
	if msgid == "" and (msgstr == "" or msgstr == " "): return
	if msgid == "":
		sys.stdout.write("#empty msgid, msgstr is {0}\n\n".format(msgstr.replace('"', '\\"').encode('utf_8').splitlines()[0]))
		return
	if path == None: path = os.path.basename(infile)
	sys.stdout.write("#: {reference}\n".format(reference=path).encode('utf_8'))
	sys.stdout.write("msgid ")
	
	if False:
		sys.stdout.write('""\n')
	else:
		lines = re.sub(r'["\\]', r'\\\g<0>', msgid ).encode('utf_8').splitlines();
		#lines = msgid.replace('"', '\\"').encode('utf_8').splitlines();
		sys.stdout.write('"')
		sys.stdout.write('\\n"\n"'.join(lines))
		sys.stdout.write('"\n')
	sys.stdout.write("msgstr ")
	if msgstr == "":
		sys.stdout.write('""\n')
	else:
		lines = re.sub(r'["\\]', r'\\\g<0>', msgstr ).encode('utf_8').splitlines();
		#lines = msgstr.replace('"', '\\"').encode('utf_8').splitlines();
		sys.stdout.write('"')
		sys.stdout.write('\\n"\n"'.join(lines))
		sys.stdout.write('"\n')
	sys.stdout.write('\n')

def iterDOM2 (Node, props):
	my_name = ""
	text = ""
	if Node.hasAttributes():
		for name, value in Node.attributes.items():
			if name == "name":
				continue
			if name in props['attr'].keys():
				emitPair(props['attr'][name], value)
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
					name = i.attributes['name'].value
					if name in props['children'].keys():
						iterDOM2(i, props['children'][name])
			except (AttributeError):
				pass
	text = text.strip()
	if text != "": emitPair(props['text'] , text)

if __name__ == "__main__":
	if len(sys.argv) > 2:
		infile  = sys.argv[1]
		infile2 = sys.argv[2]
		try:
			dom1 = parse(infile)
			a = iterDOM(dom1.documentElement)
			#b = {}; b.update(a); c =  b.popitem()[1];dom2 = parse(infile2)
			c = a.popitem()[1];
			dom2 = parse(infile2)

			iterDOM2(dom2.documentElement, c)
		except (xml.parsers.expat.ExpatError):
			pass
