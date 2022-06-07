# This program is released under a GNU General Public License v3.0 http://www.gnu.org/licenses/gpl-3.0
# Author: Steven J. Baskauf
# Date: 2022-06-07

import pandas as pd
import requests

local_upload_directory = '/Users/baskausj/triplestore_upload/'
local_code_directory = '/Users/baskausj/triplestore_code/'

def extract_local_name(iri):
    """Extracts the local name part of an IRI"""
    pieces = iri.split('/')
    last_piece = len(pieces)
    return pieces[last_piece - 1]

# Get the list of datasets from the TDWG rs.tdwg.org repo
dataset_index_df = pd.read_csv('https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/index/index-datasets.csv', na_filter=False, dtype = str)
#dataset_index_df = dataset_index_df.head(1).copy(deep=True) # uncomment to test with one row

associations_list = []
for index, dataset in dataset_index_df.iterrows():
    # Build a row of the graph_file_associations.csv file
    dataset_dict = {}
    dataset_dict['sd:name'] = 'http://rs.tdwg.org/'
    dataset_dict['sd:graph'] = dataset['dataset_iri']
    filename = extract_local_name(dataset['dataset_iri']) + '.ttl'
    dataset_dict['filename'] = filename
    dataset_dict['s3_upload_status'] = ''
    dataset_dict['graph_load_status'] = ''
    associations_list.append(dataset_dict)

    print('downloading', filename)
    retrieve_url = 'http://rs.tdwg.org/dump/' + filename
    #print(retrieve_url)
    response = requests.get(retrieve_url)
    #print(response.text)
    with open(local_upload_directory + filename, 'wt', encoding='utf-8') as file_object:
        file_object.write(response.text)
        
# Now get the DCAT description of all of the datasets
dcat_description_iri = 'http://rs.tdwg.org/index'
associations_list.append({'sd:name': 'http://rs.tdwg.org/', 'sd:graph': dcat_description_iri, 'filename': 'index.ttl', 's3_upload_status': '', 'graph_load_status': ''})
print('downloading index.ttl')
response = requests.get(dcat_description_iri + '.ttl')
with open(local_upload_directory + 'index.ttl', 'wt', encoding='utf-8') as file_object:
    file_object.write(response.text)

print('saving metadata files')
# Save the file assocations
associations_df = pd.DataFrame(associations_list)
associations_df.to_csv(local_code_directory + 'graph_file_associations.csv', index = False)

# Find the latest modification date of the datasets
date_series = dataset_index_df.sort_values(by=['dcterms_modified'], ascending=False).iloc[0]
last_modified = date_series['dcterms_modified']

# Create the named_graphs.csv file
graphs_dict = {}
graphs_dict['sd:name'] = 'http://rs.tdwg.org/'
graphs_dict['dcterms:issued'] = last_modified
graphs_dict['dc:publisher'] = 'Vanderbilt Heard Libraries'
graphs_dict['rdf:type'] = 'sd:NamedGraph'
graphs_dict['dcterms:isPartOf'] = ''
graphs_dict['tdwgutility:status'] = 'production'
graphs_dict['load_status'] = ''

named_graphs_df = pd.DataFrame([graphs_dict])
named_graphs_df.to_csv(local_code_directory + 'named_graphs.csv', index = False)

print('done')
 