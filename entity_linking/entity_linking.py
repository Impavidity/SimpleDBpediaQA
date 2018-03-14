import os
import pickle

from collections import defaultdict
from tqdm import tqdm
from argparse import ArgumentParser
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
import sys
sys.path.append('../script')
from utils import process_original_entity, repalce_punc, processed_text, process_entity


inverted_index = defaultdict(list)
stopword = set(stopwords.words('english'))

def get_ngram(text):
    #ngram = set()
    ngram = []
    tokens = text.split()
    for i in range(len(tokens)+1):
        for j in range(i):
            if i-j <= 3:
                #ngram.add(" ".join(tokens[j:i]))
                temp = " ".join(tokens[j:i])
                if temp not in ngram:
                    ngram.append(temp)
    #ngram = list(ngram)
    ngram = sorted(ngram, key=lambda x: len(x.split()), reverse=True)
    return ngram

def get_stat_inverted_index(filename):
    """
    Get the number of entry and max length of the entry (How many mid in an entry)
    """
    with open(filename, "rb") as handler:
        global  inverted_index
        inverted_index = pickle.load(handler)
        inverted_index = defaultdict(str, inverted_index)
    print("Total type of text: {}".format(len(inverted_index)))
    max_len = 0
    _entry = ""
    for entry, value in inverted_index.items():
        if len(value) > max_len:
            max_len = len(value)
            _entry = entry
    print("Max Length of entry is {}, text is {}".format(max_len, _entry))


def entity_linking(data_type, predictedfile, goldfile, HITS_TOP_ENTITIES, output):
    print("Source : {}".format(predictedfile))
    predicted = open(predictedfile)
    gold = open(goldfile)
    fout = open(output, 'w')
    total = 0
    top1 = 0
    top3 = 0
    top5 = 0
    top10 = 0
    top20 = 0
    top50 = 0
    top100 = 0

    for idx, (line, gold_line) in tqdm(enumerate(zip(predicted.readlines(), gold.readlines()))):
        total += 1
        line = line.strip().split(" %%%% ")
        gold_entity = gold_line.strip().split('\t')[2].replace("http://dbpedia.org/resource/", "dbr:")
        # Use n-gram to filter most of the keys
        # We use the list to maintain the candidates
        # for counting
        # print(line[1])
        C = []
        # C_counts = []
        C_scored = []
        line_id = line[0]
        tokens = get_ngram(line[1])
        if len(tokens) > 0:
            maxlen = len(tokens[0].split())
        for item in tokens:
            if len(item.split()) < maxlen and len(C) == 0:
                maxlen = len(item.split())
            if len(item.split()) < maxlen and len(C) > 0:
                break
            if item in stopword:
                continue
            C.extend(inverted_index[item])
            # if len(C) > 0:
            #     break
        for dbpedia_text_parsed in set(C):
            dbpedia_text = process_entity(repalce_punc(dbpedia_text_parsed[0].replace("dbr:", "")))
            score = fuzz.ratio(dbpedia_text, line[1]) / 100.0
            C_scored.append((dbpedia_text_parsed[0], score))

        C_scored = sorted(list(set(C_scored)), key=lambda t: (t[1], -len(t[0])), reverse=True)
        cand_mids = C_scored[:HITS_TOP_ENTITIES]
        fout.write("{}".format(line_id))
        for dbpedia_text, score in cand_mids:
            fout.write(" %%%% {}\t{}".format(dbpedia_text, score))
        fout.write('\n')
        midList = [x[0] for x in cand_mids]
        if gold_entity in midList[:1]:
            top1 += 1
        if gold_entity in midList[:3]:
            top3 += 1
        if gold_entity in midList[:5]:
            top5 += 1
        if gold_entity in midList[:10]:
            top10 += 1
        if gold_entity in midList[:20]:
            top20 += 1
        if gold_entity in midList[:50]:
            top50 += 1
        if gold_entity in midList[:100]:
            top100 += 1

    print(data_type)
    print("Top1 Entity Linking Accuracy: {}".format(top1 / total))
    print("Top3 Entity Linking Accuracy: {}".format(top3 / total))
    print("Top5 Entity Linking Accuracy: {}".format(top5 / total))
    print("Top10 Entity Linking Accuracy: {}".format(top10 / total))
    print("Top20 Entity Linking Accuracy: {}".format(top20 / total))
    print("Top50 Entity Linking Accuracy: {}".format(top50 / total))
    print("Top100 Entity Linking Accuracy: {}".format(top100 / total))

if __name__=="__main__":
    parser = ArgumentParser(description='Perform entity linking')
    parser.add_argument('--model_type', type=str, required=True, help="options are [crf|lstm|gru]")
    parser.add_argument('--index_ent', type=str, default="/mnt/collections/mwazmy/KB/SQ/DBPedia_Entity_Index.pkl",
                        help='path to the pickle for the inverted entity index')
    parser.add_argument('--data_dir', type=str, default="../data")
    parser.add_argument('--query_dir', type=str, default="../entity_detection/query_text/lstm")
    parser.add_argument('--hits', type=int, default=100)
    parser.add_argument('--output_dir', type=str, default="./results")
    args = parser.parse_args()
    print(args)

    model_type = args.model_type.lower()
    assert(model_type == "crf" or model_type == "lstm" or model_type == "gru")
    output_dir = os.path.join(args.output_dir, model_type)
    os.makedirs(output_dir, exist_ok=True)

    get_stat_inverted_index(args.index_ent)
    # entity_linking("valid",
    #                 os.path.join(args.query_dir, "query.valid"),
    #                 os.path.join(args.data_dir, "valid.txt"),
    #                 args.hits,
    #                 os.path.join(output_dir, "valid-h{}.txt".format(args.hits)))
    entity_linking("valid", "../entity_detection/query_text/lstm/query.valid",
                   "../data/valid.txt",
                   100,
                   "results/valid-h100.txt")
    # entity_linking("test",
    #                 os.path.join(args.query_dir, "query.test"),
    #                 os.path.join(args.data_dir, "test.txt"),
    #                 args.hits,
    #                 os.path.join(output_dir, "test-h{}.txt".format(args.hits)))
    entity_linking("test", "../entity_detection/query_text/lstm/query.test",
                   "../data/test.txt",
                   100,
                   "results/test-h100.txt")