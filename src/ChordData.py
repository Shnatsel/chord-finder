import os

class chordNotFound(Exception):
	pass

####################################################
# A class which builds up lists of all known chords 
# and presents data on them as needed
class ChordDatabase:
	def __init__(self, chordsCsv):
		self.chordList = []
		self.initChords(chordsCsv)

	def initChords(self, csvFile):
		try:
			File = open(csvFile,'r')
		except IOError:
			print "IOError opening: {0}".format(csvFile)
		else:
			for line in File:
				if not line.startswith('#') and (line.strip()):	# ignore comment lines and empty lines
					chordType	= line.split(',')[0]
					root 		= line.split(',')[1]
					shortName 	= line.split(',')[2]
					longName 	= line.split(',')[3]
					fingerStr 	= line.split(',')[4]
					fretStr 	= line.split(',')[5]
					chordObj = Chord(chordType, root, shortName, longName, fingerStr, fretStr)
					self.chordList.append(chordObj)


	def getSingleChordObj(self, chordTypeWanted, chordNameWanted):
		found = 0
		for chord in self.chordList:
			if ((chord.shortName == chordNameWanted) and (chord.chordType == chordTypeWanted)):
				found = 1
				break
		if (found == 1):
			return chord
		else:
			raise chordNotFound

	# Get all chord names
	def getAllChordNames(self):
		chordNameList =  []
		
		for chord in self.chordList:
			chordNameList.append(chord.shortName)
		return chordNameList
	
	# Return filtered chord names
	def getFilteredChordNames(self, typeWanted, rootStr, dimAugWanted):
		chordNameList = []
		
		for chord in self.chordList:
			filterOut = 0
			if (chord.chordType != typeWanted):
				filterOut += 1
			
			if ((rootStr != 'All') and (chord.root != rootStr)):
				filterOut += 1
					
			if ((dimAugWanted != 'All') and (chord.longName.find(dimAugWanted) == -1)):
				filterOut += 1
				
			if (filterOut == 0):
				chordNameList.append(chord.shortName)
		return chordNameList
	
	def playChordFromObj(self, chord_obj):
		""" Play a chord using the linux sox play command from a given chord object """
		open_strings = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']
		notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
		fret_data = chord_obj.fretStr.split()
		chord_str = ''
		
		for i,fret_pos in enumerate(fret_data):
			if (fret_pos == '0'):
				chord_str += open_strings[i] + " " # string is played open, so just use the string's open note
				continue
			elif (fret_pos == '-1'):
				continue # string is not played in chord, skip
			
			open_note = open_strings[i][0]
			open_octave = int(open_strings[i][1])

			for i, note in enumerate(notes):
				if (note == open_note):
					base_pos = i									# where in list are we starting
					shift_pos = base_pos + int(fret_pos)					# final "position" in list (may have looped)
														
					if shift_pos >= len(notes):
						final_note = notes[shift_pos % len(notes)]	# allow for loop if needed
					else:
						final_note = notes[shift_pos]				# otherwise return note directly
					
					octave_shift = shift_pos / len(notes) 			# how many octaves we gained
					final_octave = open_octave + octave_shift
					output_note = final_note + str(final_octave)
					chord_str += output_note + " "
		cmd_str="for p in {0}; do ( play -n synth 3 pluck $p vol 0.1 >/dev/null 2>&1 &); done".format(chord_str)
		os.system(cmd_str)
		
			
####################################################
# A class that holds data for a single static chord
class Chord:
	def __init__(self, chordType, root, shortName, longName, fingerStr, fretStr):
		self.chordType = chordType
		self.root = root
		self.shortName = shortName
		self.longName = longName
		self.fingerStr = fingerStr
		self.fretStr = fretStr


