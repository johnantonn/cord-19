# cord-19
COVID-19 Open Research Dataset Challenge (CORD-19)

# Description

Development of text and data mining techniques that can help the medical community develop answers to high priority scientific questions related to the recent coronavirus global outbreak.

# Dependencies

The code is developed with Python 3.8 while the major dependency packages include:
- [Elasticsearch Server 7.6](https://github.com/elastic/elasticsearch)
- [Elasticsearch DSL](https://github.com/elastic/elasticsearch-dsl-py/blob/master/docs/index.rst)

# Dataset

The dataset is composed of scientific paper articles related to the covid-19 disease and is provided by the respective [Kaggle competition dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge). 

More specifically, the dataset includes:
 - Metadata entries in a single `csv` file.
 
 - Full paper `json` documents.
 
# Steps

## Preprocessing

To preprocess the input data:
 - Place folders that contain the json full papers and the `metadata.csv` file in the `data/original` folder.
 
 - Run the `csv_processing.py` script:
   ```bash
   $ python app/csv_processing.py data/original data/processed
   ```
   
 - Run the `json_preprocessing.py` script:
   ```bash
   $ python app/json_preprocessing.py data/original data/processed
   ```
   
 The above will result in the processed files to be outputted in the `data/output` folder.
 
 ## Indexing
 
 To index the preprocessed data into Elasticsearch:
 - Run elasticsearch server, for more details see [here](https://github.com/elastic/elasticsearch).

 - Run the `index_metadata.py` script:
   ```bash
   $ python app/index_metadata.py
   ```
 - Run the `index_papers.py` script:
   ```bash
   $ python app/index_papers.py
   ```
