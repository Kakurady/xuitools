#!/bin/bash
#FROM=/home/nekoyasha/Downloads/slviewer-artwork-viewer-1.23.4-r124025/slviewer-artwork-viewer-1.23.4-r124025/linden/indra/newview/skins/default/xui/en-us
FROM=/home/nekoyasha/dev/imprudence/nekoyoubi/linden/indra/newview/skins/default/xui/en-us/
TO=/home/nekoyasha/dev/xuitools/zh

if test $1; then FROM=$1; fi
if test $2; then TO=$2; fi


for i in $(ls $FROM/*.xml); do
	echo $(basename $i) >&2
	j=$TO/$(basename $i)
	#if test -f $j; then $(dirname $0)/xuidelta.py $i $j 2>&1; fi
	php $(dirname $0)/xmldropper.php $i > $j~
	$(dirname $0)/xuiapply.py /home/nekoyasha/xuidiff1.po $j~ > $j
done
	
