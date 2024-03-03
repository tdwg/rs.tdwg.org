# Update TDWG documents metadata

# Author: Steve Baskauf - 2024-03-02
# Version: 0.5
# This program is released under a GNU General Public License v3.0 http://www.gnu.org/licenses/gpl-3.0

# This script is a companion to the other script that updates the vocabularies metadata and 
# should be run after it is finished and any new list of terms documents have been created.

# ---------------------------
# Configuration and function definitions 
# ---------------------------

import pandas as pd
import yaml
import json
import re
import sys
import copy
from os.path import exists
import datetime

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
            
def iso_iime(offset):
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%dT%H:%M:%S") + offset

# --------------------------------
# Load document data

#If the document already exists, its data is retrieved from current documents CSV. 
# A `document_configuration.yaml` file provides new data, which replaces any existing data 
# or is used to create a new record.
# --------------------------------
repo_path = '../../'
new_accessUrl = ''
general_config_path = 'general_configuration.yaml'

# Load data from a YAML configuration file.
if exists(general_config_path):
    with open(general_config_path) as file_object:
        config_data = yaml.safe_load(file_object)
else:
    sys.exit('Must have a general_configuration.yaml file for this script to operate.')

utc_offset = config_data['utcOffset']

# Generate the data subdirectory path from the document IRI in the configuration file
subdirectory_path = '_'.join(config_data['docIri'].split('/')[3:-1]) + '/'
    
#print(json.dumps(config_data, indent=2))
doc_config_path = subdirectory_path + 'document_configuration.yaml'
#print(doc_config_path)
author_config_path = subdirectory_path + 'authors_configuration.yaml'
#print(author_config_path)

# Set the value of any missing config keys to empty string
for key in config_data.keys():
    # Empty YAML values are read in as a None object.
    if config_data[key] is None:
        config_data[key] = ''

version_date = config_data['versionDate']
doc_iri = config_data['docIri']

# Get this value from the document_configuration.yaml file instead of the general_configuration.yaml file.
#standard_iri = config_data['standardIri']


# Pass the document IRI and version date to the document_configuration.yaml file so that it can be used to
# generate the human-readable list of terms document header. Start by opening the file and reading its text.
with open(doc_config_path, 'rt') as file_object:
    file_text = file_object.read()

# Replace the text from "current_iri:" to the end of the line with the document IRI.
file_text = re.sub('current_iri:.*\n', 'current_iri: ' + doc_iri + '\n', file_text)

# Replace all the text between the key and the newline with the new date_issued value.
file_text = re.sub('doc_modified:.*\n', "doc_modified: '" + version_date + "'\n", file_text)

# Write the modified text back out to the file.
with open(doc_config_path, 'wt') as file_object:
    file_object.write(file_text)

# --------------------------------
# Notes about mediaType, accessUri/accessUrl, and browserRedirectUri values in metadata tables

# The docs-versions.csv file has column accessUrl. As far as I can determine, this column
# is not used for anything (at least for modern vocabularies that have human-maintained list of terms documents) 
# and is a vestigial field left to keept the columns stable. 

# The docs-versions.csv file has a column for mediaType. However, it is not exposed anywhere. It is the media type of 
# the web page that is redirected to using the accessUrl field. Generally it is expected to be text/html. It is maintained
# in the docs-versions.csv file in the event that a metadata link is added to the HTML page as a human-readable distribution.

# The mediaType and accessUri fields in the docs-formats.csv and docs-versions-formats.csv files refer to the raw source 
# files used to generate the HTML files that are served. 

# The docs.csv file has a column for accessUrl. However, it is not exposed anywhere. Rather the accessUri column in
# the docs-formats.csv file is used to provide the access IRI. So the accessUrl field in the
# docs.csv file is not updated by this script.

# The browserRedirectUri field in the docs.csv and docs-versions.csv file is accessed by the server to provide the URL
# for redirects from the permanent document version IRIs to that actual web pages. So it is important for
# it to be updated by this script.



# --------------------------------
# Load the current documents CSV file and try to locate a row for the current document.
# --------------------------------

current_docs_df = csv_read(repo_path + 'docs/docs.csv')

# Get the keys of the current_docs_df DataFrame
current_docs_df_keys = current_docs_df.keys()

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
#print('Existing row data:')
#print(json.dumps(row_data, indent=2))
#print()

# Try to load new document data from a configuration file.
if exists(doc_config_path):
    with open(doc_config_path) as file_object:
        new_row_data = yaml.safe_load(file_object)
    
    # Need to stash any new accessUrl, media type, and browser redirect URL that are provided
    if new_row_data['accessUrl'] != None: # Empty YAML values are read in as a None keyword.
        new_accessUrl = new_row_data['accessUrl']

    if new_row_data['mediaType'] != None:
        current_mediaType = new_row_data['mediaType']
    else:
        current_mediaType = ''

    if new_row_data['browserRedirectUri'] != None:
        current_browserRedirectUri = new_row_data['browserRedirectUri']
    else:
        current_browserRedirectUri = ''
    
    # The media type is not recorded in the current docs CSV file. It is recorded in the
    # docs_formats.csv and docs_versions_formats.csv file. So it needs to be removed from the new_row_data
    # dictionary to prevent it from added to the row data for the current document.
    del new_row_data['mediaType']

    # For new documents, the data from the document_configuration.yaml file is used as the initial record.
    if new_document:
        # Create an empty row_data dictionary using the current_docs_df_keys
        row_data = dict.fromkeys(current_docs_df_keys, '')

        # Add the data from the new_row_data dictionary to the row_data dictionary
        for key in new_row_data.keys():
            if new_row_data[key] != None:
                row_data[key] = new_row_data[key]
            else:
                row_data[key] = ''

    # For existing documents, any new data replaces the existing data.
    else:
        for key in new_row_data.keys():
            if new_row_data[key] != None: # Empty YAML values are read in as a None keyword.
                row_data[key] = new_row_data[key]

    # Generate the citation from other metadata bits.
    citation_template = '{creator}. {year}. {document_title}. {publisher}. {current_iri}{ratification_date}'
    citation_template.replace('{creator}', row_data['creator'])
    citation_template.replace('{year}', row_data['doc_modified'][:4])
    citation_template.replace('{document_title}', row_data['documentTitle'])
    citation_template.replace('{publisher}', row_data['publisher'])
    citation_template.replace('{current_iri}', doc_iri)
    citation_template.replace('{ratification_date}', row_data['doc_modified'])
    row_data['citation'] = citation_template
    
else:
    # If the document is new but there isn't a config file, there are no data to work with for the document
    if new_document:
        sys.exit('New documents must have a document_configuration.yaml file.')

# Replace any existing doc_modified date with the new version date
row_data['doc_modified'] = version_date

# Get the standard IRI from the dcterms_isPartOf value. This will come from any existing row data
# or from the document_configuration.yaml file if it is provided.
standard_iri = row_data['dcterms_isPartOf']

#print('New row data:')
#print(json.dumps(row_data, indent=2))

# --------------------------------
# Write new data to the current documents CSV
# --------------------------------

if new_document: # If it's a new document, the row data gets added to the end of the DataFrame
    # Constructs a one-row DataFrame from a list containing a single dict, then concatenates it to the end
    # of the existing DataFrame.
    current_docs_df = pd.concat([current_docs_df, pd.DataFrame([row_data])])
else: # The new values of the row cells replace the old one.
    for key in row_data:
        current_docs_df.at[row_index, key] = row_data[key]

current_docs_df.to_csv(repo_path + 'docs/docs.csv', index = False)

# --------------------------------
# Update the documents versions metadata
# --------------------------------

# Generate a new version for the document based on the current document IRI and version_date.
doc_version_iri = row_data['current_iri'] + version_date

# Load versions list and find most recent version if not a new document.
versions_list_df = csv_read(repo_path + 'docs/docs-versions.csv')
if not new_document:
    matching_versions = versions_list_df[versions_list_df['current_iri']==doc_iri]
    matching_versions = matching_versions.sort_values(by=['version_iri'], ascending=[False])
    most_recent_version_iri = matching_versions.iat[0, 1]
#print(most_recent_version_iri)

# Update the list of document versions in the docs folder
version_row_data = {'current_iri': row_data['current_iri'], 'version_iri': doc_version_iri}
versions_list_df = pd.concat([versions_list_df, pd.DataFrame([version_row_data])])

versions_list_df.to_csv(repo_path + 'docs/docs-versions.csv', index = False)

# Wrangle current document metadata row dictionary to match the versions metadata column headers
versions_data = copy.deepcopy(row_data)

del versions_data['doc_created']
del versions_data['doc_modified']
versions_data['version_issued'] = version_date
versions_data['version_iri'] = doc_version_iri

# The media type recorded directly in the versions file is the media type of the redirected web page. So it will be assumed to be text/html.
# NOTE: this is different from the media type recorded in the docs-formats.csv and docs-versions-formats.csv files, which is the media 
# type of the document file. These values are set later on in the script.
versions_data['mediaType'] = 'text/html'

# Update the document versions metadata in the docs-versions folder
versions_metadata_df = csv_read(repo_path + 'docs-versions/docs-versions.csv')
versions_metadata_df = pd.concat([versions_metadata_df, pd.DataFrame([versions_data])])

# For pre-existing documents:
# the browserRedirectUri value for the previous version needs to be changed from the current document URL to the
# URL of the previous version. This will be done assuming that the standard pattern for version file naming within a
# directory is followed. This is the current document URL (with trailing slash) followed by the version date with no
# trailing slash. 

if not new_document:
    # Find the row for the pre-existing document
    row_matches = versions_metadata_df.index[versions_metadata_df['version_iri']==most_recent_version_iri].tolist()
    if len(row_matches) == 0:
        print('Error: No row in the docs-versions/docs-versions.csv file matches the previous document IRI:' + most_recent_version_iri)
        exit()
    else:
        if len(row_matches) > 1:
            print('Warning: Multiple rows in the docs-versions/docs-versions.csv file match the previous document IRI.\n' + str(row_matches))
            row_index = row_matches[0]
        else:
            row_index = row_matches[0]
        
        # Find the column index for the version_issued column
        version_issued_column_index = versions_metadata_df.columns.get_loc('version_issued')
        # Get the issued date
        previous_version_date = versions_metadata_df.iat[row_index, version_issued_column_index]

        # Find the column index for the browserRedirectUri column
        browserRedirectUri_column_index = versions_metadata_df.columns.get_loc('browserRedirectUri')
        # Now make the replacement
        versions_metadata_df.iat[row_index, browserRedirectUri_column_index] = current_browserRedirectUri + previous_version_date

versions_metadata_df.to_csv(repo_path + 'docs-versions/docs-versions.csv', index = False)

# Update the versions replacements unless the document is new
if not new_document:
    versions_replacements_df = csv_read(repo_path + 'docs-versions/docs-versions-replacements.csv')
    replacement_row_data = {'replacing_document': doc_version_iri, 'replaced_document': most_recent_version_iri}
    versions_replacements_df = pd.concat([versions_replacements_df, pd.DataFrame([replacement_row_data])])
    versions_replacements_df.to_csv(repo_path + 'docs-versions/docs-versions-replacements.csv', index = False)

# --------------------------------
# Update the access URLs and media types
# --------------------------------

# Load format information
formats_metadata_df = csv_read(repo_path + 'docs/docs-formats.csv', na_filter=False, dtype = str)

# Look for the previously used format information for this doc
if not new_document:
    old_accessUrl = formats_metadata_df.loc[formats_metadata_df.doc_iri == doc_iri, 'accessUri'].values[0]
    old_mediaType = formats_metadata_df.loc[formats_metadata_df.doc_iri == doc_iri, 'mediaType'].values[0]
    
#print(old_accessUrl)
#print(old_mediaType)

# If there is a newly provided access URL and media type for the current document, use it.
# Otherwise use the old one.

# NOTE: if it's a new document, a new accessUrl must be provided along with the rest of the metadata.
# If that isn't done, the script here doesn't handle it and will throw an error later when current_accessUrl
# doesn't have a value.
if new_accessUrl:
    current_accessUrl = new_accessUrl
else:
    current_accessUrl = old_accessUrl

if not current_mediaType:
    try:
        current_mediaType = old_mediaType
    # Handle the case where the creator of a new document doesn't bother to give the format in the doc config file
    except: # We assume the document is in Markdown if no information is given
        current_mediaType = 'text/markdown'
        
# For pre-existing documents, we try to replace the values of the accessUrl and mediaType, which might change.
if not new_document:
    # Find the row for the pre-existing document
    not_found = False
    row_matches = formats_metadata_df.index[formats_metadata_df['doc_iri']==doc_iri].tolist()
    if len(row_matches) == 0:
        not_found = True # If not previously present, we'll add it as if it were a new document and fix it.
    else:
        if len(row_matches) > 1:
            print('Warning: Multiple rows in the docs-formats.csv file match the document IRI:' + str(row_matches))
            row_index = row_matches[0]
        else:
            row_index = row_matches[0]
        # Now make the replacements
        formats_metadata_df.at[row_index, 'mediaType'] = current_mediaType
        formats_metadata_df.at[row_index, 'accessUri'] = current_accessUrl
        
# Cases where we need to add a row because the media type wasn't there before  
if new_document or not_found:
    format_row_data = {'doc_iri': doc_iri, 'mediaType': current_mediaType, 'accessUri': current_accessUrl}
    formats_metadata_df = pd.concat([formats_metadata_df, pd.DataFrame([format_row_data])])

# Now save the updated table
formats_metadata_df.to_csv(repo_path + 'docs/docs-formats.csv', index = False)

# Load format information for versions.
versions_format_metadata_df = csv_read(repo_path + 'docs-versions/docs-versions-formats.csv')

# The previous version needs to have its access URL changed since it's not the current version webpage any more.
if not new_document:
    # Find the row for the pre-existing document
    not_found = False
    row_matches = versions_format_metadata_df.index[versions_format_metadata_df['version_iri']==most_recent_version_iri].tolist()
    if len(row_matches) == 0:
        print('no match found')
        not_found = True # If not previously present, we'll add it as if it were a new document and fix it.
    else:
        if len(row_matches) > 1:
            print('Warning: Multiple rows in the docs-versions-formats.csv file match the document IRI:' + str(row_matches))
            row_index = row_matches[0]
        else:
            row_index = row_matches[0]

        # We will generate the new access URL assuming that the standard pattern for version URLs is being used.
        # That is, the current document file is named "index.md" and the previous version file is named with the date of the
        # previous version, plus ".md". So we must find the previous version date, then construct the URL by replacing the
        # "index" in the current URL with the date.

        # Find the date of the previous version by matching the most_recent_version_iri to the version_iri column of the
        # versions_metadata_df DataFrame, then getting the version_issued value from the same row.
        previous_version_date = versions_metadata_df.loc[versions_metadata_df.version_iri == most_recent_version_iri, 'version_issued'].values[0]
        #print(previous_version_date)

        # Construct the new access URL by replacing the "index" in the current URL with the date.
        versions_format_metadata_df.at[row_index, 'accessUri'] = current_accessUrl.replace('index', previous_version_date)
            
    # Handle the edge case where the row for the previous document is missing.
    # Doesn't error trap the case where the old access URI isn't provided, but hey, it's an edge case and be more careful.
    if not_found:
        versions_format_row_data = {'version_iri': most_recent_version_iri, 'mediaType': old_mediaType, 'accessUri': config_data['lastVersionAccessUri']}
        versions_format_metadata_df = pd.concat([versions_format_metadata_df, pd.DataFrame([versions_format_row_data])])

# For versions, a new row is always added to the file
versions_format_row_data = {'version_iri': doc_version_iri, 'mediaType': current_mediaType, 'accessUri': current_accessUrl}
versions_format_metadata_df = pd.concat([versions_format_metadata_df, pd.DataFrame([versions_format_row_data])])

versions_format_metadata_df.to_csv(repo_path + 'docs-versions/docs-versions-formats.csv', index = False)

# --------------------
## Update data about authors

# Behaviors:
# 1. If there is a configuration file, it gets used as-is. 
# - For new documents, the authors get added. This is also true for docs-roles.csv .
# - For existing documents, the data from the config file replaces the existing data for the current doc. 
#   Also true for docs-roles.csv .
# 2. If there is no configuration file, the current doc data is unchanged. The previous author information 
#    gets used for the new version. No change is made to the docs-roles.csv file.
# --------------------

# Load existing author data
authors_df = csv_read(repo_path + 'docs/docs-authors.csv')
roles_df = csv_read(repo_path + 'docs-roles/docs-roles.csv')

# Try to load new document data from a configuration file.
# For new documents, the data from the YAML file must be used as the initial record.
if exists(author_config_path):
    # Load the new author data from the YAML file
    with open(author_config_path) as file_object:
        author_data = yaml.safe_load(file_object)
    for author_number in range(len(author_data)):
        # Need to add in the document column
        author_data[author_number]['document'] = doc_iri
        
        # Need to turn None values into empty strings
        for key in author_data[author_number].keys():
            if author_data[author_number][key] == None: # Empty YAML values are read in as a None keyword.
                author_data[author_number][key] = ''
        
    #print(json.dumps(new_author_data, indent=2))
    
    if not new_document:
        # For existing documents, any new data replaces the existing data.
        # Remove existing rows where the doc IRI matches, then add in new author data
        authors_df = authors_df[authors_df['document']!=doc_iri]
        roles_df = roles_df[roles_df['document']!=doc_iri]
        
    # Write the modified author DataFrame back out to the authors data file
    authors_df = pd.concat([authors_df, pd.DataFrame(author_data)])    
    authors_df.to_csv(repo_path + 'docs/docs-authors.csv', index = False)
    
    # The new (or replacement) rows for docs-roles.csv need to be constructed.
    roles_list = []
    for author in author_data:
        roles_dict = {'document': doc_iri, 'contributor_role': author['contributor_role'], 'contributor_literal': author['contributor_literal']}
        # Put the author IRI in the column that corresponds to their role
        contributor_role_column_header = author['contributor_role'].replace(' ', '_') # column headers don't have spaces
        roles_dict[contributor_role_column_header] = author['contributor_iri']
        # Perform a check to warn if the author's role isn't one that's already represented in the columns of the CSV
        if not contributor_role_column_header in roles_df.columns:
            print('WARNING: author', author['contributor_literal'], 'has the role', author['contributor_role'], 'that is not an existing column in the docs-roles.csv file')
        roles_list.append(roles_dict)
    # Now add the generated rows to the end of the dataframe and save
    roles_df = pd.concat([roles_df, pd.DataFrame(roles_list)])    
    roles_df.to_csv(repo_path + 'docs-roles/docs-roles.csv', index = False)    
        
else: # No new author data found, use existing data. The authors of the current documents (docs-authors.csv) are unchanged.
    # Load the existing data from the CSV
    author_data = []
    for index, row in authors_df.iterrows():
        # The row is a Pandas series whose items can be referenced by their identifiers (from the column headers)
        if row['document']==doc_iri:
            row_dict = row.to_dict()
            author_data.append(row_dict)
            
    #print(json.dumps(rows_list, indent=2))
    
# Create author records for the new version
versions_author_metadata_df = csv_read(repo_path + 'docs-versions/docs-versions-authors.csv')

# In each row of the new metadata, change the "document" column to the "document-version" column with a new IRI
versions_author_data = []
for author_dict in author_data:
    del author_dict['document']
    author_dict['document_version'] = doc_version_iri
    versions_author_data.append(author_dict)

# Now add the modified versions author data to the original DataFrame
versions_author_metadata_df = pd.concat([versions_author_metadata_df, pd.DataFrame(versions_author_data)])
versions_author_metadata_df.to_csv(repo_path + 'docs-versions/docs-versions-authors.csv', index = False)

# --------------------
## Update standards components with doc information

# The code in this section will generate a new version of the standard if the version doesn't already exist.
# NOTE: It will not generate a new standard from scratch. That can be done manually or using the 
# vocabularies update script.

# Any changes to the standard description or citation must be done manually.
# --------------------#

# Determine whether the standard had already been updated to a new version or not
std_df = csv_read(repo_path + 'standards/standards.csv')

# Find the row index for the existing standard. 
# NOTE: The standard record must exist and there must only be one row for it. New standards must be added manually.
row_matches = std_df.index[std_df['standard']==standard_iri].tolist()
row_index = row_matches[0]

# Find the standard_modified value for the existing standard
std_modified = std_df.at[row_index, 'standard_modified']

# Check whether the last standard_modified value is the same as the versionDate in the config file
if std_modified != config_data['versionDate']:
    std_version_iri = standard_iri + '/version/' + config_data['versionDate']

    # The standard has been updated to a new version
    # Update the standard_modified value in the standards.csv file
    std_df.at[row_index, 'standard_modified'] = config_data['versionDate']
    # Change the document_modified value to the current date
    std_df.at[row_index, 'document_modified'] = iso_iime(utc_offset)
    std_df.to_csv(repo_path + 'standards/standards.csv', index = False)
    
    # Add a new row to the standards-versions.csv file in the standards folder
    std_version_df = csv_read(repo_path + 'standards/standards-versions.csv')
    std_version_row_data = {'version': std_version_iri, 'standard': standard_iri}
    std_version_df = pd.concat([std_version_df, pd.DataFrame([std_version_row_data])])
    std_version_df.to_csv(repo_path + 'standards/standards-versions.csv', index = False)

    # Add a new row to the standards-versions.csv file in the standards-versions folder
    std_version_df = csv_read(repo_path + 'standards-versions/standards-versions.csv')

    # Find the most recent version of the standard
    std_version_sort_df = std_version_df[std_version_df['standard']==standard_iri].copy()
    std_version_sort_df = std_version_sort_df.sort_values(by=['version'], ascending=False)
    # Get the index of the most recent version
    most_recent_version_index = std_version_sort_df.index[0]
    #print(most_recent_version_index)
    most_recent_version_iri = std_version_sort_df.at[most_recent_version_index, 'version']
    #print(most_recent_version_iri)

    # Edit the most recent version row
    std_version_df.at[most_recent_version_index, 'standard_status'] = 'superseded'
    std_version_df.at[most_recent_version_index, 'document_modified'] = iso_iime(utc_offset)

    # Add a new row for the new version
    # Convert the most recent row into a dictionary
    std_version_row_data = std_version_sort_df.loc[most_recent_version_index].to_dict()
    # Change the version IRI to the new version IRI
    std_version_row_data['version'] = std_version_iri
    # Change the status to 'recommended'
    std_version_row_data['standard_status'] = 'recommended'
    # Change the document_modified date to the current date
    std_version_row_data['document_modified'] = iso_iime(utc_offset)
    # Change the version_issued date to the version date in the config file
    std_version_row_data['version_issued'] = config_data['versionDate']
    # Add the new row to the DataFrame
    std_version_df = pd.concat([std_version_df, pd.DataFrame([std_version_row_data])])
    # Save the DataFrame to the CSV file
    std_version_df.to_csv(repo_path + 'standards-versions/standards-versions.csv', index = False)

    # Add a row to the standards-versions-replacements.csv file
    std_version_replacements_df = csv_read(repo_path + 'standards-versions/standards-versions-replacements.csv')
    std_version_replacements_row_data = {'replacing_standard_version': std_version_iri, 'replaced_standard_version': most_recent_version_iri}
    std_version_replacements_df = pd.concat([std_version_replacements_df, pd.DataFrame([std_version_replacements_row_data])])
    std_version_replacements_df.to_csv(repo_path + 'standards-versions/standards-versions-replacements.csv', index = False)

# Update the standard and standard version parts to include the new version

if new_document:
    # Load existing standards data
    stds_parts_df = csv_read(repo_path + 'standards/standards-parts.csv')
    
    # Add a new row for the new document
    stds_parts_row_data = {'standard': standard_iri, 'part': doc_iri, 'rdf_type': 'foaf:Document'}
    stds_parts_df = pd.concat([stds_parts_df, pd.DataFrame([stds_parts_row_data])])

    stds_parts_df.to_csv(repo_path + 'standards/standards-parts.csv', index = False)

# Load existing standards versions data
stds_version_parts_df = csv_read(repo_path + 'standards-versions/standards-versions-parts.csv')

# Need to remove the obsolete version of this doc that was already assigned to this version of the standard.
if not new_document:
    stds_version_parts_df = stds_version_parts_df[~((stds_version_parts_df['part']==most_recent_version_iri) & (stds_version_parts_df['standard_version']==standard_iri + '/version/' + version_date))]

# Add a new row for the new document version
stds_version_parts_row_data = {'standard_version': standard_iri + '/version/' + version_date, 'part': doc_version_iri}
stds_version_parts_df = pd.concat([stds_version_parts_df, pd.DataFrame([stds_version_parts_row_data])])

stds_version_parts_df.to_csv(repo_path + 'standards-versions/standards-versions-parts.csv', index = False)

print('done')
