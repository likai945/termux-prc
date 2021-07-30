#!/bin/bash
line(){
	for i in $(seq `echo "$1" | wc -L`)
	do
		echo -en '\e[33m-\e[0m'
	done
		echo
}
check(){
	while [ 1 ]
	do
		read -p "screenshot ${1##*/}?" e
		if [ ${e:="yes"} == "yes" ];then
			cd $1
			line `pwd`
			pwd
			line `pwd`
			ls
			break
		elif [ $e == "no" ];then
			break
		else
			echo "yes or no"
		fi
	done
}
####the program####
check /data/data/com.termux/files/home/playground 
check ..
