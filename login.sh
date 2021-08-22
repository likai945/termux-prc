#!/data/data/com.termux/files/usr/bin/bash
user='66a98ac20df4b708292457c6928faf38'
password='fe5bce4b36915b6edca604182fe907fa'
gate=1629630926
login(){
	now=`date +%s`
	if [ $now -lt $gate ];then
		wt=$[gate-now]
		echo "$wt seconds after" >&2
		return 2
	else
	while [ 1 ]
	do
		read -p "enter your name: " usr
		read -sp "enter your password: " passwd
		md5us=`echo $usr | md5sum | awk '{print $1}'`
		md5pw=`echo $passwd | md5sum | awk '{print $1}'`
		if [ "$md5us" == "$user" -a "$md5pw" == "$password" ];then
		echo -e "\nwelcome, $usr." && return 0
		else
		echo -e "\nuser or password not correct." >&2
		fi
		let i++
		nown=`date +%s`
		if [ $i -ge 3 ];then
			echo "3 times wrong,you can try again after 60 seconds." >&2
			sed -i "/^gate/s/^.*$/gate=$[nown+60]/" $0
			return 1
		fi
	done
	fi
}
chgeSth(){
	if [ "$1" == "user" ];then
		chg=$user
		n="-n"
	elif [ "$1" == "password" ];then
		chg=$password
		x=s
	fi
	read -${x}p "your old $1:" oldpw
	echo $n
	md5opw=`echo $oldpw | md5sum | awk '{print $1}'`
	if [ "$md5opw" == "$chg" ];then
		read -${x}p "your new $1:" newpwo
		echo $n
		read -${x}p "new $1 again:" newpwt
		echo $n
		if [ "$newpwo" == "$newpwt" ];then
			if [ "$1" == "password" ];then
				if [[ $newpwo =~ [0-9]+ ]] && [[ $newpwo =~ [a-z]+ ]] && [[ $newpwo =~ [A-Z]+ ]] && [ ${#newpwo} -ge 8 ];then
				echo j > /dev/null
			else
				echo "not legal, 8 long, big letters small letters and digits in need." >&2
				return 4
				fi
			fi
			echo "$1 changed"
			md5npw=`echo $newpwo | md5sum | awk '{print $1}'`
			sed -i "/^$1/s/^.*$/$1=\'$md5npw\'/" $0
			else
				echo "$1 not the same" >&2
				return 1
		fi
	else
		echo "enter the right old $1." >&2
		return 2
	fi
}
case $1 in
	--login)
		login;;
	--password)
		login;
		chgeSth password;;
	--user)
		login;
		chgeSth user;;
	*)
		echo 'login|password|user'
esac
