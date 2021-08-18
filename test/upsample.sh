upsample_es () {
    shp_size=`wc -l < data/corpus.shp`
    times=12
    new_size=$((shp_size*times))
    echo $shp_size $new_size
    head -n $new_size data/corpus.es > data/corpus.shp+es
    for i in $(seq 1 $times);do
        cat data/corpus.shp >> data/corpus.shp+es
    done
    echo `wc -l data/corpus.shp+es`
}

upsample_all () {
    size_each=500000
    shp_size=`wc -l < data/corpus.shp`
    quy_size=`wc -l < data/corpus.quy`
    shp_times=$((size_each/shp_size))
    quy_times=$((size_each/quy_size))
    echo $shp_times $quy_times

    gshuf -n $size_each data/corpus.es >  data/corpus.all
    gshuf -n $size_each data/corpus.en >> data/corpus.all
    cat data/corpus.shp > data/corpus.shp.tmp
    for i in $(seq 1 $shp_times);do
        cat data/corpus.shp >> data/corpus.shp.tmp
    done
    head -n $size_each data/corpus.shp.tmp >> data/corpus.all
    cat data/corpus.quy > data/corpus.quy.tmp
    for i in $(seq 1 $quy_times);do
        cat data/corpus.quy >> data/corpus.quy.tmp
    done
    head -n $size_each data/corpus.quy.tmp >> data/corpus.all
    rm data/corpus.*.tmp
    wc -l data/corpus.all
}

upsample_es
upsample_all