# Mandarin NER Model in Disaster Management
> **Adapted from:** [*transfer-learning-for-chinese-ner*](https://github.com/ProHiryu/transfer-learning-for-chinese-ner)
> **Publish:** [*Data-Augmented Hybrid Named Entity Recognition for Disaster Management by Transfer Learning*](https://www.mdpi.com/2076-3417/10/12/4234)

## Models
### Methodolgy Structure
<center>
<img src="https://i.imgur.com/wadCBeQ.png" height=300>
</center>

### Transfer Learning Prototype
> **Cited from** *Yang, Z.; Salakhutdinov, R.; Cohen, W.W. Transfer learning for sequence tagging with hierarchical recurrent networks. arXiv 2017, arXiv:1703.06345*
<center>
<img src="https://i.imgur.com/fN8fRHq.png" height=200>
</center>

### Augmented Model (Transfer Learning)
<center>
<img src="https://i.imgur.com/UkmJdFn.png" height=500>
</center>

### Example
<center>
<img src="https://i.imgur.com/e3Gbpx3.png" height=200>
</center>

## Requirements

```
tensorflow > 1.14.0
python == 3.7
```

## Usage

In commander: (detailed options are described in app.py)
```
python app.py
options:  [--mode=train,demo]
          [--embedding_size]
          [--hidden_size]
          [--dropout]
          [--PROJ]
          [--lr]
          [--grad_clip]
          [--project_size]
          [--batch_size]
          [--epochs]
          [--train_data]
          [--test_data]
          [--transfer_train_data]
          [--transfer_test_data]
          [--model_path]
          [--demo_model_path]
          [--map_path]
          [--wiki_path]
          [--tag2label_path]
          [--transfer_tag2label_path]
```
