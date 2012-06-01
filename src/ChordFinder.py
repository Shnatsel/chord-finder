#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Main chord-finder entry point """

import wx, os

import ChordData, DrawChord, DrawRootFinder, Instruments, Palettes, Gui

CONFIG = {}

CONFIG['VERSION'] = '1.0'

if os.path.realpath(__file__).split('/')[1] == 'usr':
    # Installed
    CONFIG['data_dir'] = '/usr/data/chord-finder/'
else:
    # Not Installed / Dev environment
    CONFIG['data_dir'] = os.path.dirname(os.path.abspath(__file__))+'/../data/'

#################
#### MAIN () ####
#################
CHORD_DB = ChordData.ChordDatabase(CONFIG['data_dir']+'ChordData.csv')
APP = wx.PySimpleApp(0)
wx.InitAllImageHandlers()
MAIN_FRAME = Gui.MainFrame(None, -1, "", CHORD_DB, CONFIG)
APP.SetTopWindow(MAIN_FRAME)
MAIN_FRAME.Show()
MAIN_FRAME.Centre()
APP.MainLoop()
