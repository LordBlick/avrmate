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

class clCfgAVR:
	def __init__(self):
		self.selSUT=''
		self.bDefaultLock=False
		self.argsAVRdude = []
		self.reHex=re.compile('(0x)([0-9A-F]{1,2})$', re.I | re.L)
		self.reBin=re.compile('(0b)([01]{1,8})$', re.I | re.L)
		self.reDec=re.compile('([0-9]{1,3})$', re.L)
		self.devParam = avrList.devParam()
		self.uiInit()
		gtk.main()

	def uiInit(self):
		from uiMain import uiCfgAVR
		self.ui = uiCfgAVR()
		self.ui.title="AVRmate - Fusebits Calculator V.0.51"
		self.ui.uiInit()

		self.ui.mainWindow.connect("destroy", lambda w: gtk.main_quit())
		self.ui.mainWindow.connect("delete_event", gtk.main_quit)
		self.ui.cbUcSelect.connect("changed", self.ucChanged)
		self.chooseInit()
		self.ui.cbPgmSelect.connect("changed", self.pgmChanged)
		
		for pgmName in self.devParam.lsProgrammers:
			self.ui.lsPgmSelect.append(pgmName)
		self.ui.cbPgmSelect.set_active(0)

		self.ui.checkClk.connect("toggled", self.avrErTog)
		self.ui.checkErase.connect("toggled", self.avrErTog)
		### Begin of Tree Store ###
		self.ui.crtcbBitsValue.connect('changed', self.cbBitsChanged)
		self.ui.crtcbBitsValue.connect('editing_started', self.callSkipSelection)

		self.ui.crtxtBitsValue.connect("edited", self.byteEdited)
		self.ui.crtxtBitsValue.connect('editing_started', self.callSkipSelection)
		#self.ui.crtxtBitsValue.connect('editing_canceled', self.callSkipSelection, "Canceled", None)
		### End of Tree Store ###

		self.ui.textAvrdudeCmd.connect("icon-release", self.avrdudeIcGo)
		self.ui.textAvrdudeCmd.connect("activate", self.avrdudeGo)

		self.ui.buttonPng.connect("clicked", self.winShoot)
		self.ui.buttonTest.connect("clicked", self.treeTest)
		self.ui.buttonExit.connect("clicked", self.appExit)
		return

	def chooseInit(self):
		self.ucList=self.devParam.devParams()
		self.lnUcList=len(self.ucList)
		for ucIndex in range(self.lnUcList):
			self.ui.lsUcSelect.append([self.ucList[ucIndex]])
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
		self.avrData=self.devParam.getAVR(indexAVR)
		self.avrBits=self.devParam.avrCfgBits
		self.tvBitsIter=[]
		self.ui.tsBits.clear()
		byteFuses=sorted(self.avrData['Fuses'].keys())
		for byteFuse in byteFuses:
			locIter=[]
			locIter.append( self.ui.tsBits.append(None,
					[self.ui.fsBPixbuf,
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
				locIter.append(self.ui.tsBits.append(locIter[0],
					[self.ui.fsbPixbuf,
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
		locIter.append( self.ui.tsBits.append(None,
				[self.ui.lBPixbuf, 'LockByte',
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
			locIter.append(self.ui.tsBits.append(locIter[0],
				[self.ui.lbPixbuf,
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
		AvrdudeCmd=self.ui.textAvrdudeCmd.get_text()
		if AvrdudeCmd:
			avrdudeTargets=subprocess.Popen(
				shlex.split(AvrdudeCmd),
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT)
				#stderr=subprocess.PIPE)
			child_stdout, child_stderr = avrdudeTargets.communicate()
			if child_stderr:
				self.errBox(message=child_stderr)
			if child_stdout:
				self.infoBox(message=child_stdout)
		return

	def avrdudeListuC(self):
		return

	def avrdudeIcGo(self, widget, icoPos, sigEvent):
		self.avrdudeGo(widget)
		return

	def callSkipSelection(self, cellrenderer, editable, path):
		#print(cellrenderer, editable, path)
		self.treeUnselect()
		return

	def cbBitsChanged(self, comboCellRenderer, cell_path, select_iter):
		bitIter = self.ui.tsBits.get_iter(cell_path)
		lSt=self.ui.tsBits.get_value(bitIter, 5) # Get ListStore saved at 5 collumn
		self.ui.tsBits.set(bitIter, 3, lSt.get_value(select_iter, 0), 4, lSt.get_value(select_iter, 1))
		self.byteUpdate(int(cell_path[0:1]))
		#self.treeUnselect()
		self.avrDudeUp()

	def byteEdited(self, cellRendererText, cell_path, newText):
		reHexTxt=self.reHex.match(newText)
		reBinTxt=self.reBin.match(newText)
		byteIt = self.ui.tsBits.get_iter(cell_path)
		if reHexTxt:
			byteVal=int(reHexTxt.group(2).upper(), 16)
		elif reBinTxt:
			byteVal=int(reBinTxt.group(2), 2)
		elif self.reDec.match(newText):
			byteVal=int(newText, 10)
		else:
			byteVal=0x100
		if byteVal in range(0x100):
			self.ui.tsBits.set(byteIt, 3,'0b{:08b}'.format(byteVal), 4, '0x{:02X}'.format(byteVal))
		self.bitsUpdate(int(cell_path[0:1]))
		self.treeUnselect()
		self.avrDudeUp()
		return

	def pgmChanged(self, widget):
		viewModel = widget.get_model()
		index = widget.get_active()
		if index > -1:
			self.avdPgm=viewModel[index][1]
			self.avdPgmPort=viewModel[index][2]
			self.avrDudeUp()
		return

	def ucChanged(self, widget):
		viewModel = widget.get_model()
		index = widget.get_active()
		if index > -1:
			self.ui.tvBits.freeze_child_notify()
			modelBits=self.ui.tvBits.get_model()
			self.ui.tvBits.set_model(None)

			# Add rows to the viewModel
			# ...
			self.treeFill(index)

			self.ui.tvBits.set_model(modelBits)
			self.ui.tvBits.thaw_child_notify()
			self.ui.tvBits.expand_all()
			self.bDefaultLock=True

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
			bitName=self.ui.tsBits.get_value(bitIt, 8)
			bitVal=self.ui.tsBits.get_value(bitIt, 4)
			if bitName=='SUT_SEL':
				bitName=self.selSUT
				bitDesc=self.avrBits[bitName]['Desc']
				bitModel=self.bitListView(bitName)
				self.ui.tsBits.set(bitIt, 2, bitDesc, 5, bitModel)
				if not(bitVal in self.avrBits[bitName]['Config'][1].keys()):
					bitVal=self.defaultBit(bitName)[0]
					self.ui.tsBits.set_value(bitIt, 4, bitVal)
				self.ui.tsBits.set_value(bitIt, 3, self.avrBits[bitName]['Config'][1][bitVal])
			if bitName[0:6]=='CKSEL4':
				if 'SUT_SEL' in self.avrBits[bitName]:
					self.selSUT=self.avrBits[bitName]['SUT_SEL'][bitVal]
				else:
					self.selSUT=''
			binByteTxt="%s%s" % (bitVal, binByteTxt)
		byteVal=int(binByteTxt, 2)
		self.ui.tsBits.set(byteIt, 3,'0b{:08b}'.format(byteVal), 4, '0x{:02X}'.format(byteVal))
		byteName=self.ui.tsBits.get_value(byteIt, 8)
		if byteName=='Lock' and self.bDefaultLock==True:
			self.defaultLock='0x{:02X}'.format(byteVal)
			self.bDefaultLock=False
		return


	def bitsUpdate(self, selectNo):
		bDefaultSet=False
		byteIt=self.tvBitsIter[selectNo][0]
		bitCfgs=len(self.tvBitsIter[selectNo])-1
		binByteTxt=self.ui.tsBits.get_value(byteIt, 3)[2:10]
		bitPtr=8
		for n in range(bitCfgs):
			bitIt=self.tvBitsIter[selectNo][n+1]
			bitName=self.ui.tsBits.get_value(bitIt, 8)
			if bitName=='SUT_SEL':
				bitName=self.selSUT
				bitDesc=self.avrBits[bitName]['Desc']
				bitModel=self.bitListView(bitName)
				self.ui.tsBits.set(bitIt, 2, bitDesc, 5, bitModel)
			widthConfig=self.avrBits[bitName]['Config'][0]
			bitPtrB=bitPtr-widthConfig
			bitVal=binByteTxt[bitPtrB:bitPtr]
			if bitName.startswith('CKSEL4'):
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
			self.ui.tsBits.set(bitIt, 3, setupTxt, 4, bitVal)
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
			}[self.ui.checkClk.get_active()]
			updateText+={
				True:' -e',
				False:''
			}[self.ui.checkErase.get_active()]
			for byteCfg in range(len(self.tvBitsIter)):
				byteIt=self.tvBitsIter[byteCfg][0]
				byteNm=self.devParam.avdCfgByte(self.ui.tsBits.get_value(byteIt, 8))
				byteVal=self.ui.tsBits.get_value(byteIt, 4)
				if byteNm=='lock' and byteVal!=self.defaultLock or byteNm!='lock':
					updateText+=' -U %s:w:%s:m' % (byteNm, byteVal)
			setText="avrdude -c %s -P %s -p %s%s" % (self.avdPgm, self.avdPgmPort, self.devParam.avdName(self.avrData['Name']), updateText)
			self.ui.textAvrdudeCmd.set_text(setText)
		except AttributeError:
			pass
		return

	def treeUnselect(self):
		mode=self.ui.tvBitsSelection.get_mode()
		self.ui.tvBitsSelection.set_mode(gtk.SELECTION_NONE)
		self.ui.tvBitsSelection.set_mode(mode)
		return

	def avrErTog(self, widget):
		self.avrDudeUp()
		return

	def treeTest(self, widget):
		return
		

	def appExit(self, widget):
		self.devParam.empty()
		gtk.main_quit()

	def winShoot(self, widget):
		screen = gtk.gdk.screen_get_default()
		gdk_win =screen.get_active_window()
		posX, posY, width, height  = gdk_win.get_frame_extents()
		pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, width, height)
		# Retrieve the pixel data from the gdk.window attribute (self.ui.mainWindow.window)
		# of the gtk.window object
		#screenshot = pixbuf.get_from_drawable(
			#self.ui.mainWindow.window,
			#self.ui.mainWindow.get_colormap(),
			#0, 0, 0, 0, width, height)
		
		screenshot = pixbuf.get_from_drawable(
			gtk.gdk.get_default_root_window(),
			gtk.gdk.colormap_get_system(),
			posX, posY, 0, 0, width, height)
		
		#gtk.FileChooser
		screenshot.save('screenshot.png', 'png')
		del screenshot
		gc.collect()
		return

	def infoBox(self, message="Known Comes...!", caption = 'Information...'):
		dlg = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format=None)
		dlg.set_markup(message)
		dlg.set_title(caption)
		dlg.run()
		dlg.destroy()

	def errBox(self, message="Unknown Comes...!", caption = 'Error!'):
		dlg = gtk.MessageDialog(parent=None, flags=gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=None)
		dlg.set_markup(message)
		dlg.set_title(caption)
		dlg.run()
		dlg.destroy()



if __name__ == "__main__":
	configAVR = clCfgAVR()
