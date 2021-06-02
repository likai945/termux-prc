#!/bin/bash
read -p 'nikname: ' nn
echo '在昵称后输入内容，没昵称则按回车键，退出请键入exit'
while [ 1 ]
do
read -p "$nn: " nr
if [ ! $nr ];then
        echo ''
elif [ $nr == 'exit' ];then
        exit
else
#echo $nr >> /root/ceshi
        ssh root@192.168.2.5 "echo -e '\n'${nn}:$nr > /dev/pts/0"
fi
done