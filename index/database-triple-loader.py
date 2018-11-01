# Steve Baskauf 2018-10-31 Freely available under a GNU GPLv3 license. 
# By its nature, this software overwrites and deletes data, so use at your own risk. 
# See https://github.com/baskaufs/guid-o-matic/blob/master/rdf-mover.md for usage notes about the script this was hacked from.

#libraries for GUI interface
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst

import csv #library to read/write/parse CSV files
import requests #library to do HTTP communication

root = Tk()

# this sets up the characteristics of the window
root.title("TDWG RDF database dumper")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#set up array of labels, text entry boxes, and buttons
#repoText = StringVar()
#ttk.Label(mainframe, textvariable=repoText).grid(column=3, row=3, sticky=(W, E))
#repoText.set('Github repo path')
#githubRepoBox = ttk.Entry(mainframe, width = 25, textvariable = StringVar())
#githubRepoBox.grid(column=4, row=3, sticky=W)
#githubRepoBox.insert(END, 'baskaufs/msc/')

#subpathText = StringVar()
#ttk.Label(mainframe, textvariable=subpathText).grid(column=3, row=4, sticky=(W, E))
#subpathText.set('Github repo subpath')
#repoSubpathBox = ttk.Entry(mainframe, width = 25, textvariable = StringVar())
#repoSubpathBox.grid(column=4, row=4, sticky=W)
#repoSubpathBox.insert(END, '')

#basexUriText = StringVar()
#ttk.Label(mainframe, textvariable=basexUriText).grid(column=3, row=5, sticky=(W, E))
#basexUriText.set('BaseX API URI root')
#basexUriBox = ttk.Entry(mainframe, width = 50, textvariable = StringVar())
#basexUriBox.grid(column=4, row=5, sticky=W)
#basexUriBox.insert(END, 'http://vuswwg.jelastic.servint.net/gom/rest/')


#databaseText = StringVar()
#ttk.Label(mainframe, textvariable=databaseText).grid(column=3, row=6, sticky=(W, E))
#databaseText.set('Database name')
#databaseBox = ttk.Entry(mainframe, width = 20, textvariable = StringVar())
#databaseBox.grid(column=4, row=6, sticky=W)
#databaseBox.insert(END, 'test')

#passwordText = StringVar()
#ttk.Label(mainframe, textvariable=passwordText).grid(column=3, row=7, sticky=(W, E))
#passwordText.set('BaseX database pwd')
#passwordBox = ttk.Entry(mainframe, width = 15, textvariable = StringVar(), show='*')
#passwordBox.grid(column=4, row=7, sticky=W)
#passwordBox.insert(END, '[pwd]')

#def gitToBaseButtonClick():
#	dataToBasex(githubRepoBox.get(), repoSubpathBox.get(), databaseBox.get(), basexUriBox.get(), passwordBox.get())
#gitToBaseButton = ttk.Button(mainframe, text = "Transfer from Github to BaseX", width = 30, command = lambda: gitToBaseButtonClick() )
#gitToBaseButton.grid(column=4, row=8, sticky=W)

emptyText = StringVar()
#ttk.Label(mainframe, textvariable=emptyText).grid(column=3, row=9, sticky=(W, E))
#emptyText.set(' ')

dumpUriText = StringVar()
ttk.Label(mainframe, textvariable=dumpUriText).grid(column=3, row=10, sticky=(W, E))
dumpUriText.set('Graph dump URI root')
dumpUriBox = ttk.Entry(mainframe, width = 50, textvariable = StringVar())
dumpUriBox.grid(column=4, row=10, sticky=W)
dumpUriBox.insert(END, 'http://rs-test.tdwg.org/dump/')

endpointUriText = StringVar()
ttk.Label(mainframe, textvariable=endpointUriText).grid(column=3, row=11, sticky=(W, E))
endpointUriText.set('SPARQL endpoint URI')
endpointUriBox = ttk.Entry(mainframe, width = 50, textvariable = StringVar())
endpointUriBox.grid(column=4, row=11, sticky=W)
endpointUriBox.insert(END, 'https://sparql.vanderbilt.edu/sparql')

pwd2Text = StringVar()
ttk.Label(mainframe, textvariable=pwd2Text).grid(column=3, row=12, sticky=(W, E))
pwd2Text.set('Endpoint password')
passwordBox2 = ttk.Entry(mainframe, width = 15, textvariable = StringVar(), show='*')
passwordBox2.grid(column=4, row=12, sticky=W)
passwordBox2.insert(END, '[pwd]')

graphNameText = StringVar()
ttk.Label(mainframe, textvariable=graphNameText).grid(column=3, row=13, sticky=(W, E))
graphNameText.set('Graph name')
graphNameBox = ttk.Entry(mainframe, width = 50, textvariable = StringVar())
graphNameBox.grid(column=4, row=13, sticky=W)
graphNameBox.insert(END, 'http://rs.tdwg.org/')

def baseToTripleButtonClick():
    csvData = getCsvObject('https://raw.githubusercontent.com/tdwg/rs.tdwg.org/master/index/', 'index-datasets.csv', ',')
    loadList = []
    for row in csvData:
        loadList.append(row[1])
    for database in range(1,len(loadList)):  # start range at 1 to avoid header row (0)
    #for database in range(1,2):  # uncomment this line to test using only one database
		# for whatever reason, the .ttl serializations of the dumps were loading zero triples.  But the .rdf serializations were fine.
		# I'm wondering if this is related to the content-type reported by the dump.  I verified that it's "text/turtle", which I thought was a valid type to load
        dataToTriplestore(dumpUriBox.get(), loadList[database]+'.rdf', endpointUriBox.get(), graphNameBox.get(), passwordBox2.get())
baseToTripleButton = ttk.Button(mainframe, text = "Transfer from server to Triplestore", width = 30, command = lambda: baseToTripleButtonClick() )
baseToTripleButton.grid(column=4, row=14, sticky=W)

ttk.Label(mainframe, textvariable=emptyText).grid(column=3, row=15, sticky=(W, E))

rdfFileMessage = StringVar()
ttk.Label(mainframe, textvariable=rdfFileMessage).grid(column=4, row=16, sticky=(W, E))
rdfFileMessage.set('Note: raw files from Github do not have the correct RDF content-type based on file extension. ')

rdfFileText = StringVar()
ttk.Label(mainframe, textvariable=rdfFileText).grid(column=3, row=17, sticky=(W, E))
rdfFileText.set('RDF file URI')
rdfFileBox = ttk.Entry(mainframe, width = 100, textvariable = StringVar())
rdfFileBox.grid(column=4, row=17, sticky=W)
rdfFileBox.insert(END, '# https://bioimages.vanderbilt.edu/baskauf/00000.rdf')

def moveFileButtonClick():
	moveFile(rdfFileBox.get(), endpointUriBox.get(), graphNameBox.get(), passwordBox2.get())
moveFileButton = ttk.Button(mainframe, text = "Load file into named graph", width = 30, command = lambda: moveFileButtonClick() )
moveFileButton.grid(column=4, row=18, sticky=W)

ttk.Label(mainframe, textvariable=emptyText).grid(column=3, row=19, sticky=(W, E))

def dropGraphButtonClick():
	dropGraph(endpointUriBox.get(), graphNameBox.get(), passwordBox2.get())
dropGraphButton = ttk.Button(mainframe, text = "Drop (delete) graph", width = 30, command = lambda: dropGraphButtonClick() )
dropGraphButton.grid(column=4, row=20, sticky=W)

ttk.Label(mainframe, textvariable=emptyText).grid(column=3, row=21, sticky=(W, E))

logText = StringVar()
ttk.Label(mainframe, textvariable=logText).grid(column=3, row=22, sticky=(W, E))
logText.set('Action log')
#scrolling text box hacked from https://www.daniweb.com/programming/software-development/code/492625/exploring-tkinter-s-scrolledtext-widget-python
edit_space = tkst.ScrolledText(master = mainframe, width  = 100, height = 25)
# the padx/pady space will form a frame
edit_space.grid(column=4, row=22, padx=8, pady=8)
edit_space.insert(END, '')

def updateLog(message):
	edit_space.insert(END, message + '\n')
	edit_space.see(END) #causes scroll up as text is added
	root.update_idletasks() # causes updated to log window, see https://stackoverflow.com/questions/6588141/update-a-tkinter-text-widget-as-its-written-rather-than-after-the-class-is-fini

#def generateFilenameList(coreDoc):
#	filenameList = [{'name': 'namespace','tag': 'namespaces'},{'name': coreDoc + '-column-mappings','tag': 'column-index'},{'name': coreDoc + '-classes','tag': 'base-classes'}]
#	return filenameList

def getCsvObject(httpPath, fileName, fieldDelimiter):
	# retrieve remotely from GitHub
	uri = httpPath + fileName
	r = requests.get(uri)
	updateLog(str(r.status_code) + ' ' + uri)
	body = r.text
	csvData = csv.reader(body.splitlines()) # see https://stackoverflow.com/questions/21351882/reading-data-from-a-csv-file-online-in-python-3
	return csvData

# XML creation functions hacked from http://code.activestate.com/recipes/577423-convert-csv-to-xml/
#def buildGenericXml(rootElementName, csvData):
#	xmlData = ''
#	xmlData = xmlData + '<' + rootElementName + '>' + "\n"
	
#	rowNum = 0
#	for row in csvData:
#		if rowNum == 0:
#			tags = row
			# replace spaces w/ underscores in tag names
#			for i in range(len(tags)):
#				tags[i] = tags[i].replace(' ', '_')
#		else: 
#			xmlData = xmlData + '<record>' + "\n"
#			for i in range(len(tags)):
#				xmlData = xmlData + '    ' + '<' + tags[i] + '>' + escapeBadXmlCharacters(row[i]) + '</' + tags[i] + '>' + "\n"
#			xmlData = xmlData + '</record>' + "\n"
#		rowNum +=1
	
#	xmlData = xmlData + '</' + rootElementName + '>' + "\n"
#	return xmlData
	
def escapeBadXmlCharacters(dirtyString):
	ampString = dirtyString.replace('&','&amp;')
	ltString = ampString.replace('<','&lt;')
	cleanString = ltString.replace('>','&gt;')
	return cleanString
	
#def buildLinkedMetadataXml(httpPath, csvData, fieldDelimiter):
#	xmlData = '<?xml version="1.0" encoding="UTF-8" ?>' + '\n'
#	xmlData = xmlData + '<linked-metadata>' + "\n"
	
#	rowNum = 0
#	for row in csvData:
#		if rowNum == 0:
#			tags = row
#		else:
#			xmlData = xmlData + '<file>' + "\n"
			
#			xmlData = xmlData + '    ' + '<link_column>' + row[tags.index('link_column')] + '</link_column>' + "\n"
#			xmlData = xmlData + '    ' + '<link_property>' + row[tags.index('link_property')] + '</link_property>' + "\n"
#			xmlData = xmlData + '    ' + '<suffix1>' + row[tags.index('suffix1')] + '</suffix1>' + "\n"
#			xmlData = xmlData + '    ' + '<link_characters>' + row[tags.index('link_characters')] + '</link_characters>' + "\n"
#			xmlData = xmlData + '    ' + '<suffix2>' + row[tags.index('suffix2')] + '</suffix2>' + "\n"
#			xmlData = xmlData + '    ' + '<forward_link>' + row[tags.index('forward_link')] + '</forward_link>' + "\n"
#			fileName = row[tags.index('filename')]
#			fileNameRoot = fileName[0:fileName.find('.')]
#			csvSubData = getCsvObject(httpPath, fileNameRoot + '-classes.csv', ',')
#			xmlData = xmlData + buildGenericXml('classes', csvSubData)
#			csvSubData = getCsvObject(httpPath, fileNameRoot + '-column-mappings.csv', ',')
#			xmlData = xmlData + buildGenericXml('mapping', csvSubData)
#			csvSubData = getCsvObject(httpPath, fileName, fieldDelimiter) # metadata file may have a different delimiter than comma
#			xmlData = xmlData + buildGenericXml('metadata', csvSubData)
			
#			xmlData = xmlData + '</file>' + "\n"
#		rowNum +=1
	
#	xmlData = xmlData + '</linked-metadata>' + "\n"
#	return xmlData

#def writeDatabaseFile(databaseWritePath, filename, body, pwd):
#	uri = databaseWritePath + '/' + filename
#	hdr = {'Content-Type' : 'application/xml'}
#	r = requests.put(uri, auth=('admin', pwd), headers=hdr, data = body.encode('utf-8'))
#	updateLog(str(r.status_code) + ' ' + uri + '\n')
#	updateLog(r.text + '\n')

#def dataToBasex(githubRepo, repoSubpath, database, basexServerUri, pwd):
#	databaseWritePath = basexServerUri + database

	# first must do a PUT to the database URI to create it if it doesn't exist
#	r = requests.put(databaseWritePath, auth=('admin', pwd) )
#	updateLog('create XML database')
#	updateLog(str(r.status_code) + ' ' + databaseWritePath + '\n')

#	httpReadPath = 'https://raw.githubusercontent.com/' + githubRepo + 'master/' + repoSubpath + database + '/'
	# must open the configuration/constants file separately in order to discover the core document and separator character
#	updateLog('read constants')
#	csvData = getCsvObject(httpReadPath, 'constants.csv', ',')
	
	# pull necessary constants out of the CSV object
#	rowNum = 0
#	for row in csvData:  # only one row of data below headers
#		if rowNum == 0:
#			tags = row
#		else:
#			coreDocFileName = row[tags.index('coreClassFile')]
#			fieldDelimiter = row[tags.index('separator')]
#		rowNum +=1
	# find the file name without extension
#	coreDocRoot = coreDocFileName[0:coreDocFileName.find('.')]
	
	# write the configuration data; not sure why csvData wasn't preserved to this point ???
#	updateLog('read configuration')
#	tempCsvData = getCsvObject(httpReadPath, 'constants.csv', ',')
#	body = '<?xml version="1.0" encoding="UTF-8" ?>' + '\n' + buildGenericXml('constants', tempCsvData)
#	updateLog('write configuration')
#	writeDatabaseFile(databaseWritePath, 'constants.xml', body, pwd)
	
	# write each of the various associated files	
#	nameList = generateFilenameList(coreDocRoot)
#	for name in nameList:
#		updateLog('read file')
#		csvData = getCsvObject(httpReadPath, name['name'] + '.csv', ',')
#		body = '<?xml version="1.0" encoding="UTF-8" ?>' + '\n' + buildGenericXml(name['tag'], csvData)
#		updateLog('write file')
#		writeDatabaseFile(databaseWritePath, name['name'] + '.xml', body, pwd)
	
	# The main metadata file must be handled separately, since may have a non-standard file extension or delimiter
#	updateLog('read core metadata')
#	csvData = getCsvObject(httpReadPath, coreDocFileName, fieldDelimiter)
#	body = '<?xml version="1.0" encoding="UTF-8" ?>' + '\n' + buildGenericXml('metadata', csvData)
#	updateLog('write core metadata')
#	writeDatabaseFile(databaseWritePath, coreDocRoot + '.xml', body, pwd)
	
	# The linked class data has a different format and must be handled separately
#	updateLog('read linked metadata')
#	csvData = getCsvObject(httpReadPath, 'linked-classes.csv', ',')
#	body = buildLinkedMetadataXml(httpReadPath, csvData, fieldDelimiter)
#	updateLog('write linked metadata')
#	writeDatabaseFile(databaseWritePath, 'linked-classes.xml', body, pwd)
#	updateLog('Ready')

def performSparqlUpdate(endpointUri, pwd, updateCommand):
	# SPARQL Update requires HTTP POST
	updateLog(updateCommand + '\n')
	hdr = {'Content-Type' : 'application/sparql-update'}
	r = requests.post(endpointUri, auth=('admin', pwd), headers=hdr, data = updateCommand)
	updateLog(str(r.status_code) + ' ' + r.url + '\n')
	updateLog(r.text + '\n')
	updateLog('Ready')	

def dataToTriplestore(dumpUri, database, endpointUri, graphName, pwd):
    updateCommand = 'LOAD <' + dumpUri + database + '> INTO GRAPH <' + graphName + '>'
    print(updateCommand) # print this to the terminal so that we can see what's going on while the GUI is doing spinning circle
    updateLog('update SPARQL endpoint into graph ' + graphName)
    performSparqlUpdate(endpointUri, pwd, updateCommand)

def moveFile(rdfFileUri, endpointUri, graphName, pwd):
	updateCommand = 'LOAD <' + rdfFileUri + '> INTO GRAPH <' + graphName + '>'
	updateLog('move file ' + rdfFileUri + ' into graph ' + graphName)
	performSparqlUpdate(endpointUri, pwd, updateCommand)

def dropGraph(endpointUri, graphName, pwd):
	updateCommand = 'DROP GRAPH <' + graphName + '>'
	updateLog('drop graph ' + graphName)
	performSparqlUpdate(endpointUri, pwd, updateCommand)

def main():	
    root.mainloop()
	
if __name__=="__main__":
	main()

