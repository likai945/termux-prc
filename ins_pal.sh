#!/bin/bash
#####compute the average temprature of each pool#####
at(){
	tmp_data=`ls -t *.runlog | head -1`
	awk -F '|' '$1~/'$1'/\
	{if ($2~/^[[:digit:]]+$/) \
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}'\
	$tmp_data
}
#####show the information#####
show(){
	tmp_data=`ls -t *.runlog | head -1`
	kx3=`at '-03A-'`
	kx4=`at '-04A-'`
	kx5_srv=`at '05A.*SRV'`
	kx5_dbs=`at '05A.*DBS'`
	echo -e "\e[032m================================"
	echo -e "ITEM\t INPUT_TMP\tCPU_TMP\e[0m"
	echo -e "kx3_dbs\t $kx3"
	echo -e "kx4_dbs\t $kx4"
	echo -e "kx5_srv\t $kx5_srv"
	echo -e "kx5_dbs\t $kx5_dbs"
	echo -e "\e[032m================================\e[0m"
	echo -e "the data comes from $tmp_data"
}
#####check if the pics not shotted this day#####
listNotThisDayShots(){
	rq=`ls -lR | grep -E '\.sh' | awk '{print $6,$7}' | sort | uniq | wc -l`
	if [ $rq -gt 1 ];then
		echo -e '\e[42mScreenshots not this day:\e[0m'
		ls -lR | grep '\.sh' | grep -v "`date "+%b %e"`" | awk '{print $NF}'
	else
		echo -e "\e[44mall pictures screenshotted this day.\e[0m"
	fi
}
#####check if there are any empty directories#####
listEmptyDir(){
	mn=`ls -R | sed -n '/:/,+1p' | sed -n '/^$/{x;p};h' | wc -l`
	en=`ls -R | sed -n '/:/,+1p' | tail -1 | grep ':' | wc -l`
	if [ $[mn+en] -eq 0 ];then
		echo -e '\e[44mno mempty directories:\e[0m' 
	else
		echo -e '\e[42mempty directories:\e[0m' 
		ls -R | sed -n '/:/,+1p' | sed -n '/^$/{x;p};h'
		ls -R | sed -n '/:/,+1p' | tail -1 | grep ':'
	fi
}
#######the program######
case $1 in 
	--at|--AT)
		show;;
	--cf|--CF)
		listNotThisDayShots;
		listEmptyDir;;
	*)
		echo "at|cf"
esac
