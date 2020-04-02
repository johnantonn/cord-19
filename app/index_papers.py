"""
  Index json papers into Elasticsearch
  - The original json files need to have beeen preprocessed 
    and placed in output directory
  - Elasticsearch server must be up 'n' running
"""
from elasticsearch_dsl import Index, connections, analyzer, tokenizer, Mapping
import json
import os

# Default connection and Elasticsearch client
connections.create_connection()
es = connections.get_connection()

# Analyzer
my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer(
                           'trigram', 'nGram', min_gram=3, max_gram=3),
                       filter=['lowercase']
                       )

m = Mapping.from_es('first_draft', using='default')

# Index
i = Index('new_draft')
i.analyzer(my_analyzer)
i.mapping(m)
i.create()

# Indexing
outputDir = 'E:/COVID-19_test/'
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
            es.index(index="new_draft", id=doc["paper_id"], body=doc)
            print('Indexing document id:', count)
            myfile.close()
    else:
        continue
