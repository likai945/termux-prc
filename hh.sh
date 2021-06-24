#!/bin/bash
while [ 1 ]
do
	n=`date +%M`
	[ $n == "00" -o $n == "30" ] && echo -e '\a' && echo -n "acted on `date +%H:%M`? " && sleep 61
done
