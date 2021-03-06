#!/bin/bash
# 1:label 2:ratio 3:dataset 4:resolution
echo $1 $2 $3 $4
for k in $( seq 1 10 )
do
    mkdir -p $3/log_$2
    python3 ladder.py $1 ${k} $2 $3 $4 2>&1 | tee $3/log$4_$2/log_label$1_${k}_$2.log
    echo $1 ${k} $2 $3
done
