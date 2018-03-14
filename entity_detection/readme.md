p8shi@dragon00:/mnt/collections/p8shi/dev/SimpleDBPediaQA/entity_detection$ python top_retrieval.py --trained_model saved_checkpoints/lstm/id1_best_model.pt --entity_detection_mode LSTM
Note: You are using GPU for training
EntityDetection (
  (embed): Embedding(31598, 300)
  (lstm): LSTM(300, 300, num_layers=2, dropout=0.3, bidirectional=True)
  (dropout): Dropout (p = 0.3)
  (relu): ReLU ()
  (hidden2tag): Sequential (
    (0): Linear (600 -> 600)
    (1): BatchNorm1d(600, eps=1e-05, momentum=0.1, affine=True)
    (2): ReLU ()
    (3): Dropout (p = 0.3)
    (4): Linear (600 -> 4)
  )
)
Dataset: valid
/mnt/collections/p8shi/dev/SimpleDBPediaQA/entity_detection/entity_detection.py:57: UserWarning: RNN module weights are not part of single contiguous chunk of memory. This means they need to be compacted at every call, possibly greately increasing memory usage. To compact weights again call flatten_parameters().
  outputs, (ht, ct) = self.lstm(x, (h0, c0))
Dev Precision:  89.926233% Recall:  90.615563% F1 Score:  90.269582%
4305it [00:00, 134608.20it/s]
Dataset: test
Dev Precision:  89.537965% Recall:  90.413031% F1 Score:  89.973370%
8595it [00:00, 134061.88it/s]