# Written by Steve Baskauf 2020-06-29 CC0
# Updated to run as a stand-alone script 2021-07-26
# Additional modifications to require less manual work 2023-08-27

import csv
import json
import yaml
import re
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
with open('config.yaml', 'rt', encoding='utf-8') as file_object:
    config = yaml.safe_load(file_object)

# Configuration for vocabulary and standard metadata. If changes are to an existing vocabulary, the values will be ignored.
with open('vocab.yaml', 'rt', encoding='utf-8') as file_object:
    config_vocab = yaml.safe_load(file_object)

date_issued = config['date_issued'] # generally will be ratification date
local_offset_from_utc = config['local_offset_from_utc'] # time zone used by system clock
vocab_type = config['vocab_type'] # 1 is simple vocabulary, 2 is simple controlled vocabulary, 3 is c.v. with broader hierarchy
standardUri = config['standard'] # IRI of containing standard
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

    # Find new and modified terms.
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

# This function contains the Step 5 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def generate_current_terms_metadata(standardUri, terms_metadata, modifications_metadata, mods_local_name, modified_terms, local_offset_from_utc, date_issued, namespaceUri, termlist_uri, database, versions, term_list_label, term_list_description, pref_namespace_prefix, use_namespace_in_fragment, prepend_url, separator):
    pieces = termlist_uri.split('/')
    list_localname_value = pieces[3] + '/' + pieces[4] + '/'

    term_modified_dateTime = findColumnWithHeader(terms_metadata[0], 'document_modified')[1]
    term_localName = findColumnWithHeader(terms_metadata[0], 'term_localName')[1]
    term_modified = findColumnWithHeader(terms_metadata[0], 'term_modified')[1]
    term_created = findColumnWithHeader(terms_metadata[0], 'term_created')[1]
    term_isDefinedBy = findColumnWithHeader(terms_metadata[0], 'term_isDefinedBy')[1]

    # step through each row in the modification metadata table and modify existing current terms when applicable
    for mods_rownumber in range(1, len(modifications_metadata)):
        mods_localname_string = modifications_metadata[mods_rownumber][mods_local_name]
        modified = False
        for term_name in modified_terms:
            # only make a modification if it's on the list of terms to be modified
            if mods_localname_string == term_name:
                modified = True
        # this section of code modifies existing terms
        if modified:
            # find the row in the terms metadata file for the term to be modified
            for term_rownumber in range(1, len(terms_metadata)):
                if mods_localname_string == terms_metadata[term_rownumber][term_localName]:
                    terms_metadata[term_rownumber][term_modified_dateTime] = isoTime(local_offset_from_utc)
                    terms_metadata[term_rownumber][term_modified] = date_issued
                    # replace every column that's in the modifications metadata
                    for column_number in range(0, len(modifications_metadata[0])):
                        # find the column in the current terms metadata table that matches the modifications column and replace the current term's value
                        result = findColumnWithHeader(terms_metadata[0], modifications_metadata[0][column_number])
                        if result[0] == True:
                            terms_metadata[term_rownumber][result[1]] = modifications_metadata[mods_rownumber][column_number]
                        else:
                            pass # this shouldn't really happen since there already was a check that all columns existed in the versions table
        # this section of code adds new term metadata
        else: 
            newTermRow = []
            for column in range(0, len(terms_metadata[0])):
                newTermRow.append('')
            newTermRow[term_modified_dateTime] = isoTime(local_offset_from_utc)
            newTermRow[term_modified] = date_issued
            newTermRow[term_created] = date_issued
            newTermRow[term_isDefinedBy] = namespaceUri
            # replace every column that's in the modifications metadata
            for column_number in range(0, len(modifications_metadata[0])):
                # find the column in the current terms metadata table that matches the modifications column and replace the current term's value
                result = findColumnWithHeader(terms_metadata[0], modifications_metadata[0][column_number])
                if result[0] == True:
                    newTermRow[result[1]] = modifications_metadata[mods_rownumber][column_number]
                else:
                    pass # this shouldn't really happen since there already was a check that all columns existed in the versions table
            terms_metadata.append(newTermRow)
    writeCsv('../' + database + '/' + database + '.csv', terms_metadata)

    # Section 5 for generating new term lists
    term_lists_table_filename = '../term-lists/term-lists.csv'
    term_lists_table = readCsv(term_lists_table_filename)

    term_lists_versions_joins_filename = '../term-lists/term-lists-versions.csv'
    term_lists_versions_joins = readCsv(term_lists_versions_joins_filename)

    term_lists_members_filename = '../term-lists/term-lists-members.csv'
    term_lists_members = readCsv(term_lists_members_filename)

    term_lists_versions_metadata_filename = '../term-lists-versions/term-lists-versions.csv'
    term_lists_versions_metadata = readCsv(term_lists_versions_metadata_filename)

    term_lists_versions_members_filename = '../term-lists-versions/term-lists-versions-members.csv'
    term_lists_versions_members = readCsv(term_lists_versions_members_filename)

    term_lists_versions_replacements_filename = '../term-lists-versions/term-lists-versions-replacements.csv'
    term_lists_versions_replacements = readCsv(term_lists_versions_replacements_filename)

    datasets_index_filename = '../index/index-datasets.csv'
    datasets_index = readCsv(datasets_index_filename)

    if namespaceUri == 'http://rs.tdwg.org/dwc/terms/attributes/':
        termlistVersionUri = 'http://rs.tdwg.org/dwc/version/terms/attributes/' + date_issued
    else:
        uriPieces = termlist_uri.split('/')
        # split the URI between the vocabulary and term list subpaths
        termlistVersionUri = uriPieces[0] + '//' + uriPieces[2] + '/' + uriPieces[3] + '/version/' + uriPieces[4] + '/' + date_issued

    modified_datetime = findColumnWithHeader(term_lists_table[0], 'document_modified')[1]
    list_uri = findColumnWithHeader(term_lists_table[0], 'list')[1]
    list_localName_column = findColumnWithHeader(term_lists_table[0], 'list_localName')[1]
    list_label = findColumnWithHeader(term_lists_table[0], 'label')[1]
    list_description = findColumnWithHeader(term_lists_table[0], 'description')[1]
    list_created = findColumnWithHeader(term_lists_table[0], 'list_created')[1]
    list_modified = findColumnWithHeader(term_lists_table[0], 'list_modified')[1]
    list_prefix_column = findColumnWithHeader(term_lists_table[0], 'vann_preferredNamespacePrefix')[1]
    list_pref_namespace_column = findColumnWithHeader(term_lists_table[0], 'vann_preferredNamespaceUri')[1]
    list_database_column = findColumnWithHeader(term_lists_table[0], 'database')[1]
    list_versions_database_column = findColumnWithHeader(term_lists_table[0], 'versions_database')[1]
    list_versions_uri_column = findColumnWithHeader(term_lists_table[0], 'versions_uri')[1]
    standard_column = findColumnWithHeader(term_lists_table[0], 'standard')[1]

    aNewTermList = True
    for rowNumber in range(1, len(term_lists_table)):
        # by convention, the namespace URI used for the terms is the same as the URI of the term list
        # Note 2022-04-20: I think that is only true for TDWG-minted term lists, not borrowed ones!
        if termlist_uri == term_lists_table[rowNumber][list_uri]:
            aNewTermList = False
            term_list_rowNumber = rowNumber
            term_lists_table[rowNumber][list_modified] = date_issued
            term_lists_table[rowNumber][modified_datetime] = isoTime(local_offset_from_utc)
            # here is the opportunity to find out the standard URI for the modified term list
            # 2024-03-01 note: this is now provided in the config.yaml file.
            #standardUri = term_lists_table[rowNumber][standard_column]
            # print(term_lists_table[rowNumber])
    if aNewTermList:  # this will happen if the term list did not previously exist
        # Create a new row for the term list table that is a list with length equal to the 0th row of the table
        new_term_list_row = [''] * len(term_lists_table[0])
        
        """
        try:
            new_term_list = readCsv('files_for_new/new_term_list.csv')
        except:
            print('The term list was not found and there was no new_term_list.csv file.')
            sys.exit()
        """
        # Note: no error trapping is done here, so make sure that the new_term_list columns are the same as term_lists_table
        new_term_list_row[modified_datetime] = isoTime(local_offset_from_utc)
        new_term_list_row[list_uri] = termlist_uri
        new_term_list_row[list_localName_column] = list_localname_value
        new_term_list_row[list_created] = date_issued
        new_term_list_row[list_modified] = date_issued
        new_term_list_row[list_prefix_column] = pref_namespace_prefix
        new_term_list_row[list_pref_namespace_column] = namespaceUri
        new_term_list_row[list_database_column] = database
        new_term_list_row[list_versions_database_column] = versions
        new_term_list_row[list_versions_uri_column] = termlistVersionUri
        new_term_list_row[standard_column] = standardUri

        # This is now about the only value that's dependent on filling out the new_term_list.csv file.
        # 2024-03-01 note: this is now provided in the config.yaml file.
        #standardUri = new_term_list[1][standard_column]

        """
        # Assign the label and description passed into the function if not empty string. Otherwise, fall back on what's 
        # already in the new term list table.
        if term_list_label != '':
            new_term_list_row[list_label] = term_list_label
        if term_list_description != '':
            new_term_list_row[list_description] = term_list_description
        """

        # Label and description are now required in the config.yaml file, so no need to check for empty strings.
        new_term_list_row[list_label] = term_list_label
        new_term_list_row[list_description] = term_list_description

        # the length of the table (including header row) will be one more than the last row number
        term_list_rowNumber = len(term_lists_table)
        term_lists_table.append(new_term_list_row)
        # after the new row is appended, its row number will be one more than the previous last row number

        # The new term list's dataset directory must be added to the dataset list. 
        row_for_current_terms = [isoTime(local_offset_from_utc), # document_modified
                                database, # term_localName
                                'http://rs.tdwg.org/index', # dcterms_isPartOf
                                'http://rs.tdwg.org/index/' + database, # dataset_iri
                                date_issued, # dcterms_modified
                                new_term_list_row[list_description], # label
                                ''] # rdfs_comment
        datasets_index.append(row_for_current_terms)
        
        # New term lists will always have a new version dataset directory, so add it, too.
        row_for_versions = [isoTime(local_offset_from_utc), # document_modified
                            versions, # term_localName
                            'http://rs.tdwg.org/index', # dcterms_isPartOf
                            'http://rs.tdwg.org/index/' + versions, # dataset_iri
                            date_issued, # dcterms_modified
                            new_term_list_row[list_description] + ' versions', # label
                            ''] # rdfs_comment
        datasets_index.append(row_for_versions)
        
    else: # If the term list isn't new, then its modified date needs to be updated.
        # find the row in the dataset director file for the dataset being modified
        for dataset_rownumber in range(1, len(datasets_index)):
            # update current terms modified date
            if database == datasets_index[dataset_rownumber][1]: # the name is in column 1
                datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
                datasets_index[dataset_rownumber][4] = date_issued # the date modified is in column 4
            # update versions modified date
            if versions == datasets_index[dataset_rownumber][1]:
                datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
                datasets_index[dataset_rownumber][4] = date_issued

    # Update the date for the term lists and term list versions regardless of whether it's new or not
    for dataset_rownumber in range(1, len(datasets_index)):
        if 'term-lists' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
        if 'term-lists-versions' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
        if 'vocabularies' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
        if 'vocabularies-versions' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
        if 'standards' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
        if 'standards-versions' == datasets_index[dataset_rownumber][1]:
            datasets_index[dataset_rownumber][0] = isoTime(local_offset_from_utc)
            datasets_index[dataset_rownumber][4] = date_issued
            
    writeCsv('../term-lists/term-lists.csv', term_lists_table)
    writeCsv('../index/index-datasets.csv', datasets_index)

    term_lists_versions_joins.append([termlistVersionUri, termlist_uri])
    writeCsv('../term-lists/term-lists-versions.csv', term_lists_versions_joins)

    for newTerm in new_terms:
        term_lists_members.append([termlist_uri, namespaceUri + newTerm])
    writeCsv('../term-lists/term-lists-members.csv', term_lists_members)

    # find the columns than contain needed information
    document_modified = findColumnWithHeader(term_lists_versions_metadata[0], 'document_modified')[1]
    version_uri = findColumnWithHeader(term_lists_versions_metadata[0], 'version')[1]
    version_modified = findColumnWithHeader(term_lists_versions_metadata[0], 'version_modified')[1]
    status_column = findColumnWithHeader(term_lists_versions_metadata[0], 'status')[1]
    localname_column = findColumnWithHeader(term_lists_versions_metadata[0], 'list_localName')[1]
    list_version_label = findColumnWithHeader(term_lists_versions_metadata[0], 'label')[1]
    list_version_description = findColumnWithHeader(term_lists_versions_metadata[0], 'description')[1]
    list_version_prefix_column = findColumnWithHeader(term_lists_versions_metadata[0], 'vann_preferredNamespacePrefix')[1]
    list_version_namespace_uri_column = findColumnWithHeader(term_lists_versions_metadata[0], 'vann_preferredNamespaceUri')[1]
    list_uri = findColumnWithHeader(term_lists_versions_metadata[0], 'list')[1]

    if aNewTermList:
        # Create a new row for the term list table that is a list with length equal to the 0th row of the table

        """
        # get the template for the term list version from first data row in the new_term_list_version.csv file
        try:
            new_term_list_version = readCsv('files_for_new/new_term_list_version.csv')
        except:
            print('The term list version was not found and there was no new_term_list_version.csv file.')
            sys.exit()
        """
        #newListRow = new_term_list_version[1]

        mostRecentListNumber = 0 # dummy list number. Must have a value to be returned, but is not used for a new term list

        # Label, description, and pref prefix are now required in the config.yaml file, so no need to check for empty strings.
        """
        # Assign the label, description, and pref prefix passed into the function if not empty string. Otherwise, fall back on what's 
        # already in the new term list version table.
        if term_list_label != '':
            newListRow[list_version_label] = term_list_label
        if term_list_description != '':
            newListRow[list_version_description] = term_list_description
        if pref_namespace_prefix != '':
            newListRow[list_version_prefix_column] = pref_namespace_prefix
        """

    else:
        # find the most recent previous version of the term list
        mostRecent = 'a' # start the value of mostRecent as something earlier alphabetically than all of the list URIs
        mostRecentListNumber = 0 # dummy list number to be replaced when most recent list is found
        for termListRowNumber in range(1, len(term_lists_versions_metadata)):
            # the row is one of the versions of the list
            if term_lists_versions_metadata[termListRowNumber][list_uri] == termlist_uri:
                # Make the version of the row the mostRecent if it's later than the previous mostRecent
                if term_lists_versions_metadata[termListRowNumber][version_uri] > mostRecent:
                    mostRecent = term_lists_versions_metadata[termListRowNumber][version_uri]
                    mostRecentListNumber = termListRowNumber

        # change the status of the most recent list to superseded
        term_lists_versions_metadata[mostRecentListNumber][status_column] = 'superseded'
        term_lists_versions_metadata[mostRecentListNumber][document_modified] = isoTime(local_offset_from_utc)

        # start the new list row with the metadata from the most recent list
        #newListRow = copy.deepcopy(term_lists_versions_metadata[mostRecentListNumber])

    newListRow = [''] * len(term_lists_versions_metadata[0])

    # Insert metadata to make the most recent list have the updated values
    newListRow[document_modified] = isoTime(local_offset_from_utc)
    newListRow[version_uri] = termlistVersionUri
    newListRow[version_modified] = date_issued
    newListRow[status_column] = 'recommended'
    newListRow[localname_column] = list_localname_value
    newListRow[list_version_label] = term_list_label
    newListRow[list_version_description] = term_list_description
    newListRow[list_version_prefix_column] = pref_namespace_prefix
    newListRow[list_version_namespace_uri_column] = namespaceUri
    newListRow[list_uri] = termlist_uri

    # append the new term list row to the old list of term lists
    term_lists_versions_metadata.append(newListRow)

    # save as a file
    writeCsv('../term-lists-versions/term-lists-versions.csv', term_lists_versions_metadata)

    # -----------------
    # Code added 2024-03-03 to update the redirects file that controls redirects for current terms for this namespace.
    # The redirect record is in the repo_path + 'html/redirects.csv' file.

    redirects_df = pd.read_csv('../html/redirects.csv', dtype=str)
    
    # Create a row for namespace redirect
    if use_namespace_in_fragment:
        use_namespace = 'yes'
        connector = separator
    else:
        use_namespace = 'no'
        connector = ''
    term_redirects_row_data = {'database': database, 'redirect': 'yes', 'type': 'term', 'namespace': pref_namespace_prefix, 'prefix': prepend_url, 'useNamespace': use_namespace, 'connector': connector}

    # Find the row index for the namespace redirect in the pandas dataframe and replace it with the new data.
    # If the row is not found, add it to the end of the pandasdataframe.
    matching_rows_index = redirects_df[redirects_df['database'] == database].index
    if len(matching_rows_index) > 1:
        print('Error: More than one row found for the namespace redirect in the redirects.csv file.')
        sys.exit()
    elif len(matching_rows_index) == 1:
        # replace the row with the new data
        redirects_df.loc[matching_rows_index[0]] = term_redirects_row_data
    else:
        # add the row to the end of the dataframe
        redirects_df = pd.concat([redirects_df, pd.DataFrame([term_redirects_row_data])])

    # Create row for term version redirect
    version_redirects_row_data = {'database': database + '-versions', 'redirect': 'no', 'type': 'termVersion', 'namespace': pref_namespace_prefix, 'prefix': '', 'useNamespace': '', 'connector': ''}
    matching_rows_index = redirects_df[redirects_df['database'] == database + '-versions'].index
    if len(matching_rows_index) > 1:
        print('Error: More than one row found for the term version redirect in the redirects.csv file.')
        sys.exit()
    elif len(matching_rows_index) == 1:
        # replace the row with the new data
        redirects_df.loc[matching_rows_index[0]] = version_redirects_row_data
    else:
        # add the row to the end of the dataframe
        redirects_df = pd.concat([redirects_df, pd.DataFrame([version_redirects_row_data])])

    redirects_df.to_csv('../html/redirects.csv', index = False)

    return version_uri, aNewTermList, term_lists_versions_members, term_lists_versions_metadata, mostRecentListNumber, termlistVersionUri, term_lists_versions_replacements, term_lists_table, term_list_rowNumber

# This function contains the Step 6 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def update_termlist_version_members(aNewTermList, mostRecentListNumber, date_issued, namespaceUri, new_terms, modified_terms, version_uri, termlistVersionUri, term_lists_versions_metadata, term_lists_versions_members, term_lists_versions_replacements):
    # create a list of every term version that was in the most recent previous list version
    newTermVersionMembersList = []
    # create a corresponding list of local names for those versions
    termLocalNameList = []

    if not aNewTermList:
        for termVersion in term_lists_versions_members:
            # the first column contains the term list version
            if term_lists_versions_metadata[mostRecentListNumber][version_uri] == termVersion[0]:
                newTermVersionMembersList.append(termVersion[1])

                # dissect the term version URI to pull out the local name of the term version
                pieces = termVersion[1].split('/')
                versionLocalNamePiece = pieces[len(pieces)-1]
                # split off the local name string from the issue date part of the version local name
                termLocalNameList.append(versionLocalNamePiece.split('-')[0])

        # For each modified term, find its previous version and replace it with the new version.
        for modified_term in modified_terms:
            for termVersionRowNumber in range(0, len(newTermVersionMembersList)):
                if modified_term == termLocalNameList[termVersionRowNumber]:
                    # change the version on the list to the new one
                    newTermVersionMembersList[termVersionRowNumber] = namespaceUri + 'version/' + termLocalNameList[termVersionRowNumber] + '-' + date_issued

    # For each newly added term, add its new version to the list.
    for new_term in new_terms:
        newTermVersionMembersList.append(namespaceUri + 'version/' + new_term + '-' + date_issued)

    # Now that the list is created of new term versions that are part of the new term version list,
    # add a record for each one to the term list versions members table
    for termVersionMember in newTermVersionMembersList:
        term_lists_versions_members.append([termlistVersionUri, termVersionMember])

    # Write the updated term list versions members table to a file
    writeCsv('../term-lists-versions/term-lists-versions-members.csv', term_lists_versions_members)

    if not aNewTermList:
        term_lists_versions_replacements.append([termlistVersionUri, term_lists_versions_metadata[mostRecentListNumber][version_uri]])
        writeCsv('../term-lists-versions/term-lists-versions-replacements.csv', term_lists_versions_replacements)

# This function contains the Step 7 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def update_vocabulary_metadata(date_issued, local_offset_from_utc, term_lists_table, term_list_rowNumber, termlistVersionUri):
    vocabularies_table_filename = '../vocabularies/vocabularies.csv'
    vocabularies_table = readCsv(vocabularies_table_filename)

    vocabularies_versions_joins_filename = '../vocabularies/vocabularies-versions.csv'
    vocabularies_versions_joins = readCsv(vocabularies_versions_joins_filename)

    vocabularies_members_filename = '../vocabularies/vocabularies-members.csv'
    vocabularies_members = readCsv(vocabularies_members_filename)

    vocabularies_versions_metadata_filename = '../vocabularies-versions/vocabularies-versions.csv'
    vocabularies_versions_metadata = readCsv(vocabularies_versions_metadata_filename)

    vocabularies_versions_members_filename = '../vocabularies-versions/vocabularies-versions-members.csv'
    vocabularies_versions_members = readCsv(vocabularies_versions_members_filename)

    vocabularies_versions_replacements_filename = '../vocabularies-versions/vocabularies-versions-replacements.csv'
    vocabularies_versions_replacements = readCsv(vocabularies_versions_replacements_filename)

    # find the vocabulary subpath for the updated term list
    list_localName_column = findColumnWithHeader(term_lists_table[0], 'list_localName')[1]
    list_localName = term_lists_table[term_list_rowNumber][list_localName_column]
    # the vocabulary subpath is the first part of the list local name
    vocab_subpath = list_localName.split('/')[0]
    termList_subpath = list_localName.split('/')[1]

    # generate the vocabulary URI
    vocabularyUri = 'http://rs.tdwg.org/' + vocab_subpath + '/'

    # generate the vocabulary version URI
    vocabularyVersionUri = 'http://rs.tdwg.org/version/' + vocab_subpath + '/' + date_issued

    # check for the case where the script was previously run to update a different term list in the same new vocabulary version
    temp = findColumnWithHeader(vocabularies_versions_metadata[0], 'version')[1]
    alreadyAddedVocab = False
    for versionRow in vocabularies_versions_metadata:
        if versionRow[temp] == vocabularyVersionUri:
            alreadyAddedVocab = True

    modified_datetime = findColumnWithHeader(vocabularies_table[0], 'document_modified')[1]
    vocabulary_uri = findColumnWithHeader(vocabularies_table[0], 'vocabulary')[1]
    vocabulary_localName_column = findColumnWithHeader(vocabularies_table[0], 'vocabulary_localName')[1]
    vocabulary_label = findColumnWithHeader(vocabularies_table[0], 'label')[1]
    vocabulary_description = findColumnWithHeader(vocabularies_table[0], 'description')[1]
    vocabulary_created = findColumnWithHeader(vocabularies_table[0], 'vocabulary_created')[1]
    vocabulary_modified = findColumnWithHeader(vocabularies_table[0], 'vocabulary_modified')[1]
    vocabulary_dc_creator_column = findColumnWithHeader(vocabularies_table[0], 'dc_creator')[1]
    vocabulary_dcterms_license_column = findColumnWithHeader(vocabularies_table[0], 'dcterms_license')[1]

    aNewVocabulary = True
    for rowNumber in range(1, len(vocabularies_table)):
        if vocabularyUri == vocabularies_table[rowNumber][vocabulary_uri]:
            aNewVocabulary = False
            vocabulary_rowNumber = rowNumber
            # In the case where changes are made to a second term list of a new vocabulary, the new modified date will be the same as before
            vocabularies_table[rowNumber][vocabulary_modified] = date_issued
            vocabularies_table[rowNumber][modified_datetime] = isoTime(local_offset_from_utc)

            # Update the vocabulary_label, vocabulary_description, vocabulary_dc_creator_column, and vocabulary_dcterms_license columns from the vocabulary configuration file
            vocabularies_table[rowNumber][vocabulary_label] = config_vocab['vocabulary_label']
            vocabularies_table[rowNumber][vocabulary_description] = config_vocab['vocabulary_description']
            vocabularies_table[rowNumber][vocabulary_dc_creator_column] = config_vocab['dc_creator']
            vocabularies_table[rowNumber][vocabulary_dcterms_license_column] = config_vocab['dcterms_license']

    if aNewVocabulary: # this will happen if the vocabulary did not previously exist
        """ 
        try:
            new_vocabulary_row = readCsv('files_for_new/new_vocabulary.csv')[1]
        except:
            print('The vocabulary was not found and there was no new_vocabulary.csv file.')
            sys.exit()
        new_vocabulary_row[vocabulary_created] = date_issued
        new_vocabulary_row[vocabulary_modified] = date_issued
        new_vocabulary_row[modified_datetime] = isoTime(local_offset_from_utc)
        vocabularies_table.append(new_vocabulary_row)
        """
        # Create a new row for the vocabulary table that is a list with length equal to the 0th row of the table
        new_vocabulary_row = [''] * len(vocabularies_table[0])

        new_vocabulary_row[modified_datetime] = isoTime(local_offset_from_utc)

        # Assign the vocabulary URI to the new vocabulary row
        new_vocabulary_row[vocabulary_uri] = vocabularyUri

        # Generate the vocabulary local name from the last subpath of the vocabulary IRI
        vocabularyLocalName = vocabularyUri.split('/')[-2] + '/'
        new_vocabulary_row[vocabulary_localName_column] = vocabularyLocalName

        # Assign the vocabulary label from the vocabulary configuration file to the new vocabulary row
        new_vocabulary_row[vocabulary_label] = config_vocab['vocabulary_label']

        # Assign the vocabulary description from the vocabulary configuration file to the new vocabulary row
        new_vocabulary_row[vocabulary_description] = config_vocab['vocabulary_description']

        # Assign the created and modified dates to the new vocabulary row
        new_vocabulary_row[vocabulary_created] = date_issued
        new_vocabulary_row[vocabulary_modified] = date_issued

        # Assign the creator and license from the vocabulary configuration file to the new vocabulary row
        new_vocabulary_row[vocabulary_dc_creator_column] = config_vocab['dc_creator']
        new_vocabulary_row[vocabulary_dcterms_license_column] = config_vocab['dcterms_license']

        # Append the new vocabulary row to the table
        vocabularies_table.append(new_vocabulary_row)

    writeCsv('../vocabularies/vocabularies.csv', vocabularies_table)

    if not alreadyAddedVocab:
        vocabularies_versions_joins.append([vocabularyVersionUri, vocabularyUri])
        writeCsv('../vocabularies/vocabularies-versions.csv', vocabularies_versions_joins)

    if aNewTermList:
        vocabularies_members.append([vocabularyUri, termlist_uri])
        writeCsv('../vocabularies/vocabularies-members.csv', vocabularies_members)

    # find the columns than contain needed information
    document_modified = findColumnWithHeader(vocabularies_versions_metadata[0], 'document_modified')[1]
    version_uri = findColumnWithHeader(vocabularies_versions_metadata[0], 'version')[1]
    version_issued = findColumnWithHeader(vocabularies_versions_metadata[0], 'version_issued')[1]
    status_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'vocabulary_status')[1]
    label_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'label')[1]
    description_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'description')[1]
    vocabulary_uri = findColumnWithHeader(vocabularies_versions_metadata[0], 'vocabulary')[1]
    creator_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'dc_creator')[1]
    license_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'dcterms_license')[1]

    if not alreadyAddedVocab:
        # Create a new empty row for the vocabulary versions table that is a list with length equal to the 0th row of the table
        newVocabularyRow = [''] * len(vocabularies_versions_metadata[0])

        if aNewVocabulary: # this will happen if the vocabulary did not previously exist
            pass
            """
            try:
                newVocabularyRow = readCsv('files_for_new/new_vocabulary_version.csv')[1]
            except:
                print('The vocabulary version was not found and there was no new_vocabulary_version.csv file.')
                sys.exit()
            
            # the new row will be added to the end and therefore will have an index number - number of rows before appending
            mostRecentVocabularyNumber = len(vocabularies_versions_metadata)
            """
        else:
            # find the most recent previous version of the vocabulary
            mostRecent = 'a' # start the value of mostRecent as something earlier alphabetically than all of the vocabulary version URIs
            mostRecentVocabularyNumber = 0 # dummy vocabulary number to be replaced when most recent vocabulary version is found
            for vocabularyRowNumber in range(1, len(vocabularies_versions_metadata)):
                # the row is one of the versions of the vocabulary
                if vocabularies_versions_metadata[vocabularyRowNumber][vocabulary_uri] == vocabularyUri:
                    # Make the version of the row the mostRecent if it's later than the previous mostRecent
                    if vocabularies_versions_metadata[vocabularyRowNumber][version_uri] > mostRecent:
                        mostRecent = vocabularies_versions_metadata[vocabularyRowNumber][version_uri]
                        mostRecentVocabularyNumber = vocabularyRowNumber

            # change the status of the most recent vocabulary to superseded
            vocabularies_versions_metadata[mostRecentVocabularyNumber][status_column] = 'superseded'
            vocabularies_versions_metadata[mostRecentVocabularyNumber][document_modified] = isoTime(local_offset_from_utc)

            # start the new vocabulary row with the metadata from the most recent vocabulary
            #newVocabularyRow = copy.deepcopy(vocabularies_versions_metadata[mostRecentVocabularyNumber])

        # Insert metadata into the new vocabulary row
        newVocabularyRow[document_modified] = isoTime(local_offset_from_utc)
        newVocabularyRow[version_uri] = vocabularyVersionUri
        newVocabularyRow[version_issued] = date_issued
        newVocabularyRow[status_column] = 'recommended'
        newVocabularyRow[label_column] = config_vocab['vocabulary_label']
        newVocabularyRow[description_column] = config_vocab['vocabulary_description']
        newVocabularyRow[vocabulary_uri] = vocabularyUri
        newVocabularyRow[creator_column] = config_vocab['dc_creator']
        newVocabularyRow[license_column] = config_vocab['dcterms_license']

        # append the new term list row to the old list of term lists
        vocabularies_versions_metadata.append(newVocabularyRow)

        # save as a file
        writeCsv('../vocabularies-versions/vocabularies-versions.csv', vocabularies_versions_metadata)

    # If this is the second term list change for a new vocabulary version, the previous term list versions will already have been added.
    # So they don't need to be added to the list.  
    if not alreadyAddedVocab:
        # create a list of every term list version that was in the most recent previous vocabulary version
        newVocabularyMembersList = []
        # create a corresponding list of local names for those term list versions
        termListLocalNameList = []

        if aNewVocabulary:
            # the new term list version should be added to the list
            newVocabularyMembersList.append(termlistVersionUri)
        else:
            # find all of the term list versions for the most recent vocabulary version
            for termListVersion in vocabularies_versions_members:
                # the first column contains the vocabulary version
                if vocabularies_versions_metadata[mostRecentVocabularyNumber][version_uri] == termListVersion[0]:
                    newVocabularyMembersList.append(termListVersion[1])

                    # dissect the term list version URI to pull out the local name of the term list version
                    pieces = termListVersion[1].split('/')
                    versionLocalNamePiece = pieces[len(pieces)-2]
                    termListLocalNameList.append(versionLocalNamePiece)
            if aNewTermList:
                # the new term list version needs be added to the list
                newVocabularyMembersList.append(termlistVersionUri)
            else:
                # For the modified term list, find its previous version and replace it with the new new version.
                for termListVersionRowNumber in range(0, len(newVocabularyMembersList)):
                    if termList_subpath == termListLocalNameList[termListVersionRowNumber]:
                        # change the term list version on the list to the new one
                        newVocabularyMembersList[termListVersionRowNumber] = termlistVersionUri
        
        # Now that the list of new term list versions that are part of the new vocabulary version list is created,
        # add a record for each one to the vocabulary versions members table
        for termListVersionMember in newVocabularyMembersList:
            vocabularies_versions_members.append([vocabularyVersionUri, termListVersionMember])

    # In the case where previous term list versions have already been added and a new vocabulary version already generated, 
    # we only need to update the new term list version.
    else: 
        if aNewTermList:
            # the new term list version needs be added to the list
            vocabularies_versions_members.append([vocabularyVersionUri, termlistVersionUri])
        else:
            # For a modified term list, find its previous version and replace it with the new version.
            for termListVersionRowNumber in range(1, len(vocabularies_versions_members)):
                # consider only term lists that match the vocabulary version URI
                if vocabularies_versions_members[termListVersionRowNumber][0] == vocabularyVersionUri:
                    # dissect the term list version URI to pull out the local name of the term list version
                    pieces = vocabularies_versions_members[termListVersionRowNumber][1].split('/')
                    versionLocalNamePiece = pieces[len(pieces)-2]
                    # check for a match of the term list version local name with the namespace string
                    if versionLocalNamePiece == namespace:
                        # change the term list version on the list to the new one
                        vocabularies_versions_members[termListVersionRowNumber][1] = termlistVersionUri
        
    # Write the updated vocabularies versions members table to a file
    writeCsv('../vocabularies-versions/vocabularies-versions-members.csv', vocabularies_versions_members)

    if not(aNewVocabulary) and not(alreadyAddedVocab):
        vocabularies_versions_replacements.append([vocabularyVersionUri, vocabularies_versions_metadata[mostRecentVocabularyNumber][version_uri]])
        writeCsv('../vocabularies-versions/vocabularies-versions-replacements.csv', vocabularies_versions_replacements)
    return aNewVocabulary, vocab_subpath, vocabularyUri, vocabularyVersionUri

# This function contains the last cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def update_standard_metadata(date_issued, local_offset_from_utc, standardUri, vocab_subpath, vocabularyUri, vocabularyVersionUri, aNewVocabulary):
    standards_table_filename = '../standards/standards.csv'
    standards_table = readCsv(standards_table_filename)

    standards_versions_joins_filename = '../standards/standards-versions.csv'
    standards_versions_joins = readCsv(standards_versions_joins_filename)

    standards_parts_filename = '../standards/standards-parts.csv'
    standards_parts = readCsv(standards_parts_filename)

    standards_versions_metadata_filename = '../standards-versions/standards-versions.csv'
    standards_versions_metadata = readCsv(standards_versions_metadata_filename)

    standards_versions_parts_filename = '../standards-versions/standards-versions-parts.csv'
    standards_versions_parts = readCsv(standards_versions_parts_filename)

    standards_versions_replacements_filename = '../standards-versions/standards-versions-replacements.csv'
    standards_versions_replacements = readCsv(standards_versions_replacements_filename)

    # find the standard number for the standard
    standard_number = standardUri.split('/')[4]

    # generate the standard version URI
    standardVersionUri = standardUri + '/version/' + date_issued

    # check for the case where the script was previously run to update a different term list in the same new standard version
    temp = findColumnWithHeader(standards_versions_metadata[0], 'version')[1]
    alreadyAddedStandard = False
    for versionRow in standards_versions_metadata:
        if versionRow[temp] == standardVersionUri:
            alreadyAddedStandard = True

    modified_datetime = findColumnWithHeader(standards_table[0], 'document_modified')[1]
    standard_uri = findColumnWithHeader(standards_table[0], 'standard')[1]
    standard_label = findColumnWithHeader(standards_table[0], 'label')[1]
    standard_description = findColumnWithHeader(standards_table[0], 'description')[1]
    standard_created = findColumnWithHeader(standards_table[0], 'standard_created')[1]
    standard_modified = findColumnWithHeader(standards_table[0], 'standard_modified')[1]

    aNewStandard = True
    for rowNumber in range(1, len(standards_table)):
        if standardUri == standards_table[rowNumber][standard_uri]:
            aNewStandard = False
            standard_rowNumber = rowNumber
            # in cases where changes are made to a second term list of a new standard, the new modified date will be the same as before
            standards_table[rowNumber][standard_modified] = date_issued
            standards_table[rowNumber][modified_datetime] = isoTime(local_offset_from_utc)

            # Update the standard_label and standard_description columns from the standard configuration file
            standards_table[rowNumber][standard_label] = config_vocab['standard_label']
            standards_table[rowNumber][standard_description] = config_vocab['standard_description']

    if aNewStandard: # this will happen if the standard did not previously exist
        pass
        """
        try:
            new_standard_row = readCsv('files_for_new/new_standard.csv')[1]
        except:
            print('The standard was not found and there was no new_standard.csv file.')
            sys.exit()
        new_standard_row[standard_created] = date_issued
        new_standard_row[standard_modified] = date_issued
        new_standard_row[modified_datetime] = isoTime(local_offset_from_utc)
        # the row is set to what the last row will be after appending
        standard_rowNumber = len(standards_table)
        standards_table.append(new_standard_row)
        """
        # Create a new row for the standard table that is a list with length equal to the 0th row of the table
        new_standard_row = [''] * len(standards_table[0])

        new_standard_row[modified_datetime] = isoTime(local_offset_from_utc)

        # Assign the standard URI to the new standard row
        new_standard_row[standard_uri] = standardUri

        # Assign the standard label from the vocab configuration file to the new standard row
        new_standard_row[standard_label] = config_vocab['standard_label']

        # Assign the standard description from the vocab configuration file to the new standard row
        new_standard_row[standard_description] = config_vocab['standard_description']

        # Assign the created and modified dates to the new standard row
        new_standard_row[standard_created] = date_issued
        new_standard_row[standard_modified] = date_issued

        # Append the new standard row to the table
        standards_table.append(new_standard_row)

    writeCsv('../standards/standards.csv', standards_table)

    if not alreadyAddedStandard:
        standards_versions_joins.append([standardVersionUri, standardUri])
        writeCsv('../standards/standards-versions.csv', standards_versions_joins)

    if aNewVocabulary:
        standards_parts.append([standardUri, vocabularyUri, 'tdwgutility:Vocabulary'])
        writeCsv('../standards/standards-parts.csv', standards_parts)

    # find the columns than contain needed information
    document_modified = findColumnWithHeader(standards_versions_metadata[0], 'document_modified')[1]
    version_uri = findColumnWithHeader(standards_versions_metadata[0], 'version')[1]
    version_issued = findColumnWithHeader(standards_versions_metadata[0], 'version_issued')[1]
    status_column = findColumnWithHeader(standards_versions_metadata[0], 'standard_status')[1]
    label_column = findColumnWithHeader(standards_versions_metadata[0], 'label')[1]
    description_column = findColumnWithHeader(standards_versions_metadata[0], 'description')[1]
    standard_uri = findColumnWithHeader(standards_versions_metadata[0], 'standard')[1]

    if not alreadyAddedStandard:
        # Create a new empty row for the standards versions table that is a list with length equal to the 0th row of the table
        newStandardRow = [''] * len(standards_versions_metadata[0])

        if aNewStandard: # this will happen if the standard did not previously exist
            pass
            """
            try:
                newStandardRow = readCsv('files_for_new/new_standard_version.csv')[1]
            except:
                print('The standard version was not found and there was no new_standard_version.csv file.')
                sys.exit()
            # the new row will be added to the end and therefore will have an index number - number of rows before appending
            mostRecentStandardNumber = len(standards_versions_metadata)
            """
        else:
            # find the most recent previous version of the standard
            mostRecent = 'a' # start the value of mostRecent as something earlier alphabetically than all of the standard version URIs
            mostRecentStandardNumber = 0 # dummy standard number to be replaced when most recent standard version is found
            for standardRowNumber in range(1, len(standards_versions_metadata)):
                # the row is one of the versions of the standard
                if standards_versions_metadata[standardRowNumber][standard_uri] == standardUri:
                    # Make the version of the row the mostRecent if it's later than the previous mostRecent
                    if standards_versions_metadata[standardRowNumber][version_uri] > mostRecent:
                        mostRecent = standards_versions_metadata[standardRowNumber][version_uri]
                        mostRecentStandardNumber = standardRowNumber

            # change the status of the most recent standard to superseded
            standards_versions_metadata[mostRecentStandardNumber][status_column] = 'superseded'
            standards_versions_metadata[mostRecentStandardNumber][document_modified] = isoTime(local_offset_from_utc)

            # start the new standard row with the metadata from the most recent vocabulary
            #newStandardRow = copy.deepcopy(standards_versions_metadata[mostRecentStandardNumber])

        # substitute metadata to make the most recent standard version have the modified dates for the new standard version
        newStandardRow[document_modified] = isoTime(local_offset_from_utc)
        newStandardRow[version_uri] = standardVersionUri
        newStandardRow[version_issued] = date_issued
        newStandardRow[status_column] = 'recommended'
        newStandardRow[label_column] = config_vocab['standard_label']
        newStandardRow[description_column] = config_vocab['standard_description']
        newStandardRow[standard_uri] = standardUri

        # append the new term list row to the old list of term lists
        standards_versions_metadata.append(newStandardRow)

        # save as a file
        writeCsv('../standards-versions/standards-versions.csv', standards_versions_metadata)

    # If this is the second term list change for a new standard version, the previous vocabulary version will have 
    # been added.  So in that case the vocabulary versions need to be checked to prevent duplication.

    if not alreadyAddedStandard:
        # create a list of every vocabulary version that was in the most recent previous standard version
        newStandardMembersList = []
        # create a corresponding list of local names for those term list versions
        vocabularyLocalNameList = []

        if aNewStandard:
            # the new vocabulary version needs to be added to the list
            newStandardMembersList.append(vocabularyVersionUri)
        else:
            # find the vocabulary versions for the most recent standard version
            for vocabularyVersion in standards_versions_parts:
                # the first column contains the standard version
                if standards_versions_metadata[mostRecentStandardNumber][version_uri] == vocabularyVersion[0]:
                    # Must screen for vocabulary versions and exclude documents.
                    # Check the third from end piece of the URI to see if it's 'version'
                    pieces = vocabularyVersion[1].split('/')
                    if pieces[len(pieces)-3] == 'version':
                        newStandardMembersList.append(vocabularyVersion[1])

                        # dissect the vocabulary version URI to pull out the local name of the vocabulary version
                        pieces = vocabularyVersion[1].split('/')
                        versionLocalNamePiece = pieces[len(pieces)-2]
                        vocabularyLocalNameList.append(versionLocalNamePiece)

            if aNewVocabulary:
                # the new vocabulary version needs to be added to the list
                newStandardMembersList.append(vocabularyVersionUri)
            else:
                # For the modified vocabulary, find its previous version and replace it with the new version.
                print('modified vocabulary')
                for vocabularyVersionRowNumber in range(0, len(newStandardMembersList)):
                    if vocab_subpath == vocabularyLocalNameList[vocabularyVersionRowNumber]:
                        # change the vocabulary version on the list to the new one
                        newStandardMembersList[vocabularyVersionRowNumber] = vocabularyVersionUri
                
                # Thus far, only the vocabulary versions for the most recent standard version have been added to the list.
                # The document versions that are not vocabulary versions must also be added to the list.
                # Find the vocabulary versions for the most recent standard version
                for standard_part_version in standards_versions_parts:
                    # the first column contains the standard version
                    if standards_versions_metadata[mostRecentStandardNumber][version_uri] == standard_part_version[0]:
                        # Must screen for document versions.
                        # Check the third from end piece of the URI to see if it's NOT 'version'
                        # Note: legacy DwC documents don't follow the pattern, so you can't just look for 'doc'.
                        pieces = standard_part_version[1].split('/')
                        if pieces[len(pieces)-3] != 'version':
                            newStandardMembersList.append(standard_part_version[1])

        # Now that the list of new vocabulary versions that are part of the new standard version list is created,
        # add a record for each one to the standard versions members table
        for vocabularyVersionMember in newStandardMembersList:
            standards_versions_parts.append([standardVersionUri, vocabularyVersionMember])
            
    # In the case where previous vocabulary versions have already been added and a new standard version already generated
    # we only need to update the new vocabulary version
    else:
        if aNewVocabulary:
            # the new vocabulary version needs to be added to the list
            standards_versions_parts.append([standardVersionUri, vocabularyVersionUri])
        else:
            # in this case a vocabulary is modified rather than new. So find its version under the current standard version
            # and replace it with the new vocabulary version.  If the change was to a different term list but in the same
            # standard, that's fine - the vocabulary version will be replaced with the same one and duplication will still
            # be prevented
            for vocabularyVersionRowNumber in range(0, len(standards_versions_parts)):
                # consider only vocabularies that match the standard version URI
                if standards_versions_parts[vocabularyVersionRowNumber][0] == standardVersionUri:
                    # dissect the vocabulary version URI to pull out the local name of the vocabulary version
                    pieces = standards_versions_parts[vocabularyVersionRowNumber][1].split('/')
                    versionLocalNamePiece = pieces[len(pieces)-2]
                    # check for a match of the vocabulary version local name with the vocabulary string
                    if versionLocalNamePiece == vocabulary:
                        # change the vocabulary version on the list to the new one
                        standards_versions_parts[vocabularyVersionRowNumber][1] = vocabularyVersionUri

    # Write the updated vocabularies versions members table to a file
    writeCsv('../standards-versions/standards-versions-parts.csv', standards_versions_parts)

    if not(aNewStandard) and not(alreadyAddedStandard):
        standards_versions_replacements.append([standardVersionUri, standards_versions_metadata[mostRecentStandardNumber][version_uri]])
        writeCsv('../standards-versions/standards-versions-replacements.csv', standards_versions_replacements)

# -----------------------
# Main routine
# -----------------------
        
# Set up a list to keep track of the IRIs of terms that have changed so that they can later be added to the 
# Executive Committee decisions CSV
changed_terms_iris = []

for namespace in namespaces:
    # Step 1 (from first cell in development Jupyter notebook simplified_process_rs_tdwg_org.ipynb)
    # Set the values of flags that control the flow of program execution
    borrowed = namespace['borrowed']
    new_term_list = namespace['new_term_list']
    utility_namespace = namespace['utility_namespace']
    use_namespace_in_fragment = namespace['use_namespace_in_fragment']

    # Set the values of namespace-specific configuration variables
    namespaceUri = namespace['namespace_uri']
    database = namespace['database']
    prepend_url = namespace['prepend_url']
    separator = namespace['separator']
    versions = database + '-versions'
    modifications_filename = namespace['modifications_file_path']
    version_namespace = namespaceUri + 'version/'
    """
    if new_term_list:
        if 'label' in namespace:
            term_list_label = namespace['label']
        else:
            term_list_label = ''
        if 'description' in namespace:
            term_list_description = namespace['description']
        else:
            term_list_description = ''
        if 'pref_namespace_prefix' in namespace:
            pref_namespace_prefix = namespace['pref_namespace_prefix']
        else:
            pref_namespace_prefix = ''
    else:
        term_list_label = ''
        term_list_description = ''
        pref_namespace_prefix = ''
    """
    # No longer make it an option to provide these values in the namespace configuration file. They are now required.
    term_list_label = namespace['label']
    term_list_description = namespace['description']
    pref_namespace_prefix = namespace['pref_namespace_prefix']

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

    # Step 2. Create new mapping and configuration files. If run for existing term lists, it will overwrite a bunch of stuff
    if new_term_list:
        generate_and_copy_mapping_and_config_files(vocab_type, namespaceUri, database, modifications_filename)

    # Step 3. Determine values needed to interpret and modify tables later
    terms_metadata, modifications_metadata, mods_local_name, metadata_localname_column, mods_term_localName, new_terms, modified_terms = determine_state_of_data_tables(database, modifications_filename)

    # Add the IRIs of terms that have changed to the list of changed terms
    for term in modified_terms:
        changed_terms_iris.append(termlist_uri + term)
    for term in new_terms:
        changed_terms_iris.append(termlist_uri + term)

    # Step 4. Create term versions-related metadata. Generally only applies to TDWG-minted terms, not borrowed ones
    if not borrowed and not utility_namespace:
        generate_term_versions_metadata(database, versions, version_namespace, mods_local_name, modified_terms,local_offset_from_utc, date_issued, modifications_metadata)

    # Step 5. Generate current terms metadata
    version_uri, aNewTermList, term_lists_versions_members, term_lists_versions_metadata, mostRecentListNumber, termlistVersionUri, term_lists_versions_replacements, term_lists_table, term_list_rowNumber = generate_current_terms_metadata(standardUri, terms_metadata, modifications_metadata, mods_local_name, modified_terms, local_offset_from_utc, date_issued, namespaceUri, termlist_uri, database, versions, term_list_label, term_list_description, pref_namespace_prefix, use_namespace_in_fragment, prepend_url, separator)

    # Step 6. Update list of termlist members and add the termlist replacement (TDWG namespaces only)
    if not borrowed and not utility_namespace:
        update_termlist_version_members(aNewTermList, mostRecentListNumber, date_issued, namespaceUri, new_terms, modified_terms, version_uri, termlistVersionUri, term_lists_versions_metadata, term_lists_versions_members, term_lists_versions_replacements)
    
    # Step 7. Update vocabulary-related metadata
    # NOTE: This must be within the namespace loop because the member term list information must be
    # updated for each term list. However, the whole-vocabulary metadata will not be changed after its
    # updated by the first namespace loop.
    if not utility_namespace: # utility namespaces are not part of any vocabularies or standards
        aNewVocabulary, vocab_subpath, vocabularyUri, vocabularyVersionUri = update_vocabulary_metadata(date_issued, local_offset_from_utc, term_lists_table, term_list_rowNumber, termlistVersionUri)

    # Step 8. Update standard-related metadata
    # NOTE: I'm think this could be left out of the loop, since it should only need to be run once as long as
    # the script isn't being run for namespaces from more than one vocabulary. But it doesn't hurt to be in the loop, either.
    if not utility_namespace: # utility namespaces are not part of any vocabularies or standards
        update_standard_metadata(date_issued, local_offset_from_utc, standardUri, vocab_subpath, vocabularyUri, vocabularyVersionUri, aNewVocabulary)
    print('completed', namespaceUri, 'namespace')

# -----------------------
# Once the namespace loop is complete, values in the general_configuration
# files must be updated using values from the config.yaml file.
# -----------------------

# Read the text of the general_configuration.yaml file.
with open('document_metadata_processing/general_configuration.yaml', 'rt') as file_object:
    general_config_text = file_object.read()

# Replace versionDate value with the new date_issued value.
general_config_text = re.sub('versionDate:.*\n', "versionDate: '" + date_issued + "'\n", general_config_text)

# Replace the utcOfset value with the new local_offset_from_utc value.
general_config_text = re.sub('utcOffset:.*\n', "utcOffset: " + local_offset_from_utc + "\n", general_config_text)

# Replace the docIri with the new list_of_terms_iri value.
general_config_text = re.sub('docIri:.*\n', "docIri: " + config['list_of_terms_iri'] + "\n", general_config_text)

# Write the updated text to the file.
with open('document_metadata_processing/general_configuration.yaml', 'wt') as file_object:
    file_object.write(general_config_text)

# -----------------------
# Update the Executive Committee decisions metadata
# -----------------------
    
# Open and read in the Executive Committee decisions CSV file with all values as strings
decisions_df = pd.read_csv('../decisions/decisions.csv', dtype=str)

# Determine if the decision has already been made for a different vocabulary or document by checking whether the
# rdfs_comment column in the last row is the same as the decisions_text value in the config.yaml file.
if decisions_df['rdfs_comment'].iloc[-1] != config['decisions_text']:
    # Find the decision number from the last token (i.e. number) of the label column of the last row
    decision_number = int(decisions_df['label'].iloc[-1].split(' ')[-1])

    # Increment the decision number by 1 and convert it to a string.
    decision_number += 1
    decision_number_string = str(decision_number)

    # Add a new row to the decisions CSV file
    row_dict = {}
    row_dict['document_modified'] = isoTime(local_offset_from_utc)
    row_dict['term_localName'] = 'decision-' + date_issued + '_' + decision_number_string
    row_dict['term_isDefinedBy'] = 'http://rs.tdwg.org/decisions/'
    row_dict['term_modified'] = date_issued
    row_dict['label'] = 'TDWG Executive Committee decision ' + decision_number_string
    row_dict['rdfs_comment'] = config['decisions_text']
    decisions_df = decisions_df.append(row_dict, ignore_index=True)

    # Write the updated decisions CSV file
    decisions_df.to_csv('../decisions/decisions.csv', index=False)
else:
    # The last decision is the same as in the config, so use its number as the decision number string
    decision_number_string = str(int(decisions_df['label'].iloc[-1].split(' ')[-1]))

# For each term that has changed, add the IRI and decision term_localName as a row to the decisions-links.csv file.

# Open and read in the decisions-links CSV file with all values as strings
decisions_links_df = pd.read_csv('../decisions/decisions-links.csv', dtype=str)

# Add a row to the decisions-links CSV file for each term that has changed
for term_iri in changed_terms_iris:
    row_dict = {}
    row_dict['linked_affected_resource'] = term_iri
    row_dict['decision_localName'] = 'decision-' + date_issued + '_' + decision_number_string
    decisions_links_df = decisions_links_df.append(row_dict, ignore_index=True)

# Write the updated decisions-links CSV file
decisions_links_df.to_csv('../decisions/decisions-links.csv', index=False)
