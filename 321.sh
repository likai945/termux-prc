#!/bin/bash 
l=`cat $1 | wc -l`
for i in `cat $1`
do
	if [ $[j%3] -eq 0 ];then
		line=$i
	else
		line=$line,$i
	fi
	[ $[j%3] -eq 2 ] && echo $line >> $2
	[ $[j+1] -eq $l ] && echo $line >> $2
	let j++
done
