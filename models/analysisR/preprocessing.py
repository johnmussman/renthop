import json
import pandas as pd
from collections import defaultdict

raw = {}
with open('../../input/train.json', 'rb') as fp:
    for r in fp:
 	   raw = json.loads(r)

units = {}
for unit in raw['listing_id']:
    units[unit] = {}

bool_features = defaultdict(int)
unfeatures = ('listing_id', 'photos', 'description')

# screen for desired features while building up rest of unit info
bool_features = defaultdict(int)

for feature in raw:
    if feature not in unfeatures:
    	if feature == 'features':
    		for unit in raw[feature]:
    			units[unit][feature] = {}
    			for f in raw[feature][unit]:
	    			bool_features[f.strip().lower()] += 1
	    			units[unit][feature][f.strip().lower()] = 1
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

n = 0
with open('framed_data_1.csv', 'w') as df:
	df.write('unit')
	for feature in raw:
		if feature not in unfeatures:
			if feature == 'features':
				for f in retained_bool_feature:
					df.write('\t' + f)
			else:
				df.write('\t' + feature)
	df.write('\n')
	for unit in units:
		df.write(unit)
		for feature in raw:
			if feature not in unfeatures:
				if feature == "features":
					for f in retained_bool_feature:
						df.write('\t')
						if f in units[unit][feature]:
							df.write(str(1))
						else:
							df.write(str(0))
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

print 'Featureset:'
print retained_bool_feature