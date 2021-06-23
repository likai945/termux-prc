#!/bin/bash
while [ 1 ]
do
	while [ 1 ]
	do
		n=`date +%M`
		[ $n == "00" -o $n == "30" ] && echo -e '\a\a\a' && read -p "acted on `date +%H:%M`? " a
		[[ "$a" =~ "yes" ]] && break
	done
	while [ 1 ]
	do
		n=`date +%M`
		[ $n == "00" -o $n == "30" ] || break
	done
done
