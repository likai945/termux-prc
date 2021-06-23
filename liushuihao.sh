#!/bin/bash
sc=`cat shangci`
today=`date +%j`
[ -e $sc ] && [ $sc -ne $today ] && rm $sc && echo 1 > $today && echo $today > shangci
i=`cat $today`
echo -e "\t\t$i" && let i++ && echo $i > $today
