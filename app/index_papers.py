"""
  Elasticsearch client for:
    - papers index creation with custom mapping
    - indexing of papers
  Prerequisites:
    - elasticsearch server must be up 'n' running
    - no index with the same name must exist
    - paper json documents must be provided in 'data/processed' directory
"""
from elasticsearch_dsl import connections, analyzer, tokenizer, Index, Mapping, Nested, Text, Object, Long, Field, Keyword
import json
import os

# Define index name
indexName = 'papers'

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

    # Define mapping
    m = Mapping()

    # abstract
    m.field('abstract', Field(
        properties={
            'section': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'text': Text(fields={'keyword': Keyword(ignore_above=256)})
        })
    )
    # back_matter
    m.field('back_matter', Field(
        properties={
            'section': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'text': Text(fields={'keyword': Keyword(ignore_above=256)})
        })
    )
    # bib_entries
    m.field('bib_entries', Field(
        properties={
            'authors': Field(
                properties={
                    'first': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'last': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'middle': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'suffix': Text(fields={'keyword': Keyword(ignore_above=256)})
                }
            ),
            'id': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'issn': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'other_ids': Object(),
            'pages': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'ref_id': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'title': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'venue': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'volume': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'year': Long()
        })
    )
    # body_text
    m.field('body_text', Nested(
        include_in_parent=True,
        properties={
            'cite_spans': Field(
                properties={
                    'end': Long(),
                    'ref_id': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'start': Long(),
                    'text': Text(fields={'keyword': Keyword(ignore_above=256)})
                }
            ),
            'ref_spans': Field(
                properties={
                    'end': Long(),
                    'ref_id': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'start': Long(),
                    'text': Text(fields={'keyword': Keyword(ignore_above=256)})
                }
            ),
            'section': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'text': Text(fields={'keyword': Keyword(ignore_above=256)})
        }
    ))
    # metadata
    m.field('metadata', Field(
        properties={
            'authors': Field(
                properties={
                    'affiliation': Field(
                        properties={
                            'institution': Text(fields={'keyword': Keyword(ignore_above=256)}),
                            'laboratory': Text(fields={'keyword': Keyword(ignore_above=256)}),
                            'location': Field(
                                properties={
                                    'country': Text(fields={'keyword': Keyword(ignore_above=256)}),
                                    'settlement': Text(fields={'keyword': Keyword(ignore_above=256)})
                                }
                            )
                        }
                    ),
                    'email': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'first': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'last': Text(fields={'keyword': Keyword(ignore_above=256)}),
                    'suffix': Text(fields={'keyword': Keyword(ignore_above=256)})
                }
            ),
            'title': Text(fields={'keyword': Keyword(ignore_above=256)})
        })
    )
    # paper_id
    m.field('paper_id', 'text', fields={'keyword': Keyword(ignore_above=256)})
    # ref_entries
    m.field('ref_entries', Field(
        properties={
            'id': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'text': Text(fields={'keyword': Keyword(ignore_above=256)}),
            'type': Text(fields={'keyword': Keyword(ignore_above=256)})
        })
    )

    # Create index
    i.analyzer(my_analyzer)
    i.mapping(m)
    i.create()
    print('Created index', indexName)
else:
    print('Index', indexName, 'already exists, skipping creation.')

# Index paper json documents
inputDir = 'data/processed'
count = 0
for path, subdirs, files in os.walk(inputDir):
    for name in files:
        if name.endswith(".json"):
            # increment counter
            count += 1
            # read file
            with open(os.path.join(path, name), 'r') as myfile:
                data = myfile.read()
                # load into json object
                doc = json.loads(data)
                # index to Elasticsearch
                es.index(index=indexName, id=doc["paper_id"], body=doc)
                print('Indexed document, counter:', count)
                myfile.close()
    else:
        continue

print('Indexed', count, 'papers.')
