#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import gtk, pango

class tabParam:
	def __init__(tp, pos, size):
		tp.X, tp.Y = pos
		tp.W, tp.H = size

	def default_spc(tp):
		tp.spcW, tp.spcH = tp.W-10, tp.H-40

	def set_spc(tp, spc):
		tp.spcW, tp.spcH = spc

class apw:
	def __init__(self):
		self.BGcolor = None
		self.BGcolorA = None
		self.BGcolorEntry = None
		self.FGcolor = None
		self.gtk, self.pango = gtk, pango

	def rundir(self):
		from os import chdir as cd
		cd(self.callDir)

	def rcGet(self, use_common_rc=False):
		from os import path as pt
		from sys import _current_frames as _cf
		callingFilename = _cf().values()[0].f_back.f_code.co_filename
		self.callDir = pt.dirname(callingFilename)
		if use_common_rc:
			rcDirName = pt.dirname(pt.abspath(__file__))
		else:
			rcDirName = self.callDir
		rcfile=('%s/gtkrc' % rcDirName)
		if pt.isfile(rcfile):
			gtk.rc_set_default_files(rcfile,)
			gtk.rc_parse(rcfile)
			print("Rc file exist...")
		else:
			print('Rc file disapears ?')

	#def TabCtrl(self, hFixed, posX, poxY, width, height, fontDesc=None):
		#hTabC.set_size_request(width, height)
		#hFixed.put(hTabC, posX, poxY)

	def putScroll(self, hFixed, widget, posX, poxY, width, height):
		hScroll = gtk.ScrolledWindow()
		hScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hScroll.add(widget)
		hScroll.set_size_request(width, height)
		hFixed.put(hScroll, posX, poxY)

	def TabCtrl(self, hFixed, tp, fontDesc=None):
		hTabC = gtk.Notebook()
		hTabC.tp = tp
		hTabC.set_tab_pos(gtk.POS_TOP)
		hTabC.set_size_request(tp.W, tp.H)
		hFixed.put(hTabC, tp.X, tp.Y)
		hTabC.show()
		if fontDesc:
			hTabC.modify_font(fontDesc)
		if self.BGcolor:
			hTabC.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		if self.BGcolorA:
			hTabC.modify_bg(gtk.STATE_ACTIVE, self.BGcolorA)
		return hTabC

	def addTab(self, tabFrame, tabCtrl, txtLabel, fontDesc=None):
		hLabel = gtk.Label(txtLabel)
		if self.FGcolor:
			hLabel.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		hLabel.modify_fg(gtk.STATE_ACTIVE, self.FGcolorA)
		if fontDesc:
			hLabel.modify_font(fontDesc)
		tabCtrl.append_page(tabFrame, hLabel)
		return hLabel

	def Frame(self, txtLabel, hFixed, posX, poxY, width, height, fontDesc=None):
		hFrame = gtk.Frame()
		#hFrame = gtk.Frame(txtLabel)
		#if self.FGcolor:
			#hFrame.child.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		labelBox = gtk.EventBox()
		frameLabel = gtk.Label(' '+txtLabel+' ')
		frameLabel.show()
		if self.FGcolor:
			frameLabel.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		labelBox.add(frameLabel)
		if self.BGcolor:
			labelBox.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		hFrame.set_label_widget(labelBox)
		if fontDesc:
			frameLabel.modify_font(fontDesc)
		if self.FGcolor:
			hFrame.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		hFrame.set_size_request(width, height)
		if hFixed:
			hFixed.put(hFrame, posX, poxY)
		return hFrame

	def npLabel(self, txtLabel, fontDesc=None):
		hLabel = gtk.Label(txtLabel)
		if self.FGcolor:
			hLabel.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		if fontDesc:
			hLabel.modify_font(fontDesc)
		hLabel.show()
		return hLabel

	def Label(self, txtLabel, hFixed, posX, poxY, width, height=None, fontDesc=None):
		if not height:
			height=self.Height
		hLabel = self.npLabel(txtLabel, fontDesc=fontDesc)
		hLabel.set_size_request(width, height)
		if hFixed:
			hFixed.put(hLabel, posX, poxY)
			
		return hLabel

	# Create a new backing pixmap of the appropriate size
	def evConfDrawA(self, widget, event, pixDraw, debug=False):
		x, y, width, height = widget.get_allocation()
		pixDraw = gtk.gdk.Pixmap(widget.window, width, height, depth=-1)
		pixDraw.draw_rectangle(widget.get_style().black_gc, True, 0, 0, width, height)
		if debug:
			print("Configure...")
		return True

	# Redraw the screen from the backing pixmap
	def evExpDrawA(self, widget, event, pixDraw, debug=False):
		x , y, width, height = event.area
		widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL], pixDraw, x, y, x, y, width, height)
		if debug:
			print("Expose...")
		return False

	#def DrawBox(self, hFixed, posX, poxY, width, height,
			#EvFlags=gtk.gdk.POINTER_MOTION_MASK|gtk.gdk.POINTER_MOTION_HINT_MASK, confCall=None, expsCall=None):
	def DrawBox(self, hFixed, posX, poxY, width, height):
		hDraw = gtk.DrawingArea()
		hDraw.set_size_request(width, height)
		if hFixed:
			hFixed.put(hDraw, posX, poxY)
		hPangoLay = hDraw.create_pango_layout("")
		#hDraw.set_events(EvFlags)
		hDraw.pixDraw = None
		if confCall:
			hDraw.connect("configure-event", self.evConfDrawA, hDraw.pixDraw)
		if expsCall:
			hDraw.connect("expose-event", self.evExpDrawA, hDraw.pixDraw)
		hDraw.confCall = confCall
		hDraw.expsCall = expsCall
		return hDraw

	def HSeparator(self, hFixed, posX, poxY, width):
		hHSep = gtk.HSeparator()
		hHSep.set_size_request(width, 10)
		hFixed.put(hHSep, posX, poxY)
		#if self.FGcolor:
			#hHSep.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		return hHSep

	def VSeparator(self, hFixed, posX, poxY, height):
		hVSep = gtk.VSeparator()
		hVSep.set_size_request(5, height)
		hFixed.put(hVSep, posX, poxY)
		return hVSep

	def Check(self, txtLabel, hFixed, posX, poxY, width, height=None, fontDesc=None):
		if not height:
			height=self.Height
		hCheck = gtk.CheckButton(label=txtLabel, use_underline=False)
		if self.FGcolor:
			hCheck.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		hLabel=hCheck.child
		if fontDesc:
			hLabel.modify_font(fontDesc)
		hCheck.set_size_request(width, height)
		hFixed.put(hCheck, posX, poxY)
		return hCheck

	def npToggle(self, txtLabel, hFixed, posX, poxY, width, fontDesc=None):
		hToggle = gtk.ToggleButton(label=txtLabel, use_underline=False)
		if self.FGcolor:
			hToggle.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		if fontDesc:
			hLabel = hToggle.child
			hLabel.modify_font(fontDesc)
		return hToggle

	def Toggle(self, txtLabel, hFixed, posX, poxY, width, height=None, fontDesc=None):
		if not height:
			height=self.Height
		hToggle = self.npToggle(txtLabel, hFixed, posX, poxY, width, fontDesc=fontDesc)
		hToggle.set_size_request(width, height)
		hFixed.put(hToggle, posX, poxY)
		return hToggle

	def gobjInspect(self, hObj):
		tc = ta = ''
		for atr in dir(hObj):
			r_atr = getattr(hObj, atr)
			if callable(r_atr):
				tc += "\t%s\n" % atr
			else:
				ta += "\t%s\n" % atr
		print("Callables:\n%s" % tc)
		print("Atributes:\n%s" % ta)
		for atr in dir(hObj.props):
			print("\tProp: %s(%s)" % (atr, str(type(getattr(hObj.props, atr)))))
		#self.gobjInspect(image)
		#print("xpad:%i, ypad:%i, width_request:%i"% (image.props.xpad, image.props.ypad, image.props.width_request))
		#try:
			#import readline
		#except ImportError:
			#print("Unable to load readline module.")
		#else:
			#import rlcompleter
			#readline.parse_and_bind("tab: complete")
		#import code; code.interact(local=locals())

	def replaceButtStockImage(self, hButt, stockID, size=2):
		"Probably size16 = 1; size32 = 2..."
		image = hButt.child
		if not(isinstance(image, gtk.Image)):
			return
		image.set_from_stock(stock_id=stockID, size=size)

	def npButt(self, txtLabel, fileImage=None, stockID=None, fontDesc=None):
		if stockID == None and fileImage == None:
			hButt = gtk.Button(label=txtLabel, use_underline=False)
			if fontDesc:
				hLabel = hButt.child
				hLabel.modify_font(fontDesc)
		else:
			if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
				txtLabel = bool(txtLabel)
			if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
				if stockID:
					hButt = gtk.Button(stock=stockID)
				elif fileImage:
					image = gtk.Image()
					image.set_from_file(fileImage)
					hButt = gtk.Button()
					hButt.add(image)
				if type(txtLabel)==str:
					hLabel = hButt.get_children()[0].get_children()[0].get_children()[1]
					hLabel.set_text(txtLabel)
					if fontDesc:
						hLabel.modify_font(fontDesc)
			else:
				image = gtk.Image()
				if stockID:
					image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
				elif fileImage:
					image.set_from_file(fileImage)
				hButt = gtk.Button()
				hButt.add(image)
		if self.FGcolor:
			hButt.modify_fg(gtk.STATE_NORMAL, self.FGcolor)
		return hButt

	def Butt(self, txtLabel, hFixed, posX, poxY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
		"""If stockID is set, txtLabel set as True means full stock button,
		non-null string - own Label for stock image,
		in other case - button with only stock image"""
		if not height:
			height=self.Height
		hButt = self.npButt(txtLabel, fileImage=fileImage, stockID=stockID, fontDesc=fontDesc)
		#if self.BGcolor:
			#hButt.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		hButt.set_size_request(width, height)
		hFixed.put(hButt, posX, poxY)
		return hButt

	def ComboBox(self, modelCb, hFixed, posX, poxY, width, height=None, fontDesc=None, wrap=None, selTxt=0):
		if not height:
			height=self.Height
		hCb = gtk.ComboBox()
		crtCb = gtk.CellRendererText()
		#dir(crtCb.props)
		#if self.BGcolor:
			#crtCb.set_property('background-gdk', self.BGcolor)
		#if self.FGcolor:
			#crtCb.set_property('foreground-gdk', self.FGcolor)
		if self.BGcolor:
			crtCb.set_property('cell-background-gdk', self.BGcolor)
		#crtCb.set_property('cell-background-set', True)
		if fontDesc:
			crtCb.set_property('font-desc', fontDesc)
		hCb.pack_start(crtCb)
		hCb.set_attributes(crtCb, text=selTxt)
		if wrap:
			hCb.set_wrap_width(wrap)
		else:
			crtCb.set_property('ellipsize', pango.ELLIPSIZE_END)
		hCb.set_model(modelCb)
		hCb.set_size_request(width, height+4)
		#if self.BGcolor:
			#hCb.child.set_property('background-gdk', self.BGcolor)
		#if self.FGcolor:
			#hCb.child.modify_base(gtk.STATE_PRELIGHT, self.FGcolor)
			#hCb.child.modify_bg(gtk.STATE_PRELIGHT, self.FGcolor)
			#hCb.modify_base(gtk.STATE_PRELIGHT, self.FGcolor)
			#hCb.modify_bg(gtk.STATE_PRELIGHT, self.FGcolor)
		hFixed.put(hCb, posX, poxY-2)
		#for prop in crtCb.props:
			#v = crtCb.get_property(prop)
			#if 'background' in prop:
				#print("Properity name: \"%s\", Value:" % (prop), v)
		return hCb

	def textClr(self, widget, icoPos, sigEvent):
		if icoPos == gtk.ENTRY_ICON_SECONDARY:
			widget.set_text('')

	def npEntry(self, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		hEntry = gtk.Entry()
		if self.BGcolorEntry:
			hEntry.modify_base(gtk.STATE_NORMAL, self.BGcolorEntry)
		if self.FGcolor:
			hEntry.modify_text(gtk.STATE_NORMAL, self.FGcolor)
		if fontDesc:
			hEntry.modify_font(fontDesc)
		if startIco:
			self.textInput.set_icon_from_pixbuf(0, startIco)
		if clearIco:
			hEntry.set_icon_from_stock(1, gtk.STOCK_CLOSE)
			hEntry.set_icon_tooltip_text (1, 'Clear')
			hEntry.connect("icon-release", self.textClr)
		hEntry.set_property("editable", bool(bEditable))
		return hEntry

	def Entry(self, hFixed, posX, poxY, width, height=None, startIco=None, clearIco=False, bEditable=True, fontDesc=None):
		if not height:
			height=self.Height
		hEntry = self.npEntry(clearIco=clearIco, bEditable=bEditable, fontDesc=fontDesc)
		hEntry.set_size_request(width, height)
		hFixed.put(hEntry, posX, poxY)
		return hEntry

	def Num(self, numTup, hFixed, posX, poxY, width, partDigits=0, height=None, fontDesc=None):
		if not height:
			height=self.Height
		numInit, numMin, numMax, numStep = numTup
		hAdj =  gtk.Adjustment(value=numInit, lower=numMin, upper=numMax, step_incr=numStep,
			page_incr=0, page_size=0)
		hSpin = gtk.SpinButton(hAdj, 0, partDigits)
		hSpin.set_numeric(True)
		if self.BGcolorEntry:
			hSpin.modify_base(gtk.STATE_NORMAL, self.BGcolorEntry)
		if self.FGcolor:
			hSpin.modify_text(gtk.STATE_NORMAL, self.FGcolor)
		if fontDesc:
			hSpin.modify_font(fontDesc)
		hSpin.set_size_request(width, height)
		hSpin.set_update_policy(gtk.UPDATE_IF_VALID)
		hFixed.put(hSpin, posX, poxY)
		return hSpin

	def apwTreeTxtColumn(self, txtLabel, colWidth, nCol, lsRendProp):
		crtxt = gtk.CellRendererText()
		crtxt.set_property('font-desc', self.fontDesc)
		if self.FGcolor:
			crtxt.set_property('foreground-gdk', self.FGcolor)
		for Prop in lsRendProp:
			crtxt.set_property(Prop[0], Prop[1])
		ttcLabel = gtk.Label(txtLabel)
		ttcLabel.show()
		ttcLabel.modify_font(self.fontDesc)
		tvc = gtk.TreeViewColumn()
		tvc.set_alignment(0.5)
		if colWidth:
			tvc.set_min_width(colWidth)
			tvc.set_max_width(colWidth)
		tvc.set_widget(ttcLabel)
		tvc.pack_start(crtxt, False)
		tvc.set_attributes(crtxt, text=nCol)
		return tvc, crtxt

	def TreeTxtColumn(self, txtLabel, colWidth, nCol, lsRendProp, fontDesc=None, tooltip=None):
		if txtLabel and not fontDesc:
			tvc = gtk.TreeViewColumn(txtLabel)
		else:
			tvc = gtk.TreeViewColumn()
		tvc.set_alignment(0.5) # Headers Center
		if colWidth:
			tvc.set_min_width(colWidth)
			tvc.set_max_width(colWidth)
		if fontDesc:
			ttcLabel = self.npLabel(txtLabel, fontDesc=fontDesc)
			tvc.set_widget(ttcLabel)
		if tooltip:
			pass
			#tvc.get_widget().get_parent().props.tooltip_text = tooltip
		lscrtxt = []
		for n in nCol:
			crtxt = gtk.CellRendererText()
			if fontDesc:
				crtxt.set_property('font-desc', fontDesc)
			if self.FGcolor:
				crtxt.set_property('foreground-gdk', self.FGcolor)
			for Prop in lsRendProp:
				crtxt.set_property(Prop[0], Prop[1])
			#if n == nCol[-1]:
				#tvc.pack_end(crtxt, True)
			#else:
				#tvc.pack_start(crtxt, True)
			tvc.pack_start(crtxt, True)
			tvc.set_attributes(crtxt, text=n)
			lscrtxt.append(crtxt)
		return tvc, lscrtxt

	def TreeCheckColumn(self, txtLabel, colWidth, nCol, lsRendProp, fontDesc=None, tooltip=None):
		if txtLabel and not fontDesc:
			tvc = gtk.TreeViewColumn(txtLabel)
		else:
			tvc = gtk.TreeViewColumn()
		tvc.set_alignment(0.5) # Headers Center
		if colWidth:
			tvc.set_min_width(colWidth)
			tvc.set_max_width(colWidth)
		if fontDesc:
			ttcLabel = self.npLabel(txtLabel, fontDesc=fontDesc)
			tvc.set_widget(ttcLabel)
		cellRendr = gtk.CellRendererToggle()
		for Prop in lsRendProp:
			cellRendr.set_property(Prop[0], Prop[1])
		tvc.pack_start(cellRendr, True)
		tvc.set_attributes(cellRendr, active=nCol)
		return tvc, cellRendr

	def TreeColors(self, treeView):
		if hasattr(self, 'BGcolorTreeView') and(isinstance(self.BGcolorTreeView, gtk.gdk.Color)):
			treeView.modify_base(gtk.STATE_NORMAL, self.BGcolorTreeView)
		for state in (gtk.STATE_SELECTED, gtk.STATE_ACTIVE):
			if hasattr(self, 'BGcolorSel') and(isinstance(self.BGcolorSel, gtk.gdk.Color)):
				for call in (treeView.modify_base, treeView.modify_bg):
					call(state, self.BGcolorSel)
			if hasattr(self, 'FGcolorSel') and(isinstance(self.FGcolorSel, gtk.gdk.Color)):
				for call in (treeView.modify_text, treeView.modify_fg):
					call(state, self.FGcolorSel)

	def TreeColumn(self, txtLabel, colWidth, tCol, dcRendProp, fontDesc=None):
		if txtLabel and not fontDesc:
			tvc = gtk.TreeViewColumn(txtLabel)
		else:
			tvc = gtk.TreeViewColumn()
		tvc.set_alignment(0.5) # Headers Center
		if colWidth:
			tvc.set_min_width(colWidth)
			tvc.set_max_width(colWidth)
		if fontDesc:
			ttcLabel = self.npLabel(txtLabel, fontDesc=fontDesc)
			tvc.set_widget(ttcLabel)
		lsCR = []
		for n in tCol:
			if n[0]=='txt':
				cellRendr = gtk.CellRendererText()
				if fontDesc:
					cellRendr.set_property('font-desc', fontDesc)
				if self.FGcolor:
					cellRendr.set_property('foreground-gdk', self.FGcolor)
				if dcRendProp.has_key('txt'):
					for Prop in dcRendProp['txt']:
						cellRendr.set_property(Prop[0], Prop[1])
				tvc.pack_start(cellRendr, True)
				if n[1]!=None:
					if callable(n[1]):
						if len(n)>2:
							tvc.set_cell_data_func(cellRendr, n[1], n[2:])
					elif type(n[1])==int:
						tvc.set_attributes(cellRendr, text=n[1])
				lsCR.append(cellRendr)
			elif n[0]=='pix':
				cellRendr = gtk.CellRendererPixbuf()
				if dcRendProp.has_key('pix'):
					for Prop in dcRendProp['pix']:
						cellRendr.set_property(Prop[0], Prop[1])
				tvc.pack_start(cellRendr, True)
				if n[1]!=None:
					if callable(n[1]):
						if len(n)>2:
							tvc.set_cell_data_func(cellRendr, *n[1:])
						else:
							tvc.set_cell_data_func(cellRendr, n[1])
					elif type(n[1])==int:
						tvc.set_attributes(cellRendr, pixbuf=n[1])
				lsCR.append(cellRendr)
			elif n[0]=='togg':
				cellRendr = gtk.CellRendererToggle()
				if dcRendProp.has_key('togg'):
					for Prop in dcRendProp['togg']:
						cellRendr.set_property(Prop[0], Prop[1])
				tvc.pack_start(cellRendr, True)
				tvc.set_attributes(cellRendr, active=n[1])
				lsCR.append(cellRendr)
			elif n[0]=='combo':
				cellRendr = gtk.CellRendererCombo()
				if dcRendProp.has_key('combo'):
					for Prop in dcRendProp['combo']:
						cellRendr.set_property(Prop[0], Prop[1])
				tvc.pack_start(cellRendr, True)
				if n[1]!=None:
					tvc.set_attributes(cellRendr, text=n[1], model=n[2])
				if len(n)>3:
					tvc.set_attributes(cellRendr, editable=n[3])
				lsCR.append(cellRendr)
		return tvc, lsCR

	def dbgDir(self, _class):
		print("Class: %s" % _class.__str__())
		for atrib in dir(_class):
			c_atrib = getattr(_class, atrib)
			if callable(c_atrib):
				print("\tMethod: %s()" % atrib)
			elif atrib=='props':
				print("\tProperities[%i]: %s" % (len(c_atrib), str(c_atrib)))
				#for _prop in dir(c_atrib):
				for _prop in _class.props:
					print("\t\tproperity: %s:%s" % (str(_prop), str(_class.get_property(_prop.name))))
			else:
				print("\tattr: %s" % atrib)

	def TreeTogg(self, cell_rend, path, tree, col):
		model = tree.get_model()
		_iter = model.get_iter(path)
		model.set_value(_iter, col, not(model.get_value(_iter, col)))
		_sel = tree.get_selection()
		mode = _sel.get_mode()
		_sel.set_mode(gtk.SELECTION_NONE)
		_sel.set_mode(mode)
		print("path: %s(%s)" % (path, str(type(path))))
		#self.dbgDir(model)

	def skipSelection(self, cellrenderer, hEntry, path, tvSel):
		#print(cellrenderer, hEntry, path)
		if hasattr(self, 'descFontTvEntry'):
			hEntry.modify_font(self.descFontTvEntry)
		mode=tvSel.get_mode()
		tvSel.set_mode(gtk.SELECTION_NONE)
		tvSel.set_mode(mode)
		return

	def dialogChooseFile(self, parent=None, startDir=None, startFile=None, title='Select a file...', act='file_open', bShowHidden=False):
		action = {
			'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
			'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
			'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
			}[act]
		hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
		hDialog.modify_bg(gtk.STATE_NORMAL, self.BGcolor)
		hDialog.set_default_response(gtk.RESPONSE_OK)
		hDialog.set_show_hidden(bShowHidden)
		#print("bShowHidden:%s\n\tReaded ShowHidden:%s"% (bShowHidden, str(hDialog.get_show_hidden())))
		if startDir:
			hDialog.set_current_folder(startDir)
		if startFile:
			if act=='file_save':
				hDialog.set_current_name(startFile)
			elif act=='file_open':
				hDialog.set_filename(startFile)
		respFileName = hDialog.run()
		#print("Readed ShowHidden:%s\nProp ShowHidden:%s" %
			#(str(hDialog.get_show_hidden()), str(hDialog.props.show_hidden)))
		fileName = None
		if respFileName==gtk.RESPONSE_OK:
			fileName = hDialog.get_filename()
		hDialog.destroy()
		return fileName

	def TextView(self, hFixed, posX, poxY, width, height, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
		hTextView = EasyTextView()
		hTextView.set_property("editable", bEditable)
		if self.BGcolorEntry:
			hTextView.modify_base(gtk.STATE_NORMAL, self.BGcolorEntry)
		if self.FGcolor:
			hTextView.modify_text(gtk.STATE_NORMAL, self.FGcolor)
		if fontDesc:
			hTextView.modify_font(fontDesc)
		if bWrap:
			hTextView.set_wrap_mode(gtk.WRAP_WORD)
		hTextView.setTabSpace(tabSpace, fontDesc=fontDesc)
		scrollViewTxt = gtk.ScrolledWindow()
		vadj = scrollViewTxt.get_vadjustment()
		vadj.connect('changed', hTextView.reScrollV, scrollViewTxt)

		scrollViewTxt.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollViewTxt.add(hTextView)
		scrollViewTxt.set_size_request(width, height)
		hFixed.put(scrollViewTxt, posX, poxY)
		return hTextView

	def setFrameFont(self, frame, fontDesc):
		for widget in frame.children():
			if isinstance(widget, gtk.Button):
				widget.child.modify_font(fontDesc)
			elif isinstance(widget, gtk.Frame):
				widget.get_label_widget().child.modify_font(fontDesc)
			elif isinstance(widget, gtk.CellLayout):
				for cell in widget.get_cells():
					if isinstance(cell, gtk.CellRendererText):
						cell.set_property('font-desc', fontDesc)
				if isinstance(widget, gtk.TreeViewColumn):
					ttcLabel = widget.get_widget()
					if ttcLabel:
						ttcLabel.modify_font(fontDesc)
			elif isinstance(widget, gtk.ScrolledWindow):
				self.setFrameFont(widget, fontDesc)

			else:
				widget.modify_font(fontDesc)

class EasyTextView(gtk.TextView):
	def __init__(self):
		super(EasyTextView, self).__init__()

	def clear_text(self):
		self.get_buffer().set_text('')

	def get_text(self):
		tBuff = self.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())

	def insert_end(self, txt, tag=None):
		buff = self.get_buffer()
		end = buff.get_end_iter()
		if tag:
			buff.insert_with_tags(end, txt, tag)
		else:
			buff.insert(end, txt)
		del(end)

	def reScrollV(self, adjV, scrollV):
		"""Scroll to the bottom of the TextView when the adjustment changes."""
		adjV.set_value(adjV.upper - adjV.page_size)
		scrollV.set_vadjustment(adjV)
		return

	def setTabSpace(self, spaces, fontDesc=None):
		pangoTabSpc = self.getTabPixelWidth(spaces, fontDesc=fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		self.set_tabs(tabArray)
		return pangoTabSpc

	def getTabPixelWidth(self, spaces, fontDesc=None):
		txtTab = ' ' * spaces
		#pangoContext = self.get_pango_context()
		pangoLayout = self.create_pango_layout(txtTab)
		#print("WTF is Font? \"%s\"" % pangoLayout.get_font_description())
		if fontDesc:
			pangoLayout.set_font_description(fontDesc)
		pangoTabSpc = pangoLayout.get_pixel_size()[0]
		del(pangoLayout)
		return pangoTabSpc
