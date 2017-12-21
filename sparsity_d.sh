declare -a timing

p=$1
d=$2

echo v,t_avg,t_sd > time/d${d}p${p}.csv

for v in `seq 1000 1000 50000`;
do
	percent=0.001
	vcount=$(($v+$v))
	c=$(expr $percent*$vcount | bc)
	c=${c%.*}
	for i in {1..5};
	do
		l=$(python bnoc.py -dir output -o network -v $v $v -c $c -d $d -n 0.0 -b -m $p)
		timing[i]=$(printf "%.3f" "${l}")
	done

	timing_average=($(Rscript -e 'mean(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_average=${timing_average[1]}
	timing_sd=($(Rscript -e 'sd(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_sd=$(printf "%.3f" "${timing_sd[1]}")

	echo $vcount,${timing_average},${timing_sd} >> time/d${d}p${p}.csv
done
