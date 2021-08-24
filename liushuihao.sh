#!/bin/bash
sc=236
jt=`date +%j`
i=18
count(){
	while [ 1 ];do
		read -p "count? " c
		if [[ ${c:="yes"} == "yes" ]];then
			echo -e "\t$i"
			let i++
			sed -i "/^i=/s/^.*$/i=$i/" $0
		elif [[ "$c" =~ "quit" ]];then
			sed -i "/^i=/s/^.*$/i=$i/" $0
			break
		fi
	done
}

######the main######

if [ "$jt" != "$sc" ];then
	i=1
	sed -i "/^sc=/s/^.*$/sc=$jt/" $0
	count
else
	count
fi
