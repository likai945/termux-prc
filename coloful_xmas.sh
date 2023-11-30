#!/bin/bash
read -p 'floor: ' f
n=${f:=9}

function prt(){
	for j in `seq $1`
	do
		color=$[RANDOM%7+31]
		[ $j -le $2 ] && brick=' ' || brick='*'
		echo -ne "\e[${color}m${brick}"
	done
	echo
}

for i in `seq $n`
do
	blk_num=$[n-i]
	prt $[i+n-1] $blk_num
done

[ $n -gt 3 -a $n -lt 10 ] && trunk=1 || trunk=$[n/10]
for i in `seq $trunk`
do
prt $n $[n-1]
done
