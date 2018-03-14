p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/entity_linking$ python entity_linking.py --model_type lstm
Namespace(data_dir='../data', hits=100, index_ent='/mnt/collections/mwazmy/KB/SQ/DBPedia_Entity_Index.pkl', model_type='lstm', output_dir='./results', query_dir='../entity_detection/query_text/lstm')
Total type of text: 13995825
Max Length of entry is 922487, text is category
Source : ../entity_detection/query_text/lstm/query.valid
4305it [04:54, 14.63it/s]
valid
Top1 Entity Linking Accuracy: 0.7797909407665505
Top3 Entity Linking Accuracy: 0.8578397212543554
Top5 Entity Linking Accuracy: 0.8822299651567944
Top10 Entity Linking Accuracy: 0.9068524970963996
Top20 Entity Linking Accuracy: 0.9219512195121952
Top50 Entity Linking Accuracy: 0.9298490127758421
Top100 Entity Linking Accuracy: 0.9326364692218351
Source : ../entity_detection/query_text/lstm/query.test
8595it [09:27, 15.14it/s]
test
Top1 Entity Linking Accuracy: 0.7718440954043049
Top3 Entity Linking Accuracy: 0.8516579406631762
Top5 Entity Linking Accuracy: 0.8771378708551484
Top10 Entity Linking Accuracy: 0.9015706806282723
Top20 Entity Linking Accuracy: 0.9192553810354858
Top50 Entity Linking Accuracy: 0.9279813845258872
Top100 Entity Linking Accuracy: 0.931239092495637