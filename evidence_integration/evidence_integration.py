# python evidence_integration.py --ent_type lstm --rel_type cnn --index_reachpath subgraph.pkl
# --data_path ../data/test.txt --ent_path ../Entity_Linking/results/test-h100.txt
# --rel_path ../Relation_Prediction/results/cnn/test.txt

from argparse import ArgumentParser
import os
import math
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def valid_combination(entity, relation, direction, constraint=None):
    if direction == "forward":
        query_str = 'SELECT ?a WHERE {' + '<{}> <{}> ?a . '.format(entity.replace('"', "%22").replace("'", "%27"), relation)
        if constraint != None:
            query_str += '?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}>'.format(constraint)
    else:
        query_str = 'SELECT ?a WHERE {' + '?a <{}> <{}> . '.format(relation, entity.replace('"', "%22").replace("'", "%27"))
        if constraint != None:
            query_str += '?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}>'.format(constraint)
    query_str += '}'
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    try:
        result = sparql.query().convert()
    except:
        print(query_str + "\n")
        return False

    for item in result["results"]["bindings"]:
        if 'xml:lang' in item['a']:
            if item['a']['xml:lang'] == 'en':
                return True
        else:
            return True
    return False



def get_answers(filename):
    id2sub = {}
    id2rel = {}
    id2obj = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            idx = line[0]
            sub = line[2]
            rel = line[3]
            id2sub[idx] = sub
            id2rel[idx] = rel

    return id2sub, id2rel, id2obj

def get_ents(filename, HITS_ENT):
    print("Predicted Entity Source: {}".format(filename))
    id2ents = defaultdict(list)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().split(' %%%% ')
            idx = line[0]
            candidates = line[1:][:HITS_ENT]
            for candidate in candidates:
                entity, score = candidate.split('\t')
                id2ents[idx].append((entity, float(score)))
    return id2ents

def get_rels(filename, HITS_REL):
    print("Predicted Relation Source: {}".format(filename))
    id2rels = defaultdict(list)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().split(' %%%% ')
            idx = line[0]
            rel = line[1]
            label = line[2]
            score = math.exp(float(line[3]))
            if len(id2rels[idx]) < HITS_REL:
                id2rels[idx].append((rel, label, score))
    return id2rels

def normalize_entity(text):
    return "http://dbpedia.org/resource/" + text[4:]

def evidence_integration(data_path, ent_path, rel_path, output_dir, HITS_ENT, HITS_REL, is_heuristics):
    # Gold Answer
    id2goldEntity, id2goldRels, id2goldObj = get_answers(data_path)
    id2predictedEntity = get_ents(ent_path, HITS_ENT)
    id2rels = get_rels(rel_path, HITS_REL)
    file_base_name = os.path.basename(data_path)
    fout = open(os.path.join(output_dir, file_base_name), 'w')
    retrieved_top1 , retrieved_top2, retrieved_top3 = 0, 0, 0
    answer_retrieved_top1, answer_retrieved_top2, answer_retrieved_top3 = 0, 0, 0
    found, notfound_both, notfound_entity, notfound_rel = 0, 0, 0, 0
    idxs = id2goldEntity.keys()
    id2answers = defaultdict(list)

    lineids_found1 = []
    lineids_found2 = []
    lineids_found3 = []

    for idx in idxs:
        if idx not in id2predictedEntity and idx not in id2rels:
            notfound_both += 1
            continue
        elif idx not in id2predictedEntity:
            notfound_entity += 1
            continue
        elif idx not in id2rels:
            notfound_rel += 1
            continue

        found += 1
        predictedEntity = id2predictedEntity[idx]
        predictedRel = id2rels[idx]
        if is_heuristics:
            for (entity, entity_score) in predictedEntity:
                entity_norm = normalize_entity(entity)
                for (raw_rel, rel_label, rel_score) in predictedRel:
                    rel = raw_rel.split("@")
                    rel = (rel[0], rel[1])
                    if valid_combination(entity_norm, rel[0], rel[1]):
                        comb_score = (entity_score ** 0.6) * (rel_score ** 0.1)
                        id2answers[idx].append((entity_norm, raw_rel, entity_score, rel_score, comb_score))

            id2answers[idx].sort(key=lambda t: t[4], reverse=True)
        else:
            id2answers[idx] = [(predictedEntity[0][0], predictedRel[0][0])]

        # write to file


        fout.write("{}".format(idx))
        for answer in id2answers[idx]:
            entity, rel, entity_score, rel_score, comb_score = answer
            fout.write(" %%%% {}\t{}\t{}\t{}\t{}".format(entity, rel, entity_score, rel_score, comb_score))
        fout.write('\n')
        truth_entity = id2goldEntity[idx]
        truth_rel = id2goldRels[idx]
        flag = 0
        if len(id2answers[idx]) >= 1 and id2answers[idx][0][0] == truth_entity \
                and id2answers[idx][0][1] == truth_rel:
            retrieved_top1 += 1
            retrieved_top2 += 1
            retrieved_top3 += 1
            flag += 1
            lineids_found1.append(idx)
        elif len(id2answers[idx]) >= 2 and id2answers[idx][1][0] == truth_entity \
                and id2answers[idx][1][1] == truth_rel:
            retrieved_top2 += 1
            retrieved_top3 += 1
            lineids_found2.append(idx)
        elif len(id2answers[idx]) >= 3 and id2answers[idx][2][0] == truth_entity \
                and id2answers[idx][2][1] == truth_rel:
            retrieved_top3 += 1
            lineids_found3.append(idx)

        if flag == 1:
            print(idx, truth_entity, truth_rel, truth_obj, id2answers[idx][0])
            break
    print()
    print("found:              {}".format(found / len(id2goldEntity) * 100.0))
    print("retrieved at top 1: {}".format(retrieved_top1 / len(id2goldEntity) * 100.0))
    print("retrieved at top 2: {}".format(retrieved_top2 / len(id2goldEntity) * 100.0))
    print("retrieved at top 3: {}".format(retrieved_top3 / len(id2goldEntity) * 100.0))
    print("answer retrieved at top 1: {}".format(answer_retrieved_top1 / len(id2goldEntity) * 100.0))
    print("answer retrieved at top 2: {}".format(answer_retrieved_top2 / len(id2goldEntity) * 100.0))
    print("answer retrieved at top 3: {}".format(answer_retrieved_top3 / len(id2goldEntity) * 100.0))
    # print("retrieved at inf:   {}".format(retrieved / len(id2goldmids) * 100.0))
    fout.close()
    return id2answers


if __name__=="__main__":
    parser = ArgumentParser(description='Perform evidence integration')
    parser.add_argument('--ent_type', type=str, required=True, help="options are [crf|lstm|gru]")
    parser.add_argument('--rel_type', type=str, required=True, help="options are [lr|cnn|lstm|gru]")
    # parser.add_argument('--index_reachpath', type=str, default="subgraph.pkl",
    #                     help='path to the pickle for the reachability index')
    # parser.add_argument('--index_degreespath', type=str, default="../indexes/degrees_2M.pkl",
    #                     help='path to the pickle for the index with the degree counts')
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--ent_path', type=str, help='path to the entity linking results')
    parser.add_argument('--rel_path', type=str, help='path to the relation prediction results')
    parser.add_argument('--hits_ent', type=int, default=50, help='the hits here has to be <= the hits in entity linking')
    parser.add_argument('--hits_rel', type=int, default=5, help='the hits here has to be <= the hits in relation prediction retrieval')
    parser.add_argument('--no_heuristics', action='store_false', help='do not use heuristics', dest='heuristics')
    parser.add_argument('--output_dir', type=str, default="./results")
    args = parser.parse_args()
    print(args)

    ent_type = args.ent_type.lower()
    rel_type = args.rel_type.lower()
    assert (ent_type == "crf" or ent_type == "lstm" or ent_type == "gru")
    assert (rel_type == "lr" or rel_type == "cnn" or rel_type == "lstm" or rel_type == "gru")
    output_dir = os.path.join(args.output_dir, "{}-{}".format(ent_type, rel_type))
    os.makedirs(output_dir, exist_ok=True)


    test_answers = evidence_integration(args.data_path, args.ent_path, args.rel_path, args.output_dir, args.hits_ent, args.hits_rel, args.heuristics)
