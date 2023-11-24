#!/bin/bash
read -p 'floor: ' f
n=${f:=9}
for i in `seq $n`
do
	#star_num=$[i*2-1]
	blk_num=$[n-i]
	color=$[RANDOM%7+31]
	for j in `seq $[i+n-1]` #blk_num + star_num
		do
		[ $j -le $blk_num ] && brick=' ' || brick='*'
		echo -ne "\e[${color}m${brick}"
	done
	echo -e "\e[0m"
done
