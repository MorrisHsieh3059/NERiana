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
    V1.0.2 ==> 1) 更新訓練檔案: tranfer_test (original: 原本來源的、ver1: 手動新增第一版)
               2) 新增transfer_tag: event (json, pkl)

目前待解決:
    1. pattern 複雜句型
    2. 兩個以上句子
    3. 口語單字(例如：)
完成後
    3. 結合到 chatbot


拿原本的去修
     1. Intro:
        使用者體驗 (ruled based) -- 窮舉無極限 ---------------------------------------------------------------------- (呼應)
        所以要提升 (transfer learning) --> contribution 更robust的理解使用者的訊息 可以理解原本ruled base中沒有的單字      |
                                                                                                                      |
     2. Literature Review:                                                                                            |
        把html/css/js的拿掉                                                                                           
        換成transfer learning --> 學習歷程                                                                                   
            莫凡的refernce  (15,16 graphical)
            魟魚/風箏                                                                                  
            但我們把她導入到NLP                                                                                  
            把原本genernal的model introduce to the specific domain                                         
                --> data augmentation  ----------------------------------- (呼應)                                        
                                                                             |                                        
     3. Methodology:                                                         |                                        
        append                                                               |                                        
            i.)   data preprocess                                            |                                        
            ii.)  data augmentation                                          |                                        
            iii.) add train data to existing model ----------------------- (呼應)                                        

     4. Exp result
        i)   our result
        ii)  diff w/ the original
        iii) validation (smarter than rule-based) -- 找學姊(良緣) ------------------------------------------------------

     5. Discussion
        提出來跟大家討論的地方
        補足地方

     6. contribution   
        open source
