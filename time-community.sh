declare -a timing

p=$1
d=$2
v=$3
vcount=$(($v+$v))
echo c,t_avg,t_sd > time/v${vcount}d${d}p${p}.csv

for c in `seq 0 2 160`;
do

	for i in {1..3};
	do
		l=$(python bnoc.py -dir output -o network -v $v $v -c $c -d $d -n 0.0 -b -m $p)
		timing[i]=$(printf "%.3f" "${l}")
	done

	timing_average=($(Rscript -e 'mean(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_average=${timing_average[1]}
	timing_sd=($(Rscript -e 'sd(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_sd=$(printf "%.3f" "${timing_sd[1]}")

	echo $c,${timing_average},${timing_sd} >> time/v${vcount}d${d}p${p}.csv
done
