#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

#/usr/src/examples/python-serial-2.6

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject
import gc
import re
import shlex, subprocess
import avrList

class uiCfgAVR:
	def __init__(self):
		self.selSUT=''
		self.bDefaultLock=False
		self.argsAVRdude = []
		self.reHex=re.compile('(0x)([0-9A-F]{1,2})$', re.I | re.L)
		self.reBin=re.compile('(0b)([01]{1,8})$', re.I | re.L)
		self.reDec=re.compile('([0-9]{1,3})$', re.L)

		self.BGcolor = gtk.gdk.Color('#383430')
		self.BGcolorEntry = gtk.gdk.Color('#201810')
		self.BGcolorSelect = gtk.gdk.Color('#201810')
		self.FGcolor = gtk.gdk.Color('#FFF')
		#self.FGcolorHover = gtk.gdk.Color('#8F8')

		if __name__ == "__main__":
			self.uiInit()
			self.mainWindow.connect("destroy", lambda w: gtk.main_quit())
			self.buttonExit.connect("clicked", lambda w: gtk.main_quit())
			gtk.main()

	def uiInit(self, dialog=False):
		from os import chdir as cd
		from os import path as pt
		self.execDir = pt.dirname(pt.abspath(__file__))
		cd(self.execDir)
		rcfile=('%s/gtkrc' % self.execDir)
		if pt.isfile(rcfile):
			gtk.rc_set_default_files(rcfile,)
			gtk.rc_parse(rcfile)
			print("Rc file exist...")
		else:
			print('Rc file disapears ?')
		self.cfBPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Configbyte.png")
		self.fsBPixbuf =  gtk.gdk.pixbuf_new_from_file("pic/Fusebyte.png")
		self.fsbPixbuf =  gtk.gdk.pixbuf_new_from_file("pic/Fusebit.png")
		self.lBPixbuf =  gtk.gdk.pixbuf_new_from_file("pic/Lockbyte.png")
		self.lbPixbuf =  gtk.gdk.pixbuf_new_from_file("pic/Lockbit.png")
		self.lghtPixbuf =  gtk.gdk.pixbuf_new_from_file("pic/Lightenings.png")
		
		gtk.window_set_default_icon_list(self.fsBPixbuf, self.lghtPixbuf)

		if not hasattr(self, 'title'):
			self.title="AVRmate - Fusebits Calculator V.0.51 User interface"
		
		self.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.wdhMain, self.hgtMain = (640, 750)
		self.mainWindow.set_geometry_hints(
			min_width=self.wdhMain, min_height=self.hgtMain,
			max_width=self.wdhMain, max_height=self.hgtMain)
		self.mainWindow.set_title(self.title)
		self.mainWindow.set_border_width(5)
		styleMain=self.mainWindow.get_style().copy()
		
		self.fixedFrame = gtk.Fixed()
		
		self.labelUcSelect = gtk.Label("µC :")
		self.labelUcSelect.set_size_request(20, 30)
		self.labelUcSelect.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		
		self.fixedFrame.put(self.labelUcSelect, 10, 5)
		
		self.cbUcSelect = gtk.ComboBox()
		self.cbUcSelect.set_size_request(110, 30)
		self.lsUcSelect = gtk.ListStore(str)
		self.crtUcSelect = gtk.CellRendererText()
		self.crtUcSelect.set_property('cell-background-gdk', self.BGcolor)
		self.crtUcSelect.set_property('foreground-gdk', self.FGcolor)
		self.cbUcSelect.pack_start(self.crtUcSelect)
		self.cbUcSelect.set_attributes(self.crtUcSelect, text=0)
		self.cbUcSelect.set_wrap_width(3)
		self.cbUcSelect.set_model(self.lsUcSelect)
		
		self.fixedFrame.put(self.cbUcSelect, 40, 5)

		self.labelPgmSelect = gtk.Label("Programmer:")
		self.labelPgmSelect.set_size_request(65, 30)
		self.labelPgmSelect.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		
		self.fixedFrame.put(self.labelPgmSelect, 160, 5)
		
		self.cbPgmSelect = gtk.ComboBox()
		self.cbPgmSelect.set_size_request(140, 30)
		self.lsPgmSelect = gtk.ListStore(str, str, str)
		self.crtPgmSelect = gtk.CellRendererText()
		self.crtPgmSelect.set_property('cell-background-gdk', self.BGcolor)
		self.crtPgmSelect.set_property('foreground-gdk', self.FGcolor)
		self.cbPgmSelect.pack_start(self.crtPgmSelect)
		self.cbPgmSelect.set_attributes(self.crtPgmSelect, text=0)
		self.cbPgmSelect.set_wrap_width(3)
		self.cbPgmSelect.set_model(self.lsPgmSelect)
		
		self.fixedFrame.put(self.cbPgmSelect, 230, 5)

		self.checkClk = gtk.CheckButton("Slower Clock")
		self.checkClk.set_size_request(100, 30)
		
		self.fixedFrame.put(self.checkClk, 420, 5)

		self.checkErase = gtk.CheckButton("Chip Erase")
		self.checkErase.set_size_request(100, 30)
		
		self.fixedFrame.put(self.checkErase, 530, 5)

		### Begin of Tree Store ###
		self.tsBits = gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, str, gtk.ListStore, bool, bool, str)
		
		
		self.tvBitsFontSize = 10
		self.tvBits = gtk.TreeView(self.tsBits)
		

		#Column #1 - Name
		colWidth = 125
		self.tvcBitsName = gtk.TreeViewColumn('Name')
		self.tvcBitsName.set_alignment(0.5)
		self.tvcBitsName.set_min_width(colWidth)
		self.tvcBitsName.set_max_width(colWidth)
		
		self.crpxBitsNameB = gtk.CellRendererPixbuf()
		self.crpxBitsNameB.set_property('cell-background-gdk', gtk.gdk.Color('#050'))
		self.tvcBitsName.pack_start(self.crpxBitsNameB, False)
		self.tvcBitsName.set_attributes(self.crpxBitsNameB, pixbuf=0)
		
		self.crtxtBitsName = gtk.CellRendererText()
		self.crtxtBitsName.set_property('cell-background-gdk', gtk.gdk.Color('#280'))
		self.crtxtBitsName.set_property('stretch', pango.STRETCH_EXTRA_CONDENSED)
		self.crtxtBitsName.set_property('size-points', self.tvBitsFontSize)
		self.tvcBitsName.pack_start(self.crtxtBitsName, False)
		self.tvcBitsName.set_attributes(self.crtxtBitsName, text=1)
		
		self.tvBits.append_column(self.tvcBitsName)

		#Column #2 - Description
		colWidth = 180
		self.tvcBitsDesc = gtk.TreeViewColumn('Description')
		self.tvcBitsDesc.set_alignment(0.5)
		self.tvcBitsDesc.set_min_width(colWidth)
		self.tvcBitsDesc.set_max_width(colWidth)
		self.crtxtBitsDesc = gtk.CellRendererText()
		self.crtxtBitsDesc.set_property('cell-background-gdk', gtk.gdk.Color('#850'))
		self.crtxtBitsDesc.set_property('size-points', self.tvBitsFontSize)
		self.crtxtBitsDesc.set_property('wrap-mode', True)
		self.crtxtBitsDesc.set_property('wrap-width', colWidth)
		self.tvcBitsDesc.pack_start(self.crtxtBitsDesc, True)
		self.tvcBitsDesc.set_attributes(self.crtxtBitsDesc, text=2)

		
		self.tvBits.append_column(self.tvcBitsDesc)

		#Column #3 - Value
		self.crtcbBitsValue = gtk.CellRendererCombo()
		cbWidth = 230
		self.crtcbBitsValue.set_property('cell-background-gdk', gtk.gdk.Color('#055'))
		self.crtcbBitsValue.set_property('size-points', self.tvBitsFontSize)
		self.crtcbBitsValue.set_property('text-column', 0)
		self.crtcbBitsValue.set_property('has-entry', False)
		self.crtcbBitsValue.set_property('width', cbWidth)
		
		self.tvcBitsValue = gtk.TreeViewColumn('Setup Value', self.crtcbBitsValue, text=3, model=5, editable=6)
		self.tvcBitsValue.set_alignment(0.5)
		
		self.crtxtBitsValue = gtk.CellRendererText()
		self.crtxtBitsValue.set_property('cell-background-gdk', gtk.gdk.Color('#085'))
		self.crtxtBitsValue.set_property('size-points', self.tvBitsFontSize)
		self.crtxtBitsValue.set_property('xalign', 0.95)
		
		self.tvcBitsValue.pack_start(self.crtxtBitsValue, True)
		self.tvcBitsValue.set_attributes(self.crtxtBitsValue, text=4, editable=7)
		
		self.tvBits.append_column(self.tvcBitsValue)
		
		self.tvBits.set_tooltip_column(2, )
		#self.tvBits.set_tooltip_column(8, )
		self.tvBits.set_enable_tree_lines(True)
		self.tvBits.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color('#242D20'))
		self.tvBits.modify_text(gtk.STATE_NORMAL, self.FGcolor)
		
		self.tvBits.modify_base(gtk.STATE_ACTIVE, self.BGcolorSelect)
		self.tvBits.modify_text(gtk.STATE_ACTIVE, self.FGcolor)
		#uiDebug = "Composite child:%s\ntvBits props:\n" % self.tvBits.composite_child
		uiDebug = "tvBits props:\n"
		for propEz in dir(self.tvBits.props):
			uiDebug += "\t%s\n" % propEz
		print(uiDebug)

		self.scroll=gtk.ScrolledWindow()
		self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scroll.add(self.tvBits)
		self.scroll.set_size_request(605, 610)
		self.fixedFrame.put(self.scroll, 10, 40)
		self.tvBitsSelection = self.tvBits.get_selection()
		self.tvBitsSelection.set_mode(gtk.SELECTION_SINGLE)
		### End of Tree Store ###

		self.textAvrdudeCmd = gtk.Entry()
		self.textAvrdudeCmd.set_property("editable", False)
		self.textAvrdudeCmd.set_icon_from_pixbuf(0, self.lghtPixbuf)
		self.textAvrdudeCmd.set_icon_tooltip_text(0, 'Click here or pres enter in right text to start avrdude')
		self.textAvrdudeCmd.set_size_request(605, 30)
		self.textAvrdudeCmd.modify_base(gtk.STATE_NORMAL, self.BGcolorEntry)
		self.textAvrdudeCmd.modify_text(gtk.STATE_NORMAL, self.FGcolor)
		
		self.fixedFrame.put(self.textAvrdudeCmd, 10, 660)
		
		self.imageLogo = gtk.Image()
		self.imageLogo.set_from_pixbuf(self.cfBPixbuf)
		
		self.fixedFrame.put(self.imageLogo, 10, 700)
		
		self.buttonPng = gtk.Button("Save as png")
		self.buttonPng.set_size_request(70, 25)
		
		self.fixedFrame.put(self.buttonPng, 400, 715)

		self.buttonTest = gtk.Button("Test")
		self.buttonTest.set_size_request(50, 25)
		
		self.fixedFrame.put(self.buttonTest, 480, 715)

		accGroup = gtk.AccelGroup()
		self.mainWindow.add_accel_group(accGroup)

		self.buttonExit = gtk.Button("Exit (Ctrl+Q)")
		self.buttonExit.set_size_request(80, 25)

		self.buttonExit.add_accelerator(
			"clicked",
			accGroup,
			ord('Q'),
			gtk.gdk.CONTROL_MASK,
			gtk.ACCEL_VISIBLE)
		
		self.fixedFrame.put(self.buttonExit, 540, 715)
		#self.fixedFrame.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		
		self.mainWindow.add(self.fixedFrame)
		
		self.mainWindow.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		#self.mainWindow.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		
		self.mainWindow.show_all()
		self.mainWindow.set_keep_above(True)
		return

	def chooseInit(self):
		self.ucClList=avrList.listAVR()
		self.ucList=self.ucClList.listAVRs()
		self.lnUcList=len(self.ucList)
		for ucIndex in range(self.lnUcList):
			self.lsUcSelect.append([self.ucList[ucIndex]])
		#self.cbUcSelect.set_active(0)
		return
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

	def quit_cb(self, widget):
		self.ucClList.empty()
		gtk.main_quit()


if __name__ == "__main__":
	uiCfgAVR()
