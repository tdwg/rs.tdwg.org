import csv
import os
import sys

headerItems = ['summary','cover_image', 'cover_image_by', 'cover_image_ref', 'tags', 'github', 'website', 'website_title', 'status']

# read standards metadata from rs.tdwg.org repo
standards = []
with open('../../standards/standards.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        standards.append(row)

# read parts of standards from rs.tdwg.org repo
standardsParts = []
with open('../../standards/standards-parts.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        standardsParts.append(row)

# read docs metadata from rs.tdwg.org repo
docs = []
with open('../../docs/docs.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        docs.append(row)

# read contributor metadata from rs.tdwg.org repo
contributors = []
with open('../../docs/docs-authors.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        contributors.append(row)

# read vocabs metadata from rs.tdwg.org repo
vocabs = []
with open('../../vocabularies/vocabularies.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        vocabs.append(row)

# read additional data to build web page
pageInfo = []
with open('pageInfo.csv', 'r', newline='', encoding='utf-8') as fileObject:
    readerObject = csv.DictReader(fileObject)
    for row in readerObject:
        pageInfo.append(row)

# create a directory for output if it doesn't already exist
try:
    os.mkdir('output')
except:
    pass

for pageIndex in range(0,len(pageInfo)):
#for pageIndex in range(21, 22):
    # match this page with its record in the standards metadata
    found = False
    for standardIndex in range(0, len(standards)):
        if pageInfo[pageIndex]['standard'] == standards[standardIndex]['standard']:
            found = True
            standardNumber = standardIndex

    # if successful in finding a standards record, build the Markdown
    if found:
        # uncomment the triple single-quotes block to suppress file output
        #'''
        # create a directory for output if it doesn't already exist
        try:
            os.mkdir('output/' + pageInfo[pageIndex]['directoryName'])
        except:
            pass

        outObject = open('output/' + pageInfo[pageIndex]['directoryName'] + '/index.md', 'wt', encoding='utf-8')
        #'''        
        #outObject = sys.stdout # uncomment this line to output to the console
        
        print('---', file=outObject)
        print('title: ' + standards[standardNumber]['label'], file=outObject)
        for headerItem in headerItems:
            if pageInfo[pageIndex][headerItem] != '':
                print(headerItem + ': ' + pageInfo[pageIndex][headerItem], file=outObject)
        print('---', file=outObject)
        print('', file=outObject)
        print('## Header section', file=outObject)
        print('', file=outObject)
        print('Title', file=outObject)
        print(': ' + standards[standardNumber]['label'], file=outObject)
        print('', file=outObject)
        print('Date created', file=outObject)
        print(': ' + standards[standardNumber]['standard_created'], file=outObject)
        print('', file=outObject)
        print('Status', file=outObject)
        print(': ' + standards[standardNumber]['status'], file=outObject)
        print('', file=outObject)
        print('Category', file=outObject)
        print(': ' + standards[standardNumber]['category'], file=outObject)
        print('', file=outObject)
        print('## Parts of the standard', file=outObject)
        print('', file=outObject)

        # find vocabularies and documents that are part of the standard
        docsInStd = []
        vocabsInStd = []
        for part in standardsParts:
            if part['standard'] == pageInfo[pageIndex]['standard']:
                if part['rdf_type'] == 'foaf:Document':
                    docsInStd.append(part['part'])
                elif part['rdf_type'] == 'tdwgutility:Vocabulary':
                    vocabsInStd.append(part['part'])
        sentence = 'This standard is comprised of '
        if len(vocabsInStd) > 1:
            sentence += str(len(vocabsInStd)) + ' vocabularies and '
        if len(vocabsInStd) == 1:
            sentence += 'one vocabulary and '
        if len(docsInStd) > 1:
            sentence += str(len(docsInStd)) + ' documents: '
        if len(docsInStd) == 1:
            sentence += 'one document: '
        print(sentence, file=outObject)
        print('', file=outObject)

        # print vocabularies (if any)
        if len(vocabsInStd) > 0:
            print('Vocabularies:', file=outObject)
            print('', file=outObject)
            for vocabToList in vocabsInStd:
                for vocab in vocabs:
                    if vocab['vocabulary'] == vocabToList:
                        print(vocab['label'] + ' (<' + vocab['vocabulary'] + '>)', file=outObject)
            print('', file=outObject)

        # print documents
        print('Documents:', file=outObject)
        print('', file=outObject)
        for docToList in docsInStd:
                for doc in docs:
                    if doc['current_iri'] == docToList:
                        print('**Title:** ' + doc['documentTitle'] + '\\', file=outObject)
                        print('**IRI:** [' + doc['current_iri'] + '](' + doc['browserRedirectUri'] + ')\\', file=outObject)
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
