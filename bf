#!/bin/bash
cd
for i in `ls`;do
[ -f $i ] && cp $i ../usr/Termuxbak/backup/hm && echo -e "$i \e[32m✓\e[0m" && let e++
done
echo -e "\e[32m---------------\ncopied $e files\e[0m"
read -p "pack them all? " y
[[ "$y" =~ "no" ]] && exit
[[ "${y:=yes}" =~ "yes" ]] && zip -r zz/`date +%F`bak.zip ../usr/Termuxbak/backup/hm &> /dev/null 
echo -e "\e[32m\t\tDONE✓\e[0m"
