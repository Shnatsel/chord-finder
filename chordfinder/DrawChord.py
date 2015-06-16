''' Module for drawing the main chord image '''

import PIL.Image, PIL.ImageDraw, PIL.ImageFont

def draw_frets(draw, instrument, movable_shift, image_width, palette, font_path):
  '''Add the frets onto the image'''
  for fret_num in xrange(1, (instrument.number_of_frets - movable_shift)):
    fret_pos_y = (fret_num * instrument.fret_spacing) + (instrument.top_gap + instrument.nut_width)
    draw.line((instrument.margin, fret_pos_y, image_width, fret_pos_y), palette.fret_colour, width=3)

    if fret_num % 2 != 0:                     # only draw odd numbered frets (less screen clutter)
      # Calculate coords to draw a triangular fret side markings
      point_a = (instrument.margin - 10, (fret_num * instrument.fret_spacing) + instrument.top_gap + instrument.string_width - 5)
      point_b = (instrument.margin - 3, (fret_num * instrument.fret_spacing) + instrument.top_gap + instrument.string_width)
      point_c = (instrument.margin - 10, (fret_num * instrument.fret_spacing) + instrument.top_gap + instrument.string_width + 5)
      draw.polygon((point_a, point_b, point_c), palette.fret_tri_colour)
      sans16 = PIL.ImageFont.truetype(font_path, 20)
      text_pos = (3, (fret_num * instrument.fret_spacing) + instrument.top_gap - 10)  # the 3 is arb, 10 allows for text font size
      draw.text(text_pos, 'F'+str(fret_num+movable_shift), font=sans16, fill=palette.tri_text_colour)
  return draw


def draw_fret_markers(draw, instrument, movable_shift, palette):
  '''Add the fret markers onto the image'''
  for fret_pos in instrument.marker_positions:
    y_pos = (instrument.top_gap + instrument.nut_width) + ((fret_pos - movable_shift) * instrument.fret_spacing) - (instrument.fret_spacing / 2) # middle of the fret area

    if y_pos <= instrument.top_gap: # Dont draw markers that land in the top area
      continue

    if fret_pos in instrument.double_markings:
      x_pos = instrument.margin + instrument.first_string_gap + instrument.string_spacing
      draw.ellipse((x_pos-instrument.marker_size, y_pos-instrument.marker_size,
        x_pos+instrument.marker_size, y_pos+instrument.marker_size),
        palette.fret_marker_colour)
      x_pos = instrument.margin + instrument.first_string_gap + instrument.string_spacing * 4
      draw.ellipse((x_pos-instrument.marker_size, y_pos-instrument.marker_size,
        x_pos+instrument.marker_size, y_pos+instrument.marker_size),
        palette.fret_marker_colour)
    else:
      x_pos = instrument.margin + instrument.first_string_gap + ((instrument.number_of_strings / 2) * instrument.string_spacing) - (instrument.string_spacing / 2)
      draw.ellipse((x_pos-instrument.marker_size, y_pos-instrument.marker_size,
        x_pos+instrument.marker_size, y_pos+instrument.marker_size),
        palette.fret_marker_colour)
  return draw


def draw_strings(draw, instrument, image_height, palette):
  '''Add the strings onto the image'''
  for string_num in xrange(instrument.number_of_strings):
    string_pos_x = (string_num * instrument.string_spacing) + instrument.first_string_gap + instrument.margin # horizontal string position
    string_pos_y = instrument.top_gap + instrument.nut_width
    draw.line((string_pos_x, string_pos_y, string_pos_x, image_height),
          palette.string_colour, width=instrument.string_width)
  return draw


def draw_barre_arc(draw, instrument, finger_data_list, string_num, x_pos, y_pos, palette):
  '''Add barre arcs to image if needed'''
  if '-' in finger_data_list[string_num]: # Allow for barre arcs
    finger_str = finger_data_list[string_num][0]
    arc_end = int(finger_data_list[string_num][3])
    x_pos_start = x_pos - 20 # 20 is arb
    y_pos_start = y_pos - 30 # 30 is arb
    x_pos_end = (x_pos + (instrument.string_spacing * ((arc_end-1) - string_num))) + 20 # 20 is arb
    y_pos_end = y_pos + 60 # 60 is arb

    # Debugging code
    #draw.ellipse((x_pos_start-4,y_pos_start-4,x_pos_start+4,y_pos_start+4), fill='red')
    #draw.ellipse((x_pos_end-4,y_pos_end-4,x_pos_end+4,y_pos_end+4), fill='red')

    draw.arc((x_pos_start, y_pos_start, x_pos_end, y_pos_end), 225, 315, fill=palette.arc_colour)
  else:
    finger_str = str(finger_data_list[string_num])

  return finger_str


def draw_finger_circles(draw, instrument, movable_shift, finger_data_list, fret_num, string_num, font_path, palette):
  '''Draw finger circles'''
  x_pos = (string_num * instrument.string_spacing) + instrument.first_string_gap + instrument.margin
  y_pos = (instrument.top_gap + instrument.nut_width) + (instrument.fret_spacing * (fret_num - movable_shift)) - (instrument.fret_spacing
   / 2) # We want the middle of the fret area, not the actual fret position

  draw.ellipse((x_pos-instrument.finger_size, y_pos-instrument.finger_size,
          x_pos+instrument.finger_size, y_pos+instrument.finger_size), palette.finger_circle_colour)

  finger_str = draw_barre_arc(draw, instrument, finger_data_list, string_num, x_pos, y_pos, palette)

  # Draw finger text
  x_pos -= (instrument.finger_font_size / 2)
  y_pos -= (instrument.finger_font_size / 2)
  sans16 = PIL.ImageFont.truetype(font_path, 20)
  draw.text((x_pos+4, y_pos), finger_str, font=sans16, fill=palette.finger_text_colour) # +4 is to make text char line up correctly


def draw_string_data_and_finger_circles(draw, instrument, finger_data_list, movable_shift, fret_data_list, font_path, palette):
  '''Draw open / close string data ("X" or "O"), and fingering circles'''
  for string_num, fret_num in enumerate(fret_data_list):
    fret_num = int(fret_num)

    x_pos = (string_num * instrument.string_spacing) + instrument.first_string_gap + instrument.margin
    y_pos = instrument.top_gap / 2
    if fret_num == -1:    # An "X" is needed
      draw.line((x_pos-instrument.top_gap_data_size, y_pos-instrument.top_gap_data_size,
            x_pos+instrument.top_gap_data_size, y_pos+instrument.top_gap_data_size), palette.xo_colour, width=2)
      draw.line((x_pos-instrument.top_gap_data_size, y_pos+instrument.top_gap_data_size,
            x_pos+instrument.top_gap_data_size, y_pos-instrument.top_gap_data_size), palette.xo_colour, width=2)
    elif fret_num == 0: # An "O" is needed
      draw.ellipse((x_pos-instrument.top_gap_data_size, y_pos-instrument.top_gap_data_size,
              x_pos+instrument.top_gap_data_size, y_pos+instrument.top_gap_data_size), outline=None)
    elif fret_num > 0:    # not -1 or 0 of "X" or "O", must be fingering information
      draw_finger_circles(draw, instrument, movable_shift, finger_data_list, fret_num, string_num, font_path, palette)
  return draw


def draw_chord(instrument, palette, chord_type, finger_data_str, fret_data_str, image_dimentions, output_file):
  ''' Draw the main chord image to file '''
  finger_data_list = finger_data_str.split()
  fret_data_list = fret_data_str.split()

  font_path = '/usr/share/fonts/dejavu/DejaVuSerifCondensed-Bold.ttf' # FIX ME!
  movable_shift = 0
  if chord_type == 'Movable':
    min_fret = 100
    for fret in fret_data_list:
      fret = int(fret)
      if (fret < min_fret) and (fret > 0):
        min_fret = fret

    movable_shift = min_fret - 2                    # How far to alter fretting when drawing movable chord, -1 allows for space above

  # Create a new image
  image_width = image_dimentions[0]
  image_height = image_dimentions[1]
  image = PIL.Image.new('RGB', image_dimentions)

  draw = PIL.ImageDraw.Draw(image)
  # Draw the fretboard
  draw.polygon([(instrument.margin, instrument.top_gap + instrument.nut_width), (image_width, instrument.top_gap + instrument.nut_width), (image_width, image_height), (instrument.margin, image_height)], palette.fret_board_colour)

  # Draw the plastic nut if needed
  if movable_shift == 0:
    draw.line((instrument.margin, instrument.top_gap, image_width, instrument.top_gap), palette.nut_colour, width=8)

  draw = draw_frets(draw, instrument, movable_shift, image_width, palette, font_path)
  draw = draw_fret_markers(draw, instrument, movable_shift, palette)
  draw = draw_strings(draw, instrument, image_height, palette)
  draw = draw_string_data_and_finger_circles(draw, instrument, finger_data_list, movable_shift, fret_data_list, font_path, palette)


  del draw
  # Write image to disk
  image.save(output_file, 'PNG')
