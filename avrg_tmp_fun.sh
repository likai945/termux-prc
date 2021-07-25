#!/bin/bash
tmp_data=`ls -t *.runlog | head -1`
at(){
	awk -F '|' '$1~/'$1'/\
	{if ($2~/^[[:digit:]]+$/) \
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}'\
	$tmp_data
}
show(){
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
#####main#####
show
