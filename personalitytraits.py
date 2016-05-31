#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
from PIL import ImageTk, Image
import ttk, json, os

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
mainFrame = ttk.Frame(root, padding="5")
mainFrame.grid(column=0, row=0, sticky=(N,S,E,W))
summaryFrame = ttk.Frame(root, padding="5")
summaryFrame.grid(column=0, row=1, sticky=(N,S,E,W))

# Functions to change the information displayed in the UI depending on what trait or personality has been selected.
def setTrait(selectedTraitIndex):
	for key in ('Name', 'Element', 'Type', 'Personality', 'DisplayName', 'ShortQuote',\
		'Quality1', 'Quality2', 'Quality3', 'LongQuote', 'Superficial', 'Deep', 'AllConsuming'):
		SelectedTraits[key].set(traits[selectedTraitIndex][key])
	SelectedTraits["DisplayName"].set("An eidolon displays " + traits[selectedTraitIndex]["DisplayName"] + " if:")
	currentImages['Type'] = ImageTk.PhotoImage(Image.open(os.path.join('assets', SelectedTraits['Type'].get().encode('utf-8')+'.png')))
	currentImages['Element'] = ImageTk.PhotoImage(Image.open(os.path.join('assets', SelectedTraits['Element'].get().encode('utf-8')+'.png')))
	elements['Type'] = ttk.Label(summaryFrame, image=currentImages['Type'])
	elements['Element'] = ttk.Label(summaryFrame, image=currentImages['Element'])

def chooseTrait(*args):
	setTrait(traitNames[selectedTraitName.get()])
def choosePersonality(*args):
	setTrait(personalities[selectedPersonalityName.get()])

# Sets defaults for the dropdown lists at the top, and the images.
traitNames, personalities= {}, {}
for index, traitobj in enumerate(traits):
	traitNames[traitobj["Name"]] = index
	personalities[traitobj["Personality"]] = index
selectedTraitName, selectedPersonalityName = StringVar(), StringVar()
selectedTraitName.set("Words Within")
selectedPersonalityName.set("Boastful")
# currentImages = {'Type':ImageTk.PhotoImage(Image.open('Personality.png')), 'Element':ImageTk.PhotoImage(Image.open('Air.png'))}
currentImages, SelectedTraits = {'Type':None, 'Element':None}, {}

# Creates variables that are aware of what is active, and sets defaults for them
for key in traits[0].keys():
	SelectedTraits[key] = StringVar()
	if key in ('Type', 'Element'):
		print key + ": setting image."
		elements[key] = ttk.Label(summaryFrame, image=currentImages[key])
	elif key in ('Superficial', 'Deep', 'AllConsuming', 'LongQuote'):
		print key + ": setting messagebox."
		elements[key] = Message(summaryFrame, textvariable=SelectedTraits[key], width=700)
	else:
		print key + ": setting text label."
		elements[key] = ttk.Label(summaryFrame, textvariable=SelectedTraits[key])
chooseTrait()
print str(SelectedTraits['Type'].get())
print str(SelectedTraits['Element'].get())

# Creates the dropdown lists and buttons at the top, and grids them
apply(OptionMenu, (mainFrame, selectedTraitName) + tuple(traitNames)).grid(column=0, row=0, sticky=(N,S))
apply(OptionMenu, (mainFrame, selectedPersonalityName) + tuple(personalities)).grid(column=1, row=0, sticky=(N,S))
ttk.Button(mainFrame, text="Choose Trait", command=chooseTrait).grid(column=0, row=1)
ttk.Button(mainFrame, text="Choose Personality", command=choosePersonality).grid(column=1, row=1)

# Grids everything else
elements['Name'].grid(column=0, row=0, columnspan=3, sticky=(N,S,E,W))
elements['Personality'].grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))
elements['Type'].grid(column=0, row=2, columnspan=2, sticky=W)
elements['Element'].grid(column=2, row=2)
elements['ShortQuote'].grid(column=0, row=3, columnspan=3, sticky=W)
elements['DisplayName'].grid(column=0, row=4, columnspan=3, sticky=W)
ttk.Label(summaryFrame, text="•").grid(column=0, row=5, sticky=E)
elements['Quality1'].grid(column=1, row=5, columnspan=2, sticky=W)
ttk.Label(summaryFrame, text="•").grid(column=0, row=6, sticky=E)
elements['Quality2'].grid(column=1, row=6, columnspan=2, sticky=W)
ttk.Label(summaryFrame, text="•").grid(column=0, row=7, sticky=E)
elements['Quality3'].grid(column=1, row=7, columnspan=2, sticky=W)
elements['LongQuote'].grid(column=0, row=8, columnspan=3, sticky=W)
elements['Superficial'].grid(column=0, row=9, columnspan=3, sticky=W)
elements['Deep'].grid(column=0, row=10, columnspan=3, sticky=W)
elements['AllConsuming'].grid(column=0, row=11, columnspan=3, sticky=W)

root.mainloop()