import csv
import os
import sys

# reads a CSV file via a local file path and returns a list of dicts where headers are keys
def readCsvAsDicts(path):
    dictList = []
    with open(path, 'r', newline='', encoding='utf-8') as fileObject:
        readerObject = csv.DictReader(fileObject)
        for row in readerObject:
            dictList.append(row)
    return dictList

# read metadata from local clone of rs.tdwg.org repo
standards = readCsvAsDicts('../../standards/standards.csv')
standardsParts = readCsvAsDicts('../../standards/standards-parts.csv')
docs = readCsvAsDicts('../../docs/docs.csv')
contributors = readCsvAsDicts('../../docs/docs-authors.csv')
vocabs = readCsvAsDicts('../../vocabularies/vocabularies.csv')
pageInfo = readCsvAsDicts('pageInfo.csv')

# These list items serve both as the keys in the header section and column headers in pageInfo.csv
headerItems = ['summary','cover_image', 'cover_image_by', 'cover_image_ref', 'tags', 'github', 'website', 'website_title', 'status']

# create a directory for output if it doesn't already exist
try:
    os.mkdir('output')
except:
    pass

# loop through the rows of the pageInfo CSV table and generate a Markdown page for each
for page in pageInfo:

    # match this page with its record in the standards metadata
    found = False
    for standardIndex in range(0, len(standards)):
        if page['standard'] == standards[standardIndex]['standard']:
            found = True
            standardNumber = standardIndex

    # if successful in finding a standards metadata record, build the Markdown
    if found:
        # create a directory for the standard if it doesn't already exist
        try:
            os.mkdir('output/' + page['directoryName'])
        except:
            pass

        # opent the index.md file in the standard's directory
        outObject = open('output/' + page['directoryName'] + '/index.md', 'wt', encoding='utf-8')
        
        # print the Jekyll metadata header section
        print('---', file=outObject)
        # use the official standards title for now, perhaps chage to shortened version
        print('title: ' + standards[standardNumber]['label'], file=outObject)
        for headerItem in headerItems:
            if page[headerItem] != '':
                print(headerItem + ': ' + page[headerItem], file=outObject)
        print('---', file=outObject)

        # print the header section required by the SDS
        print('', file=outObject)
        print('## Header section', file=outObject)
        print('', file=outObject)
        print('Title', file=outObject)
        print(': ' + standards[standardNumber]['label'], file=outObject)
        print('', file=outObject)
        print('Permanent IRI to be cited and linked', file=outObject)
        print(': <' + standards[standardNumber]['standard'] + '>', file=outObject)
        print('', file=outObject)
        print('Publisher', file=outObject)
        print(': [Biodiversity Information Standards (TDWG)](https://www.tdwg.org/)', file=outObject)
        print('', file=outObject)
        print('Ratified', file=outObject)
        print(': ' + standards[standardNumber]['standard_created'], file=outObject)
        print('', file=outObject)
        print('Status', file=outObject)
        print(': [' + standards[standardNumber]['status'] + '](https://www.tdwg.org/standards/status-and-categories/)', file=outObject)
        print('', file=outObject)
        if standards[standardNumber]['category'] != '':
            print('Category', file=outObject)
            print(': [' + standards[standardNumber]['category'] + '](https://www.tdwg.org/standards/status-and-categories/)', file=outObject)
            print('', file=outObject)
        print('Abstract', file=outObject)
        print(': ' + standards[standardNumber]['description'], file=outObject)
        print('', file=outObject)
        print('Bibliographic citation', file=outObject)
        print(': ' + standards[standardNumber]['citation'], file=outObject)
        print('', file=outObject)

        # describe the parts of the standard (vocabularies and documents)
        print('## Parts of the standard', file=outObject)
        print('', file=outObject)

        # make lists of documents and vocabularies that are part of the standard 
        docsInStd = []
        vocabsInStd = []
        for part in standardsParts:
            if part['standard'] == page['standard']:
                if part['rdf_type'] == 'foaf:Document':
                    docsInStd.append(part['part'])
                elif part['rdf_type'] == 'tdwgutility:Vocabulary':
                    vocabsInStd.append(part['part'])

        # summarize the number of vocabularies and documents in the standard
        sentence = 'This standard is comprised of '
        if len(vocabsInStd) > 1:
            sentence += str(len(vocabsInStd)) + ' vocabularies and '
        if len(vocabsInStd) == 1:
            sentence += 'one vocabulary and '
        if len(docsInStd) > 1:
            sentence += str(len(docsInStd)) + ' documents. '
        if len(docsInStd) == 1:
            sentence += 'one document. '
        print(sentence, file=outObject)
        print('', file=outObject)

        # print vocabularies (if any)
        if len(vocabsInStd) > 0:
            print('Vocabularies:', file=outObject)
            print('', file=outObject)
            for vocabToList in vocabsInStd:
                # find the current vocabulary in the vocabularies metadata
                for vocab in vocabs:
                    if vocab['vocabulary'] == vocabToList:
                        print(vocab['label'] + ' (<' + vocab['vocabulary'] + '>)', file=outObject)
            print('', file=outObject)

        # print documents
        print('Documents:', file=outObject)
        print('', file=outObject)
        for docToList in docsInStd:
            # find the current document in the documents metadata
            for doc in docs:
                if doc['current_iri'] == docToList:
                    # print metadata about each document
                    print('**Title:** ' + doc['documentTitle'] + '\\', file=outObject)
                    print('**Permanent IRI:** [' + doc['current_iri'] + '](' + doc['browserRedirectUri'] + ')\\', file=outObject)
                    print('**Created:** ' + doc['doc_created'] + '\\', file=outObject)
                    print('**Last modified:** ' + doc['doc_modified'] + '\\', file=outObject)
                    print('**Contributors:**\\', file=outObject)
                    for contributor in contributors:
                        if contributor['document'] == docToList:
                            listing = contributor['contributor_literal'] + ' (' + contributor['contributor_role'] + ')'
                            if contributor['affiliation'] != '':
                                listing += ' - ' + contributor['affiliation']
                            print(listing + '\\', file=outObject)
                    print('**Publisher:** ' + doc['publisher'] + '\\', file=outObject)
                    print('**Abstract:** ' + doc['abstract'] + '\\', file=outObject)
                    if doc['comment'] != '':
                        print('**Note:** ' + doc['comment'] + '\\', file=outObject)
                    print('**Citation:** ' + doc['citation'], file=outObject)
                    print('', file=outObject)
