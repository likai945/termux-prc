#!/bin/bash
#####check if the pics not shotted this day#####
listNotThisDayShots(){
	rq=`ls -lR | grep -E '\.sh' | awk '{print $6,$7}' | sort | uniq | wc -l`
	[ $rq -gt 1 ] && \
	echo -e '\e[42mScreenshots not this day:\e[0m' && \
	ls -lR | grep '\.sh' | grep -v "`date "+%b %e"`" | awk '{print $NF}' || \
	echo -e "\e[44mall pictures screenshotted this day.\e[0m"
}
#####check if there are any empty directories#####
listEmptyDir(){
	echo -e '\e[42mempty directories:\e[0m' 
ls -R | sed -n '/:/,+1p' | sed -n '/^$/{x;p};h'
ls -R | sed -n '/:/,+1p' | tail -1 | grep ':'
}
ifNoEmptyDir(){
	echo -e '\e[44mno mempty directories:\e[0m' 
}
fork(){
	mn=`ls -R | sed -n '/:/,+1p' | sed -n '/^$/{x;p};h' | wc -l`
	en=`ls -R | sed -n '/:/,+1p' | tail -1 | grep ':' | wc -l`
	[ $[mn+en] -eq 0 ] #&& return 0 
}
#######the program######
listNotThisDayShots
if fork;then 
	ifNoEmptyDir
else
	listEmptyDir
fi
