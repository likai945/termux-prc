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
	cat << _EOF_
================================
ITEM 	 INPUT_TMP	CPU_TMP
kx3_srv  $kx3_srv
kx3_dbs  $kx3_dbs
kx4_srv  $kx4_srv
kx4_dbs  $kx4_dbs
kx5_srv  $kx5_srv
kx5_dbs  $kx5_dbs
================================
the data comes from $tmp_data
_EOF_
}
#####check if the pics not shotted this day#####
listOtherDaysShots(){
	echo 'Screenshots not this day:'
	ls -lR | grep -E '.jpg|.png' | grep -v "`date "+%b %e"`" | awk '{print $NF}'
}
checkNotThisDayShots(){
	rq=`ls -lR | grep -E '.jpg|.png' | awk '{print $7,$8}'  | sort | uniq | wc -l`
	if [ $rq -gt 1 ];then
		listOtherDaysShots
	else
		ls -lR | grep -E '.jpg|.png' | grep -q "`date "+%b %e"`" 
		if [ $? -eq 0 ];then
			echo "all pictures screenshotted this day."
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
		echo 'no empty directories.' 
	else
		echo 'empty directories:' 
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
		echo -e "--at\tshow the average of tempratures."
		echo -e "--cf\tcheck old pictures and empty directories."
esac
