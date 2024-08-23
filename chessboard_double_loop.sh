for i in {1..8}
do
	for j in {1..8}
	do
		col=$[7**((i+j)%2)+40]
		echo -en "\e[${col}m  \e[0m"
	done
	echo
done
