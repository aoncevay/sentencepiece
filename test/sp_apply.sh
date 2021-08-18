apply_sp_model () {
    lang=${1}
    name=${2}
    model_type=${3}
    vocab_size=${4}
    input_data=${5}
    model_lang=${6}
    build=${7-""}
    
    echo "$lang $model_lang $name $model_type $vocab_size $input_data"
    output_file=data/encoded/$model_lang.$input_data.$name.$model_type.$vocab_size
    input_data=data/$lang.$input_data.src

    sp_model_prefix=models.$model_lang/$name.$model_type.$vocab_size
    #vocab_str=$(($vocab_size / 1000))
    #sp_model_prefix=$project_dir/sp_models/multi/sp.$model_type.${vocab_str}k.$model_name
    #echo "Applying $sp_model_prefix on $input_data"

    ../build$build/src/spm_encode \
        --model $sp_model_prefix.model \
        --output_format=piece < $input_data \
        > $output_file
}

#model_lang="shp+es" all
model_lang="all" # "shp+es"
lang=shp
m_types="bpe unigram"
v_sizes="4000 8000 16000 32000"
split="train dev test"
for m in $m_types; do
    for v in $v_sizes; do
        for s in $split; do
            apply_sp_model $lang base $m $v $s $model_lang ""
            apply_sp_model $lang reqp $m $v $s $model_lang .reqp
            #apply_sp_model $lang base $m $v $s $lang ""
            #apply_sp_model $lang reqp $m $v $s $lang .reqp
        done
    done
done