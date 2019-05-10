import sys
from run_link import run

kb_dir = '/home/pvf/liumeiyi/DeepPath/NELL-995/raw.kb'
for line in sys.stdin:
	#print line
	entity1,entity2,relation = line.strip().split('\t')
	link_entity_list = run(kb_dir,entity1,entity2,10)
