# transfer-learning-for-chinese-ner

> follow paper TRANSFER LEARNING FOR SEQUENCE TAGGING WITH HIERARCHICAL RECURRENT NETWORKS

## Models

![](http://ww1.sinaimg.cn/large/e1ac6bd5ly1fwq2lqapizj21ba16ajzt.jpg)

本文将transfer learning分为了三个层次

1. cross-domain transfer where label mapping is possible
2. cross-domain transfer with disparate label sets
3. cross-lingual transfer

这里仅先实现第二点，作中文NER，原文GitHub是theano实现的，这里用tensorflow

## Requirements

```
tensorflow > 1.10
python == 3.65
```

V1.0:
    V1.0.0 ==> 把NER對應到Transfer learning的結果初步顯示，以單詞(Char)為單位
    V1.0.1 ==> 以詞彙(Vocab)為單位的顯示各名詞實體(Entity)
        V1.0.1.result_upload ==> 1) 主程式重新命名(main -> app); 2) 各程式格式修正; 3) 12/6初步模型結果
