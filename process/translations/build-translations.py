#!/usr/bin/python3
#
# Script that:
#
# 1) builds source *.en.csv files for translation, suitable for automatic input into Crowdin.
#    - English,
#    - one translation per line,
#    - consistent column ordering,
#    - stable identifier column,
#
# 2) Uses the Crowdin-generated translations (*.xx.csv) to create files compatible with the existing rs.tdwg.org scripts (*-translations.csv).
#
# See https://github.com/tdwg/rs.tdwg.org/blob/master/TRANSLATIONS.md for more information.
#
# Matthew Blissett, 2022-02, CC0

import os
import re
import csv
from collections import OrderedDict

# Source (English) files to push to Crowdin.
termfiles_to_translate = [
    'terms/terms',
    'dc-for-dwc/dc-for-dwc',
    'dcterms-for-dwc/dcterms-for-dwc',
    'establishmentMeans/establishmentMeans',
    'degreeOfEstablishment/degreeOfEstablishment',
    'pathway/pathway',
    'latimer/latimer',
    'dcterms-for-ltc/dcterms-for-ltc',
    'humboldt/humboldt'
]

# From those source files, these columns will be made available for translation
translate_these_columns = {
    # This for everything
    'label': 'Label',

    # These for DWC (terms, dc-for-dwc, dcterms-for-dwc)
    'rdfs_comment': 'Comment',
    'dcterms_description': 'Description',
    'examples': 'Examples',

    # These for establishmentMeans, degreeOfEstablishment, pathway
    'definition': 'Definition',
    'usage': 'Usage',
    'notes': 'Notes'
}

# Output structure (defined in crowdin.yml)
# identifier,context,source_or_translation
crowdin_fieldnames = ['identifier', 'context', 'text']

# Fields to be output into the *-translations.csv file
output_translation_columns = {
    'label': 'label',
    'definition': 'definition',
    'usage': 'usage',
    'notes': 'notes'
}
# DWC has a different structure
dwc_structure = ['terms/terms', 'dc-for-dwc/dc-for-dwc', 'dcterms-for-dwc/dcterms-for-dwc']
dwc_output_translation_columns = {
    'label': 'label',
    'rdfs_comment': 'rdfs_comment',
    'dcterms_description': 'dcterms_description',
    'examples': 'examples'
}

for termfile in termfiles_to_translate:
    print("Processing source file "+termfile+".csv")

    # Output file with column names known to Crowdin
    with open(termfile+'.en.csv', 'w', newline='') as crowdinEnglishFile:
        crowdinEnglishTerms = csv.writer(crowdinEnglishFile, quoting=csv.QUOTE_MINIMAL, lineterminator=os.linesep)
        crowdinEnglishTerms.writerow(crowdin_fieldnames)

        # Input file
        with open(termfile+'.csv', newline='') as originalTermsFile:
            originalTerms = csv.DictReader(originalTermsFile)

            for originalRow in originalTerms:
                # Don't (yet) bother translating deprecated terms
                if originalRow['term_deprecated'] != "true":
                    # Find any columns eligible for translation
                    for translatableCol in translate_these_columns.keys():
                        if translatableCol in originalRow.keys() and len(originalRow[translatableCol]) > 0:
                            if translatableCol == 'examples':
                                # Remove the `quoted` examples, and see if there's any notes to translate
                                pattern = '`[^`]+`[;., \n]*'
                                examples_without_examples = re.sub(pattern, '', originalRow[translatableCol])
                                if len(examples_without_examples) < 2:
                                    continue

                            identifier = originalRow['term_localName']+":"+translatableCol
                            context = translate_these_columns[translatableCol]+" for "+originalRow['label'] + ' http://rs.tdwg.org/dwc/terms/'+originalRow['term_localName']
                            crowdinEnglishTerms.writerow([identifier, context, originalRow[translatableCol]])

    print("Generating file "+termfile+"-translations.csv")

    # Read any *.??.csv files (produced by Crowdin) and generate a *-translations.csv file
    with open(termfile+'-translations.csv', 'w', newline='') as translationsFile:
        languages = ['en','cs','de','es','fr','ko','nl','ru','zh-Hans', 'zh-Hant']

        if termfile in dwc_structure:
            print("Special mapping for "+termfile+"-translations.csv")
            current_output_translation_columns = dwc_output_translation_columns
        else:
            current_output_translation_columns = output_translation_columns

        # *-translations.csv file has columns
        # term_localName,label_en,label_…,definition_en,definition_…
        fieldnames = ['term_localName']
        translationsFile.write('term_localName')
        for col in current_output_translation_columns.keys():
            for lang in languages:
                fieldnames += col+'_'+lang
                translationsFile.write(","+current_output_translation_columns[col]+"_"+lang)
        translationsFile.write("\n")

        # Record each term in a dictionary with entries label_en etc.
        combinedTranslations = OrderedDict()

        xfieldnames = ['identifier', 'context', 'text']

        for lang in languages:
            if (os.path.exists(termfile+'.'+lang+'.csv')):
                print("  Reading "+termfile+'.'+lang+'.csv')
                with open(termfile+'.'+lang+'.csv', newline='') as oneLanguageFile:
                    oneLanguageTerms = csv.DictReader(oneLanguageFile)

                    for row in oneLanguageTerms:
                        wholeIdentifier = row['identifier'] # e.g. basisOfRecord:label
                        text = row['text']

                        (localName, column) = wholeIdentifier.split(':')
                        if localName not in combinedTranslations:
                            combinedTranslations[localName] = dict()
                        combinedTranslations[localName][column+'_'+lang] = text

        # Write a row with a term and the translations
        for localName, translations in combinedTranslations.items():
            translationsFile.write(localName)
            for col in current_output_translation_columns.keys():
                for lang in languages:
                    if col+"_"+lang in translations:
                        text = translations[col+"_"+lang]
                        text = text.replace('"', '""')
                        if ',' in text or '"' in text:
                            translationsFile.write(',"'+text+'"')
                        else:
                            translationsFile.write(','+text)
                    else:
                        translationsFile.write(',')
            translationsFile.write("\n")

    print("  Done.")
