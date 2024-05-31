#将word模板转换为excel模板，用于选择题，稍加修改亦可用于判断题
#by LiKai
#May 30, 2024

> tiku
dos2unix $1 &> /dev/null
echo -e '\n\n' >> $1
sed -i 's/,/，/' $1
line=`cat $1 | wc -l`

for i in `seq $line`
do
	l=`sed -n "${i}p" $1`
	echo $l | grep -Eq "^[0-9]+、"
	if [ $? -eq 0 ];then
		item=$l
	else
		echo $l | grep -qE '^答案:[A-Z]+' 
		if [ $? -eq 0 ];then
			item=$l,$item
			echo $item >> tiku
			unset item
		else
			item=$item,$l
		fi
	fi
done

for i in A B C D E F G H I J K
do
	sed -i "s/$i、//" tiku
	sed -i 's/,,/,/g' tiku
done

sed -ri 's/^答案://' tiku

sed -i 's/ *,/,/g' tiku
sed -i 's/,$//' tiku

awk -F ',' -v OFS=',' '{t=$1;$1=$2;$2=t;print;}' tiku > newtiku

mv newtiku tiku
sed -ri 's/^[0-9]+、//' tiku
