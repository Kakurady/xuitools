#!/bin/bash
#FROM=/home/nekoyasha/Downloads/slviewer-artwork-viewer-1.23.4-r124025/slviewer-artwork-viewer-1.23.4-r124025/linden/indra/newview/skins/default/xui/en-us
FROM=/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/en-us/
TO=/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/zh/

if test $1; then FROM=$1; fi
if test $2; then TO=$2; fi
echo "msgid \"\"
msgstr \"\"
\"Last-Translator: Kakurady <kakurady@gmail.com>\\n\"
\"MIME-Version: 1.0\\n\"
\"Content-Type: text/plain; charset=utf-8\\n\"
\"Content-Transfer-Encoding: 8bit\\n\""

for i in $(ls $FROM/*.xml); do
	echo $(basename $i) >&2
	j=$TO/$(basename $i)
	#if test -f $j; then $(dirname $0)/xuidelta.py $i $j 2>&1; fi
	if test -f $j; then $(dirname $0)/xuidelta.py $i $j; fi
done
	
