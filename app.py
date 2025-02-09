#!/anaconda3/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

import tensorflow as tf
import numpy as np
import os, argparse, time, random
from model import SpecModel
from utils import get_sentence, get_transform, preprocess_data, BatchManager, load_wordvec
from conlleval import return_report

## Session configuration\
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # default: 0
os.environ["CUDA_VISIBLE_DEVICES"] = '0' #use GPU with ID=0
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
config.gpu_options.allow_growth = True #allocate dynamically

## hyperparameters
parser = argparse.ArgumentParser(description='Transfer Learning on BiLSTM-CRF for Chinese NER task')
parser.add_argument('--embedding_size', type=int, default=100, help='char embedding_dim')
parser.add_argument('--hidden_size', type=int, default=150, help='dim of lstm hidden state')
parser.add_argument('--dropout', type=float, default=0.5, help='dropout keep_prob')
parser.add_argument('--PROJ', type=str, default='Linear', help='use domain masks or not')
parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
parser.add_argument('--grad_clip', type=float, default=5.0, help='gradient clipping')
parser.add_argument('--project_size', type=int, default=150, help='dim of project hidden state')
parser.add_argument('--batch_size', type=int, default=20, help='#sample of each minibatch')
parser.add_argument('--mode', type=str, default='demo', help='mode of want')
parser.add_argument('--epochs', type=int, default=40, help='nums of epochs')
parser.add_argument('--train_data', type=str, default='data/train', help='normal train data')
parser.add_argument('--test_data', type=str, default='data/test', help='normal test data')
parser.add_argument('--transfer_train_data', type=str, default='data/transfer_train', help='transfer train data')
parser.add_argument('--transfer_test_data', type=str, default='data/transfer_test', help='transfer train data')
parser.add_argument('--model_path', type=str, default='ckpt', help='path to save model')
parser.add_argument('--demo_model_path', type=str, default='20200121', help='path to call demo model')
parser.add_argument('--map_path', type=str, default='data/maps.pkl', help='path to save maps')
parser.add_argument('--wiki_path', type=str, default='data/wiki_100.utf8', help='wiki chinese embeddings')
parser.add_argument('--tag2label_path', type=str, default='data/tag2label.json', help='config tag2label')
parser.add_argument('--transfer_tag2label_path', type=str, default='data/transfer_tag2label.json', help='config transfer tag2label')
# parser.add_argument('--transfer_map_path', type=str, default='data/transfer_maps.pkl', help='path to save maps of transfer')
# parser.add_argument('--demo_model', type=str, default='1521112368', help='model for test and demo')
args = parser.parse_args()

paths = {}
model_path = os.path.join(".", "ckpt/")
if not os.path.exists(model_path): os.makedirs(model_path)
ckpt_prefix = os.path.join(model_path, "model")
paths['model_path'] = ckpt_prefix

def get_train_data():
    normal_train, normal_test = get_sentence(args.train_data, args.test_data)
    transfer_train, transfer_test = get_sentence(args.transfer_train_data, args.transfer_test_data)
    char2id, id2char, tag2id, id2tag, transfer_tag2id, transfer_id2tag = get_transform(normal_train + transfer_train,
                                                                                       args.map_path,
                                                                                       args.tag2label_path,
                                                                                       args.transfer_tag2label_path)
    train_data = preprocess_data(normal_train, char2id, tag2id)
    train_manager = BatchManager(train_data, args.batch_size)
    test_data = preprocess_data(normal_test, char2id, tag2id)
    test_manager = BatchManager(test_data, args.batch_size)
    transfer_train_data = preprocess_data(transfer_train, char2id, transfer_tag2id)
    transfer_train_manager = BatchManager(transfer_train_data, args.batch_size)
    transfer_test_data = preprocess_data(transfer_test, char2id, transfer_tag2id)
    transfer_test_manager = BatchManager(transfer_test_data, args.batch_size)

    return train_manager, test_manager, transfer_train_manager, transfer_test_manager, id2char, id2tag, transfer_id2tag

def train(max_epoch=args.epochs):
    train_manager, test_manager, transfer_train_manager, transfer_test_manager, id2char, id2tag, transfer_id2tag = get_train_data()
    with tf.Session(config=config) as sess:
        normal_model   = SpecModel (args=args,
                                    num_tags=len(id2tag),
                                    vocab_size=len(id2char),
                                    name='normal')
        transfer_model = SpecModel (args=args,
                                    num_tags=len(transfer_id2tag),
                                    vocab_size=len(id2char),
                                    name='transfer')
        normal_model.build()
        transfer_model.build()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)
        ckpt = tf.train.get_checkpoint_state(args.model_path)
        if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            print("Creating model with random parameters")
            sess.run(tf.global_variables_initializer())
            embeddings = sess.run(normal_model.get_embeddings().read_value())
            embeddings = load_wordvec(args.wiki_path, id2char, args.embedding_size, embeddings)
            sess.run(normal_model.get_embeddings().assign(embeddings))

        print("========== Start training ==========")
        for i in range(max_epoch):
            loss = []
            transfer_loss = []
            for batch, transfer_batch in zip(train_manager.iter_batch(), transfer_train_manager.iter_batch()):
                step, batch_loss = normal_model.run_one_step(sess, True, batch)
                loss.append(batch_loss)
                if step % 1000 == 0:
                    print("Step: %d Loss: %f" % (step, batch_loss))
                transfer_step, transfer_batch_loss = transfer_model.run_one_step(sess, True, transfer_batch)
                transfer_loss.append(transfer_batch_loss)
                if transfer_step % 1000 == 0:
                    print("Step: %d Transfer Loss: %f" % (transfer_step, transfer_batch_loss))
            print("Epoch: {} Loss: {:>9.6f}".format(i, np.mean(loss)))
            results = normal_model.evaluate(sess, test_manager, id2tag)
            for line in test_ner(results, "data/test_result"):
                print(f"<<Test NER res>>: \n\t\t---> {line}")
            print("Epoch: {} Transfer Loss: {:>9.6f}".format(i, np.mean(transfer_loss)))
            results = transfer_model.evaluate(sess, transfer_test_manager, transfer_id2tag)

            for line in test_ner(results, "data/transfer_test_result"):
                print(f"<<Test transfer res>>: \n\t---> {line}")
            ckpt_file = os.path.join(args.model_path, str(i) + "ner.ckpt")
            saver.save(sess, ckpt_file)
        print("========== Finish training ==========")

def single_train(max_epoch=args.epochs):
    train_manager, test_manager, transfer_train_manager, transfer_test_manager, id2char, id2tag, transfer_id2tag = get_train_data()
    with tf.Session(config=config) as sess:
        transfer_model = SpecModel(args=args,
                                   num_tags=len(transfer_id2tag),
                                   vocab_size=len(id2char),
                                   name='transfer')
        transfer_model.build()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)
        ckpt = tf.train.get_checkpoint_state(args.model_path)
        if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
            print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            print("Creating model with random parameters")
            sess.run(tf.global_variables_initializer())
            embeddings = sess.run(transfer_model.get_embeddings().read_value())
            embeddings = load_wordvec(args.wiki_path, id2char, args.embedding_size, embeddings)
            sess.run(transfer_model.get_embeddings().assign(embeddings))
        print("========== Start training ==========")
        for i in range(max_epoch):
            transfer_loss = []
            for transfer_batch in transfer_train_manager.iter_batch():
                transfer_step, transfer_batch_loss = transfer_model.run_one_step(sess, True, transfer_batch)
                transfer_loss.append(transfer_batch_loss)
                if transfer_step % 1000 == 0:
                    print(f"Step: {transfer_step} Transfer Loss: {transfer_batch_loss}")
            print("Epoch: {} Transfer Loss: {:>9.6f}".format(i, np.mean(transfer_loss)))
            results = transfer_model.evaluate(sess, transfer_test_manager, transfer_id2tag)
            for line in test_ner(results, "data/transfer_test_result"):
                print(f"<<Test NER res>>: \n\t\t---> {line}")
            ckpt_file = os.path.join(args.model_path, str(i) + "ner.ckpt")
            saver.save(sess, ckpt_file)
        print("========== Finish training ==========")

def test_ner(results, path):
    output_file = os.path.join(path)
    with open(output_file, "w", encoding='utf-8') as f:
        to_write = []
        for block in results:
            for line in block:
                to_write.append(line + "\n")
            to_write.append("\n")

        f.writelines(to_write)
    eval_lines = return_report(output_file)
    return eval_lines

def load_input_sentence(sent):
    sentence = []
    for letter in sent:
        sentence.append([letter, 'O'])
    return [sentence]

if __name__ == "__main__":
    if args.mode == 'train':
        train()

    elif args.mode == 'single_train':
        single_train()

    elif args.mode == 'demo':
        """ Globalize it for eternal use """
        # for demo use only
        import pickle
        with open('./data/maps.pkl', 'rb') as fr:
            info = pickle.load(fr)
            char2id = info[0]
            id2char = info[1]
            transfer_tag2id = info[4]
            transfer_id2tag = info[5]
        """ End """


        ### find the latest demo model
        demo_path = os.path.join(".", args.demo_model_path) + "/"
        ckpt_file = tf.train.latest_checkpoint(demo_path)
        print(f"----------------<file route>---------------- ==> {ckpt_file}")

        model = SpecModel(args=args,
                          num_tags=len(transfer_id2tag),
                          vocab_size=len(id2char),
                          name='transfer')
        model.build()
        saver = tf.train.Saver()

        with tf.Session(config=config) as sess:
            print('============= demo =============')
            saver.restore(sess, ckpt_file)

            while True:
                print('Please input your sentence (or key \'exit\' to exit):')
                demo_sent = input().strip()
                demo_sent = demo_sent.replace(" ", "")
                # if demo_sent == '' or demo_sent.isspace():
                if demo_sent == 'exit':
                    print('See you next time!')
                    break
                else:
                    demo_transfer_test = load_input_sentence(demo_sent)
                    demo_transfer_test_data = preprocess_data(demo_transfer_test, char2id, transfer_tag2id)
                    demo_transfer_test_manager = BatchManager(demo_transfer_test_data, args.batch_size)
                    demo_data = model.evaluate(sess, demo_transfer_test_manager, transfer_id2tag)
                    """
                        demo_data format:
                            [
                               [
                                   'char <O> <pred>', ...,
                               ]
                            ]
                        Notes:
                            char
                            <O>: default tag (no meaning)
                            <pred>: predicted transfer tag
                    """

                    ret = { "product_name": [],
                            "time": [],
                            "person_name": [],
                            "org_name": [],
                            "company_name": [],
                            "location": [],
                            "event": [], }
                    # print(f"-------------\n{demo_data[0]}\n--------------")
                    isWord = False
                    tempWord = ""
                    tempTag = ""
                    lastIdx = len(demo_data[0]) - 1
                    idx = 0
                    for sect in demo_data[0]:
                        char, _, tag = sect.split(" ")

                        if (tag == "O" or "B-" in tag) and isWord:
                            ret[tempTag].append(tempWord)
                            isWord = False
                            tempTag = ""
                            tempWord = ""

                        if tag != "O":
                            if not isWord:
                                tempTag = tag[2:]
                                isWord = True
                            tempWord += char

                        if idx == lastIdx and tag != "O":
                            ret[tempTag].append(tempWord)

                        idx += 1
                    print("\n================================ NER / TL results ==================================")

                    for key in ret:
                        """
                            ret format:
                            {
                                "<TAG>": [<word>, ..., <word>],
                            }
                        """
                        # print(f"{key} -->\n      {ret[key]}")
                        print(f"{key} -->")
                        for i in range(len(ret[key])):
                            print(f"    {i + 1}. {ret[key][i]}")

                    print("\n=============================== NER/TL results END =================================")
                    # print(f"char '{char}' with tag '{tag}'")
                    # for char, tag in zip(demo_data[0][0], demo_data[0][1]):
                    #     print(f"{char} with tag '{tag}'")
