"""
  Index json papers into Elasticsearch
  - The original json files need to have beeen preprocessed 
    and placed in output directory
  - Elasticsearch server must be up 'n' running
"""
from elasticsearch_dsl import Index, connections, analyzer, tokenizer
import json
import os
import csv

# Default connection and Elasticsearch client
connections.create_connection()
es = connections.get_connection()

# Analyzer
my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer(
                           'trigram', 'nGram', min_gram=3, max_gram=3),
                       filter=['lowercase']
                       )

# Index
i = Index('papers')
i.analyzer(my_analyzer)
i.create()

# Indexing
outputDir = '..\output'
count = 0
for filename in os.listdir(outputDir):
    if filename.endswith(".json"):
        # increment counter
        count += 1
        # read file
        with open(os.path.join(outputDir, filename), 'r') as myfile:
            data = myfile.read()
            # load into json object
            doc = json.loads(data)
            # index to Elasticsearch
            es.index(index="papers", id=count, body=doc)
            print('Indexing document id:', count)
            myfile.close()
    else:
        continue

# Simple match query
sr = es.search(index="papers", body={"query": {"match_all": {}}})
print("Got %d hits" % sr['hits']['total']['value'])
