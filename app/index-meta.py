"""
  Indexing of metadata to Elasticsearch
    - The metadata.csv file needs to be at the parent directory
"""
from elasticsearch_dsl import Index, Text, Document, connections, analyzer, tokenizer
import json
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
i = Index('metadata')
i.analyzer(my_analyzer)
i.create()

# Index metadata
count = 0
metaProps = []
metaDoc = {}
with open('metadata_with_new_dates.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        count += 1
        if(count != 1):
            # create json
            for col in row:
                metaDoc[metaProps[row.index(col)]] = col
                # index json
                es.index(index="metadata", id=count-1, body=metaDoc)
                print('Indexing document id:', count-1)
        else:
            # create json schema
            metaProps = row

print('Finished')
