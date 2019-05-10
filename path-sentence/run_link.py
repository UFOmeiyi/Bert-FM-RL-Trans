#!/usr/bin/env python

from KB import KB
from BFS import BFS
import sys

def run(kb_file, entity1, entity2, diff_num):
	kb = KB()
	with open(kb_file, 'r') as f:
		for line in f.readlines():
			ent1, rel, ent2 = extract(line.rstrip())
			rel_inv = rel + '_inv'
			kb.addRelation(ent1, rel, ent2)
			kb.addRelation(ent2, rel_inv, ent1)
	#print 'Finishing building'
	num_intermediates = int(diff_num)
	intermediates = pickRandomIntermediatesFrom(kb, entity1, entity2, num_intermediates)
	res_entity_lists = []
	res_path_lists = []
	for i in range(num_intermediates):
		suc1, entity_list1, path_list1 = BFS(kb, entity1, intermediates[i])
		if intermediates[i]==entity2:
			res_entity_lists.append(entity_list1 + entity2)
			res_path_lists.append(path_list1)
		else:
			if not suc1:
				continue
			suc2, entity_list2, path_list2 = BFS(kb, intermediates[i], entity2)
			res_entity_lists.append(entity_list1 + entity_list2[1:])
			res_path_lists.append(path_list1 + path_list2)
	prettyPrint(res_entity_lists, res_path_lists)

def extract(line):
	return line.split('\t')

def pickRandomIntermediatesFrom(kb, entity1, entity2, num_intermediates):
	try:
		return kb.pickRandomIntermediatesBetween(entity1, entity2, num_intermediates)	
	except ValueError as err:
		print(err.args)

def prettyPrint(entity_lists, path_lists):
	if len(entity_lists) == 0:
		print 'Cannot find any path'
	for i in range(len(path_lists)):
		print_link = []
		for j in range(len(path_lists[i])):
			print_link.append(entity_lists[i][j])
			print_link.append(path_lists[i][j])
		print_link.append(entity_lists[i][-1])
		#print print_link
		print ' '.join(i.strip().split(':')[-1] for i in print_link)
	print_link = []

if __name__ == "__main__":
	main()
