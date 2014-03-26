#!/bin/bash

WD=$1

#list=(`ls $WD/*/fastq/*fastq`)
list=(`ls $WD/*fastq`)

for i in `seq 0 100`
do
	for j in `seq 0 5`
	do
		idx=$(($i * 6 + $j))
		if [ "$idx" -lt "${#list[@]}" ]; then
			echo -e "$i\t$j\t$idx\t${list[$idx]}"
			gzip ${list[$idx]} &
		else
			break
		fi
	done
	wait
done
