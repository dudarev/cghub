names=("four_pos_queries_with_cache" \
"four_pos_queries_without_cache" \
"three_pos_queries_with_cache" \
"three_pos_queries_without_cache")

for i in "${names[@]}"
do
    echo $i
    ./gprof2dot -f pstats stats/$i.stats | dot -Tpng -o imgs/tree_$i.png
done

for i in "${names[@]}"
do
    python plot.py stats/$i.csv imgs/time_$i.png
done
