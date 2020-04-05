"""
  Elasticsearch client for:
    - metadata index creation (dynamic mapping)
    - indexing of metadata
  Prerequisites:
    - elasticsearch server must be up 'n' running
    - no index with the same name must exist
    - metadata csv file must be provided in 'data/processed' directory
"""
from elasticsearch_dsl import Index, Text, Document, connections, analyzer, tokenizer
import csv
import os

# Define index name
indexName = 'metadata'

# Default connection and Elasticsearch client
connections.create_connection()
es = connections.get_connection()

# Check if index already exists
i = Index(indexName)
index_exists = i.exists()

if not index_exists:
    # Define analyzer
    my_analyzer = analyzer(
        'my_analyzer',
        type="standard",
        stopwords='_english_'
    )

    # Create index
    i.analyzer(my_analyzer)
    i.create()
    print('Created index', indexName)
else:
    print('Index', indexName, 'already exists, skipping creation.')


# Index metadata documents
inputFile = 'data/processed/metadata.csv'
count = 0
metaProps = []
metaDoc = {}
with open(inputFile, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        count += 1
        if(count != 1):
            # create document
            for col in row:
                metaDoc[metaProps[row.index(col)]] = col
            # index document
            es.index(index=indexName, id=count-1, body=metaDoc)
            print('Indexed document, counter:', count-1)
        else:
            # create schema
            metaProps = row

print('Indexed', count, 'metadata entries.')
