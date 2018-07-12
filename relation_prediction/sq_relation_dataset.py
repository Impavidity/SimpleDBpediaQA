from torchtext import data

class SQdataset(data.TabularDataset):
    @classmethod
    def splits(cls, text_field, label_field, path,
               train='train.txt', validation='valid.txt', test='test.txt'):
        return super(SQdataset, cls).splits(
            path=path, train=train, validation=validation, test=test,
            format='tsv', fields=[('id', None), ('text', text_field), ('sub', None), ('small_relation', None),
                                  ("direction", None),("relation", label_field), ('freebase_relation', None), ('ed', None)]
        )