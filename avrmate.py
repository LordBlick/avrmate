#!/usr/bin/env python
# -*- coding: utf-8 -*-



import pygtk
pygtk.require('2.0')
import gtk, gobject
import pango
import re
import shlex, subprocess
import avrList

class FuseAVR:
	def __init__(self):
		self.selSUT=''
		self.argsAVRdude = []
		self.reHex=re.compile('(0x)([0-9A-F]{1,2})$', re.I | re.L)
		self.reBin=re.compile('(0b)([01]{1,8})$', re.I | re.L)
		self.reDec=re.compile('([0-9]{1,3})$', re.L)
		self.uiInit()
		gtk.main()

	def uiInit(self):
		self.cfBPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Configbyte.png")
		self.fsBPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Fusebyte.png")
		self.fsbPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Fusebit.png")
		self.lBPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Lockbyte.png")
		self.lbPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Lockbit.png")
		self.lghtPixbuf = gtk.gdk.pixbuf_new_from_file("pic/Lightenings.png")
		#self.fsBSmallPixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 32, 32)
		#self.fsBPixbuf.scale(self.fsBSmallPixbuf, 0, 0, 40, 10, 0, 0, 0.2, 0.2, gtk.gdk.INTERP_HYPER)
		#self.fsBSmallPixbuf=self.fsBPixbuf.scale_simple(50, 10, gtk.gdk.INTERP_HYPER)
		
		gtk.window_set_default_icon_list(self.fsBPixbuf, self.lghtPixbuf)
		
		self.title="Kalkulator Fusebitów AVR"
		
		self.dialogWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.dialogWindow.set_geometry_hints(
			min_width=640, min_height=750, max_width=640, max_height=750)
		self.dialogWindow.set_title(self.title)
		self.dialogWindow.set_border_width(5)
		self.dialogWindow.connect("destroy", lambda w: gtk.main_quit())
		self.dialogWindow.connect("delete_event", gtk.main_quit)
		
		self.fixedFrame = gtk.Fixed()
		
		self.labelUcSelect = gtk.Label("µC :")
		self.labelUcSelect.set_size_request(20, 30)
		
		self.fixedFrame.put(self.labelUcSelect, 10, 5)
		
		self.cbUcSelect = gtk.ComboBox()
		self.cbUcSelect.set_size_request(110, 30)
		self.lsUcSelect = gtk.ListStore(str)
		self.crtUcSelect = gtk.CellRendererText()
		self.cbUcSelect.pack_start(self.crtUcSelect)
		self.cbUcSelect.set_attributes(self.crtUcSelect, text=0)
		self.cbUcSelect.set_wrap_width(3)
		self.cbUcSelect.set_model(self.lsUcSelect)
		self.cbUcSelect.connect("changed", self.ucChanged)
		
		self.fixedFrame.put(self.cbUcSelect, 40, 5)
		self.chooseInit()

		self.labelPgmSelect = gtk.Label("Programmer:")
		self.labelPgmSelect.set_size_request(65, 30)
		
		self.fixedFrame.put(self.labelPgmSelect, 160, 5)
		
		self.cbPgmSelect = gtk.ComboBox()
		self.cbPgmSelect.set_size_request(140, 30)
		self.lsPgmSelect = gtk.ListStore(str, str, str)
		self.crtPgmSelect = gtk.CellRendererText()
		self.cbPgmSelect.pack_start(self.crtPgmSelect)
		self.cbPgmSelect.set_attributes(self.crtPgmSelect, text=0)
		self.cbPgmSelect.set_wrap_width(3)
		self.cbPgmSelect.set_model(self.lsPgmSelect)
		self.cbPgmSelect.connect("changed", self.pgmChanged)
		
		self.fixedFrame.put(self.cbPgmSelect, 230, 5)
		for pgmName in (
		('USBasp', 'usbasp', '/dev/usbasp'),
		('AVR Dragon ISP', 'dragon_isp', 'usb'),
		('AVR Dragon PP', 'dragon_pp', 'usb'),
		('Amountec JTAG Key', 'jtagkey', 'usb')):
			self.lsPgmSelect.append(pgmName)
		self.cbPgmSelect.set_active(0)

		self.checkClk = gtk.CheckButton("Slower Clock")
		self.checkClk.set_size_request(100, 30)
		self.checkClk.connect("toggled", self.avrErTog)
		
		self.fixedFrame.put(self.checkClk, 420, 5)

		self.checkErase = gtk.CheckButton("Chip Erase")
		self.checkErase.set_size_request(100, 30)
		self.checkErase.connect("toggled", self.avrErTog)
		
		self.fixedFrame.put(self.checkErase, 530, 5)

		
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
		self.crtcbBitsValue.connect('changed', self.cbBitsChanged)
		
		self.tvcBitsValue = gtk.TreeViewColumn('Setup Value', self.crtcbBitsValue, text=3, model=5, editable=6)
		self.tvcBitsValue.set_alignment(0.5)
		
		self.crtxtBitsValue = gtk.CellRendererText()
		self.crtxtBitsValue.set_property('cell-background-gdk', gtk.gdk.Color('#085'))
		self.crtxtBitsValue.set_property('size-points', self.tvBitsFontSize)
		self.crtxtBitsValue.set_property('xalign', 0.95)
		self.crtxtBitsValue.connect("edited", self.byteEdited)
		
		self.tvcBitsValue.pack_start(self.crtxtBitsValue, True)
		self.tvcBitsValue.set_attributes(self.crtxtBitsValue, text=4, editable=7)
		
		self.tvBits.append_column(self.tvcBitsValue)
		
		self.tvBits.set_tooltip_column(2, )
		#self.tvBits.set_tooltip_column(8, )
		self.tvBits.set_enable_tree_lines(True)

		self.scroll=gtk.ScrolledWindow()
		self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scroll.add(self.tvBits)
		self.scroll.set_size_request(605, 610)
		self.fixedFrame.put(self.scroll, 10, 40)
## ## ## ## ## ## ##

		self.textAvrdudeCmd = gtk.Entry()
		self.textAvrdudeCmd.set_property("editable", False)
		self.textAvrdudeCmd.set_icon_from_pixbuf(0, self.lghtPixbuf)
		self.textAvrdudeCmd.set_icon_tooltip_text(0, 'Click here or pres enter in right text to start avrdude')
		self.textAvrdudeCmd.connect("icon-release", self.avrdudeIcGo)
		self.textAvrdudeCmd.connect("activate", self.avrdudeGo)
		self.textAvrdudeCmd.set_size_request(605, 30)
		
		self.fixedFrame.put(self.textAvrdudeCmd, 10, 660)
		
		self.imageLogo = gtk.Image()
		self.imageLogo.set_from_pixbuf(self.cfBPixbuf)
		
		self.fixedFrame.put(self.imageLogo, 10, 700)
		
		self.buttonTest = gtk.Button("Test")
		self.buttonTest.set_size_request(50, 25)
		self.buttonTest.connect("clicked", self.treeTest)
		
		self.fixedFrame.put(self.buttonTest, 480, 715)

		accGroup = gtk.AccelGroup()
		self.dialogWindow.add_accel_group(accGroup)

		self.buttonExit = gtk.Button("Exit (Ctrl+Q)")
		self.buttonExit.set_size_request(80, 25)
		self.buttonExit.connect("clicked", self.quit_cb)

		self.buttonExit.add_accelerator(
			"clicked",
			accGroup,
			ord('Q'),
			gtk.gdk.CONTROL_MASK,
			gtk.ACCEL_VISIBLE)
		
		self.fixedFrame.put(self.buttonExit, 540, 715)
		
		self.dialogWindow.add(self.fixedFrame)
		self.dialogWindow.show_all()
		self.dialogWindow.set_keep_above(True)
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

	def defaultBit(self, bitName):
		widthConfig=self.avrBits[bitName]['Config'][0]
		if 'Default' in self.avrBits[bitName]:
			defaultConfig=self.avrBits[bitName]['Default']
		elif len(self.avrBits[bitName]['Config'][1]) ==1:
			defaultConfig=self.avrBits[bitName]['Config'][1].keys()[0]
			#print "Juppiiii.....!!!\n\t default:%s" % defaultConfig
		else:
			defaultConfig=''
			for n in range(widthConfig):
				defaultConfig+='1'
		if defaultConfig in self.avrBits[bitName]['Config'][1]:
			defaultVal=self.avrBits[bitName]['Config'][1][defaultConfig]
		else:
			defaultVal="Unknown"
		return (defaultConfig, defaultVal)

	def bitListView(self, bitName):
		setList=sorted(self.avrBits[bitName]['Config'][1].keys())
		lsmodel = gtk.ListStore(str, str)
		for item in setList:
			lsmodel.append([ self.avrBits[bitName]['Config'][1][item], item ])
		return lsmodel

	def treeFill(self, indexAVR):
		self.avrData=self.ucClList.getAVR(indexAVR)
		self.avrBits=self.ucClList.bitsAVR
		self.tvBitsIter=[]
		self.tsBits.clear()
		byteFuses=sorted(self.avrData['Fuses'].keys())
		for byteFuse in byteFuses:
			locIter=[]
			locIter.append( self.tsBits.append(None,
					[self.fsBPixbuf,
					'FuseByte%s' % (byteFuse),
					'%s FuseByte' % (byteFuse),
				'',
				'',
				None,
				False,
				True,
				byteFuse]
				))
			for bitFuse in self.avrData['Fuses'][byteFuse]:
				bitSelName=bitFuse
				if bitFuse=='SUT_SEL':
					bitFuse=self.selSUT
				if 'NameShow' in self.avrBits[bitFuse]:
					bitShowName=self.avrBits[bitFuse]['NameShow']
				else:
					bitShowName=bitFuse
				defaultFuse=self.defaultBit(bitFuse)
				modelFuse=self.bitListView(bitFuse)
				if bitFuse[0:6]=='CKSEL4':
					if 'SUT_SEL' in self.avrBits[bitFuse]:
						self.selSUT=self.avrBits[bitFuse]['SUT_SEL'][defaultFuse[0]]
					else:
						self.selSUT=''
				locIter.append(self.tsBits.append(locIter[0],
					[self.fsbPixbuf,
					'%s' % (bitShowName),
					self.avrBits[bitFuse]['Desc'],
					defaultFuse[1],
					defaultFuse[0],
				modelFuse,
				True,
				False,
				bitSelName]
				))
				
			self.tvBitsIter.append(locIter)
		locIter=[]
		locIter.append( self.tsBits.append(None,
				[self.lBPixbuf, 'LockByte',
				'Lock Byte',
				'',
				'',
				None,
				False,
				True,
				'Lock']
				))
		for bitLock in self.avrData['Lock']:
			defaultLock=self.defaultBit(bitLock)
			modelLock=self.bitListView(bitLock)
			locIter.append(self.tsBits.append(locIter[0],
				[self.lbPixbuf,
				'%s' % (bitLock),
				self.avrBits[bitLock]['Desc'],
				defaultLock[1],
				defaultLock[0],
				modelLock,
				True,
				False,
				bitLock]
			))
		self.tvBitsIter.append(locIter)
		
		return

	def avrdudeGo(self, widget):
		#avrdudeTargets=subprocess.Popen(
			#shlex.split('avrdude -p?'),
			#stdout=subprocess.PIPE,
			#stderr=subprocess.PIPE)
		#child_stdout, child_stderr = avrdudeTargets.communicate()
		#for lineErr in child_stderr.splitlines():
			#findEqu=lineErr.find(' = ')
			#if findEqu!=-1:
				#findE=lineErr.find(' [', findEqu+3)
				#uC=self.ucClList.nameFromAVD(lineErr[0:findEqu].strip())
				#uC2=lineErr[findEqu+3:findE].strip()
				#if uC!=-1:
					#print "Is really \"%s\" match \"%s\" ?" % (uC, uC2)
		#print "stdout:\n%s\nstderr:\n%s" % (child_stdout, child_stderr)

		return

	def avrdudeIcGo(self, widget, icoPos, sigEvent):
		self.avrdudeGo(widget)
		return

	def cbBitsChanged(self, comboCellRenderer, cell_path, select_iter):
		bitIter = self.tsBits.get_iter(cell_path)
		lSt=self.tsBits.get_value(bitIter, 5) # Get ListStore saved at 5 collumn
		self.tsBits.set(bitIter, 3, lSt.get_value(select_iter, 0), 4, lSt.get_value(select_iter, 1))
		self.byteUpdate(int(cell_path[0:1]))
		self.avrDudeUp()

	def byteEdited(self, cellRendererText, cell_path, newText):
		reHexTxt=self.reHex.match(newText)
		reBinTxt=self.reBin.match(newText)
		byteIt = self.tsBits.get_iter(cell_path)
		if reHexTxt:
			byteVal=int(reHexTxt.group(2).upper(), 16)
		elif reBinTxt:
			byteVal=int(reBinTxt.group(2), 2)
		elif self.reDec.match(newText):
			byteVal=int(newText, 10)
		else:
			byteVal=0x100
		if byteVal in range(0x100):
			self.tsBits.set(byteIt, 3,'0b{:08b}'.format(byteVal), 4, '0x{:02X}'.format(byteVal))
		self.bitsUpdate(int(cell_path[0:1]))
		self.avrDudeUp()
		return

	def pgmChanged(self, widget):
		viewModel = widget.get_model()
		index = widget.get_active()
		if index > -1:
			self.avdPgm=viewModel[index][1]
			self.avrDudeUp()
		return

	def ucChanged(self, widget):
		viewModel = widget.get_model()
		index = widget.get_active()
		if index > -1:
			self.tvBits.freeze_child_notify()
			modelBits=self.tvBits.get_model()
			self.tvBits.set_model(None)

			# Add rows to the viewModel
			# ...
			self.treeFill(index)

			self.tvBits.set_model(modelBits)
			self.tvBits.thaw_child_notify()
			self.tvBits.expand_all()

		for n in range(len(self.tvBitsIter)):
			self.byteUpdate(n)
		self.avrDudeUp()
		return

	def byteUpdate(self, selectNo):
		byteIt=self.tvBitsIter[selectNo][0]
		bitCfgs=len(self.tvBitsIter[selectNo])-1
		binByteTxt=''
		for n in range(bitCfgs):
			bitIt=self.tvBitsIter[selectNo][n+1]
			bitName=self.tsBits.get_value(bitIt, 8)
			bitVal=self.tsBits.get_value(bitIt, 4)
			if bitName=='SUT_SEL':
				bitName=self.selSUT
				bitDesc=self.avrBits[bitName]['Desc']
				bitModel=self.bitListView(bitName)
				self.tsBits.set(bitIt, 2, bitDesc, 5, bitModel)
				if not(bitVal in self.avrBits[bitName]['Config'][1].keys()):
					bitVal=self.defaultBit(bitName)[0]
					self.tsBits.set_value(bitIt, 4, bitVal)
				self.tsBits.set_value(bitIt, 3, self.avrBits[bitName]['Config'][1][bitVal])
			if bitName[0:6]=='CKSEL4':
				if 'SUT_SEL' in self.avrBits[bitName]:
					self.selSUT=self.avrBits[bitName]['SUT_SEL'][bitVal]
				else:
					self.selSUT=''
			binByteTxt="%s%s" % (bitVal, binByteTxt)
		byteVal=int(binByteTxt, 2)
		self.tsBits.set(byteIt, 3,'0b{:08b}'.format(byteVal), 4, '0x{:02X}'.format(byteVal))
		return


	def bitsUpdate(self, selectNo):
		bDefaultSet=False
		byteIt=self.tvBitsIter[selectNo][0]
		bitCfgs=len(self.tvBitsIter[selectNo])-1
		binByteTxt=self.tsBits.get_value(byteIt, 3)[2:10]
		bitPtr=8
		for n in range(bitCfgs):
			bitIt=self.tvBitsIter[selectNo][n+1]
			bitName=self.tsBits.get_value(bitIt, 8)
			if bitName=='SUT_SEL':
				bitName=self.selSUT
				bitDesc=self.avrBits[bitName]['Desc']
				bitModel=self.bitListView(bitName)
				self.tsBits.set(bitIt, 2, bitDesc, 5, bitModel)
			widthConfig=self.avrBits[bitName]['Config'][0]
			bitPtrB=bitPtr-widthConfig
			bitVal=binByteTxt[bitPtrB:bitPtr]
			if bitName[0:6]=='CKSEL4':
				if 'SUT_SEL' in self.avrBits[bitName]:
					self.selSUT=self.avrBits[bitName]['SUT_SEL'][bitVal]
				else:
					self.selSUT=''
			setList=sorted(self.avrBits[bitName]['Config'][1].keys())
			if bitVal in setList:
				setupTxt=self.avrBits[bitName]['Config'][1][bitVal]
			else:
				bitVal, setupTxt=self.defaultBit(bitName)
				bDefaultSet=True
			self.tsBits.set(bitIt, 3, setupTxt, 4, bitVal)
			bitPtr=bitPtrB
		if bitPtr>0:
			bDefaultSet=True
		if bDefaultSet:
			self.byteUpdate(selectNo)
		return

	def avrDudeUp(self):
		try:
			updateText={
				True:' -B 8',
				False:''
			}[self.checkClk.get_active()]
			updateText+={
				True:' -e',
				False:''
			}[self.checkErase.get_active()]
			for byteCfg in range(len(self.tvBitsIter)):
				byteIt=self.tvBitsIter[byteCfg][0]
				byteNm=self.ucClList.avdCfgByte(self.tsBits.get_value(byteIt, 8))
				byteVal=self.tsBits.get_value(byteIt, 4)
				updateText+=' -U %s:w:%s:m' % (byteNm, byteVal)
			setText="avrdude -c %s -p %s%s" % (self.avdPgm, self.ucClList.avdName(self.avrData['Name']), updateText)
			self.textAvrdudeCmd.set_text(setText)
		except AttributeError:
			pass
		return

	def avrErTog(self, widget):
		self.avrDudeUp()
		return

	def treeTest(self, widget):
		for n in range(len(self.tvBitsIter)):
			self.bitsUpdate(n)
		self.avrDudeUp()
		return

	def quit_cb(self, widget):
		self.ucClList.empty()
		gtk.main_quit()



if __name__ == "__main__":
	configAVR = FuseAVR()
