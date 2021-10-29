# Script to build source CSV files for translation, suitable for automatic input into Crowdin.
#
# That means:
# - English,
# - one translation per line,
# - consistent column ordering,
# - stable identifier column,
#
# Matthew Blissett, 2021-10, CC0

import os
import re
import csv        # library to read/write/parse CSV files

# Output:
# identifier,context,source_or_translation

columns = ['label', 'rdfs_comment', 'dcterms_description', 'examples']

column_labels = {'label': 'Label', 'rdfs_comment': 'Comment', 'dcterms_description': 'Description', 'examples': 'Examples'}

with open('terms/terms.en.csv', 'w', newline='') as englishFile:
    fieldnames = ['identifier', 'context', 'text']
    englishTerms = csv.writer(englishFile, quoting=csv.QUOTE_MINIMAL, lineterminator=os.linesep)
    englishTerms.writerow(fieldnames)

    with open('terms/terms.csv', newline='') as termsFile:
        terms = csv.DictReader(termsFile)

        for row in terms:
            if row['term_deprecated'] != "true":
                for col in columns:
                    if len(row[col]) > 0:
                        if col == 'examples':
                            # Remove the `quoted` examples, and see if there's any notes to translate
                            pattern = '`[^`]+`[;., \n]*'
                            examples_without_examples = re.sub(pattern, '', row[col])
                            if len(examples_without_examples) < 2:
                                continue
                        identifier = row['term_localName']+":"+col
                        context = column_labels[col]+" for "+row['label'] + ' http://rs.tdwg.org/dwc/terms/'+row['term_localName']
                        englishTerms.writerow([identifier, context, row[col]])
