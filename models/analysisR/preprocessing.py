import json
import pandas as pd
from collections import defaultdict
from operator import itemgetter

raw = {}
with open('../../input/train.json', 'rb') as fp:
    for r in fp:
 	   raw = json.loads(r)

units = {}
for unit in raw['listing_id']:
    units[unit] = {}

bool_features = defaultdict(int)
unfeatures = ('listing_id', 'photos')

# screen for desired features while building up rest of unit info
bool_features = defaultdict(int)

# todo: look at description and extract common ngrams (1, 2, 3)
# for now, just bigrams
description_ngrams = defaultdict(int)

# get only 50 most popular buildings and managers
building_ids = defaultdict(int)
manager_ids = defaultdict(int)

# todo: strip out all non-alphanumeric chars
unwanted_chars = ['\t', '/', '<', '>', '.']

for feature in raw:
	if feature not in unfeatures:
		if feature == 'description':
			for unit in raw[feature]:
				d = raw[feature][unit].lower().strip()
				for char in unwanted_chars:
					d = d.replace(char, '')
				units[unit][feature] = {}
				prev_word = ''
				for word in d.split(' '):
					if len(word) > 3:
						if prev_word:
							bigram = prev_word + ' ' + word
							description_ngrams[bigram] += 1
							units[unit][feature][bigram] = 1
						prev_word = word
		elif feature == 'features':
			for unit in raw[feature]:
				units[unit][feature] = {}
				for f in raw[feature][unit]:
					f_ = f.strip().lower()
					bool_features[f_] += 1
					units[unit][feature][f_] = 1
		elif feature == 'building_id':
			for unit in raw[feature]:
				building_id = raw[feature][unit].strip().replace('\t','')
				units[unit][feature] = building_id
				building_ids[building_id] += 1
		elif feature == 'manager_id':
			for unit in raw[feature]:
				manager_id = raw[feature][unit].strip().replace('\t','')
				units[unit][feature] = manager_id
				manager_ids[manager_id] += 1
		else:
			for unit in raw[feature]:
				try:
					units[unit][feature] = raw[feature][unit].strip().replace('\t','')
				except:
					units[unit][feature] = raw[feature][unit]

retained_bool_feature = set()
for feature in bool_features:
	if bool_features[feature] > 999:
		retained_bool_feature.add(feature)

retained_building_ids = set([x for x,y in sorted(building_ids.items(), key=itemgetter(1), reverse=True)[1:50]])
retained_manager_ids = set([x for x,y in sorted(manager_ids.items(), key=itemgetter(1), reverse=True)[1:50]])
retained_descriptors = set([x for x,y in sorted(description_ngrams.items(), key=itemgetter(1), reverse=True)[1:100]])

n = 0
with open('framed_data_1.csv', 'w') as df:
	df.write('unit')
	for feature in raw:
		if feature not in unfeatures:
			if feature == 'description':
				for f in retained_descriptors:
					df.write('\t' + f)
			elif feature == 'features':
				for f in retained_bool_feature:
					df.write('\t' + f)
			else:
				df.write('\t' + feature)
	df.write('\n')
	for unit in units:
		df.write(unit)
		for feature in raw:
			if feature not in unfeatures:
				if feature == "description": 
					for f in retained_descriptors:
						df.write('\t')
						if f in units[unit][feature]:
							df.write(str(1))
						else:
							df.write(str(0))
				elif feature == "features":
					for f in retained_bool_feature:
						df.write('\t')
						if f in units[unit][feature]:
							df.write(str(1))
						else:
							df.write(str(0))
				elif feature == "building_id":
					if units[unit][feature] in retained_building_ids:
						df.write('\t' + str(units[unit][feature]))
					else:
						df.write('\t' + 'other')
				elif feature == "manager_id":
					if units[unit][feature] in retained_manager_ids:
						df.write('\t' + str(units[unit][feature]))
					else:
						df.write('\t' + 'other')
				elif feature in units[unit]:
					try:
						df.write('\t' + str(units[unit][feature]))
					except:
						df.write('\t')					
		df.write('\n')
		n += 1
		if n % 10000 == 0:
			print n, ' done.'
print 'All done.'