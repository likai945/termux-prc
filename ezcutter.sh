#!/bin/bash
> sbm
for i in `cat kxxnj`
do
	e=`echo $i | awk -F'-' '{print$8}'`
	[[ $e =~ "ZX" ]] && ne=${e%ZX*}ZX || ne=$e
	echo $ne >> sbm
done
> kxxnj
