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

# Additional column (beyond term_localName) to use to create an identifier, necessary if the same
# term_localName is used e.g. in different classes.
termfile_identifiers = {
    'latimer/latimer': 'tdwgutility_organizedInClass'
}

# From those source files, these columns will be made available for translation if they exist in the standard
translate_these_columns = {
    # This for everything
    'label': 'Label',

    # These for DWC (terms, dc-for-dwc, dcterms-for-dwc)
    'rdfs_comment': 'Comment',
    'dcterms_description': 'Description',
    'examples': 'Examples',

    # These for establishmentMeans, degreeOfEstablishment, pathway, latimer
    'definition': 'Definition',
    'usage': 'Usage',
    'notes': 'Notes'
}

# Output structure (defined in crowdin.yml)
# identifier,context,source_or_translation
crowdin_fieldnames = ['identifier', 'context', 'text']

for termfile in termfiles_to_translate:
    print("Processing source file "+termfile+".csv")

    if (termfile in termfile_identifiers):
        additionalIdentifier = termfile_identifiers[termfile]
    else:
        additionalIdentifier = None

    # Output file with column names known to Crowdin
    with open(termfile+'.en.csv', 'w', newline='') as crowdinEnglishFile:
        crowdinEnglishTerms = csv.writer(crowdinEnglishFile, quoting=csv.QUOTE_MINIMAL, lineterminator=os.linesep)
        crowdinEnglishTerms.writerow(crowdin_fieldnames)

        # Input file
        with open(termfile+'.csv', newline='') as originalTermsFile:
            originalTerms = csv.DictReader(originalTermsFile)
            print("Column headers in "+termfile+'.csv are', originalTerms.fieldnames)

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

                            identifier = originalRow['term_localName']+":"
                            # Additional parts for identifiers, in case term_localName isn't enough
                            if (additionalIdentifier):
                                identifier += originalRow[additionalIdentifier].replace(':', '~')+":"
                            identifier += translatableCol

                            context = translate_these_columns[translatableCol]+" for "+originalRow['label']
                            if (additionalIdentifier):
                                context += ' (' + additionalIdentifier + ': ' + originalRow[additionalIdentifier] + ')'

                            context += ' http://rs.tdwg.org/dwc/terms/'+originalRow['term_localName']
                            crowdinEnglishTerms.writerow([identifier, context, originalRow[translatableCol]])

    print("Generating file "+termfile+"-translations.csv")

    # Read any *.??.csv files (produced by Crowdin) and generate a *-translations.csv file
    with open(termfile+'-translations.csv', 'w', newline='') as translationsFile:
        languages = ['en','cs','de','es','fr','ko','nl','ru','zh-Hans','zh-Hant']

        # Output the translated columns, maintaining column order.
        current_output_translation_columns = list(filter(lambda c: c in translate_these_columns, originalTerms.fieldnames))

        # *-translations.csv file has columns
        # term_localName,label_en,label_…,definition_en,definition_…
        fieldnames = ['term_localName']
        translationsFile.write('term_localName')

        if (additionalIdentifier):
            fieldnames.append(additionalIdentifier)
            translationsFile.write(","+additionalIdentifier)
        for col in current_output_translation_columns:
            for lang in languages:
                fieldnames.append(col+"_"+lang)
                translationsFile.write(","+col+"_"+lang)
        translationsFile.write("\n")

        print("Will write these columns in "+termfile+'-translations.csv', fieldnames)

        # Record each term in a dictionary with entries label_en etc.
        combinedTranslations = OrderedDict()

        for lang in languages:
            if (os.path.exists(termfile+'.'+lang+'.csv')):
                print("  Reading "+termfile+'.'+lang+'.csv')
                with open(termfile+'.'+lang+'.csv', newline='') as oneLanguageFile:
                    oneLanguageTerms = csv.DictReader(oneLanguageFile)

                    for row in oneLanguageTerms:
                        wholeIdentifier = row['identifier'] # e.g. basisOfRecord:label
                        text = row['text']

                        if (wholeIdentifier.count(':') == 1):
                            (localName, column) = wholeIdentifier.split(':')
                            key = localName
                        elif (wholeIdentifier.count(':') == 2):
                            (localName, additional, column) = wholeIdentifier.split(':')
                            key = localName + ',' + additional.replace('~', ':')
                        else:
                            print("Identifier: «" + wholeIdentifier + "»," + str(wholeIdentifier.count(':')))
                        if key not in combinedTranslations:
                            combinedTranslations[key] = dict()
                        combinedTranslations[key][column+'_'+lang] = text

        # Write a row with a term and the translations
        for key, translations in combinedTranslations.items():
            translationsFile.write(key)
            for col in current_output_translation_columns:
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
