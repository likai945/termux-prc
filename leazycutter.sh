#!/data/data/com.termux/files/usr/bin/bash
add_column(){
	if [ -f $1 ];then
	pl=`wc -l $1 | awk '{print $1}'`
	for i in `seq $pl`
	do
		let k++
		if [ $k -eq 1 ];then
			sbm='识别码'
		else
			psbm=`sed -n $i'p' $1 | awk -F',' '{print $4}' | awk -F'-' '{print $8}'`
			[[ $psbm =~ ZX ]] && sbm=${psbm%ZX*}ZX || sbm=$psbm
		fi
		ol=`sed -n $i'p' $1`
		echo $ol,$sbm >> $2
	done
	fi
}

cmb_pages(){
	if [ -f $2 ] && [ -f $1 ];then
		spl=`wc -l $2 | awk '{print $1}'`
		spn=$[spl-1]
		tail -n $spn $2 >> $1
	elif [ -f $2 ] && [ !-f $1 ];then
		mv $2 $1
	fi
}

#####program#####

rm sbmkx3.csv &> /dev/null
rm sbmkx4.csv &> /dev/null
rm sbmkx5.csv &> /dev/null
cmb_pages kx41.csv kx42.csv
add_column kx3.csv sbmkx3.csv
add_column kx41.csv sbmkx4.csv
add_column kx5.csv sbmkx5.csv
rm kx3.csv &> /dev/null
rm kx41.csv &> /dev/null
rm kx42.csv &> /dev/null
rm kx5.csv &> /dev/null

