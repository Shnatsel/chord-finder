class Instrument:
  '''A class which simply allows various related variables to be set together.'''
  def __init__(self):
    self.number_of_strings = 6
    self.number_of_frets = 21
    self.fret_spacing = 75    # Spacing between frets
    self.string_spacing = 40  # Spacing between strings
    self.string_width = 3   # Width of each string
    self.first_string_gap = 20  # Gap from left side of image for first string
    self.top_gap = 50   # Size of area above strings that contains "X", or "O"
    self.top_gap_data_size = 8  # Size of "X" or "O" when drawn
    self.finger_size = 14   # Size of circle for fingering information
    self.finger_font_size = 20  # Size of text in fingering circle
    self.nut_width = 5    # Width to draw the plastic nut (fret 0)
    self.marker_positions = [3, 5, 7, 9, 12, 15, 17] # Position of fret markings
    self.double_markings = [12] # Fret 12 is a double fret marking
    self.marker_size = 10
    self.margin = 50    # Left hand margin on image
