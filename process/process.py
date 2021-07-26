# Written by Steve Baskauf 2020-06-29 CC0
# Updated to run as a stand-alone script 2021-07-26

import csv
import json
import sys
import os
import shutil
import datetime
import copy
import pandas as pd

# -----------------------
# Configuration section
# -----------------------

# The mutable values come from a JSON configuration file, config.json, that is in the same directory as
# the script. See the example at:
with open('config.json', 'rt', encoding='utf-8') as file_object:
    read_text = file_object.read()
    config = json.loads(read_text)
#print(json.dumps(config, indent=2))

date_issued = config['date_issued'] # generally will be ratification date
local_offset_from_utc = config['local_offset_from_utc'] # time zone used by system clock
vocab_type = config['vocab_type'] # 1 is simple vocabulary, 2 is simple controlled vocabulary, 3 is c.v. with broader hierarchy
namespaces = config['namespaces'] # list of namespace-specific configuration data

# -------------
# Utility functions
# -------------

def readCsv(filename):
    fileObject = open(filename, 'r', newline='', encoding='utf-8')
    readerObject = csv.reader(fileObject)
    array = []
    for row in readerObject:
        array.append(row)
    fileObject.close()
    return array

def writeCsv(fileName, array):
    fileObject = open(fileName, 'w', newline='', encoding='utf-8')
    writerObject = csv.writer(fileObject)
    for row in array:
        writerObject.writerow(row)
    fileObject.close()

    # returns a list with first item Boolean and second item the index
def findColumnWithHeader(header_row_list, header_label):
    found = False
    for column_number in range(0, len(header_row_list)):
        if header_row_list[column_number] == header_label:
            found = True
            found_column = column_number
    if found:
        return [True, found_column]
    else:
        return [False, 0]
    
def isoTime(offset):
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%Y-%m-%dT%H:%M:%S") + offset

# -------------
# Core processing functions
# -------------

# This function contains the Step 2 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def generate_and_copy_mapping_and_config_files(vocab_type, namespaceUri, database, modifications_filename):
    # get the mutable column headers from the modifications file
    modifications_metadata = readCsv(modifications_filename)
    mutable_header = modifications_metadata[0][1:len(modifications_metadata[0])]

    # create database directories
    try:
        os.mkdir('../' + database)
        os.mkdir('../' + database + '-versions')
    # do nothing if there is an error (i.e. they already exist)
    except:
        pass

    # copy files needed in the current terms database directory
    endings = ['-classes.csv', '-replacements-classes.csv', '-replacements-column-mappings.csv', '-replacements.csv', '-versions-classes.csv', '-versions-column-mappings.csv', '-versions.csv']
    source_path = 'files_for_new/current_terms/'
    for file_ending in endings:
        source = source_path + 'template' + file_ending
        destination = '../' + database + '/' + database + file_ending
        dest_path = shutil.copyfile(source, destination)
    dest_path = shutil.copyfile(source_path + 'namespace.csv', '../' + database + '/namespace.csv')

    # select current terms column mapping file appropriate for modifications spreadsheet
    if vocab_type == 1: # simple vocabulary
        in_file = 'simple-vocabulary-column-mappings.csv'
    elif vocab_type == 2: # simple controlled vocabulary
        in_file = 'simple-cv-column-mappings.csv'
    elif vocab_type == 3: # c.v. with skos:broader hierarchy
        in_file = 'cv-hierarchy-column-mappings.csv'
    else: # This should not happen
        in_file = 'simple-vocabulary-column-mappings.csv'

    frame = pd.read_csv(source_path + in_file, na_filter=False)
    for index,row in frame.iterrows():
        # replace the placeholder IRIs with the namespace IRI
        if row['header'] == 'skos_inScheme':
            frame.at[index,'value'] = namespaceUri
        if row['header'] == 'skos_broader':
            frame.at[index,'value'] = namespaceUri
    frame.to_csv('../' + database + '/' + database + '-column-mappings.csv', index=False)
        
    # set the core class file and domain root in the constants.csv configuration file
    frame = pd.read_csv(source_path + 'constants.csv', na_filter=False)
    frame.at[0,'domainRoot'] = namespaceUri
    frame.at[0,'coreClassFile'] = database + '.csv'
    frame.to_csv('../' + database + '/constants.csv', index=False)
        
    # set the versions and replacements filenames in the linked-classes.csv file
    frame = pd.read_csv(source_path + 'linked-classes.csv', na_filter=False)
    for index,row in frame.iterrows():
        # replace the placeholder filenames with the actual linked file names
        if row['link_column'] == 'term_localName':
            frame.at[index,'filename'] = database + '-versions.csv'
        if row['link_column'] == 'replaced_term_localName':
            frame.at[index,'filename'] = database + '-replacements.csv'
    frame.to_csv('../' + database + '/linked-classes.csv', index=False)
        
    # create header row for current terms metadata CSV
    current_terms_header = ['document_modified', 'term_localName', 'term_isDefinedBy', 'term_created', 'term_modified', 'term_deprecated', 'replaces_term', 'replaces1_term', 'replaces2_term'] + mutable_header
    current_terms_table = [current_terms_header]
    file_path = '../' + database + '/' + database + '.csv'
    writeCsv(file_path, current_terms_table)


    # copy files needed in the versions database directory
    endings = ['-versions-classes.csv', '-versions-replacements-classes.csv', '-versions-replacements-column-mappings.csv', '-versions-replacements.csv']
    source_path = 'files_for_new/versions/'
    for file_ending in endings:
        source = source_path + 'template' + file_ending
        destination = '../' + database + '-versions/' + database + file_ending
        dest_path = shutil.copyfile(source, destination)
    #dest_path = shutil.copyfile(source_path + 'linked-classes.csv', '../' + database + '-versions/linked-classes.csv')
    dest_path = shutil.copyfile(source_path + 'namespace.csv', '../' + database + '-versions/namespace.csv')

    # select versions column mapping file appropriate for modifications spreadsheet
    if vocab_type == 1: # simple vocabulary
        in_file = 'simple-vocabulary-versions-column-mappings.csv'
    elif vocab_type == 2: # simple controlled vocabulary
        in_file = 'simple-cv-versions-column-mappings.csv'
    elif vocab_type == 3: # c.v. with skos:broader hierarchy
        in_file = 'cv-hierarchy-versions-column-mappings.csv'
    else: # This should not happen
        in_file = 'simple-vocabulary-versions-column-mappings.csv'

    frame = pd.read_csv(source_path + in_file, na_filter=False)
    for index,row in frame.iterrows():
        # replace the placeholder IRIs with the namespace IRI
        if row['header'] == 'skos_inScheme':
            frame.at[index,'value'] = namespaceUri
        if row['header'] == 'skos_broader':
            frame.at[index,'value'] = namespaceUri
        if row['header'] == 'term_localName':
            frame.at[index,'value'] = namespaceUri
    frame.to_csv('../' + database + '-versions/' + database + '-versions-column-mappings.csv', index=False)

    # set the core class file and domain root in the constants.csv configuration file
    frame = pd.read_csv(source_path + 'constants.csv', na_filter=False)
    frame.at[0,'domainRoot'] = namespaceUri + 'version/'
    frame.at[0,'coreClassFile'] = database + '-versions.csv'
    frame.to_csv('../' + database + '-versions/constants.csv', index=False)

    # set the versions and replacements filenames in the linked-classes.csv file
    frame = pd.read_csv(source_path + 'linked-classes.csv', na_filter=False)
    for index,row in frame.iterrows():
        # replace the placeholder filename with the actual linked file name
        if row['link_column'] == 'replaced_version_localName':
            frame.at[index,'filename'] = database + '-versions-replacements.csv'
    frame.to_csv('../' + database + '-versions/linked-classes.csv', index=False)

    # create header row for versions metadata CSV
    versions_header = ['document_modified', 'version', 'versionLocalName', 'version_isDefinedBy', 'version_issued', 'version_status', 'replaces_version', 'replaces1_version', 'replaces2_version'] + mutable_header + ['term_localName']
    versions_table = [versions_header]
    file_path = '../' + database + '-versions/' + database + '-versions.csv'
    writeCsv(file_path, versions_table)

# This function contains the Step 3 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def determine_state_of_data_tables(database, modifications_filename):
    # 2.1 read tables
    terms_metadata_filename = '../' + database + '/' + database + '.csv'
    terms_metadata = readCsv(terms_metadata_filename)

    modifications_metadata = readCsv(modifications_filename)

    # find column numbers
    result = findColumnWithHeader(modifications_metadata[0], 'term_localName')
    if result[0] == False:
        print('The modifications file does not have a term_localName column')
        sys.exit()
    else:
        mods_local_name = result[1]

    # don't error trap here because all existing files should have a local name column header
    result = findColumnWithHeader(terms_metadata[0], 'term_localName')
    metadata_localname_column = result[1]

    # create list of local names
    mods_term_localName = []
    for term_number in range(1, len(modifications_metadata)):
        mods_term_localName.append(modifications_metadata[term_number][mods_local_name])

    # find new and modified terms
    new_terms = []
    modified_terms = []
    for test_term in mods_term_localName:
        found = False
        for term in terms_metadata:
            if test_term == term[metadata_localname_column]:
                found = True
                modified_terms.append(test_term)
        if not found:
            new_terms.append(test_term)

    return terms_metadata, modifications_metadata, mods_local_name, metadata_localname_column, mods_term_localName, new_terms, modified_terms

# This function contains the Step 4 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def generate_term_versions_metadata(database, versions, version_namespace, mods_local_name, modified_terms,local_offset_from_utc, date_issued, modifications_metadata):
    term_versions_metadata_filename = '../' + versions + '/' + versions + '.csv'
    term_versions_metadata = readCsv(term_versions_metadata_filename)

    version_modified = findColumnWithHeader(term_versions_metadata[0], 'document_modified')[1]
    version_column = findColumnWithHeader(term_versions_metadata[0], 'version')[1]
    version_local_name = findColumnWithHeader(term_versions_metadata[0], 'versionLocalName')[1]
    version_isDefinedBy = findColumnWithHeader(term_versions_metadata[0], 'version_isDefinedBy')[1]
    version_issued = findColumnWithHeader(term_versions_metadata[0], 'version_issued')[1]
    version_status = findColumnWithHeader(term_versions_metadata[0], 'version_status')[1]
    replaces_version = findColumnWithHeader(term_versions_metadata[0], 'replaces_version')[1]
    version_term_local_name_column = findColumnWithHeader(term_versions_metadata[0], 'term_localName')[1]

    for term in modified_terms:
        for version_row in range(1, len(term_versions_metadata)):
            if term_versions_metadata[version_row][version_term_local_name_column] == term and term_versions_metadata[version_row][version_status] == 'recommended':
                term_versions_metadata[version_row][version_status] = 'superseded'
                term_versions_metadata[version_row][version_modified] = isoTime(local_offset_from_utc)

    for column in modifications_metadata[0]:
        result = findColumnWithHeader(term_versions_metadata[0], column)
        if result[0] == False:
            print('The versions file is missing the ', column, ' column.')
            sys.exit()

    versions_join_table_filename = '../' + database + '/' + versions + '.csv'
    versions_join_table = readCsv(versions_join_table_filename)

    newVersions = []
    newVersionJoins = []

    for row_number in range(1, len(modifications_metadata)):
        newVersion = []
        # create a column for every column in the term version file
        for column in term_versions_metadata[0]:
            # find the column in the modifications file that matches the version column and add its value
            result = findColumnWithHeader(modifications_metadata[0], column)
            if result[0] == True:
                newVersion.append(modifications_metadata[row_number][result[1]])
            else:
                newVersion.append('')
        # set the modification dateTime for the newly created version
        newVersion[version_modified] = isoTime(local_offset_from_utc)
        newVersions.append(newVersion)

    for rowNumber in range(0, len(newVersions)):
        # need to add one to the row of modifications_metadata because it includes a header row
        currentTermLocalName = modifications_metadata[rowNumber + 1][mods_local_name]
        newVersions[rowNumber][version_issued] = date_issued
        newVersions[rowNumber][version_status] = 'recommended'
        newVersions[rowNumber][version_local_name] = currentTermLocalName + '-' + date_issued
        newVersions[rowNumber][version_isDefinedBy] = version_namespace
        newVersions[rowNumber][version_column] = version_namespace + currentTermLocalName + '-' + date_issued

        # if the new version replaces an older one for the term, we need to provide a value for the `replaces_version` column
        if currentTermLocalName in modified_terms:
            # look through metadata for old versions to find the most recent version of the term
            mostRecent = 'a' # start with a string value earlier in alphabetization than any term version URI
            for version_row in range(1, len(term_versions_metadata)):
                if term_versions_metadata[version_row][version_term_local_name_column] == currentTermLocalName:
                    # Make it the mostRecent if it's later than the previous mostRecent
                    if term_versions_metadata[version_row][version_column] > mostRecent:
                        mostRecent = term_versions_metadata[version_row][version_column]
            # insert the most recent version found into the appropriate column
            newVersions[rowNumber][replaces_version] = mostRecent
        
        # create a join record for each new version and add it to the list of new joins
        newVersionJoin =[ newVersions[rowNumber][version_column], modifications_metadata[rowNumber + 1][mods_local_name] ]
        newVersionJoins.append(newVersionJoin)

    revised_term_versions_metadata = term_versions_metadata + newVersions
    writeCsv('../' + versions + '/' + versions + '.csv', revised_term_versions_metadata)

    revised_term_versions_joins = versions_join_table + newVersionJoins
    writeCsv('../' + database + '/' + versions + '.csv', revised_term_versions_joins)

    versions_replacements_table_filename = '../' + versions + '/' + versions + '-replacements.csv'
    versions_replacements_table = readCsv(versions_replacements_table_filename)

    # create a list to hold the newly generated replacements rows
    newReplacements = []

    for modifiedTerm in modified_terms:
        # generate the newly created version URI for the modified term
        newVersion = version_namespace + modifiedTerm  + '-' + date_issued
        # step through the list of previous versions and find the one with the most recent issued date
        mostRecent = 'a'
        count = 0
        for oldVersion in versions_join_table:
            if count > 0: # skip the header row
                # the second column in the join table is the term local name
                if oldVersion[1] == modifiedTerm:
                    # the first column in the join table is the full version URI
                    if oldVersion[0] > mostRecent:
                        mostRecent = oldVersion[0]
            count +=1
        # once the most revent version URI is found, we need to extract the local name
        mostRecentLocal = mostRecent.split('/')[6]
        newReplacements.append([newVersion, mostRecentLocal])

    revised_versions_replacements_table = versions_replacements_table + newReplacements
    writeCsv('../' + versions + '/' + versions + '-replacements.csv', revised_versions_replacements_table)


# -----------------------
# Main routine
# -----------------------

for namespace in namespaces:
    # Set the values of flags that control the flow of program execution
    borrowed = namespace['borrowed']
    new_term_list = namespace['new_term_list']
    utility_namespace = namespace['utility_namespace']

    # Set the values of namespace-specific configuration variables
    namespaceUri = namespace['namespace_uri']
    database = namespace['database']
    versions = database + '-versions'
    modifications_filename = namespace['modifications_file_path']
    version_namespace = namespaceUri + 'version/'

    # For borrowed terms, the termlist_uri will differ from the namespace URI. 
    # For terms minted by TDWG that follow URI pattern conventions, this should be the empty string and 
    # the termlist_uri will be set to the namespace URI.
    # In both cases the termlist version URI will be constructed from the namespace URI
    termlist_uri = namespace['termlist_uri']

    if termlist_uri == '':
        termlist_uri = namespaceUri
    else:
        # Let users get away with specifying a termlist URI as long as it's the same as the TDWG-issued namespace
        if not borrowed and namespaceUri != termlist_uri:
            print('WARNING: TDWG-minted namespaces should not have a configuration value for termlist_uri!')
            print('Namespace URI =', namespaceUri)
            print('Term list URI =', termlist_uri)
            print()

    # namespace is actually the last component of the termlist URI, not of the namespace URI
    pieces = termlist_uri.split('/')
    namespace = pieces[len(pieces)-2]
    vocabulary = pieces[len(pieces)-3]

    if new_term_list: # If run for existing term lists, it will overwrite a bunch of stuff
        generate_and_copy_mapping_and_config_files(vocab_type, namespaceUri, database, modifications_filename)

    # Determine values needed to interpret and modify tables later
    terms_metadata, modifications_metadata, mods_local_name, metadata_localname_column, mods_term_localName, new_terms, modified_terms = determine_state_of_data_tables(database, modifications_filename)

    # Create term versions-related metadata. Generally only applies to TDWG-minted terms, not borrowed ones
    if not borrowed:
        generate_term_versions_metadata(database, versions, version_namespace, mods_local_name, modified_terms,local_offset_from_utc, date_issued, modifications_metadata)
