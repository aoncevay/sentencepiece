# method to count the affixes in the GS (train, dev, test)
# returns the sorted list and a dictionary with the countings. If same count, sorted by len, then by ABC
def count_affixes_in_gold(affixes, lang):
    d_affixes = []
    gold_affixes = []
    for split in ["train", "dev", "test"]:
        with open(f"data/{lang}.{split}.tgt") as f_gold:
            for line in f_gold:
                gold_affixes.extend(line.strip().split())
    for affix in affixes:
        d_affixes.append((affix, gold_affixes.count(affix.replace("▁",""))))
    #print(d_affixes)
    # sorting first by the counting, then by the length (without counting the ▁, finally by lexicography
    d_affixes.sort(key=lambda item: (-item[1], len(item[0].replace("▁","")), item[0]))
    print(d_affixes)
    return d_affixes

# method to obtain the total list of affixes, and print or save into files
def get_affixes(lang="shp", verbose = False, save = False):
    affixes = [] # _preffix suffix
    with open(f"data/affix.{lang}", "r") as f:
        for line in f:
            line = line.strip()
            if "," in line:
                list_affix = line.split(",")
            else:
                list_affix = [line]
            #print(list_affix)
            for affix in list_affix:
                if affix[-1] == "-":
                    # this is the special symbol in SP
                    affixes.append("▁" + affix[:-1])
                else:
                    affixes.append(affix)
    affixes = sorted(list(set(affixes)))
    if verbose:
        print(len(affixes))
        print(sorted(affixes))
    if save:
        f = open(f"data/affix.{lang}.out", "w")
        sorted_affixes = count_affixes_in_gold(affixes, lang)
        f.write(" ".join([a[0] for a in sorted_affixes])) # if len(a[0]) > 1]))
        f.close()
        #f = open(f"data/reqchar.{lang}.out", "w")
        #f.write("".join([a[0] for a in sorted_affixes if len(a[0]) == 1]))
        #f.close()
    return affixes

def get_vocab(lang, name, model_type, vocab_size):
    pieces = []
    with open(f"models.{lang}/{name}.{model_type}.{vocab_size}.vocab", "r") as f:
        for line in f:
            piece, _ = line.strip().split()
            pieces.append(piece)
    return pieces

def morph_seg_eval(lang, name, model_type, vocab_size, split="test"):
    # getting the "predicted" segmentation and the GS
    with open(f"data/encoded/{lang}.{split}.{name}.{model_type}.{vocab_size}") as f_pred, open(f"data/{lang}.{split}.tgt") as f_gold:
        seg_pred = f_pred.readlines()
        seg_gold = f_gold.readlines()
    # cleaning the word boundary in the SP output
    seg_pred = [s.replace("▁", "") for s in seg_pred]
    acc, acc_affix, count_acc_affix = 0, 0, 0
    for s_pred, s_gold in zip(seg_pred, seg_gold):
        if s_pred == s_gold:
            acc += 1
        if len(s_gold.split()) > 1:
            count_acc_affix += 1
            if " ".join(s_gold.split()[1:]) == " ".join(s_pred.split()[-len(s_gold.split())+1:]):
                acc_affix += 1
    return acc/len(seg_gold), acc_affix/count_acc_affix

def count_affixes(affixes, lang, split="test"):
    with open(f"data/{lang}.{split}.tgt") as f_gold:
        seg_gold = f_gold.readlines()
    affixes_gold = []
    for seg in seg_gold:
        if len(seg.split()) > 1:
            affixes_gold.extend(seg.split()[1:])
    prec_affixes = list(set(affixes_gold).intersection(affixes))
    rest = sorted(list(set(affixes_gold) - set(affixes)))
    return len(prec_affixes)/len(list(set(affixes_gold))), rest

def main_report(affixes, lang):
    # main report of the morph evaluation
    model_types = ["bpe", "unigram"]
    vocab_sizes = ["4000", "8000", "16000", "32000"] #"1000", "2000", 
    print("%20s\trecall\ttrain\t\tdev\t\ttest" % " ")
    for m in model_types:
        for v in vocab_sizes:
            for name in ["base", "reqp"]:
                pieces = get_vocab(lang, name, m, v)
                recalled_affixes = list(set(affixes).intersection(pieces))
                recall = len(recalled_affixes)/len(affixes)*100
                str_out = f"{recall:.2f}"
                for s in ["train", "dev", "test"]:
                    acc, acc_affix = morph_seg_eval(lang, name, m, v, s)
                    str_out += f"\t{acc:.2f}/{acc_affix:.2f}"
                print("%20s\t%s" % (f"{name}.{m}.{v}", str_out))


lang = "shp"
affixes = get_affixes(lang, verbose=False, save=True)
for s in ["train", "dev", "test"]:
    prec, rest = count_affixes(affixes, lang, s)
    print("%s\t%.2f\t%s" % (s, prec, ",".join(rest)))
main_report(affixes, lang)
main_report(affixes, lang + "+es")
main_report(affixes, "all")
