#coding:utf8
import sys

#/home/pvf/liumeiyi/BERT/bert/embedding_graph.txt
relation_id = open('relation2id.txt', 'r')
relation_embedding = open('relation2vec.bern.ori', 'r')
relation_list = []
adjust_dict = {}
ori_embedding = {}
for line in relation_id:
	relation = line.strip().split('\t')[0].split(':')[1]
	relation_list.append(relation)

line_cnt = 0
for line in relation_embedding:
	line_cnt += 1
	ori_embedding[line_cnt] = line

for line in sys.stdin:
	relation = line.strip().split('\t')[0]
	embedding = map(float, line.strip().split('\t')[1].split(','))
	if relation in relation_list:
		if relation in adjust_dict:
			adjust_dict[relation].append(embedding)
		else:
			adjust_dict[relation] = [embedding]

adjust_line_cnt = 0
for i in relation_list:
	adjust_line_cnt += 1
	if i in adjust_dict.keys():
#for i in adjust_dict.keys():
		num_embedding = len(adjust_dict[i])
		sum_embedding = []
		#print adjust_dict[i]
		for j in range(num_embedding):
			sum_embedding += adjust_dict[i][j]
		#print sum_embedding
		embedding_adjust = []
		for n in sum_embedding:
			adjust_n = float(n)/num_embedding
			embedding_adjust.append(adjust_n)
		#print i + '\t' + ','.join(str(m) for m in embedding_adjust)
		#print '\t'.join(str(m) for m in embedding_adjust)
	else:
		print ori_embedding[adjust_line_cnt]

