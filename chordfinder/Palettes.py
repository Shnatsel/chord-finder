class Palette:
  '''A class which allows the entire image colour mode to be set together'''
  def __init__(self, colour_mode):
    if colour_mode == 0: # Full Colour
      self.nut_colour = (255, 255, 255)
      self.fret_colour = (187, 187, 187)
      self.fret_marker_colour = (200, 200, 200)
      self.string_colour = (255, 255, 255)
      self.xo_colour = (255, 255, 255)
      self.fret_board_colour = (90, 50, 0)
      self.finger_circle_colour = (255, 255, 60)
      self.finger_text_colour = (255, 0, 0)
      self.fret_tri_colour = (255, 0, 0)
      self.tri_text_colour = (255, 255, 255)
      self.arc_colour = (0, 255, 0)
    elif colour_mode == 1: # Monochome
      self.nut_colour = (128, 128, 128) # Best compromise
      self.fret_colour = (0, 0, 0)
      self.fret_marker_colour = (0, 0, 0)
      self.string_colour = (0, 0, 0)
      self.xo_colour = (255, 255, 255)
      self.fret_board_colour = (255, 255, 255)
      self.finger_circle_colour = (0, 0, 0)
      self.finger_text_colour = (255, 255, 255)
      self.fret_tri_colour = (255, 255, 255)
      self.tri_text_colour = (255, 255, 255)
      self.arc_colour = (0, 0, 0)
    else:
      print "Error in palette class"
