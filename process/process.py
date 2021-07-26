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

# This function contains the Step 5 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def generate_current_terms_metadata(terms_metadata, modifications_metadata, mods_local_name, modified_terms, local_offset_from_utc, date_issued, namespaceUri, termlist_uri, database, versions):
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

    list_uri = findColumnWithHeader(term_lists_table[0], 'list')[1]
    list_created = findColumnWithHeader(term_lists_table[0], 'list_created')[1]
    list_modified = findColumnWithHeader(term_lists_table[0], 'list_modified')[1]
    modified_datetime = findColumnWithHeader(term_lists_table[0], 'document_modified')[1]
    standard_column = findColumnWithHeader(term_lists_table[0], 'standard')[1]
    list_description = findColumnWithHeader(term_lists_table[0], 'description')[1]

    aNewTermList = True
    for rowNumber in range(1, len(term_lists_table)):
        # by convention, the namespace URI used for the terms is the same as the URI of the term list
        if termlist_uri == term_lists_table[rowNumber][list_uri]:
            aNewTermList = False
            term_list_rowNumber = rowNumber
            term_lists_table[rowNumber][list_modified] = date_issued
            term_lists_table[rowNumber][modified_datetime] = isoTime(local_offset_from_utc)
            # here is the opportunity to find out the standard URI for the modified term list
            standardUri = term_lists_table[rowNumber][standard_column]
            # print(term_lists_table[rowNumber])
    if aNewTermList:  # this will happen if the term list did not previously exist
        try:
            new_term_list = readCsv('files_for_new/new_term_list.csv')
        except:
            print('The term list was not found and there was no new_term_list.csv file.')
            sys.exit()
        # Note: no error trapping is done here, so make sure that the new_term_list columns are the same as term_lists_table
        new_term_list[1][modified_datetime] = isoTime(local_offset_from_utc)
        new_term_list[1][list_created] = date_issued
        new_term_list[1][list_modified] = date_issued
        standardUri = new_term_list[1][standard_column]
        # the length of the table (including header row) will be one more than the last row number
        term_list_rowNumber = len(term_lists_table)
        term_lists_table.append(new_term_list[1])
        # after the new row is appended, its row number will be one more than the previous last row number

        # The new term list's dataset directory must be added to the dataset list. 
        row_for_current_terms = [isoTime(local_offset_from_utc), # document_modified
                                database, # term_localName
                                'http://rs.tdwg.org/index', # dcterms_isPartOf
                                'http://rs.tdwg.org/index/' + database, # dataset_iri
                                date_issued, # dcterms_modified
                                new_term_list[1][list_description], # label
                                ''] # rdfs_comment
        datasets_index.append(row_for_current_terms)
        
        # New term lists will always have a new version dataset directory, so add it, too.
        row_for_versions = [isoTime(local_offset_from_utc), # document_modified
                            versions, # term_localName
                            'http://rs.tdwg.org/index', # dcterms_isPartOf
                            'http://rs.tdwg.org/index/' + versions, # dataset_iri
                            date_issued, # dcterms_modified
                            new_term_list[1][list_description] + ' versions', # label
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
    list_uri = findColumnWithHeader(term_lists_versions_metadata[0], 'list')[1]
    document_modified = findColumnWithHeader(term_lists_versions_metadata[0], 'document_modified')[1]
    version_uri = findColumnWithHeader(term_lists_versions_metadata[0], 'version')[1]
    version_modified = findColumnWithHeader(term_lists_versions_metadata[0], 'version_modified')[1]
    status_column = findColumnWithHeader(term_lists_versions_metadata[0], 'status')[1]

    if aNewTermList:
        # get the template for the term list version from first data row in the new_term_list_version.csv file
        try:
            new_term_list_version = readCsv('files_for_new/new_term_list_version.csv')
        except:
            print('The term list version was not found and there was no new_term_list_version.csv file.')
            sys.exit()
        newListRow = new_term_list_version[1]
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
        newListRow = copy.deepcopy(term_lists_versions_metadata[mostRecentListNumber])

    # substitute metadata to make the most recent list have the modified dates for the new list
    newListRow[document_modified] = isoTime(local_offset_from_utc)
    newListRow[version_uri] = termlistVersionUri
    newListRow[version_modified] = date_issued
    newListRow[status_column] = 'recommended'

    # append the new term list row to the old list of term lists
    term_lists_versions_metadata.append(newListRow)

    # save as a file
    writeCsv('../term-lists-versions/term-lists-versions.csv', term_lists_versions_metadata)
    return standardUri, version_uri, aNewTermList, term_lists_versions_members, term_lists_versions_metadata, mostRecentListNumber, termlistVersionUri, term_lists_versions_replacements, term_lists_table, term_list_rowNumber

# This function contains the Step 6 cell from the development Jupyter notebook simplified_process_rs_tdwg_org.ipynb
def update_termlist_members(aNewTermList, mostRecentListNumber, date_issued, namespaceUri, new_terms, modified_terms, version_uri, termlistVersionUri, term_lists_versions_metadata, term_lists_versions_members, term_lists_versions_replacements):
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

    vocabulary_uri = findColumnWithHeader(vocabularies_table[0], 'vocabulary')[1]
    vocabulary_created = findColumnWithHeader(vocabularies_table[0], 'vocabulary_created')[1]
    vocabulary_modified = findColumnWithHeader(vocabularies_table[0], 'vocabulary_modified')[1]
    modified_datetime = findColumnWithHeader(vocabularies_table[0], 'document_modified')[1]

    aNewVocabulary = True
    for rowNumber in range(1, len(vocabularies_table)):
        if vocabularyUri == vocabularies_table[rowNumber][vocabulary_uri]:
            aNewVocabulary = False
            vocabulary_rowNumber = rowNumber
            # In the case where changes are made to a second term list of a new vocabulary, the new modified date will be the same as before
            vocabularies_table[rowNumber][vocabulary_modified] = date_issued
            vocabularies_table[rowNumber][modified_datetime] = isoTime(local_offset_from_utc)

    if aNewVocabulary: # this will happen if the vocabulary did not previously exist 
        try:
            new_vocabulary_row = readCsv('files_for_new/new_vocabulary.csv')[1]
        except:
            print('The vocabulary was not found and there was no new_vocabulary.csv file.')
            sys.exit()
        new_vocabulary_row[vocabulary_created] = date_issued
        new_vocabulary_row[vocabulary_modified] = date_issued
        new_vocabulary_row[modified_datetime] = isoTime(local_offset_from_utc)
        vocabularies_table.append(new_vocabulary_row)

    writeCsv('../vocabularies/vocabularies.csv', vocabularies_table)

    if not alreadyAddedVocab:
        vocabularies_versions_joins.append([vocabularyVersionUri, vocabularyUri])
        writeCsv('../vocabularies/vocabularies-versions.csv', vocabularies_versions_joins)

    if aNewTermList:
        vocabularies_members.append([vocabularyUri, termlist_uri])
        writeCsv('../vocabularies/vocabularies-members.csv', vocabularies_members)

    # find the columns than contain needed information
    vocabulary_uri = findColumnWithHeader(vocabularies_versions_metadata[0], 'vocabulary')[1]
    document_modified = findColumnWithHeader(vocabularies_versions_metadata[0], 'document_modified')[1]
    version_uri = findColumnWithHeader(vocabularies_versions_metadata[0], 'version')[1]
    version_issued = findColumnWithHeader(vocabularies_versions_metadata[0], 'version_issued')[1]
    status_column = findColumnWithHeader(vocabularies_versions_metadata[0], 'vocabulary_status')[1]

    if not alreadyAddedVocab:
        if aNewVocabulary: # this will happen if the vocabulary did not previously exist 
            try:
                newVocabularyRow = readCsv('files_for_new/new_vocabulary_version.csv')[1]
            except:
                print('The vocabulary version was not found and there was no new_vocabulary_version.csv file.')
                sys.exit()
            # the new row will be added to the end and therefore will have an index number - number of rows before appending
            mostRecentVocabularyNumber = len(vocabularies_versions_metadata)
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
            newVocabularyRow = copy.deepcopy(vocabularies_versions_metadata[mostRecentVocabularyNumber])

        # substitute metadata to make the most recent vocabulary have the modified dates for the new vocabulary
        newVocabularyRow[document_modified] = isoTime(local_offset_from_utc)
        newVocabularyRow[version_uri] = vocabularyVersionUri
        newVocabularyRow[version_issued] = date_issued
        newVocabularyRow[status_column] = 'recommended'

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


# -----------------------
# Main routine
# -----------------------

for namespace in namespaces:
    # Step 1 (from first cell in development Jupyter notebook simplified_process_rs_tdwg_org.ipynb)
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

    # Step 2. Create new mapping and configuration files. If run for existing term lists, it will overwrite a bunch of stuff
    if new_term_list:
        generate_and_copy_mapping_and_config_files(vocab_type, namespaceUri, database, modifications_filename)

    # Step 3. Determine values needed to interpret and modify tables later
    terms_metadata, modifications_metadata, mods_local_name, metadata_localname_column, mods_term_localName, new_terms, modified_terms = determine_state_of_data_tables(database, modifications_filename)

    # Step 4. Create term versions-related metadata. Generally only applies to TDWG-minted terms, not borrowed ones
    if not borrowed:
        generate_term_versions_metadata(database, versions, version_namespace, mods_local_name, modified_terms,local_offset_from_utc, date_issued, modifications_metadata)

    # Step 5. Generate current terms metadata
    standardUri, version_uri, aNewTermList, term_lists_versions_members, term_lists_versions_metadata, mostRecentListNumber, termlistVersionUri, term_lists_versions_replacements, term_lists_table, term_list_rowNumber = generate_current_terms_metadata(terms_metadata, modifications_metadata, mods_local_name, modified_terms, local_offset_from_utc, date_issued, namespaceUri, termlist_uri, database, versions)

    # Step 6. Update list of termlist members and add the termlist replacement (TDWG namespaces only)
    if not borrowed:
        update_termlist_members(aNewTermList, mostRecentListNumber, date_issued, namespaceUri, new_terms, modified_terms, version_uri, termlistVersionUri, term_lists_versions_metadata, term_lists_versions_members, term_lists_versions_replacements)
    
    # Step 7. Update vocabulary-related metadata
    # NOTE: This must be within the namespace loop because the member term list information must be
    # updated for each term list. However, the whole-vocabulary metadata will not be changed after its
    # updated by the first namespace loop.
    if not utility_namespace: # utility namespaces are not part of any vocabularies or standards
        update_vocabulary_metadata(date_issued, local_offset_from_utc, term_lists_table, term_list_rowNumber, termlistVersionUri)

