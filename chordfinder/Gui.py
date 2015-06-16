""" File that contains the gui related code """

import wx, tempfile
import Instruments, Palettes, ChordData, DrawChord, DrawRootFinder


class FilterError(Exception):
  """ Place-holder class for custom error raising """
  pass

class MainFrame(wx.Frame):
  ''' The gui class '''
  # Event handlers

  def on_about(self, event):
    ''' Triggered when "about" is selected from menus, just a simple dialog window'''
    dialog = wx.MessageDialog(self, 'Welcome to chord finder\n \
    \nPlease report bugs to:\n siology.io@gmail.com', 'About chord finder', wx.OK | wx.ICON_INFORMATION)
    dialog.ShowModal()
    dialog.Destroy()


  def on_chord_changed(self, event, chord_db, config):
    '''Triggered when chord name dropdown list is altered. Sets up images for new chord'''
    chord_name = self.chord_name_combo.GetValue()

    chord_output_file = tempfile.NamedTemporaryFile('w')
    movable_image = tempfile.NamedTemporaryFile('w')

    instrument_obj = Instruments.Instrument()
    palette_obj = Palettes.Palette(self.palette_radio.GetSelection())

    try:
      chord_obj = chord_db.get_single_chord_obj(self.chord_type_radio.GetStringSelection(), chord_name)
    except ChordData.ChordNotFound:
      self.SetStatusText("Chord: {0} was not found in chord data archive".format(chord_name))
    else:
      # Link up the chord images (and movable data image, if needed)
      if self.chord_type_radio.GetStringSelection() == 'Movable':
        DrawRootFinder.draw_root_finder(instrument_obj, palette_obj, chord_obj, (290, 100), movable_image.name)
        self.movable_bitmap.SetBitmap(wx.Bitmap(movable_image.name, wx.BITMAP_TYPE_ANY))
        self.movable_bitmap.Show()
      else:
        self.movable_bitmap.Hide()
        self.Refresh()

      # Main chord info is shown either way
      DrawChord.draw_chord(instrument_obj, palette_obj, chord_obj.chord_type, chord_obj.finger_str, chord_obj.fret_str, (290, 490), chord_output_file)
      self.chord_bitmap.SetBitmap(wx.Bitmap(chord_output_file.name))
      self.SetStatusText('Showing: ' + chord_obj.long_name)


  def prev_or_next_chord(self, event, direction, chord_db, config):
    ''' Shift selected chord by one position '''
    curr_selected = self.chord_name_combo.GetSelection()

    if (direction == -1) and (curr_selected != 0):
      self.chord_name_combo.SetSelection(curr_selected-1)
    elif direction == 1:
      # Will auto-cycle to first item if needed
      self.chord_name_combo.SetSelection(curr_selected+1)
    else:
      # Move to last item in list
      self.chord_name_combo.SetSelection(self.chord_name_combo.GetCount()-1)
    self.on_chord_changed(self, chord_db, config)


  def on_filter_changed(self, event, chord_db, config):
    ''' Triggered when filter radio box is altered
        Filter the available chords to allow for the updated filter settings'''
    self.chord_name_combo.Clear()

    aug_dim_wanted = self.aug_dim_combo.GetStringSelection()
    aug_dim_wanted_long = ''

    if aug_dim_wanted == 'All':
      aug_dim_wanted_long = aug_dim_wanted
    elif aug_dim_wanted == 'aug':
      aug_dim_wanted_long = 'Augmented'
    elif aug_dim_wanted == 'dim':
      aug_dim_wanted_long = 'Diminished'
    elif aug_dim_wanted == 'dom':
      aug_dim_wanted_long = 'Dominant'
    elif aug_dim_wanted == 'm':
      aug_dim_wanted_long = 'Minor'
    elif aug_dim_wanted == 'M':
      aug_dim_wanted_long = 'Major'
    elif aug_dim_wanted == 'sus':
      aug_dim_wanted_long = 'Suspended'
    else:
      raise FilterError

    self.chord_name_combo.AppendItems(chord_db.get_filtered_chord_names(self.chord_type_radio.GetStringSelection(),
        self.root_filter_combo.GetStringSelection(), aug_dim_wanted_long))

    # Set combo to be new first entry and then change image to match
    self.chord_name_combo.SetValue(self.chord_name_combo.GetString(0))
    self.on_chord_changed(event, chord_db, config)


  def on_exit(self, event):
    '''Simple exit function'''
    self.Close(True)


  def on_play_chord(self, event, chord_db):
    '''Delegate out to bash playing a chord, avoid wheel reinvention'''

    chord_name = self.chord_name_combo.GetValue()
    if not chord_name:
      return 1

    try:
      chord_obj = chord_db.get_single_chord_obj(self.chord_type_radio.GetStringSelection(), chord_name)
    except ChordData.ChordNotFound:
      self.SetStatusText("Chord: {0} was not found in chord data archive".format(chord_name))
    else:
      chord_db.play_chord_from_obj(chord_obj)


# END OF EVENT HANDELERS

  def __init__(self, parent, ident, title, chord_db, config):
    '''Main gui class'''
    wx.Frame.__init__(self, parent, ident, title, wx.DefaultPosition, wx.Size(500, 600))

    favicon = wx.Icon(config['data_dir']+'favicon.ico', wx.BITMAP_TYPE_ICO, 16, 16)
    wx.Frame.SetIcon(self, favicon)
    self.menu_bar = wx.MenuBar()

    # Menu bar
    id_about = 101
    id_exit = 102
    self.CreateStatusBar()
    self.SetStatusText('Welcome to Chord Finder')
    menu = wx.Menu()
    menu.Append(id_about, '&About', 'More information about this program')
    menu.AppendSeparator()
    menu.Append(id_exit, 'E&xit', 'Terminate the program')
    menu_bar = wx.MenuBar()
    menu_bar.Append(menu, '&File')
    self.SetMenuBar(menu_bar)
    wx.EVT_MENU(self, id_about, self.on_about)
    wx.EVT_MENU(self, id_exit, self.on_exit)
    # End of Menu bar

    # The bitmap areas
    self.welcome_label = wx.StaticText(self, -1, 'Welcome to chord finder')
    self.chord_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(config['data_dir']+'welcomeChord.png', wx.BITMAP_TYPE_ANY))
    self.movable_bitmap = wx.StaticBitmap(self, -1)

    # Static / Movable chord type combo box and its label
    self.chord_type_radio = wx.RadioBox(self, -1, 'Type', choices=['Static', 'Movable'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
    self.chord_type_radio.Bind(wx.EVT_RADIOBOX, lambda evt, cdb=chord_db, cfg=config: self.on_filter_changed(evt, cdb, cfg))

    # Dropdown list of chord names with prev/next buttons
    self.prev_chord_button = wx.Button(self, -1, label='<', size=(30, 30))
    self.chord_name_combo = wx.ComboBox(self, -1, choices=chord_db.get_all_chord_names(), style=wx.CB_DROPDOWN, size=(130, 30))
    self.next_chord_button = wx.Button(self, -1, label='>', size=(30, 30))

    self.chord_name_combo.Bind(wx.EVT_COMBOBOX, lambda evt, cdb=chord_db, cfg=config: self.on_chord_changed(evt, cdb, cfg))
    self.prev_chord_button.Bind(wx.EVT_BUTTON, lambda evt, cdb=chord_db, cfg=config, d=-1: self.prev_or_next_chord(evt, d, cdb, cfg))
    self.next_chord_button.Bind(wx.EVT_BUTTON, lambda evt, cdb=chord_db, cfg=config, d=1: self.prev_or_next_chord(evt, d, cdb, cfg))

    # Play chord button
    self.play_chord_button = wx.Button(self, -1, label='Play chord', size=(100, 30))
    self.play_chord_button.Bind(wx.EVT_BUTTON, lambda evt, cdb=chord_db: self.on_play_chord(evt, cdb))

    # Palette choice radio box
    self.palette_radio = wx.RadioBox(self, -1, 'Palette', choices=['Colour', 'B/W'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
    self.palette_radio.Bind(wx.EVT_RADIOBOX, lambda evt, cdb=chord_db, cfg=config: self.on_filter_changed(evt, cdb, cfg))

    # Root filter combobox and its label
    self.root_filter_label = wx.StaticText(self, -1, 'Root:')
    self.root_filter_combo = wx.ComboBox(self, -1, choices=['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G'], style=wx.CB_DROPDOWN, size=(130, 30))
    self.root_filter_combo.Bind(wx.EVT_COMBOBOX, lambda evt, cdb=chord_db, cfg=config: self.on_filter_changed(evt, cdb, cfg))

    # Aug / Dom combo box and its label
    self.aug_dim_label = wx.StaticText(self, -1, 'Chord mode:')
    self.aug_dim_combo = wx.ComboBox(self, -1, choices=['All', 'M', 'm', 'dom', 'dim', 'aug', 'sus'], style=wx.CB_DROPDOWN, size=(130, 30))
    self.aug_dim_combo.Bind(wx.EVT_COMBOBOX, lambda evt, cdb=chord_db, cfg=config: self.on_filter_changed(evt, cdb, cfg))

    # Set this all up
    self.__set_properties(config=config)
    self.__do_layout()


  def __set_properties(self, config):
    """ Deal with any property setting needs """
    self.SetTitle('Guitar Chord Finder: ' + config['VERSION'])
    self.chord_bitmap.SetMinSize((290, 490))
    self.movable_bitmap.SetMinSize((290, 100))
    self.chord_type_radio.SetSelection(0)
    self.root_filter_combo.SetSelection(0)
    self.aug_dim_combo.SetSelection(0)
    self.chord_name_combo.SetSelection(-1)


  def __do_layout(self):
    """ Deal with the arrangement of the widgets """
    # Create the sizers
    main_area_sizer = wx.BoxSizer(wx.HORIZONTAL)
    right_half_sizer = wx.BoxSizer(wx.VERTICAL)
    chord_select_sizer = wx.BoxSizer(wx.HORIZONTAL)
    root_filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
    aug_dim_sizer = wx.BoxSizer(wx.HORIZONTAL)

    # Fill the sizers and create hierarchy
    main_area_sizer.Add(self.chord_bitmap, flag=wx.EXPAND)

    chord_select_sizer.Add(self.prev_chord_button, flag=wx.EXPAND)
    chord_select_sizer.Add(self.chord_name_combo, flag=wx.EXPAND)
    chord_select_sizer.Add(self.next_chord_button, flag=wx.EXPAND)

    root_filter_sizer.Add(self.root_filter_label, flag=wx.ALIGN_RIGHT)
    root_filter_sizer.Add(self.root_filter_combo, flag=wx.ALIGN_RIGHT)

    aug_dim_sizer.Add(self.aug_dim_label, flag=wx.ALIGN_RIGHT)
    aug_dim_sizer.Add(self.aug_dim_combo, flag=wx.ALIGN_RIGHT)

    # Create the sizer hierarchy
    filters_box = wx.StaticBox(self, wx.VERTICAL, label='Filters')

    filters_sizer = wx.StaticBoxSizer(filters_box, wx.VERTICAL)
    filters_sizer.Add(self.chord_type_radio, flag=wx.ALIGN_RIGHT)
    filters_sizer.Add(root_filter_sizer, flag=wx.ALIGN_RIGHT)
    filters_sizer.Add(aug_dim_sizer)

    right_half_sizer.Add(self.palette_radio)
    right_half_sizer.Add(chord_select_sizer)
    right_half_sizer.Add(self.play_chord_button)
    right_half_sizer.Add(filters_sizer)
    right_half_sizer.Add(self.movable_bitmap)

    main_area_sizer.Add(right_half_sizer)

    # Display the result
    self.SetSizer(main_area_sizer)
    main_area_sizer.Fit(self)
    self.Layout()
