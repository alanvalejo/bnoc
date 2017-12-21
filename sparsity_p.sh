declare -a edges
declare -a timing

v=$1
p=$2

vcount=$(($v+$v))
echo d,e_avg,e_sd,t_avg,t_sd > sparsity/v${vcount}p$p.csv

for d in `seq 0.1 0.05 0.9`;
do
	percent=0.001
	c=$(expr $percent*$vcount | bc)
	c=${c%.*}
	for i in {1..5};
	do
		l=$(python bnoc.py -dir output -o network -v $v $v -c $c -d $d -n 0.0 -b -m $p)
		IFS=' '; arr=($l); unset IFS;
		edges[i]=${arr[0]}
		timing[i]=$(printf "%.3f" "${arr[1]}")
	done

	edges_average=($(Rscript -e 'mean(as.numeric(commandArgs(TRUE)))' ${edges[*]}))
	edges_average=${edges_average[1]}
	edges_average=${edges_average%.*}
	edges_sd=($(Rscript -e 'sd(as.numeric(commandArgs(TRUE)))' ${edges[*]}))
	edges_sd=${edges_sd[1]}
	timing_average=($(Rscript -e 'mean(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_average=${timing_average[1]}
	timing_sd=($(Rscript -e 'sd(as.numeric(commandArgs(TRUE)))' ${timing[*]}))
	timing_sd=$(printf "%.3f" "${timing_sd[1]}")

	echo $d,${edges_average},${edges_sd},${timing_average},${timing_sd} >> sparsity/v${vcount}p$p.csv
done
