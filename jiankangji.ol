#/bin/bash
zhuijia(){
echo -e '\e[32m\nshit again?\nenter "yes" to plus one\nenter "no" to quit\n\e[0m'
while :
do
	read -p "yes or no:" opt
	rl=$[10+`echo "$opt" | wc -L`]
	[[ ${opt:=yes} =~ yes ]] && break
	[[ $opt =~ no ]] && exit
done
last=`tail -1 $jl`
ly=`echo $last | awk '{print $NF}'`
echo $last | grep -q '+' || sed -i "\$s/\($ly\)/(\1)/" $jl
nly=`tail -1 $jl | awk '{print $NF}'`
nb=${nly##*+}
nnb=$[nb+1]
sed -i "\$s/).*/)+$nnb/" $jl
}
my(){
rsync -r ${bpath}/ $HOME/termux-app && cd $HOME/termux-app && git add . && git commit -m "daily_sync_`date +%Y%b%e%X`" &> /dev/null && git push &> /dev/null && return 0
}
dxa(){
[ $? -eq 0 ] && echo -e "\e[1A\e[$[rl+0]C\e[1m\e[31m(\e[37mG\e[31m)\e[0m\n"
}
dxb(){
[ $? -eq 0 ] && echo -e "\t\t\e[1m\e[31m(\e[37mG\e[31m)\e[32mGITEE PUSHED\e[0m"
}
gh(){
rsync -r ${bpath}/ $HOME/termux-prc && cd $HOME/termux-prc && git add . && git commit -m "daily_sync_`date +%Y%b%e%X`" &> /dev/null && git push &> /dev/null && return 0
}
dxc(){
[ $? -eq 0 ] && echo -e "\e[2A\e[$[rl+3]C\e[1m\e[32m[✓]\e[0m\n"
}
dxd(){
[ $? -eq 0 ] && echo -e "\t\t\e[1m\e[32m[✓]\e[32mGITHUB PUSHED\e[0m"
}
cha(){
[ `cat $jl | wc -l` -eq 0 ] && echo -e "\t\t\033[31mNO DATA\033[0m" && exit 
zc=`date +%j`
sc=`tail -1 ${jl} | awk '{print $1}'`
d=`expr $zc - $sc`
[ $d -lt 0 ] && d=$[365+d]
[ $d -eq 1 ] && echo -e "\n\033[32m$d\033[0m day no shit" || echo -e "\n\033[32m$d\033[0m days no shit"
}
lan(){
tail=`tail -1 ${jl}`
et=${tail:18}
length=`echo "$et" | wc -L` 
echo -en "\033[?25l"
for x in `seq ${length}`;do
	echo -en "\033[$[x%7+31]m-"
	sleep 0.001
done
echo
for i in `seq ${length}`;do
	echo -en "\033[32m${et:$[i-1]:1}\033[0m"
	sleep 0.01
done
echo
for x in `seq ${length}`;do
	echo -en "\033[$[x%7+31]m-"
	sleep 0.001
done
echo -e "\033[?25h\n\033[0m"
}
ji(){
zheci=`date +%j`
shangci=$(tail -1 ${jl} | awk '{print $1}')
[ -z $shangci ] && delay=0 || delay=`expr $zheci - $shangci - 1`
[ $delay -eq -1 ] &>/dev/null && zhuijia && my && dxa && gh && dxc
[ $delay -eq -1 ] &>/dev/null && lan && exit
[ $delay -lt -1 ] && delay=$[365+delay]
shi=`date +%s`
echo -e "\033[32m\ntime recording...\ncomplete all after poop\nremark 'manual' if necessary\033[0m\n"
read -p 'the scale(nml):' s
bi=`date +%s`
[[ $s =~ quit ]] && exit
read -p 'easy or difficult(eas):' e
read -p 'color(brn):' c
read -p 'remark(null):' r
t=$[(bi-shi)/60]
[ $[(bi-shi)%60/6] -ge 5 ] && let t++
rl=$[`echo "$r" | wc -L`+13]
[[ $r == manual* ]] &>/dev/null && read -p 'duration(8min):' t && r=`echo ${r:6} | sed 's/ //g'` && rl=$[`echo "$t" | wc -L`+15]
[ $t -lt 10 ] &>/dev/null && t=0$t
echo "${zheci} d${delay} `date +%R` `date +%Y` `date +%b` `date +%d` `date +%a` | ${s:=nml} ${e:=eas} ${c:=brn} ${t:=08}min ${r:=null}" >> ${jl}
cp $jl $bpath
}
quan(){
if [ `cat $jl | wc -l` -eq 0 ];then
	echo -e "\t\t\033[31mNO DATA\033[0m"
	else
	echo -e '\n\033[32m------------------------------\033[0m'
	cat ${jl}
	echo -e '\033[32m------------------------------\033[0m\n'
fi
}
tong(){
[ `cat $jl | wc -l` -eq 0 ] && echo -e "\n\t\t\033[31mMORE DATA IN NEED\033[0m\n" && exit
ltd=`grep d0 $jl | wc -l`
ltn=`grep nml $jl | wc -l`
lte=`grep eas $jl | wc -l`
ltt=`cat $jl | wc -l`
lttd=`echo "scale=4;$ltd/$ltt" | bc`
ltrd=`echo "scale=2;$lttd/0.01" | bc`
lttn=`echo "scale=4;$ltn/$ltt" | bc`
ltrn=`echo "scale=2;$lttn/0.01" | bc`
ltte=`echo "scale=4;$lte/$ltt" | bc`
ltre=`echo "scale=2;$ltte/0.01" | bc`
echo -e "\n-----------------------------"
echo -e "\033[32mRP:$ltrd% RN:$ltrn% RE:$ltre%\033[0m"
echo -e "-----------------------------\n"
}
huitu(){
[ `cat $tz | wc -l` -eq 0 ] && echo -e "\t\t\033[31mNO DATA\033[0m" && exit 
echo -e '\n\033[?25l------------------------------'
for i in `cat ${tz}`;do
	let b++
	c=$[b%2]
	if [ $c -eq 1 ];then 
		echo -en "\033[46m${i:4}\033[0m" 
	else
		k=$[i-100] 
		for j in `seq $k`;do
			s=$[b%7+31]
			echo -en "\033[${s}m/\033[0m"
			sleep 0.01
		done
		for k in {0..2};do
			echo -en "\033[${s}m${i:$k:1}\033[0m"
			[ $k -lt 2 ] && sleep 0.01
		done
		echo
	fi
done
echo -e '------------------------------\033[?25h\n'
}
jilu(){
zheci=`date +%Y%b%d`
shangci=$(tail -1 ${tz} | awk '{print $1}')
[ $zheci == $shangci ] &> /dev/null && echo -e "\t\t\033[31mDUPLICATE RECORD\033[0m" && exit 
echo
while [ 1 ]
do
	read -p 'weight:' w
	[ $w -ge 100 ] &> /dev/null && [ $w -le 150 ] &> /dev/null && echo "${zheci} $w" >> ${tz} && cp $tz $bpath && rl=10 && break
	[ $? -ne 0 ] && echo -e "\t\t\033[31mBETWEEN 100 AND 150\033[0m"
done
}
quanbu(){
[ `cat $tz | wc -l` -eq 0 ] && echo -e "\t\t\033[31mNO DATA\033[0m" && exit
echo -e '\n\033[32m-------------\033[0m'
	cat ${tz}
echo -e '\033[32m-------------\033[0m\n'
}
tongji(){
[ `cat $tz | wc -l` -le 1 ] && echo -e "\n\t\t\033[31mMORE DATA IN NEED\033[0m\n" && exit
jntt=`cat $tz | wc -l`
jntl=`awk '{print $NF}' $tz`
jntj=0
jntk=0
jntd='-'
jntn=`awk 'NR==1{print $2}' $tz`
for jnti in $jntl;do
	[ $jnti -gt $jntn ] && jntb=$jntk && jntk=1 && jntd='/' && jntc=$[jnti-jntn] && let jntj++
	[ $jnti -lt $jntn ] && jntb=$jntk && jntk=1 && jntd='\' && jntc=$[jntn-jnti]
	[ $jnti -eq $jntn ] && let jntk++
	jntn=$jnti
done
jnttj=`echo "scale=4;$jntj/$jntt" | bc`
jnttjj=$(echo "scale=2;$jnttj/0.01" | bc)
[ `echo "$jnttjj < 1" | bc` -eq 1 ] && [ `echo "$jnttjj > 0" | bc` -eq 1 ] && jnttjj="0$jnttjj"
jntchang=`echo "LC $jntd ${jntb}d ${jntc}jn | RRBOUNDED $jntj RR $jnttjj%" | wc -L`
[ $jntd == '-' ] && echo -e "\n\t\t\033[31mMORE DATA IN NEED\033[0m\n" && exit
echo
for jntq in `seq $jntchang`;do
	echo -n "-"
done
echo
[ $jntd == '\' ] && echo -e "\033[32mLC $jntd ${jntb}d ${jntc}jn | REBOUNDED \033[31m$jntj \033[32mRR \033[31m$jnttjj%\033[0m"
[ $jntd == '/' ] && echo -e "\033[32mLC \033[31m$jntd \033[32m${jntb}d ${jntc}jn | REBOUNDED \033[31m$jntj \033[32mRR \033[31m$jnttjj%\033[0m"
echo -en "NW $jnti KP ${jntk}d"
jntg=$(expr $jntchang - 28 - `echo "$jntk" | wc -L`)
for jntgi in `seq $jntg`;do
	echo -n ' '
done
echo "BE PERSERVERATION"
for jntq in `seq $jntchang`;do
	echo -n "-"
done
echo 
echo
}
##########the program##########
bpath=/data/data/com.termux/files/usr/backup
tz=/data/data/com.termux/files/home/tz
[ ! -f $tz ] && touch $tz
jl=/data/data/com.termux/files/home/jl
[ ! -f $jl ] && touch $jl
case $1 in 
	--lac)
	cha;
	lan;;
	--laj)
	ji;
	my;
	dxa;
	gh;
	dxc;
	lan;;
	--laq)
	quan;;
	--lat)
	tong;;
	--lab)
	cp $jl $bpath;
	my;
	dxb;
	gh;
	dxd;;
	--jnh)
	huitu;;
	--jnj)
	jilu;
	my;
	dxa;
	gh;
	dxc;;
	--jnq)
	quanbu;;
	--jnt)
	tongji;;
	--jnb)
	cp $tz $bpath
	my;
	dxb;
	gh;
	dxd;;
	*)
	echo -e "\033[32mlac•laj•laq•lat•lab\njnh•jnj•jnq•jnt•jnb\033[0m"
esac
