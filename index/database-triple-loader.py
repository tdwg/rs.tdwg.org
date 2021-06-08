# Steve Baskauf 2018-10-31 Freely available under a GNU GPLv3 license. 
# By its nature, this software overwrites and deletes data, so use at your own risk. 
# See https://github.com/baskaufs/guid-o-matic/blob/master/rdf-mover.md for usage notes about the script this was hacked from.

# Revision notes 2021-06-08
# Fixes to two problems:
# 1. graphical log doesn't really work - spinning circle while script mindlessly marches forwared. Just print to console...
# 2. GitHub response with 503, causing the SPARQL updated to fail. Need to try again if 503 until 200 is obtained.

#libraries for GUI interface
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst

import csv #library to read/write/parse CSV files
import requests #library to do HTTP communication
from time import sleep

root = Tk()

# this sets up the characteristics of the window
root.title("TDWG RDF database dumper")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


emptyText = StringVar()

dumpUriText = StringVar()
ttk.Label(mainframe, textvariable=dumpUriText).grid(column=3, row=10, sticky=(W, E))
dumpUriText.set('Graph dump URI root')
dumpUriBox = ttk.Entry(mainframe, width = 50, textvariable = StringVar())
dumpUriBox.grid(column=4, row=10, sticky=W)
dumpUriBox.insert(END, 'http://rs.tdwg.org/dump/')

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
	print(message)
	#edit_space.insert(END, message + '\n')
	#edit_space.see(END) #causes scroll up as text is added
	#root.update_idletasks() # causes update to log window, see https://stackoverflow.com/questions/6588141/update-a-tkinter-text-widget-as-its-written-rather-than-after-the-class-is-fini

def getCsvObject(httpPath, fileName, fieldDelimiter):
	# retrieve remotely from GitHub
	uri = httpPath + fileName
	statusCode = ''
	while statusCode != '200':
		r = requests.get(uri)
		statusCode = str(r.status_code).strip()
		updateLog(statusCode + ' ' + uri)
		if statusCode != '200':
			sleep(2)
	body = r.text
	csvData = csv.reader(body.splitlines()) # see https://stackoverflow.com/questions/21351882/reading-data-from-a-csv-file-online-in-python-3
	return csvData
	
def escapeBadXmlCharacters(dirtyString):
	ampString = dirtyString.replace('&','&amp;')
	ltString = ampString.replace('<','&lt;')
	cleanString = ltString.replace('>','&gt;')
	return cleanString
	
def performSparqlUpdate(endpointUri, pwd, updateCommand):
	# SPARQL Update requires HTTP POST
	statusCode = ''
	while statusCode != '200':
		updateLog(updateCommand + '\n')
		hdr = {'Content-Type' : 'application/sparql-update'}
		r = requests.post(endpointUri, auth=('admin', pwd), headers=hdr, data = updateCommand)
		statusCode = str(r.status_code).strip()
		updateLog(statusCode + ' ' + r.url + '\n')
		updateLog(r.text + '\n')
		if statusCode != '200':
			sleep(2)
	updateLog('Ready')

def dataToTriplestore(dumpUri, database, endpointUri, graphName, pwd):
    updateCommand = 'LOAD <' + dumpUri + database + '> INTO GRAPH <' + graphName + '>'
    #print(updateCommand) # print this to the terminal so that we can see what's going on while the GUI is doing spinning circle
    #updateLog('update SPARQL endpoint into graph ' + graphName)
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

