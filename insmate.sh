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
	kx3_srv=`at '03A.*SRV'`
	kx3_dbs=`at '03A.*DBS'`
	kx4_srv=`at '04A.*SRV'`
	kx4_dbs=`at '04A.*DBS'`
	kx5_srv=`at '05A.*SRV'`
	kx5_dbs=`at '05A.*DBS'`
	echo -e "\e[032m================================"
	echo -e "ITEM\t INPUT_TMP\tCPU_TMP\e[0m"
	echo -e "kx3_srv\t $kx3_srv"
	echo -e "kx3_dbs\t $kx3_dbs"
	echo -e "kx4_srv\t $kx4_srv"
	echo -e "kx4_dbs\t $kx4_dbs"
	echo -e "kx5_srv\t $kx5_srv"
	echo -e "kx5_dbs\t $kx5_dbs"
	echo -e "\e[032m================================\e[0m"
	echo -e "the data comes from $tmp_data"
}
#####check if the pics not shotted this day#####
listOtherDaysShots(){
	echo -e '\e[42mScreenshots not this day:\e[0m'
	ls -lR | grep -E '.jpg|.png' | grep -v "`date "+%b %e"`" | awk '{print $NF}'
}
checkNotThisDayShots(){
	rq=`ls -lR | grep -E '.jpg|.png' | awk '{print $7,$8}'  | sort | uniq | wc -l`
	if [ $rq -gt 1 ];then
		listOtherDaysShots
	else
		ls -lR | grep -E '.jpg|.png' | grep -q "`date "+%b %e"`" 
		if [ $? -eq 0 ];then
			echo -e "\e[44mall pictures screenshotted this day.\e[0m"
		else
			listOtherDaysShots
		fi
	fi
}
#####check if there are any empty directories#####
listEmptyDir(){
	mn=`ls -R | sed -n '/:/,+1p' | sed -n '/^$/{x;p};h' | wc -l`
	en=`ls -R | sed -n '/:/,+1p' | tail -1 | grep ':' | wc -l`
	if [ $[mn+en] -eq 0 ];then
		echo -e '\e[44mno empty directories.\e[0m' 
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
		checkNotThisDayShots;
		listEmptyDir;;
	*)
		echo -e "\e[32m--at\e[0m\tshow the average of tempratures."
		echo -e "\e[32m--cf\e[0m\tcheck old pictures and empty directories."
esac
