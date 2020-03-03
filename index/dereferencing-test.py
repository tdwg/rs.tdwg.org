import requests
import csv

def read_csv_as_dicts_github(file_url):
    r = requests.get(file_url)
    file_text = r.text.split('\n')
    file_rows = csv.DictReader(file_text)
    csv_data = []
    for row in file_rows:
        csv_data.append(row)
    return csv_data

def write_csv(filename, array):
    with open(filename, 'w', newline='', encoding='utf-8') as file_object:
        writer_object = csv.writer(file_object)
        for row in array:
            writer_object.writerow(row)

def dereference_urls(outfilename, headers, subdomain, test_urls):
    results = []
    for header in headers:
        print(header)
        for relative_url in test_urls:
            full_url = subdomain + relative_url
            hdr = {'Accept' : header}
            r = requests.get(full_url, headers=hdr)
            if r.status_code == 404:
                response = ""
            else:
                response = r.text[:20]
            print(str(r.status_code) + "\t" + full_url + '\t' + r.url)
            results.append([r.status_code, full_url, r.url, response])
        print()
    write_csv(outfilename, results)

subdomain = 'http://rs-test.tdwg.org/'
headers = ['text/html', 'text/turtle', 'application/rdf+xml', 'application/ld+json']

# ------------------------
# Dereference example URLs from each database. This should test all of the URL patterns in use.
# ------------------------

print('Testing URL patterns using examples from all databases')

# load the database names from GitHub
index_url = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/index/index-datasets.csv'
index_list = read_csv_as_dicts_github(index_url)
print('retrieving data about databases:')
database_test_urls = []

# for each database, build a list of URLs for the first resource each database describes
for database in index_list:

    # get the information necessary to acquire the URL from the database core CSV file
    dbname = database['term_localName']
    print(dbname)
    config_file_url = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/' + dbname + '/constants.csv'
    config_data = read_csv_as_dicts_github(config_file_url)
    dbase_subdomain = config_data[0]['domainRoot'] # list item 0 because there's only one data row in the constant.csv file
    dbase_core_file = config_data[0]['coreClassFile']
    dbase_uri_column = config_data[0]['baseIriColumn']

    # retrieve the URL data from the core CSV file
    core_file_url = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/' + dbname + '/' + dbase_core_file
    core_data = read_csv_as_dicts_github(core_file_url)
    example_url = dbase_subdomain + core_data[0][dbase_uri_column] # list item 0 to test the first resource in the database
    if example_url[0:19] == 'http://rs.tdwg.org/':  # skip term lists for borrowed terms outside of TDWG
        database_test_urls.append(example_url[19:]) # save only the relative URL
print()

outfilename = 'pattern-dereferencing-results.csv'
print('dereferencing database pattern test URLs')
# dereference a URL from each database using the various Accept headers
dereference_urls(outfilename, headers, subdomain, database_test_urls)
print()

# ------------------------
# Dereference URLs of all standards documents to test redirects
# ------------------------

print('Testing URLs of all standards-related documents')

# load the document metadata from GitHub
docs_data_url = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/docs/docs.csv'
docs_data = read_csv_as_dicts_github(docs_data_url)

docs_urls = []
for row in docs_data:
    relative_url = row['current_iri'][19:]
    docs_urls.append(relative_url)

outfilename = 'document-dereferencing-results.csv'
print('dereferencing document URLs')
# dereference a URL of each document using the various Accept headers
dereference_urls(outfilename, headers, subdomain, docs_urls)

# ------------------------
# Dereference URLs of miscellaneous legacy documents that were served from rs.tdwg.org
# ------------------------

print('Testing redirection of legacy rs.tdwg.org URLs')

# This list of URLs was determined empiracally from requests to the old server over the period of a month
# URLs already tested above were deleted from the list

headers = ['text/html'] # headers are irrelevant since the redirects are to URLs that don't support content negotiation

# load the URLs from GitHub
legacy_data_url = 'https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/index/legacy-urls.csv'
legacy_data = read_csv_as_dicts_github(legacy_data_url)

legacy_urls = []
for row in legacy_data:
    relative_url = row['uri'][1:] # drop initial forward slash
    legacy_urls.append(relative_url)

outfilename = 'legacy-dereferencing-results.csv'
print('dereferencing legacy URLs')
dereference_urls(outfilename, headers, subdomain, legacy_urls)

print('done')
