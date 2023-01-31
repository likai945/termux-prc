#!/bin/bash
dos2unix $1 &> /dev/null
>new_$1
for i in `seq $(cat $1 | wc -l)`
do
	l=`sed -n "${i}p" $1`
	if [[ $l =~ ^202.*日$ ]]
	then
		unset j
		line=$l
		echo $line >> new_$1
	elif [[ $l =~ ^[[:space:]]*$ ]]
	then
		echo > /dev/null
	else
		let j++
		line=$j、$l
		echo $line >> new_$1
	fi
done
sed -i 's/ //' new_$1
