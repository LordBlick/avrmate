#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

okTxt="""No restrictions for SPM or LPM accessing the
%s section"""
spmTxt="SPM is not allowed to write to the %s section."
lpmTxt="""LPM  executing  from  the %s  section  is  not
allowed  to  read  from  the  %s  section.  If
Interrupt Vectors are placed in the %s section,
interrupts are disabled while executing from the
%s section"""
lspmTxt="%s\n%s" % (spmTxt, lpmTxt)
class listAVR:
	def __init__(self):
		arBoo='Boot loader'
		arApp='Application'
		self.bitsAVR = {
			#Common
			'RES1':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(1,{
					'1':"1 bit as High"})},
			'RES2':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(2,{
					'11':"2 bits as High"})},
			'RES3':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(3,{
					'111':"3 bits as High"})},
			'RES5':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(5,{
					'11111':"5 bits as High"})},
			'RES6':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(6,{
					'111111':"6 bits as High"})},
			'RES7':{'Desc':"Empty",
				'NameShow':"RESERVED",
				'Config':(7,{
					'1111111':"7 bits as High"})},
			#Locks
			'LB':{'Desc':"Standard Lockbits",
				'Config':(2,{
					'11':"No memory lock features enabled",
					'10':
"""Further  programming  of  the  Flash  and EEPROM is
disabled  in  Parallel  and  Serial  Programming  mode.
The  Fuse Bits  are  locked  in both Serial and Parallel
Programming mode""",
					'00':
"""Further programming and verification of the Flash and
EEPROM is disabled in parallel and Serial Programming
mode.  The Fuse  Bits  are  locked  in  both  Serial  and
Parallel Programming modes"""})},
			'BLB0':{'Desc':"Application Area Lockbits",
				'Config':(2,{
					'11':okTxt % arApp,
					'10':spmTxt % arApp,
					'01':lpmTxt % (arBoo, arApp, arBoo, arApp),
					'00':lspmTxt% (arApp, arBoo, arApp, arBoo, arApp) })},
			'BLB1':{'Desc':"Bootloader Area Lockbits",
				'Config':(2,{
					'11':okTxt % arBoo,
					'10':spmTxt % arBoo,
					'01':lpmTxt % (arApp, arBoo, arApp, arBoo),
					'00':lspmTxt % (arBoo, arApp, arBoo, arApp, arBoo)})},
			#Fuses
			'S8515C':{'Desc':"AT90S4414/8515\ncompatibility mode",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'M161C':{'Desc':"ATmega161 compatibility mode",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'M103C':{'Desc':"ATmega103 compatibility mode",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'RSTDISBL':{'Desc':"External Reset",
				'Config':(1,{
					'1':"Enable",
					'0':"Disable"})},
			'SELFPRGEN':{'Desc':"Self Programming",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'SPIEN':{'Desc':"Serial Programming and\nData Downloading",
				'Default':"0",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'EESAVE':{'Desc':"EEPROM memory preserving\nthrough Chip Erase",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'OCDEN':{'Desc':"On Chip Debug",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'JTAGEN':{'Desc':"JTAG Interface",
				'Default':"0",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'DWEN':{'Desc':"debugWIRE",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'WDTON':{'Desc':"Watchdog Timer",
				'Config':(1,{
					'1':"Default Disabled after Reset.\nCan be enabled by software.",
					'0':"Always Enable"})},
			'BODLEVEL3':{'Desc':"Brown-out Detector trigger level",
				'NameShow':"BODLEVEL",
				'Config':(3,{
					'111':"Disable",
					'110':"1.8V",
					'101':"2.7V",
					'100':"4.3V"})},
			'BODLEVEL3V':{'Desc':"Brown-out Detector trigger level",
				'NameShow':"BODLEVEL",
				'Config':(3,{
					'111':"Disable",
					'110':"1.8V",
					'101':"2.7V",
					'100':"4.3V",
					'011':"2.3V"})},
			'BODLEVEL2':{'Desc':"Brown-out Detector trigger level",
				'NameShow':"BODLEVEL",
				'Config':(2,{
					'11':"Disable",
					'10':"1.8V",
					'01':"2.7V",
					'00':"4.3V"})},
			'BODLEVEL1':{'Desc':"Brown-out Detector trigger level",
				'NameShow':"BODLEVEL",
				'Config':(1,{
					'1':"2.7V",
					'0':"4.3V"})},
			'BODEN':{'Desc':"Brown-out Detector",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'BOOTSZ2_2k':{'Desc':"Boot Size Configuration",
				'NameShow':"BOOTSZ",
				'Default':"00",
				'Config':(2,{
					'00':"1024 words",
					'01':"512 words",
					'10':"256 words",
					'11':"128 words"})},
			'BOOTSZ2_4k':{'Desc':"Boot Size Configuration",
				'NameShow':"BOOTSZ",
				'Default':"00",
				'Config':(2,{
					'00':"2048 words",
					'01':"1024 words",
					'10':"512 words",
					'11':"256 words"})},
			'BOOTSZ2_8k':{'Desc':"Boot Size Configuration",
				'NameShow':"BOOTSZ",
				'Default':"00",
				'Config':(2,{
					'00':"4096 words",
					'01':"2048 words",
					'10':"1024 words",
					'11':"512 words"})},
			'BOOTRST':{'Desc':"Reset Vector",
				'Config':(1,{
					'1':"Normal",
					'0':"In Bootloader Area"})},
			'CKDIV8':{'Desc':"Divide clock by",
				'Default':"0",
				'Config':(1,{
					'1':"1 (Not divided)",
					'0':" 8"})},
			'CKOUT':{'Desc':"Output Clock on CKOUT/CLKO pin",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'CKOPT':{'Desc':"Oscillator option",
				'Config':(1,{
					'1':"Disable",
					'0':"Enable"})},
			'SUT2_STD':{'Desc':"Startup time (CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"6CK, BOD should be enabled",
					'01':"6CK+4.1ms",
					'10':"6CK+65ms"})},
			'SUT2_32kCap':{'Desc':"Startup time: Low Freq. Crystal Oscillator \n32768Hz w/Internal capacitors enablable (CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"6CK, BOD should be enabled",
					'01':"6CK+4.1ms",
					'10':"6CK+65ms"})},
			'SUT2_INTXM_EXT':{'Desc':"Startup time: External Clock or\nInternal RC 8MHz (CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"6+14CK, BOD should be enabled",
					'01':"6+14CK+4.1ms",
					'10':"6+14CK+65ms"})},
			'SUT2_Cer':{'Desc':"Startup time: Ceramic Resonator\n(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"Ceramic Resonator 258+14CK+4.1ms",
					'01':"Ceramic Resonator 258+14CK+65ms",
					'10':"Ceramic Resonator 1K+14CK, BOD should be enabled",
					'11':"Ceramic Resonator 1K+14CK+4.1ms"})},
			'SUT2_CerCry':{'Desc':"Startup time: Ceramic Resonator or \nCrystal Oscillator(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"Ceramic Resonator 1k+14CK+65ms",
					'01':"Crystal Oscillator 16K+14CK, BOD should be enabled",
					'10':"Crystal Oscillator 16K+14CK+4.1ms",
					'11':"Crystal Oscillator 16k+14CK+65ms"})},
			'SUT2_CerOld':{'Desc':"Startup time: Ceramic Resonator\n(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"Ceramic Resonator 258CK+4.1ms",
					'01':"Ceramic Resonator 258CK+65ms",
					'10':"Ceramic Resonator 1kCK, BOD should be enabled",
					'11':"Ceramic Resonator 1kCK+4.1ms"})},
			'SUT2_CerCryOld':{'Desc':"Startup time: Ceramic Resonator or \nCrystal Oscillator(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"Ceramic Resonator 1kCK+65ms",
					'01':"Crystal Oscillator 16kCK, BOD should be enabled",
					'10':"Crystal Oscillator 16kCK+4.1ms",
					'11':"Crystal Oscillator 16kCK+65ms"})},
			'SUT2_32k':{'Desc':"Startup time: Low Freq. Crystal \nOscillator 32768Hz (CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"1K+14CK, BOD should be enabled",
					'01':"1K+14CK+4.1ms",
					'10':"1K+14CK+65ms"})},
			'SUT2_32k_Short':{'Desc':"Startup time: Low Freq. Crystal \nOscillator 32768Hz (CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"1kCK+4.1ms, BOD should be enabled or Fast Power Up",
					'01':"1K+14CK+65ms",
					'10':"32K+14CK+65ms(Stable Startup CLK)"})},
			'SUT2_32kSlow':{'Desc':"Startup time: Low Freq. Crystal \nOscillator 32768Hz, Slower Startup \n(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"32K+14CK, BOD should be enabled",
					'01':"32K+14CK+4.1ms",
					'10':"32K+14CK+65ms"})},
			'SUT2_ExtRC':{'Desc':"Startup time: External RC Oscillator\n(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"10",
				'Config':(2,{
					'00':"18CK, BOD should be enabled",
					'01':"18CK+4.1ms",
					'10':"18CK+65ms",
					'11':"6CK+4.1ms, BOD should be enabled or Fast Power Up"})},
			'SUT2_PLL':{'Desc':"Startup time: High Frequency PLL Clock\n(CKSEL dependend)",
				'NameShow':"SUT",
				'Default':"11",
				'Config':(2,{
					'00':"(14+1024)CK+(4+4)ms, BOD should be enabled",
					'01':"(14+16384)CK+(4+4)ms",
					'10':"(14+1024)CK+(64+4)ms",
					'11':"(14+16384)CK+(64+4)ms"})},
			'SUT2_CS2':{'Desc':"Startup time",
				'NameShow':"SUT",
				'Default':"01",
				'Config':(2,{
					'00':"6+14CK, BOD should be enabled",
					'01':"6+14CK+4ms",
					'10':"6+14CK+64ms"})},
			'CKSEL2':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"10",
				'Config':(2,{
					'00':"External Clock on CLKI",
					'01':"Calibrated Internal 4.8MHz Oscillator",
					'10':"Calibrated Internal 9.6MHz Oscillator",
					'11':"Internal 128 kHz Oscillator"})},
			'CKSEL4_INT8M_128k':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"0010",
				'Config':(4,{
					'0000':"External Clock on XTAL1 Input",
					'0010':"Calibrated Internal RC Oscillator ~8MHz",
					'0011':"128kHz Internal Oscillator",
					'0100':"Low Freq. Crystal Oscillator 32768Hz",
					'0101':"Low Freq. Crystal Oscillator 32768Hz, Slower\nStartup",
					'0110':"Full Swing Ceramic Oscillator 400kHz-20MHz",
					'0111':"Full Swing Ceramic Resonator or Crystal Oscillator\n400kHz-20MHz",
					'1000':"Low Power Ceramic Resonator 400-900kHz",
					'1001':"Low Power Ceramic Resonator or Crystal Oscillator\n400-900kHz",
					'1010':"Low Power Ceramic Resonator 0.9-3MHz",
					'1011':"Low Power Ceramic Resonator or Crystal Oscillator\n0.9-3MHz",
					'1100':"Low Power Ceramic Resonator 3-8MHz",
					'1101':"Low Power Ceramic Resonator or Crystal Oscillator\n3-8MHz",
					'1110':"Low Power Ceramic Resonator 8-16MHz",
					'1111':"Low Power Ceramic Resonator or Crystal Oscillator\n8-16MHz"}),
				'SUT_SEL':{
					'0000':'SUT2_INTXM_EXT',
					'0010':'SUT2_INTXM_EXT',
					'0011':'SUT2_CS2',
					'0100':'SUT2_32k',
					'0101':'SUT2_32kSlow',
					'0110':'SUT2_Cer',
					'0111':'SUT2_CerCry',
					'1000':'SUT2_Cer',
					'1001':'SUT2_CerCry',
					'1010':'SUT2_Cer',
					'1011':'SUT2_CerCry',
					'1100':'SUT2_Cer',
					'1101':'SUT2_CerCry',
					'1110':'SUT2_Cer',
					'1111':'SUT2_CerCry'}
				},
			'CKSEL4_INT8M_32k':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"0010",
				'Config':(4,{
					'0000':"External Clock on XTAL1 Input",
					'0010':"Calibrated Internal RC Oscillator ~8MHz",
					'0100':"Low Freq. Crystal Oscillator 32768Hz.1kCK add. startup. Int. Cap off.",
					'0101':"Low Freq. Crystal Oscillator 32768Hz.32kCK add. startup. Int. Cap off.",
					'0110':"Low Freq. Crystal Oscillator 32768Hz.1kCK add. startup. Int. Cap on.",
					'0111':"Low Freq. Crystal Oscillator 32768Hz.32kCK add. startup. Int. Cap on.",
					'1000':"External Ceramic Resonator 400-900kHz",
					'1001':"External Ceramic Resonator or Crystal Oscillator\n400-900kHz",
					'1010':"External Ceramic Resonator 0.9-3MHz",
					'1011':"External Ceramic Resonator or Crystal Oscillator\n0.9-3MHz",
					'1100':"External Ceramic Resonator 3-8MHz",
					'1101':"External Ceramic Resonator or Crystal Oscillator\n3-8MHz",
					'1110':"External Ceramic Resonator 8-16MHz",
					'1111':"External Ceramic Resonator or Crystal Oscillator\n8-16MHz"}),
				'SUT_SEL':{
					'0000':'SUT2_STD',
					'0010':'SUT2_STD',
					'0100':'SUT2_32kCap',
					'0101':'SUT2_32kCap',
					'0110':'SUT2_32kCap',
					'0111':'SUT2_32kCap',
					'1000':'SUT2_Cer',
					'1001':'SUT2_CerCry',
					'1010':'SUT2_Cer',
					'1011':'SUT2_CerCry',
					'1100':'SUT2_Cer',
					'1101':'SUT2_CerCry',
					'1110':'SUT2_Cer',
					'1111':'SUT2_CerCry'}
				},
			'CKSEL4_INT4M_8M_128k':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"0100",
				'Config':(4,{
					'0000':"External Clock on XTAL1 Input",
					'0010':"Calibrated Internal RC Oscillator ~4MHz",
					'0100':"Calibrated Internal RC Oscillator ~8MHz",
					'0110':"128kHz Internal Oscillator",
					'1000':"External Ceramic Resonator 400-900kHz",
					'1001':"External Ceramic Resonator or Crystal Oscillator\n400-900kHz",
					'1010':"External Ceramic Resonator 0.9-3MHz",
					'1011':"External Ceramic Resonator or Crystal Oscillator\n0.9-3MHz",
					'1100':"External Ceramic Resonator 3-8MHz",
					'1101':"External Ceramic Resonator or Crystal Oscillator\n3-8MHz",
					'1110':"External Ceramic Resonator 8-16MHz",
					'1111':"External Ceramic Resonator or Crystal Oscillator\n8-16MHz"}),
				'SUT_SEL':{
					'0000':'SUT2_CS2',
					'0010':'SUT2_CS2',
					'0100':'SUT2_CS2',
					'0110':'SUT2_CS2',
					'1000':'SUT2_Cer',
					'1001':'SUT2_CerCry',
					'1010':'SUT2_Cer',
					'1011':'SUT2_CerCry',
					'1100':'SUT2_Cer',
					'1101':'SUT2_CerCry',
					'1110':'SUT2_Cer',
					'1111':'SUT2_CerCry'}
				},
			'CKSEL4_PLL_INT4M_8M_128k':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"0010",
				'Config':(4,{
					'0000':"External Clock on XTAL1 Input",
					'0001':"High Frequency PLL Clock 64/16MHz",
					'0010':"Internal RC Oscillator 8MHz",
					'0011':"Int.RC Oscillator 6.4MHz (ATtiny15 compatibility)",
					'0100':"128kHz Internal Oscillator",
					'0110':"Low Freq. Crystal Oscillator 32768Hz",
					'1000':"External Ceramic Resonator 400-900kHz",
					'1001':"External Ceramic Resonator or Crystal Oscillator\n400-900kHz",
					'1010':"External Ceramic Resonator 0.9-3MHz",
					'1011':"External Ceramic Resonator or Crystal Oscillator\n0.9-3MHz",
					'1100':"External Ceramic Resonator 3-8MHz",
					'1101':"External Ceramic Resonator or Crystal Oscillator\n3-8MHz",
					'1110':"External Ceramic Resonator 8-16MHz",
					'1111':"External Ceramic Resonator or Crystal Oscillator\n8-16MHz"}),
				'SUT_SEL':{
					'0000':'SUT2_CS2',
					'0001':'SUT2_PLL',
					'0010':'SUT2_CS2',
					'0100':'SUT2_CS2',
					'0110':'SUT2_32k_Short',
					'1000':'SUT2_Cer',
					'1001':'SUT2_CerCry',
					'1010':'SUT2_Cer',
					'1011':'SUT2_CerCry',
					'1100':'SUT2_Cer',
					'1101':'SUT2_CerCry',
					'1110':'SUT2_Cer',
					'1111':'SUT2_CerCry'}
				},
			'CKSEL4_INT1M_2M_4M_8M':{'Desc':"Select Clock Source",
				'NameShow':"CKSEL",
				'Default':"0001",
				'Config':(4,{
					'0000':"External Clock on XTAL1 Input",
					'0001':"Calibrated Internal RC Oscillator ~1MHz",
					'0010':"Calibrated Internal RC Oscillator ~2MHz",
					'0011':"Calibrated Internal RC Oscillator ~4MHz",
					'0100':"Calibrated Internal RC Oscillator ~8MHz",
					'0101':"External RC Oscillator up to 900kHz",
					'0110':"External RC Oscillator 0.9-3MHz",
					'0111':"External RC Oscillator 3-8MHz",
					'1000':"External RC Oscillator 8-12MHz",
					'1001':"Low Freq. Crystal Oscillator 32768Hz",
					'1010':"External Ceramic Resonator 400-900kHz",
					'1011':"External Slower Ceramic Resonator 400-900kHz",
					'1100':"External Ceramic Resonator 0.9-3MHz",
					'1101':"External Ceramic Resonator or Crystal Oscillator\n0.9-3MHz",
					'1110':"External Ceramic Resonator 3-16MHz.\nSet CKOPT for 8-16MHz",
					'1111':"External Ceramic Resonator or Crystal Oscillator\n3-16MHz.Set CKOPT for 8-16MHz"}),
				'SUT_SEL':{
					'0000':'SUT2_STD',
					'0001':'SUT2_STD',
					'0010':'SUT2_STD',
					'0011':'SUT2_STD',
					'0100':'SUT2_STD',
					'0101':'SUT2_ExtRC',
					'0110':'SUT2_ExtRC',
					'0111':'SUT2_ExtRC',
					'1000':'SUT2_ExtRC',
					'1001':'SUT2_32k_Short',
					'1010':'SUT2_CerOld',
					'1011':'SUT2_CerCryOld',
					'1100':'SUT2_CerOld',
					'1101':'SUT2_CerCryOld',
					'1110':'SUT2_CerOld',
					'1111':'SUT2_CerCryOld'}
				}
		}
		self.lsAVR = [
			{ 'Name' : "ATmega8", 'Fuses' : {'Low':("CKSEL4_INT1M_2M_4M_8M", "SUT_SEL", "BODEN", "BODLEVEL1"), 'High':("BOOTRST", "BOOTSZ2_2k", "EESAVE", "CKOPT", "SPIEN", "WDTON", "RSTDISBL")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATmega8515", 'Fuses' : {'Low':("CKSEL4_INT1M_2M_4M_8M", "SUT_SEL", "BODEN", "BODLEVEL1"), 'High':("BOOTRST", "BOOTSZ2_2k", "EESAVE", "CKOPT", "SPIEN", "WDTON", "S8515C")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATmega16", 'Fuses' : {'Low':("CKSEL4_INT1M_2M_4M_8M", "SUT_SEL", "BODEN", "BODLEVEL1"), 'High':("BOOTRST", "BOOTSZ2_2k", "EESAVE", "CKOPT", "SPIEN", "JTAGEN", "OCDEN")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATmega32", 'Fuses' : {'Low':("CKSEL4_INT1M_2M_4M_8M", "SUT_SEL", "BODEN", "BODLEVEL1"), 'High':("BOOTRST", "BOOTSZ2_4k", "EESAVE", "CKOPT", "SPIEN", "JTAGEN", "OCDEN")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATmega162", 'Fuses' : {'Low':("CKSEL4_INT8M_32k", "SUT_SEL", "CKOUT", "CKDIV8"), 'High':("BOOTRST", "BOOTSZ2_2k", "EESAVE", "WDTON", "SPIEN", "JTAGEN", "OCDEN"), 'Extended':("RES1", "BODLEVEL3", "M161C", "RES3")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATmega164", 'Fuses' : {'Low':("CKSEL4_INT8M_128k", "SUT_SEL", "CKOUT", "CKDIV8"), 'High':("BOOTRST", "BOOTSZ2_2k", "EESAVE", "WDTON", "SPIEN", "JTAGEN", "OCDEN"), 'Extended':("BODLEVEL3", "RES5")}, 'Lock' : ("LB", "BLB0", "BLB1")},
			{ 'Name' : "ATmega644", 'Fuses' : {'Low':("CKSEL4_INT8M_128k", "SUT_SEL", "CKOUT", "CKDIV8"), 'High':("BOOTRST", "BOOTSZ2_8k", "EESAVE", "WDTON", "SPIEN", "JTAGEN", "OCDEN"), 'Extended':("BODLEVEL3", "RES5")}, 'Lock' : ("LB", "BLB0", "BLB1")},
			{ 'Name' : "ATmega128", 'Fuses' : {'Low':("CKSEL4_INT1M_2M_4M_8M", "SUT_SEL", "BODEN", "BODLEVEL1"), 'High':("BOOTRST", "BOOTSZ2_8k", "EESAVE", "CKOPT", "SPIEN", "JTAGEN", "OCDEN"), 'Extended':("WDTON", "M103C", "RES6")}, 'Lock' : ("LB", "BLB0", "BLB1", "RES2")},
			{ 'Name' : "ATtiny13", 'Fuses' : {'Low':("CKSEL2", "SUT2_CS2", "CKDIV8", "WDTON", "EESAVE", "SPIEN"), 'High':( "RSTDISBL", "BODLEVEL2", "DWEN", "SELFPRGEN")}, 'Lock' : ("LB",)},
			{ 'Name' : "ATtiny2313", 'Fuses' : {'Low':("CKSEL4_INT4M_8M_128k", "SUT_SEL", "CKOUT", "CKDIV8"), 'High':("RSTDISBL", "BODLEVEL3", "WDTON", "SPIEN", "EESAVE", "DWEN"), 'Extended':("SELFPRGEN", "RES7")}, 'Lock' : ("LB",)},
			{ 'Name' : "ATtiny25", 'Fuses' : {'Low':("CKSEL4_PLL_INT4M_8M_128k", "SUT_SEL", "CKOUT", "CKDIV8"), 'High':("BODLEVEL3", "EESAVE", "WDTON", "SPIEN", "DWEN", "RSTDISBL"), 'Extended':("SELFPRGEN", "RES7")}, 'Lock' : ("LB",)}
		]
	
	def add(self,ucAVR):
		self.lsAVR.append(ucAVR)
	
	def empty(self):
		cLib=len(self.lsAVR)
		while cLib!=0:
			self.lsAVR.pop()
			cLib-=1
	
	def listAVRs(self):
		self.namesAVR = []
		ucAVRs=len(self.lsAVR)
		for n in range(ucAVRs):
			self.namesAVR.append(self.lsAVR[n]['Name'])
		return self.namesAVR
	
	def getAVR(self, index):
		return self.lsAVR[index]

	
	def dbgListAVRs(self):
		ucAVRs=len(self.lsAVR)
		debugPrint = "\nNo of AVRs in List: %i\n" % (ucAVRs)
		for n in range(ucAVRs):
			debugPrint += "\tMikrokontroler \"%s\"" % (self.lsAVR[n]['Name'])
			CountOfFuses=len(self.lsAVR[n]['Fuses'])
			debugPrint += "; Fusebytes[%i]:\n" % (CountOfFuses)
			for keyFuse in self.lsAVR[n]['Fuses'].keys():
				#debugPrint += " %s" % (self.lsAVR[n]['Fuses'][keyFuse])
				debugPrint += "\t\t%s(" % (keyFuse)
				for bitFuse in range(len(self.lsAVR[n]['Fuses'][keyFuse])):
					debugPrint += "${%s}" % (self.lsAVR[n]['Fuses'][keyFuse][bitFuse])
				debugPrint += ")\n"
		print debugPrint
		return

	def avdName(self, FullName):
		retAVD=-1
		if FullName[0:5]=='AT90S':
			retAVD="%s" % (FullName[5:len(FullName)].lower())
		elif FullName[0:7]=='AT90USB':
			retAVD="usb%s" % (FullName[7:len(FullName)].lower())
		elif FullName[0:7]=='AT90PWM':
			retAVD="pwm%s" % (FullName[7:len(FullName)].lower())
		elif FullName[0:7]=='AT90CAN':
			retAVD="c%s" % (FullName[7:len(FullName)].lower())
		elif FullName[0:7]=='ATxmega':
			retAVD="x%s" % (FullName[7:len(FullName)].lower())
		elif FullName[0:6]=='ATmega':
			retAVD="m%s" % (FullName[6:len(FullName)].lower())
		elif FullName[0:6]=='ATtiny':
			retAVD="t%s" % (FullName[6:len(FullName)].lower())
		return retAVD

	def nameFromAVD(self, nameAVD):
		FullName=-1
		reSameDigits=re.compile('([0-9]{1,4})$', re.L)
		if nameAVD[0:1]=='m':
			FullName="ATmega%s" % (nameAVD[1:len(nameAVD)].upper())
		elif nameAVD[0:3]=='usb':
			FullName="AT90%s" % (nameAVD.upper())
		elif nameAVD[0:3]=='pwm':
			FullName="AT90%s" % (nameAVD.upper())
		elif nameAVD[0:1]=='c':
			FullName="AT90CAN%s" % (nameAVD[1:len(nameAVD)].upper())
		elif nameAVD[0:1]=='x':
			FullName="ATxmega%s" % (nameAVD[1:len(nameAVD)].upper())
		elif nameAVD[0:1]=='t':
			FullName="ATtiny%s" % (nameAVD[1:len(nameAVD)].upper())
		elif reSameDigits.match(nameAVD):
			FullName="AT90S%s" % (nameAVD)
		return FullName

	def avdCfgByte(self, FullName):
		return{
			'Lock':'lock',
			'Extended':'efuse',
			'High':'hfuse',
			'Low':'lfuse'
		}[FullName]

