for i in {0..63}
do
	div=$[i/8]
	mod=$[i%8]
	col=$[7**((div+mod)%2)+40]
	echo -ne "\e[${col}m  \e[0m"
	[ $mod -eq 7 ] && echo
done
