# -*- coding: utf-8 -*-


from qt import *

from globals import *

class FontPropertyDialog(QDialog):
	def __init__(self,parent = None,name = None):
		QDialog.__init__(self,parent,name)
	
		if not name:
			self.setName("FontProperty")
	
		self._initForm()
		self._initActions()
		self.languageChange()
	
	
	def _initForm(self):
		self.setSizeGripEnabled(0)
		self.setMinimumSize(300,310)
		self.setMaximumSize(300,310)
	
		self._buttonOk = QPushButton(self,"_buttonOk")
		self._buttonOk.setGeometry(QRect(110,270,80,30))
		self._buttonOk.setAutoDefault(TRUE)
		self._buttonOk.setDefault(TRUE)
	
		self._buttonCancel = QPushButton(self,"_buttonCancel")
		self._buttonCancel.setGeometry(QRect(210,270,80,30))
		self._buttonCancel.setAutoDefault(TRUE)
	
		self._labelName = QLabel(self,"_labelName")
		self._labelName.setGeometry(QRect(10,20,90,20))
	
		self._labelH = QLabel(self,"_labelH")
		self._labelH.setGeometry(QRect(10,80,220,20))
	
		self._labelW = QLabel(self,"_labelW")
		self._labelW.setGeometry(QRect(10,110,220,20))
	
		self._labelPoints = QLabel(self,"_labelPoints")
		self._labelPoints.setGeometry(QRect(10,140,220,20))
	
		self._labelIntline = QLabel(self,"_labelIntline")
		self._labelIntline.setGeometry(QRect(10,170,220,20))
	
		self._labelCount = QLabel(self,"_labelCount")
		self._labelCount.setGeometry(QRect(10,230,220,20))
	
		self._labelFirst = QLabel(self,"_labelFirst")
		self._labelFirst.setGeometry(QRect(10,200,220,20))
	
		self.textName = QTextEdit(self,"textName")
		self.textName.setGeometry(QRect(110,10,180,60))
		self.textName.setWordWrap(QTextEdit.WidgetWidth)
		self.textName.setWrapPolicy(QTextEdit.AtWordOrDocumentBoundary)
	
		self.spinH = QSpinBox(self,"spinH")
		self.spinH.setGeometry(QRect(240,80,50,20))
		self.spinH.setMaxValue(255)
		self.spinH.setMinValue(1)
		self.spinH.setValue(15)
	
		self.spinW = QSpinBox(self,"spinW")
		self.spinW.setGeometry(QRect(240,110,50,20))
		self.spinW.setMaxValue(128)
		self.spinW.setMinValue(8)
		self.spinW.setLineStep(8)
		self.spinW.setValue(16)
	
		self.spinPoints = QSpinBox(self,"spinPoints")
		self.spinPoints.setEnabled(FALSE)
		self.spinPoints.setGeometry(QRect(240,140,50,20))
		self.spinPoints.setMaxValue(255)
		self.spinPoints.setMinValue(1)
	
		self.spinIntline = QSpinBox(self,"spinIntline")
		self.spinIntline.setGeometry(QRect(240,170,50,20))
		self.spinIntline.setMaxValue(255)
		self.spinIntline.setMinValue(0)
		self.spinIntline.setValue(2)
	
		self.spinFirst = QSpinBox(self,"spinFirst")
		self.spinFirst.setEnabled(FALSE)
		self.spinFirst.setGeometry(QRect(240,200,50,20))
		self.spinFirst.setMaxValue(255)
		self.spinFirst.setMinValue(0)
		self.spinFirst.setValue(32)
	
		self.spinCount = QSpinBox(self,"spinCount")
		self.spinCount.setEnabled(FALSE)
		self.spinCount.setGeometry(QRect(240,230,50,20))
		self.spinCount.setMaxValue(1024)
		self.spinCount.setMinValue(1)
		self.spinCount.setValue(224)
	
	
	def _initActions(self):
		self.connect(self._buttonOk,SIGNAL("clicked()"),self.accept)
		self.connect(self._buttonCancel,SIGNAL("clicked()"),self.reject)
	
	
	def languageChange(self):
		self.setCaption(self.__tr("Font properties"))
		self._buttonOk.setText(self.__tr("OK"))
		self._buttonOk.setAccel(QString.null)
		self._buttonCancel.setText(self.__tr("Cancel"))
		self._buttonCancel.setAccel(QString.null)
		self._labelPoints.setText(self.__tr("Height (pt)"))
		self._labelH.setText(self.__tr("Height (px)"))
		self._labelName.setText(self.__tr("Font name"))
		self._labelCount.setText(self.__tr("Count of chars"))
		self._labelFirst.setText(self.__tr("First char ASCII code"))
		self._labelIntline.setText(self.__tr("Interline spacing"))
		self._labelW.setText(self.__tr("Width (px)"))
		self.textName.setText(self.__tr('New REB font'))
		QWhatsThis.add(self.textName,self.__tr("Font name (max 64 xhars)"))
		QWhatsThis.add(self.spinH,self.__tr("Font height in pixels"))
		QWhatsThis.add(self.spinW,self.__tr("Maximum char width in pixels"))
		QWhatsThis.add(self.spinPoints,self.__tr("Font height in points"))
		QWhatsThis.add(self.spinIntline,self.__tr("Spacing between lines"))
		QWhatsThis.add(self.spinFirst,self.__tr("ASCII code of first char, presents in font"))
		QWhatsThis.add(self.spinCount,self.__tr("Count of chars in font"))
	
	
	def __tr(self,s,c = None):
		return qApp.translate("FontPropertyDialog",s,c)
	




