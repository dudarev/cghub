names=("four_pos_queries_with_cache" \
"four_pos_queries_without_cache" \
"three_pos_queries_with_cache" \
"three_pos_queries_without_cache")

echo "Plotting trees"

for i in "${names[@]}"
do
    echo $i
    ./gprof2dot -f pstats stats/$i.stats | dot -Tpng -o imgs/tree_$i.png
done

echo "Plotting time vs. count plots"

for i in "${names[@]}"
do
    echo $i
    python plot.py stats/$i.csv imgs/time_$i.png
done
