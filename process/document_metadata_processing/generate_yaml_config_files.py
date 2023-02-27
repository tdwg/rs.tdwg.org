# This script can be used to generate template YAML configuration files from existing rows 
# in the table, but most times you won't need to do that.

import pandas as pd
import yaml
import json
import sys
from os.path import exists

def csv_read(path, **kwargs):
    """Loads a CSV table into a Pandas DataFrame with all cells as strings and blank cells as empty strings
    
    Keyword argument:
    rows -- the number of rows of the table to return when used for testing. When omitted, all rows are returned.
    """
    dataframe = pd.read_csv(path, na_filter=False, dtype = str)
    if 'rows' in kwargs:
        return dataframe.head(kwargs['rows']).copy(deep=True)
    else:
        return dataframe
    
repo_path = '../../'
general_config_path = 'general_configuration.yaml'

# Load data from a YAML configuration file.
if exists(general_config_path):
    with open(general_config_path) as file_object:
        config_data = yaml.safe_load(file_object)
else:
    sys.exit('Must have a general_configuration.yaml file for this script to operate.')

# The doc_iri determines the row of the table to be used to generate the sample
doc_iri = config_data['docIri']

current_docs_df = csv_read(repo_path + 'docs/docs.csv')

# Find the row index if the document already exists
row_matches = current_docs_df.index[current_docs_df['current_iri']==doc_iri].tolist()
if len(row_matches) == 0:
    print('Document IRI not found in existing data.')
    new_document = True
elif len(row_matches) > 1:
    sys.exit('Multiple rows match the document IRI:' + str(row_matches))
else:
    row_index = row_matches[0]
    new_document = False

    # .squeeze() turns a single-row or column dataframe into a series.
    # See https://stackoverflow.com/questions/50575802/convert-dataframe-row-to-dict
    # and https://www.w3resource.com/pandas/dataframe/dataframe-squeeze.php
    row_data = current_docs_df[current_docs_df['current_iri']==doc_iri].squeeze().to_dict()

with open('document_configuration.yaml', 'w', encoding = "utf-8") as file_object:
    dump = yaml.dump(row_data, allow_unicode=True, sort_keys=False)
    file_object.write(dump)

# Data for authors
current_docs_df = csv_read(repo_path + 'docs/docs-authors.csv')

rows_list = []
for index, row in current_docs_df.iterrows():
    # The row is a Pandas series whose items can be referenced by their identifiers (from the column headers)
    if row['document']==doc_iri:
        row_dict = row.to_dict()
        del row_dict['document']
        rows_list.append(row_dict)

with open('authors_configuration.yaml', 'w', encoding = "utf-8") as file_object:
    #dump = yaml.dump(rows_list)
    dump = yaml.dump(rows_list, allow_unicode=True, sort_keys=False)
    dump = dump.replace('\n-', '\n\n-') # Insert extra newline between records
    file_object.write(dump)

#print(json.dumps(rows_list, indent =2))
