#!/bin/bash
echo
ls .*.sw* 2> /dev/null
[ $? -eq 2 ] && echo -e "\t\t\e[32mNO TRASH\e[0m" && exit
echo -e "\e[32m--------------------\e[0m"
while :
read -p "sure? " s
do
	if [[ ${s:=yes} =~ yes ]];then
		rm .*.sw*
		echo -e "\t\t\e[32mTRASH CLEANED UP\e[0m"
		exit
	elif [[ $s =~ no ]];then
		exit
	else
		echo -e "\e[32myes|no\e[0m"
	fi
done
		
