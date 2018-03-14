p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/relation_prediction$ python top_retrieval.py --relation_prediction_mode CNN --trained_model saved_checkpoints/cnn/freebaserel_best_model.pt --hits 5
Note: You are using GPU for training
RelationPrediction (
  (embed): Embedding(31598, 300)
  (conv1): Conv2d(1, 300, kernel_size=(2, 300), stride=(1, 1), padding=(1, 0))
  (conv2): Conv2d(1, 300, kernel_size=(3, 300), stride=(1, 1), padding=(2, 0))
  (conv3): Conv2d(1, 300, kernel_size=(4, 300), stride=(1, 1), padding=(3, 0))
  (dropout): Dropout (p = 0.5)
  (fc1): Linear (900 -> 507)
)
Dataset: valid
valid Precision:  73.333333%
no. retrieved: 3815 out of 4305
valid Retrieval Rate  88.617886
Dataset: test
test Precision:  73.507853%
no. retrieved: 7606 out of 8595
test Retrieval Rate  88.493310

p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/relation_prediction$ python top_retrieval.py --relation_prediction_mode CNN --trained_model saved_checkpoints/cnn/id1_best_model.pt --hits 5
Note: You are using GPU for training
RelationPrediction (
  (embed): Embedding(31598, 300)
  (conv1): Conv2d(1, 300, kernel_size=(2, 300), stride=(1, 1), padding=(1, 0))
  (conv2): Conv2d(1, 300, kernel_size=(3, 300), stride=(1, 1), padding=(2, 0))
  (conv3): Conv2d(1, 300, kernel_size=(4, 300), stride=(1, 1), padding=(3, 0))
  (dropout): Dropout (p = 0.5)
  (fc1): Linear (900 -> 178)
)
Dataset: valid
valid Precision:  91.265970%
no. retrieved: 4272 out of 4305
valid Retrieval Rate  99.233449
Dataset: test
test Precision:  90.506108%
no. retrieved: 8517 out of 8595
test Retrieval Rate  99.092496


p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/relation_prediction$ python top_retrieval.py --relation_prediction_mode CNN --trained_model saved_checkpoints/cnn/full_rel_best_model.pt --hits 5
Note: You are using GPU for training
RelationPrediction (
  (embed): Embedding(31598, 300)
  (conv1): Conv2d(1, 300, kernel_size=(2, 300), stride=(1, 1), padding=(1, 0))
  (conv2): Conv2d(1, 300, kernel_size=(3, 300), stride=(1, 1), padding=(2, 0))
  (conv3): Conv2d(1, 300, kernel_size=(4, 300), stride=(1, 1), padding=(3, 0))
  (dropout): Dropout (p = 0.5)
  (fc1): Linear (900 -> 170)
)
Dataset: valid
valid Precision:  89.245064%
no. retrieved: 4267 out of 4305
valid Retrieval Rate  99.117305
Dataset: test
test Precision:  88.563118%
no. retrieved: 8502 out of 8595
test Retrieval Rate  98.917976