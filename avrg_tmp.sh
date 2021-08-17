#!/bin/bash
tmp_data=`ls -t *.runlog | head -1`
kx3=`awk -F '|' '$1~/-03A-/\
	{if ($2~/^[[:digit:]]+$/) \
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}'\
	$tmp_data`
kx4=`awk -F '|' '$1~/-04A-/\
	{if ($2~/^[[:digit:]]+$/) \
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}'\
	$tmp_data`
kx5_srv=`awk -F '|' '$1~/05A.*SRV/\
	{if ($2~/^[[:digit:]]+$/)\
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}' \
	$tmp_data`
kx5_dbs=`awk -F '|' '$1~/05A.*DBS/\
	{if ($2~/^[[:digit:]]+$/) \
		{i++;sumi=sumi+$2};\
	if ($3~/^[[:digit:]]+$/) \
		{j++;sumc=sumc+$3}}\
	END{printf ("%.2f °C\t", sumi/i);\
		printf ("%.2f °C\n", sumc/j)}' \
	$tmp_data`
echo -e "\e[032m================================"
echo -e "ITEM\t INPUT_TMP\tCPU_TMP\e[0m"
echo -e "kx3_dbs\t $kx3"
echo -e "kx4_dbs\t $kx4"
echo -e "kx5_srv\t $kx5_srv"
echo -e "kx5_dbs\t $kx5_dbs"
echo -e "\e[032m================================\e[0m"
echo -e "the data comes from $tmp_data"
