#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import json, os

# Called once to load in the JSON.	
elements = {}
with open('traits_list.json') as f:
	firsttraits = json.loads(f.read())
	traits = []
	for item in firsttraits:
		traits.append({"Name":item["Name"], "Personality":item["Personality"]})
		for i, key in enumerate(('Type', 'Element', 'DisplayName', 'ShortQuote', 'Quality1',\
			'Quality2', 'Quality3', 'LongQuote', 'Superficial', 'Deep', 'AllConsuming')):
			traits[-1][key] = item["Data"][i]

# Starts up the core tkinter stuff
root = Tk()
root.title("Mystic Empyrean Traits")
s = ttk.Style()
s.configure('white.TFrame', background='#FFFFFF')
mainFrame = ttk.Frame(root, padding="5", style='white.TFrame')
mainFrame.grid(column=0, row=0, sticky=(N,S,E,W))
mainFrame.config()
summaryFrame = ttk.Frame(root, padding="5", style='white.TFrame')
summaryFrame.grid(column=0, row=1, sticky=(N,S,E,W))
summaryFrame.config()
detailFrame = ttk.Frame(root, padding="5", style='white.TFrame')
#detailFrame.grid(column=0, row=3, sticky=(N,S,E,W))
detailFrame.config()

# Functions to change the information displayed in the UI depending on what trait or personality has been selected.
def setTrait(selectedTraitIndex):
	for key in ('Name', 'Element', 'Type', 'Personality', 'DisplayName', 'ShortQuote',\
		'Quality1', 'Quality2', 'Quality3', 'LongQuote', 'Superficial', 'Deep', 'AllConsuming'):
		SelectedTraits[key].set(traits[selectedTraitIndex][key])
	SelectedTraits["DisplayName"].set("An eidolon displays " + traits[selectedTraitIndex]["DisplayName"] + " if:")
	currentImages['Type'] = ImageTk.PhotoImage(Image.open(os.path.join('assets', SelectedTraits['Type'].get()+'-tag.png')))
	currentImages['Element'] = ImageTk.PhotoImage(Image.open(os.path.join('assets', SelectedTraits['Element'].get()+'-tag.png')).convert("RGB"))
	elements['Type'].configure(image=currentImages['Type'])
	elements['Element'].configure(image=currentImages['Element'])
	return (SelectedTraits['Name'].get(), SelectedTraits['Personality'].get())

def chooseTrait(*args):
	personality = setTrait(traitNames[selectedTraitName.get()])[1]
	selectedPersonalityName.set(personality)
def choosePersonality(*args):
	trait = setTrait(personalities[selectedPersonalityName.get()])[0]
	selectedTraitName.set(trait)

# Functions to open and close the detail view
def openDetails(*args):
	detailFrame.grid(column=0, row=2, sticky=(N,S,E,W))
	elements['OpenDetail'].grid_remove()
def closeDetails(*args):
	detailFrame.grid_remove()
	elements['OpenDetail'].grid()

# Sets defaults for the dropdown lists at the top, and the images.
traitNames, personalities= {}, {}
for index, traitobj in enumerate(traits):
	traitNames[traitobj["Name"]] = index
	personalities[traitobj["Personality"]] = index
traitNamesList, personalitiesList = sorted(traitNames.keys()), sorted(personalities.keys())
selectedTraitName, selectedPersonalityName = StringVar(), StringVar()
selectedTraitName.set("League Sprinter")
currentImages, SelectedTraits = {'Type':None, 'Element':None}, {}

# Creates variables that are aware of what is active, and sets defaults for them
for key in traits[0].keys():
	SelectedTraits[key] = StringVar()
	if key in ('Type', 'Element'):
		elements[key] = ttk.Label(summaryFrame, image=currentImages[key])
	elif key in ('Superficial', 'Deep', 'AllConsuming'):
		elements[key] = Message(detailFrame, textvariable=SelectedTraits[key], width=710)
	else:
		elements[key] = ttk.Label(summaryFrame, textvariable=SelectedTraits[key])
elements['LongQuote'] = Message(summaryFrame, textvariable=SelectedTraits['LongQuote'], width=710)
chooseTrait()

# Creates the dropdown lists and buttons at the top, and grids them
OptionMenu(mainFrame, selectedTraitName, *traitNamesList, command=chooseTrait).grid(column=0, row=0, sticky=(N,S))
OptionMenu(mainFrame, selectedPersonalityName, *personalitiesList, command=choosePersonality).grid(column=1, row=0, sticky=(N,S))
# Creates the buttons to open and close the detail view
elements['OpenDetail'] = ttk.Button(root, command=openDetails, text='+')
elements['CloseDetail'] = ttk.Button(detailFrame, command=closeDetails, text='-')

# summaryFrame stuff
elements['Name'].grid(column=0, row=0, columnspan=2, sticky=(N,S,E,W))
elements['Personality'].grid(column=2, row=0, sticky=(N,S,E,W))
elements['Type'].grid(column=0, row=1, columnspan=2, sticky=W)
elements['Element'].grid(column=2, row=1)
elements['ShortQuote'].grid(column=0, row=2, columnspan=3, sticky=W)
elements['DisplayName'].grid(column=0, row=3, columnspan=3, sticky=W)
# Qualities, which need a bullet point just before them
ttk.Label(summaryFrame, text="•").grid(column=0, row=4, sticky=E)
elements['Quality1'].grid(column=1, row=4, columnspan=2, sticky=W)
ttk.Label(summaryFrame, text="•").grid(column=0, row=5, sticky=E)
elements['Quality2'].grid(column=1, row=5, columnspan=2, sticky=W)
ttk.Label(summaryFrame, text="•").grid(column=0, row=6, sticky=E)
elements['Quality3'].grid(column=1, row=6, columnspan=2, sticky=W)
# End of the summaryFrame stuff
elements['LongQuote'].grid(column=0, row=7, columnspan=3, sticky=W)
elements['OpenDetail'].grid(column=0, row=2, sticky=W)

# detailFrame stuff.
elements['Superficial'].grid(column=0, row=0, sticky=W)
elements['Deep'].grid(column=0, row=1, sticky=W)
elements['AllConsuming'].grid(column=0, row=2, sticky=W)
elements['CloseDetail'].grid(column=1, row=3, sticky=W)

root.mainloop()