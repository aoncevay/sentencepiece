
train_sp () {
    lang=${1-shp}
    sp_model_prefix=${2-base}
    model_type=${3-unigram}
    vocab_size=${4-8000}
    build=${5-""}
    input_data="data/corpus.$lang"
    sp_model_prefix=models.$lang/$sp_model_prefix.$model_type.$vocab_size

    if [[ $build != "" ]]; then
        ~/workspace/sentencepiece-prior/build$build/src/spm_train --input $input_data \
            --model_prefix $sp_model_prefix \
            --vocab_size $vocab_size \
            --character_coverage 0.9995 \
            --model_type $model_type \
            --input_sentence_size=2000000 \
            --shuffle_input_sentence=true \
            --required_pieces_file data/affix.$lang.out \
            --control_symbols "<es>,<en>,<shp>,<quy>,<2es>,<2en>,<2shp>,<2quy>,<orig>,<bt>,<dict>,<d+r>,<reord>" \
            --hard_vocab_limit false 2> $sp_model_prefix.log
    else
        ~/workspace/sentencepiece-prior/build/src/spm_train --input $input_data \
            --model_prefix $sp_model_prefix \
            --vocab_size $vocab_size \
            --character_coverage 0.9995 \
            --model_type $model_type \
            --input_sentence_size=2000000 \
            --shuffle_input_sentence=true \
            --hard_vocab_limit false 2> $sp_model_prefix.log
    fi
    #            --required_pieces_file data/affix.$lang.out \
    #            --required_chars_file data/reqchar.$lang.out \
}


lang="all" #"shp+es"
m_types="bpe unigram"
v_sizes="8000 16000 32000 4000" #"1000 2000" 
#rm models.$lang/*
for v in $v_sizes; do
    for m in $m_types; do
        echo "$lang $m $v $s"
        train_sp $lang reqp $m $v $s ".reqp"
        train_sp $lang base $m $v $s ""
    done
done