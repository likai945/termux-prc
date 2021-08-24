#!/bin/bash
sc=23
jt=`date +%j`
i=6
count(){
	while [ 1 ];do
		read -p "count? " c
		if [[ ${c:="yes"} == "yes" ]];then
			echo -e "\t$i"
			let i++
			sed -i "/^i=/s/^.*$/i=$i/" $0
		elif [[ "$c" =~ "quit" ]];then
			exit
		fi
	done
}

######the main######

if [ "$jt" != "$sc" ];then
	i=1
	count
	sed -i "/^sc=/s/^.*$/sc=$jt/" $0
else
	count
fi
