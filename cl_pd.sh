#将word模板转换为excel模板，用于判断题
#by LiKai
#May 30, 2024
> tiku
dos2unix $1 &> /dev/null
echp -e '\n\n' >> $1
sed -i 's/,/，/' $1
line=`cat $1 | wc -l`

for i in `seq $line`
do
	l=`sed -n "${i}p" $1`
	echo $l | grep -Eq "^[0-9]+、"
	if [ $? -eq 0 ];then
		item=$l
	else
		echo $l | grep -qE '^答案:' 
		if [ $? -eq 0 ];then
			[[ "$l" =~ "×" ]] && item=$item,F || item=$item,T
			echo $item >> tiku
			unset item
		else
			item=$item,$l
		fi
	fi
done

for i in A B C D E F G H I J K
do
	sed -i 's/,,/,/g' tiku
done


sed -i 's/ *,/,/g' tiku
sed -i 's/,$//' tiku
sed -ri 's/^[0-9]+、//' tiku
