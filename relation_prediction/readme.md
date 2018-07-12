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


GRU

p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/relation_prediction$ python top_retrieval.py --relation_prediction_mode GRU --trained_model saved_checkpoints/gru/gru__best_model.pt --hits 5
Note: You are using GPU for training
RelationPrediction (
  (embed): Embedding(31598, 300)
  (gru): GRU(300, 300, num_layers=2, dropout=0.3, bidirectional=True)
  (dropout): Dropout (p = 0.3)
  (relu): ReLU ()
  (hidden2tag): Sequential (
    (0): Linear (600 -> 600)
    (1): BatchNorm1d(600, eps=1e-05, momentum=0.1, affine=True)
    (2): ReLU ()
    (3): Dropout (p = 0.3)
    (4): Linear (600 -> 170)
  )
)
Dataset: valid
/mnt/collections/p8shi/dev/SimpleDBPediaQA/relation_prediction/relation_prediction.py:85: UserWarning: RNN module weights are not part of single contiguous chunk of memory. This means they need to be compacted at every call, possibly greately increasing memory usage. To compact weights again call flatten_parameters().
  outputs, ht = self.gru(x, h0)
valid Precision:  88.106852%
no. retrieved: 4260 out of 4305
valid Retrieval Rate  98.954704
Dataset: test
test Precision:  88.097731%
no. retrieved: 8493 out of 8595
test Retrieval Rate  98.813264