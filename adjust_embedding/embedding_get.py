##############
###nohup cat /home/pvf/liumeiyi/DeepPath/scripts/BFS/path_link/concept_agentbelongstoorganization_link_10|python embedding.py > embedding_graph &
import tensorflow as tf 
import modeling
import collections
import os
import numpy as np 
import json
import sys
import logging

flags = tf.flags
FLAGS = flags.FLAGS
bert_path = '/home/pvf/liumeiyi/BERT/BERT_BASE_DIR/uncase_base/uncased_L-12_H-768_A-12/'

flags.DEFINE_string(
    'bert_config_file', os.path.join(bert_path, 'bert_config.json'),
    'config json file corresponding to the pre-trained BERT model.'
)
flags.DEFINE_string(
    'bert_vocab_file', os.path.join(bert_path,'vocab.txt'),
    'the config vocab file',
)
flags.DEFINE_string(
    'init_checkpoint', os.path.join(bert_path,'bert_model.ckpt'),
    'from a pre-trained BERT get an initial checkpoint',
)
flags.DEFINE_bool("use_tpu", False, "Whether to use TPU or GPU/CPU.")

def convert2Uni(text):
    if isinstance(text, str):
        return text
    elif isinstance(text, bytes):
        return text.decode('utf-8','ignore')
    else:
        print(type(text))
        print('####################wrong################')


def load_vocab(vocab_file):
    vocab = collections.OrderedDict()
    vocab.setdefault('blank', 2)
    index = 0
    with open(vocab_file) as reader:
    # with tf.gfile.GFile(vocab_file, 'r') as reader:
        while True:
            tmp = reader.readline()
            if not tmp:
                break
            token = convert2Uni(tmp)
            token = token.strip()
            vocab[token] = index 
            index+=1
    return vocab


#def inputs(vectors, maxlen = 50):
def inputs(vectors, maxlen):
    length = len(vectors)
    if length > maxlen:
        return vectors[0:maxlen], [1]*maxlen, [0]*maxlen
    else:
        input = vectors+[0]*(maxlen-length)
        mask = [1]*length + [0]*(maxlen-length)
        segment = [0]*maxlen
        return input, mask, segment


def response_request(text):
    #vectors = [dictionary.get('[CLS]')] + [dictionary.get(i) if i in dictionary else dictionary.get('[UNK]') for i in list(text)] + [dictionary.get('[SEP]')]
    vocab_list = ['[CLS]']
    #vectors = [dictionary.get('[CLS]')] + [dictionary.get(i) if i in dictionary else dictionary.get('[UNK]') for i in text.strip().split(' ')] + [dictionary.get('[SEP]')]
    vectors = [dictionary.get('[CLS]')]
    for i in text.strip().split(' '):
        if i in dictionary:
            vocab_list.append(i)
            vectors.append(dictionary.get(i))
        else:
            vocab_list.append(i)
            vectors.append(dictionary.get('[UNK]'))
    vocab_list.append('[SEP]')
    vectors.append(dictionary.get('[SEP]'))

    maxlen = len(text.strip().split(' ')) + 2
    input, mask, segment = inputs(vectors, maxlen)

    input_ids = np.reshape(np.array(input), [1, -1])
    input_mask = np.reshape(np.array(mask), [1, -1])
    segment_ids = np.reshape(np.array(segment), [1, -1])
    embedding = tf.squeeze(model.get_sequence_output())
    rst = sess.run(embedding, feed_dict={'input_ids_p:0':input_ids, 'input_mask_p:0':input_mask, 'segment_ids_p:0':segment_ids})

    #return json.dumps(rst.tolist(), ensure_ascii=False)
    #response_list = json.dumps(rst.tolist(), ensure_ascii=False)
    #print '\n'.join(i for i in rst.tolist())
    #print len(rst.tolist())
    for i in range(len(rst.tolist())):
        print vocab_list[i] + '\t' + ','.join(str(j) for j in rst.tolist()[i])

dictionary = load_vocab(FLAGS.bert_vocab_file)
init_checkpoint = FLAGS.init_checkpoint

sess = tf.Session()
bert_config = modeling.BertConfig.from_json_file(FLAGS.bert_config_file)

input_ids_p = tf.placeholder(shape=[None, None], dtype = tf.int32, name='input_ids_p')
input_mask_p = tf.placeholder(shape=[None, None], dtype = tf.int32, name='input_mask_p')
segment_ids_p = tf.placeholder(shape=[None, None], dtype = tf.int32, name='segment_ids_p')

model = modeling.BertModel(
    config = bert_config,
    is_training = FLAGS.use_tpu,
    input_ids = input_ids_p,
    input_mask = input_mask_p,
    token_type_ids = segment_ids_p,
    use_one_hot_embeddings = FLAGS.use_tpu,
)
#print('####################################')
restore_saver = tf.train.Saver()
restore_saver.restore(sess, init_checkpoint)

#print(response_request('appen pen'))
cnt = 0
for line in sys.stdin:
    cnt += 1
    response_request(line)
    if cnt%1000 == 0:
        logging.warning('line' + str(cnt))
