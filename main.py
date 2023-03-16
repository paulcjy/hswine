import sys
import os
from PySide6.QtWidgets import *#QApplication, QMainWindow, QStackedWidget, QCheckBox, QPushButton, QMessageBox
from PySide6.QtGui import *#QStandardItemModel, QStandardItem, QIntValidator
from PySide6.QtCore import *#Signal, Slot, Qt, QModelIndex

# 주소 검색
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request
import json

from pandasFunc import *
import var as V

from datetime import date
import time

def errorMsg(parent, message, informative=None):
	msgBox = QMessageBox(parent)
	msgBox.setIcon(QMessageBox.Warning)
	msgBox.setWindowTitle('에러')
	msgBox.setText(message)
	if informative is not None:
		msgBox.setInformativeText(informative)
	msgBox.exec_()

class saleModel(QStandardItemModel):
	def __init__(self, year=None, month=None, keyword=None, search_option=None):
		QStandardItemModel.__init__(self, 0, 15)
		
		data = make_saleTable()

		# Normal : By date
		if keyword is None:
			data = data[data['sale_date'].dt.year == int(year)]
			data = data[data['sale_date'].dt.month == int(month)]
			data.sort_values(by=['sale_date', 'sale_id'], inplace=True)

		# Search
		else:
			if search_option == 'name':
				data_cust = df['cust'].copy()
				cust_id = data_cust[data_cust['cust_name'].str.lower().str.contains(keyword.lower())]['cust_id']
				data = data[data['cust_id'].isin(cust_id)]
				data.sort_values(by='sale_date', inplace=True)

			elif search_option == 'phone':
				data_cust = df['cust'].copy()
				cust_id = data_cust[data_cust['cust_phone'].str.contains(keyword)]['cust_id']
				data = data[data['cust_id'].isin(cust_id)]
				data.sort_values(by='sale_date', inplace=True)

			elif search_option == 'prod':
				data = data[data['pd_name'].str.lower().str.contains(keyword.lower())]
				data.sort_values(by='sale_date', inplace=True)

		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i == 2:
					self.setData(self.index(self.rowCount()-1, i), str(item[i])[:10])
				elif i == 7:
					tax = QStandardItem()
					tax.setCheckable(True)
					tax.setEditable(False)
					tax.setCheckState(Qt.Checked if item[i] else Qt.Unchecked)
					self.setItem(self.rowCount()-1, i, tax)
				elif i == 10:
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}')
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 14:
					self.setData(self.index(self.rowCount()-1, i), str(self.rowCount()))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i in (3, 5, 6):
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}')
				elif i in (9, 11, 12, 13):
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))

class setModel(QStandardItemModel):
	def __init__(self, keyword=None, search_option=None):
		QStandardItemModel.__init__(self, 0, 11)

		# Load Data
		data = make_setTable()

		# Search
		if keyword is not None:
			if search_option == 'name':
				data = data[data['pd_name_x'].str.lower().str.contains(keyword.lower())]
			elif search_option == 'wine':
				data = data[data['pd_name_y'].str.lower().str.contains(keyword.lower())]

		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i in (0, 7, 10):
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 2:
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}'+'   ')
				elif i == 4:
					self.setData(self.index(self.rowCount()-1, i), str(item[i])[:7])
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 5:
					avail = QStandardItem()
					avail.setCheckable(True)
					avail.setEditable(False)
					avail.setCheckState(Qt.Checked if item[i] else Qt.Unchecked)
					self.setItem(self.rowCount()-1, i, avail)
				elif i == 8:
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}'+'   ')
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))

class wineModel(QStandardItemModel):
	def __init__(self, keyword=None):
		QStandardItemModel.__init__(self, 0, 7)

		# Load Data
		data = make_wineTable()

		# Search
		if keyword is not None:
			data = data[data['pd_name'].str.lower().str.contains(keyword.lower())]

		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i == 0:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 2:
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}'+'   ')
				elif i == 4:
					self.setData(self.index(self.rowCount()-1, i), str(item[i])[:10])
				elif i == 6:
					avail = QStandardItem()
					avail.setCheckable(True)
					avail.setEditable(False)
					avail.setCheckState(Qt.Checked if item[i] else Qt.Unchecked)
					self.setItem(self.rowCount()-1, i, avail)
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))

class etcModel(QStandardItemModel):
	def __init__(self, keyword=None):
		QStandardItemModel.__init__(self, 0, 7)

		# Load Data
		data = make_etcTable()

		# Search
		if keyword is not None:
			data = data[data['pd_name'].str.lower().str.contains(keyword.lower())]

		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i == 0:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 2:
					self.setData(self.index(self.rowCount()-1, i), f'{item[i]:,}'+'   ')
				elif i == 4:
					self.setData(self.index(self.rowCount()-1, i), str(item[i])[:10])
				elif i == 6:
					avail = QStandardItem()
					avail.setCheckable(True)
					avail.setEditable(False)
					avail.setCheckState(Qt.Checked if item[i] else Qt.Unchecked)
					self.setItem(self.rowCount()-1, i, avail)
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))

class custModel(QStandardItemModel):
	def __init__(self, keyword=None, search_option=None):
		QStandardItemModel.__init__(self, 0, 7)

		# Load Data
		data = make_custTable()

		# Search
		if keyword is not None:
			if search_option == 'name':
				data = data[data['cust_name'].str.lower().str.contains(keyword.lower())]
			elif search_option == 'phone':
				data = data[data['cust_phone'].str.contains(keyword)]

		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i == 0:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				elif i == 6:
					self.setData(self.index(self.rowCount()-1, i),f'{item[i]:,}'+'   ')
					self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i]))

class recordModel(QStandardItemModel):
	def __init__(self, cust_id):
		QStandardItemModel.__init__(self, 0, 9)
		
		# Filter by Cust ID
		data = make_saleTable(cust_id)
		data = data[data['cust_id'].isin([cust_id])][['sale_date', 'pd_name', 'pd_price', 'sale_deliv', 'sale_hs', 'sale_bis', 'sale_tax', 'sale_note']]
		data.sort_values(by='sale_date', inplace=True)
		
		# Item Setting
		for item in data.values:
			self.appendRow(None)
			for i in range(self.columnCount()):
				if i == 0:
					self.setData(self.index(self.rowCount()-1, i), str(self.rowCount()))
				elif i == 1:
					self.setData(self.index(self.rowCount()-1, i), str(item[i-1])[:10])
				elif i == 7:
					tax = QStandardItem()
					tax.setCheckable(False)
					tax.setEditable(False)
					tax.setCheckState(Qt.Checked if item[i-1] else Qt.Unchecked)
					self.setItem(self.rowCount()-1, i, tax)
				elif i in (3, 4, 5, 6):
					self.setData(self.index(self.rowCount()-1, i), f'{item[i-1]:,}')
				else:
					self.setData(self.index(self.rowCount()-1, i), str(item[i-1]))
				self.itemFromIndex(self.index(self.rowCount()-1, i)).setEditable(False)

def initTree(self, page):
	self.tree.setModel(self.model)

	self.tree.header().setSectionsMovable(False)

	self.tree.setRootIsDecorated(False)
	self.tree.setAlternatingRowColors(True)

	# Header Name
	for i in range(self.model.columnCount()):
		self.model.setHeaderData(i, Qt.Horizontal, V.colSetting[page][i]['name'])

	# Header Width
	for i in range(self.tree.header().count()):
		self.tree.setColumnWidth(i, V.colSetting[page][i]['width'])

	# Alignment Setting
	for i in range(self.model.rowCount()):
		for j in V.colSetting['alignment'][page]['center']:
			self.model.item(i, j).setTextAlignment(Qt.AlignCenter)
		for j in V.colSetting['alignment'][page]['right']:
			self.model.item(i, j).setTextAlignment(Qt.AlignRight)


class PageSwitch(QMainWindow):
	gotoSignal = Signal(str)

	def goto(self, name):
		self.gotoSignal.emit(name)

class SalePage(PageSwitch, V.Ui_sale): # TODO 고객변경 / 날짜상품변경
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.model = saleModel(year=self.viewYear.currentText(), month=self.viewMonth.currentText())
		self.setupTree()
		self.model.dataChanged.connect(self.modify)
		self.sumColumn()
		self.setWindowTitle(V.windowTitle_sale)

	def initUI(self):
		# ComboBox Setting
		self.viewYear.addItems(V.years)
		self.viewMonth.addItems(V.months)
		self.viewYear.setCurrentIndex(self.viewYear.findText(str(date.today().year)))
		self.viewMonth.setCurrentIndex(self.viewMonth.findText(str(date.today().month)))
		self.nameRBtn.setChecked(True)

		# PushButton Setting
		self.clearBtn.clicked.connect(self.updateTree)
		self.addBtn.clicked.connect(self.add)
		self.deleteBtn.clicked.connect(self.delete)
		# self.modCustBtn.clicked.connect()
		self.modCustBtn.setEnabled(False)
		# self.modProdBtn.clicked.connect()
		self.modProdBtn.setEnabled(False)
		# self.addCustBtn.clicked.connect()
		self.addCustBtn.setEnabled(False)

		self.viewYear.currentTextChanged.connect(self.updateTree)
		self.viewMonth.currentTextChanged.connect(self.updateTree)
		self.lastMonth.clicked.connect(self.viewLastMonth)
		self.nextMonth.clicked.connect(self.viewNextMonth)
		self.searchEnt.returnPressed.connect(self.search)
		self.searchBtn.clicked.connect(self.search)


	def setupTree(self):
		initTree(self, 'sale')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)
		self.tree.header().moveSection(14, 0)
		self.tree.header().moveSection(3, 1)
		self.tree.header().moveSection(12, 2)
		self.tree.header().moveSection(13, 3)
		self.tree.header().moveSection(14, 4)
		self.tree.header().moveSection(13, 5)
		self.tree.header().moveSection(14, 6)
		self.tree.header().moveSection(9, 7)
		self.tree.header().moveSection(11, 8)
		self.tree.header().moveSection(12, 9)
		self.tree.header().moveSection(13, 10)
		self.tree.header().moveSection(13, 11)
		self.tree.hideColumn(0)
		self.tree.hideColumn(1)
		self.tree.hideColumn(8)

	def updateTree(self):
		self.model = saleModel(year=self.viewYear.currentText(), month=self.viewMonth.currentText())
		initTree(self, 'sale')
		self.model.dataChanged.connect(self.modify)
		self.sumColumn()

	def sumColumn(self):
		priceSum = sum([int(self.model.itemFromIndex(self.model.index(i, 10)).text().replace(',', '')) for i in range(self.model.rowCount())])
		delivSum = sum([int(self.model.itemFromIndex(self.model.index(i,  3)).text().replace(',', '')) for i in range(self.model.rowCount())])
		hsSum    = sum([int(self.model.itemFromIndex(self.model.index(i,  5)).text().replace(',', '')) for i in range(self.model.rowCount())])
		bisSum   = sum([int(self.model.itemFromIndex(self.model.index(i,  6)).text().replace(',', '')) for i in range(self.model.rowCount())])
		self.priceSum.setText(f'{priceSum:,}')
		self.delivSum.setText(f'{delivSum:,}')
		self.hsSum.setText(f'{hsSum:,}')
		self.bisSum.setText(f'{bisSum:,}')

		taxIdx = []
		for i in range(self.model.rowCount()):
			if self.model.itemFromIndex(self.model.index(i, 7)).checkState() == Qt.Checked:
				taxIdx.append(i)
		taxSum = sum([int(self.model.itemFromIndex(self.model.index(i, 10)).text().replace(',', '')) for i in taxIdx])
		self.taxSum.setText(f'{taxSum:,}')

	def viewLastMonth(self):
		if self.viewYear.currentIndex() == 0 and self.viewMonth.currentIndex() == 0:
			return

		if self.viewMonth.currentIndex() == 0:
			self.viewMonth.setCurrentIndex(11)
			self.viewYear.setCurrentIndex(self.viewYear.currentIndex() - 1)
		else:
			self.viewMonth.setCurrentIndex(self.viewMonth.currentIndex()-1)
		self.updateTree()

	def viewNextMonth(self):
		if self.viewYear.currentIndex() == self.viewYear.count() - 1 and self.viewMonth.currentIndex() == self.viewMonth.count() - 1:
			return

		if self.viewMonth.currentIndex() == self.viewMonth.count() - 1:
			self.viewMonth.setCurrentIndex(0)
			self.viewYear.setCurrentIndex(self.viewYear.currentIndex() + 1)
		else:
			self.viewMonth.setCurrentIndex(self.viewMonth.currentIndex() + 1)
		self.updateTree()

	def add(self):
		window = NewSale(self)

	def delete(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		try:
			del_data('sale', id)
			self.updateTree()
		except Exception as e:
			errorMsg(self, str(e))

	def modify(self, index):
		# Get ID from index
		row = index.row()
		col = index.column()
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())

		if col == 2:
			changed = self.model.itemFromIndex(self.model.index(row, col)).text()
			if (len(changed) != 10) or not (changed[4] == '-' and changed[7] == '-'):
				errorMsg(self, '날짜 입력이 형식과 다릅니다.', '예) 2021-01-01')
				self.updateTree()
				return
			data = changed.replace('-', '')
		elif col == 4:
			data = self.model.itemFromIndex(self.model.index(row, col)).text()
		elif col in (3, 5, 6):
			changed = self.model.itemFromIndex(self.model.index(row, col)).text()
			if not changed.isdigit():
				errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
				self.updateTree()
				return
			else:
				data = int(changed)
		elif col == 7:
			data = True if self.model.itemFromIndex(self.model.index(row, col)).checkState() == Qt.Checked else False

		try:
			if col == 2:
				mod_sale(id, date=data)
			elif col == 3:
				mod_sale(id, deliv=data)
			elif col == 4:
				mod_sale(id, note=data)
			elif col == 5:
				mod_sale(id, hs=data)
			elif col == 6:
				mod_sale(id, bis=data)
			elif col == 7:
				mod_sale(id, tax=data)
		except TypeError as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))
		except Exception as e:
			errorMsg(self, str(e))

		self.updateTree()

	def search(self):
		if self.nameRBtn.isChecked():
			option = 'name'
		elif self.phoneRBtn.isChecked():
			option = 'phone'
		elif self.pdRBtn.isChecked():
			option = 'prod'

		self.model = saleModel(keyword=self.searchEnt.text(), search_option=option)
		initTree(self, 'sale')
		self.model.dataChanged.connect(self.modify)
		self.sumColumn()

class SetPage(PageSwitch, V.Ui_set):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.model = setModel()
		self.setupTree()
		self.model.dataChanged.connect(self.modify)
		self.setWindowTitle(V.windowTitle_set)

	def initUI(self): # 함수 연결
		self.clearBtn.clicked.connect(self.updateTree)
		self.addBtn.clicked.connect(self.add)
		self.deleteBtn.clicked.connect(self.delete)
		self.modifyBtn.clicked.connect(self.modify2)
		self.searchBtn.clicked.connect(self.search)
		self.searchEnt.returnPressed.connect(self.search)
		self.nameRBtn.setChecked(True)

	def setupTree(self):
		initTree(self, 'set')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)
		self.tree.hideColumn(6)
		self.tree.hideColumn(9)
		self.tree.header().moveSection(4, 1)
		self.tree.header().moveSection(7, 4)
		self.tree.header().moveSection(10, 5)
		self.tree.header().moveSection(9, 6)
		self.tree.header().moveSection(8, 7)

	def updateTree(self):
		self.model = setModel()
		initTree(self, 'set')
		self.model.dataChanged.connect(self.modify)

	def add(self):
		window = NewSet(self)

	def delete(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		try:
			del_data('set', id)
			self.updateTree()
		except Exception as e:
			errorMsg(self, str(e))

	def modify(self, index):
		# Get ID from index
		row = index.row()
		col = index.column()
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())

		if col in (1, 3):
			data = self.model.itemFromIndex(self.model.index(row, col)).text()
		elif col == 2:
			changed = self.model.itemFromIndex(self.model.index(row, col)).text()
			if not changed.isdigit():
				errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
				self.updateTree()
				return
			else:
				data = int(changed)
		elif col == 5:
			data = True if self.model.itemFromIndex(self.model.index(row, col)).checkState() == Qt.Checked else False

		try:
			if col == 1:
				mod_set(id, name=data)
			elif col == 2:
				mod_set(id, price=data)
			elif col == 3:
				mod_set(id, note=data)
			elif col == 5:
				mod_set(id, available=data)
		except TypeError as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))
		except Exception as e:
			errorMsg(self, str(e))

		self.updateTree()

	def modify2(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '수정할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		
		window = ModSet(self, id)

	def search(self):
		keyword = self.searchEnt.text()
		self.searchEnt.clear()

		if keyword == '':
			return

		if self.nameRBtn.isChecked():
			option = 'name'
		elif self.wineRBtn.isChecked():
			option = 'wine'

		self.model = setModel(keyword=keyword, search_option=option)
		initTree(self, 'set')
		self.model.dataChanged.connect(self.modify)

class WinePage(PageSwitch, V.Ui_wine):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.model = wineModel()
		self.setupTree()
		self.model.dataChanged.connect(self.modify)
		self.setWindowTitle(V.windowTitle_wine)

	def initUI(self): # 함수 연결
		self.clearBtn.clicked.connect(self.updateTree)
		self.addBtn.clicked.connect(self.add)
		self.deleteBtn.clicked.connect(self.delete)
		self.searchEnt.returnPressed.connect(self.search)
		self.searchBtn.clicked.connect(self.search)

	def setupTree(self):
		initTree(self, 'wine')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)
		self.tree.hideColumn(4)
		self.tree.hideColumn(5)
		self.tree.header().moveSection(6, 3)

	def updateTree(self):
		self.model = wineModel()
		initTree(self, 'wine')
		self.model.dataChanged.connect(self.modify)

	def add(self):
		window = NewProd(self, 'wine')

	def delete(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		try:
			del_data('wine', id)
			self.updateTree()
		except Exception as e:
			errorMsg(self, str(e))

	def modify(self, index):
		# Get ID from index
		row = index.row()
		col = index.column()
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())

		if col == 2:
			changed = self.model.itemFromIndex(self.model.index(row, col)).text()
			if not changed.isdigit():
				errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
				self.updateTree()
				return
			else:
				data = int(changed)
		elif col == 6:
			data = True if self.model.itemFromIndex(self.model.index(row, col)).checkState() == Qt.Checked else False
		else:
			data = self.model.itemFromIndex(self.model.index(row, col)).text()

		try:
			if col == 1:
				mod_prod(id, name=data)
			elif col == 2:
				mod_prod(id, price=data)
			elif col == 3:
				mod_prod(id, note=data)
			elif col == 6:
				mod_prod(id, available=data)
		except Exception as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))

		self.updateTree()

	def search(self):
		keyword = self.searchEnt.text()
		self.searchEnt.clear()

		if keyword == '':
			return

		self.model = wineModel(keyword=keyword)
		initTree(self, 'wine')
		self.model.dataChanged.connect(self.modify)

class EtcPage(PageSwitch, V.Ui_etc):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.model = etcModel()
		self.setupTree()
		self.model.dataChanged.connect(self.modify)
		self.setWindowTitle(V.windowTitle_etc)

	def initUI(self): # 함수 연결
		self.clearBtn.clicked.connect(self.updateTree)
		self.addBtn.clicked.connect(self.add)
		self.deleteBtn.clicked.connect(self.delete)
		self.searchEnt.returnPressed.connect(self.search)
		self.searchBtn.clicked.connect(self.search)

	def setupTree(self):
		initTree(self, 'etc')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)
		self.tree.hideColumn(4)
		self.tree.hideColumn(5)
		self.tree.header().moveSection(6, 3)

	def updateTree(self):
		self.model = etcModel()
		initTree(self, 'etc')
		self.model.dataChanged.connect(self.modify)

	def add(self):
		window = NewProd(self, 'etc')

	def delete(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		try:
			del_data('etc', id)
			self.updateTree()
		except Exception as e:
			errorMsg(self, str(e))

	def modify(self, index):
		# Get ID from index
		row = index.row()
		col = index.column()
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())

		if col == 2:
			changed = self.model.itemFromIndex(self.model.index(row, col)).text()
			if not changed.isdigit():
				errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
				self.updateTree()
				return
			else:
				data = int(changed)
		elif col == 6:
			data = True if self.model.itemFromIndex(self.model.index(row, col)).checkState() == Qt.Checked else False
		else:
			data = self.model.itemFromIndex(self.model.index(row, col)).text()

		try:
			if col == 1:
				mod_prod(id, name=data)
			elif col == 2:
				mod_prod(id, price=data)
			elif col == 3:
				mod_prod(id, note=data)
			elif col == 6:
				mod_prod(id, available=data)
		except Exception as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))

		self.updateTree()

	def search(self):
		keyword = self.searchEnt.text()
		self.searchEnt.clear()

		if keyword == '':
			return

		self.model = etcModel(keyword=keyword)
		initTree(self, 'etc')
		self.model.dataChanged.connect(self.modify)

class CustPage(PageSwitch, V.Ui_cust):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.model = custModel()
		self.setupTree()
		self.model.dataChanged.connect(self.modify)
		self.setWindowTitle(V.windowTitle_cust)

	def initUI(self): # 함수 연결
		self.clearBtn.clicked.connect(self.updateTree)
		self.addBtn.clicked.connect(self.add)
		self.deleteBtn.clicked.connect(self.delete)
		self.recordBtn.clicked.connect(self.record)
		self.searchEnt.returnPressed.connect(self.search)
		self.searchBtn.clicked.connect(self.search)
		self.nameRBtn.setChecked(True)

	def setupTree(self):
		initTree(self, 'cust')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)
		self.tree.header().moveSection(6, 4)

	def updateTree(self):
		self.model = custModel()
		initTree(self, 'cust')
		self.model.dataChanged.connect(self.modify)

	def add(self):
		window = NewCust(self)

	def delete(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		try:
			del_data('cust', id)
			self.updateTree()
		except Exception as e:
			errorMsg(self, str(e))

	def modify(self, index):
		# Get ID from index
		row = index.row()
		col = index.column()
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())
		data = self.model.itemFromIndex(self.model.index(row, col)).text()

		if col == 1:
			mod_cust(id, name=data)
		elif col == 2:
			mod_cust(id, info=data)
		elif col == 4:
			mod_cust(id, address=data)
		elif col == 5:
			mod_cust(id, note=data)
		elif col == 3:
			try:
				mod_cust(id, phone=data)
			except Exception as e:
				errorMsg(self, str(e))

		self.updateTree()

	def search(self):
		keyword = self.searchEnt.text()
		self.searchEnt.clear()

		if keyword == '':
			return

		if self.nameRBtn.isChecked():
			option = 'name'
		elif self.phoneRBtn.isChecked():
			option = 'phone'

		self.model = custModel(keyword=keyword, search_option=option)
		initTree(self, 'cust')
		self.model.dataChanged.connect(self.modify)

	def record(self):
		row = self.tree.currentIndex().row()
		if row == -1:
			errorMsg(self, '삭제할 항목이 선택되지 않았습니다.')
			return
		id = int(self.model.itemFromIndex(self.model.index(row, 0)).text())

		window = CustRecord(self, id)


class ExtendedComboBox(QComboBox):
	def __init__(self, parent=None):
		super(ExtendedComboBox, self).__init__(parent)

		self.setFocusPolicy(Qt.StrongFocus)
		self.setEditable(True)

		# add a filter model to filter matching items
		self.pFilterModel = QSortFilterProxyModel(self)
		self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
		self.pFilterModel.setSourceModel(self.model())

		# add a completer, which uses the filter model
		self.completer = QCompleter(self.pFilterModel, self)
		# always show all (filtered) completions
		self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.setCompleter(self.completer)

		# connect signals
		self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)

class NewSale(QMainWindow, V.Ui_newSale):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent

		self.setupUi(self)
		self.setFixedSize(*V.newSale_size)
		self.setWindowTitle(V.windowTitle_newSale)

		self.initUI()

		self.showMaximized()

	def initUI(self):
		# Cust Model
		data = df['cust'].copy()
		custs = []
		for cust in data.values:
			ID = str(cust[0])
			name = cust[1]
			phone = cust[3]
			custs.append(name + '  ' + phone + '  |' + ID)

		# Cust ComboBox
		self.custCmbs = []
		for i in range(20):
			cmb = ExtendedComboBox(self.custFrame)
			cmb.resize(201, 20)
			cmb.move(0, 40*i)
			cmb.addItems(custs)
			cmb.setCurrentIndex(-1)
			self.custCmbs.append(cmb)

		# List Components
		self.yearCmbs = []
		self.monthCmbs = []
		self.dayCmbs = []
		self.pdBtns = []
		self.pdEnts = []
		self.pdIdList = [[]] * 20
		self.delivCmbs = []
		self.hsEnts = []
		self.bisEnts = []
		self.taxBoxes = []
		self.noteEnts = []
		v_int = QIntValidator()
		for i in range(1, 21):
			# exec(f'self.custCmbs.append(self.custCmb_{i})')
			exec(f'self.yearCmbs.append(self.yearCmb_{i})')
			exec(f'self.monthCmbs.append(self.monthCmb_{i})')
			exec(f'self.dayCmbs.append(self.dayCmb_{i})')
			exec(f'self.pdBtns.append(self.pdBtn_{i})')
			exec(f'self.pdEnts.append(self.pdEnt_{i})')
			exec(f'self.delivCmbs.append(self.delivCmb_{i})')
			exec(f'self.hsEnts.append(self.hsEnt_{i})')
			exec(f'self.bisEnts.append(self.bisEnt_{i})')
			exec(f'self.taxBoxes.append(self.taxBox_{i})')
			exec(f'self.noteEnts.append(self.noteEnt_{i})')

		# Slot Setting
		self.addBtn.clicked.connect(self.add)
		self.addCustBtn.clicked.connect(self.addCust)
		self.dateAllBtn.clicked.connect(self.dateAll)
		self.pdAllBtn.clicked.connect(self.pdAll)
		self.delivAllBtn.clicked.connect(self.delivAll)
		self.hsAllBtn.clicked.connect(self.hsAll)
		self.bisAllBtn.clicked.connect(self.bisAll)
		self.taxAllBtn.clicked.connect(self.taxAll)
		self.noteAllBtn.clicked.connect(self.noteAll)
		for i in range(20):
			self.pdBtns[i].clicked.connect(self.enterPd)

		# ComboBox/LineEdit Setting
		for i in range(20):
			# Years
			self.yearCmbs[i].addItems(V.years)
			self.yearCmbs[i].setCurrentIndex(-1)
			self.yearCmbs[i].setMaxVisibleItems(20)
			# Months
			self.monthCmbs[i].addItems(V.months)
			self.monthCmbs[i].setCurrentIndex(-1)
			self.monthCmbs[i].setMaxVisibleItems(13)
			# Days
			self.dayCmbs[i].addItems(V.days)
			self.dayCmbs[i].setCurrentIndex(-1)
			self.dayCmbs[i].setMaxVisibleItems(32)
			# Int Validator
			self.delivCmbs[i].setValidator(v_int)
			self.hsEnts[i].setValidator(v_int)
			self.bisEnts[i].setValidator(v_int)
		self.yearCmbs[0].setCurrentIndex(self.yearCmbs[0].findText(str(date.today().year)))
		self.monthCmbs[0].setCurrentIndex(self.monthCmbs[0].findText(str(date.today().month)))
		self.dayCmbs[0].setCurrentIndex(self.dayCmbs[0].findText(str(date.today().day)))

	def addCust(self):
		window = NewCust(self)

	def dateAll(self):
		idx_year = self.yearCmbs[0].currentIndex()
		idx_month = self.monthCmbs[0].currentIndex()
		idx_day = self.dayCmbs[0].currentIndex()
		for i in range(20):
			self.yearCmbs[i].setCurrentIndex(idx_year)
			self.monthCmbs[i].setCurrentIndex(idx_month)
			self.dayCmbs[i].setCurrentIndex(idx_day)

	def pdAll(self):
		data = self.pdIdList[0]
		idSet = set(data)
		findName = dict(df['prod'][['pd_id', 'pd_name']].values)
		result = []
		for ID in idSet:
			count = data.count(ID)
			if count == 1:
				result.append(findName[ID])
			else:
				result.append(findName[ID] + ' ' + str(count) + '병')
		for i in range(20):
			self.pdIdList[i] = data
			self.pdEnts[i].setText(', '.join(result))

	def delivAll(self):
		data = self.delivCmbs[0].currentText()
		for i in range(20):
			self.delivCmbs[i].setCurrentText(data)

	def hsAll(self):
		data = self.hsEnts[0].text()
		for i in range(20):
			self.hsEnts[i].setText(data)

	def bisAll(self):
		data = self.bisEnts[0].text()
		for i in range(20):
			self.bisEnts[i].setText(data)

	def taxAll(self):
		data = self.taxBoxes[0].isChecked()
		for i in range(20):
			self.taxBoxes[i].setChecked(data)

	def noteAll(self):
		data = self.noteEnts[0].text()
		for i in range(20):
			self.noteEnts[i].setText(data)

	def enterPd(self):
		idx = int(self.sender().objectName().split('_')[-1]) - 1
		window = SelectPd(self, idx)

	def add(self):
		addList = []
		for i in range(20):
			if not self.custCmbs[i].currentText():
				continue

			year_c = self.yearCmbs[i].currentIndex() != -1
			month_c = self.monthCmbs[i].currentIndex() != -1
			day_c = self.dayCmbs[i].currentIndex() != -1
			pd_c = self.pdIdList != []
			deliv_c = self.delivCmbs[i] != ''

			if year_c and month_c and day_c and pd_c and deliv_c:
				addList.append(i)
			else:
				errorMsg(self, '필수 요소를 빠짐없이 입력하세요.')
				return

		if addList == []:
			errorMsg(self, '아무것도 입력하지 않았습니다.')
			return
		else:
			for i in addList:
				if '|' not in self.custCmbs[i].currentText():
					errorMsg(self, '고객 입력에 오류가 있습니다.')
					return
			for i in addList:
				# Date Making
				year = self.yearCmbs[i].currentText()
				month = self.monthCmbs[i].currentText()
				day = self.dayCmbs[i].currentText()
				if int(month) < 10:
					month = '0' + month
				if int(day) < 10:
					day = '0' + day

				# Data
				cust_id = int(self.custCmbs[i].currentText().split('|')[-1])
				date = year + month + day
				deliv = int(self.delivCmbs[i].currentText())
				note = self.noteEnts[i].text()
				hs = int(self.hsEnts[i].text()) if self.hsEnts[i].text() else 0
				bis = int(self.bisEnts[i].text()) if self.bisEnts[i].text() else 0
				tax = self.taxBoxes[i].isChecked()
				pd_list = self.pdIdList[i]

				try:
					add_sale(cust_id, date, deliv, note, hs, bis, tax, pd_list)
					self.close()
					self.parent.model = saleModel(year=self.parent.viewYear.currentText(), month=self.parent.viewMonth.currentText())
					initTree(self.parent, 'sale')
					self.parent.model.dataChanged.connect(self.parent.modify)
					self.parent.sumColumn()
				except TypeError as e:
					errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))
				except Exception as e:
					errorMsg(self, str(e))

class SelectPd(QMainWindow, V.Ui_selectPd):
	def __init__(self, parent, sender_idx):
		super().__init__(parent)
		self.parent = parent
		self.idx = sender_idx

		self.setupUi(self)
		self.setFixedSize(*V.selectPd_size)
		self.setWindowTitle(V.windowTitle_selectPd)

		self.setComboBox()
		self.initComboBox()

		self.addBtn.clicked.connect(self.add)

		self.show()

	def setComboBox(self):
		self.set_dict = dict(df['prod'][df['prod']['pd_cat'] == 'set'][['pd_name', 'pd_id']].values)
		self.pd_dict = dict(df['prod'][(df['prod']['pd_cat'] == 'wine') | (df['prod']['pd_cat'] == 'etc')][['pd_name', 'pd_id']].values)

		self.wineCmbs = []
		self.countCmbs = []
		for i in range(12):
			exec(f'self.wineCmbs.append(self.wineCmb_{i+1})')
			exec(f'self.countCmbs.append(self.countCmb_{i+1})')
		self.wines_counts = list(zip(self.wineCmbs, self.countCmbs))
		
		# Fill ComboBox
		self.setCmb_1.addItems(self.set_dict.keys())
		self.setCmb_1.setCurrentIndex(-1)
		self.setCmb_1.setMaxVisibleItems(30)
		self.setCmb_2.addItems(self.set_dict.keys())
		self.setCmb_2.setCurrentIndex(-1)
		self.setCmb_2.setMaxVisibleItems(30)
		for i in range(12):
			self.wineCmbs[i].addItems(self.pd_dict.keys())
			self.wineCmbs[i].setCurrentIndex(-1)
			self.wineCmbs[i].setMaxVisibleItems(30)
			self.countCmbs[i].addItems([str(i) for i in range(13)])
			self.countCmbs[i].setMaxVisibleItems(13)

	def initComboBox(self):
		if self.parent.pdIdList[self.idx] == []:
			return
		
		pass # 상품 선택을 한 뒤 다시 버튼을 누르면 골랐던 상품을 콤보박스에 띄우고 싶지만 나중에 시도

	def add(self):
		self.parent.pdIdList[self.idx] = []

		if self.setCmb_1.currentText() != '':
			self.parent.pdIdList[self.idx].append(self.set_dict[self.setCmb_1.currentText()])
		if self.setCmb_2.currentText() != '':
			self.parent.pdIdList[self.idx].append(self.set_dict[self.setCmb_2.currentText()])
		
		for wine, count in self.wines_counts:
			if wine.currentText() != '' and count.currentText() != '':
				wine_id = self.pd_dict[wine.currentText()]
				wine_count = int(count.currentText())
				for _ in range(wine_count):
					self.parent.pdIdList[self.idx].append(wine_id)

		# Set LineEdit Text
		findName = dict(df['prod'][['pd_id', 'pd_name']].values)
		idList = self.parent.pdIdList[self.idx]
		idSet = set(idList)
		result = []
		for ID in idSet:
			count = idList.count(ID)
			if count == 1:
				result.append(findName[ID])
			else:
				result.append(findName[ID] + ' ' + str(count) + '병')
		self.parent.pdEnts[self.idx].setText(', '.join(result))

		self.close()

class NewSet(QMainWindow, V.Ui_newSet):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent

		self.setupUi(self)
		self.setFixedSize(*V.newSet_size)
		self.setWindowTitle(V.windowTitle_newSet)

		self.setComboBox()

		self.addBtn.clicked.connect(self.add)

		self.show()

	def setComboBox(self):
		self.wine_list = dict(make_wineTable()[['pd_name', 'pd_id']].values)

		self.wines = [self.wineCmb1, self.wineCmb2, self.wineCmb3, self.wineCmb4, self.wineCmb5, self.wineCmb6]
		self.counts = [self.countCmb1, self.countCmb2, self.countCmb3, self.countCmb4, self.countCmb5, self.countCmb6]
		self.wines_counts = list(zip(self.wines, self.counts))

		# Fill ComboBox
		self.yearCmb.addItems(V.years)
		self.monthCmb.addItems(V.months)
		self.yearCmb.setCurrentIndex(self.yearCmb.findText(str(date.today().year)))
		self.monthCmb.setCurrentIndex(self.monthCmb.findText(str(date.today().month)))

		# Fill Wines
		for wine, count in self.wines_counts:
			wine.addItems(self.wine_list.keys())
			wine.setCurrentIndex(-1)
			wine.setMaxVisibleItems(20)
			count.addItems([str(i) for i in range(13)])
			count.setMaxVisibleItems(13)

		# Fill Bonus
		self.bonusCmb.addItems(self.wine_list.keys())
		self.bonusCmb.setCurrentIndex(-1)

		# Int Validator
		self.priceEnt.setValidator(QIntValidator())

	def add(self):
		if self.nameEnt.text() == '':
			errorMsg(self, '이름을 입력하세요.')
			return
		if self.priceEnt.text() == '':
			errorMsg(self, '가격을 입력하세요.')
			return
		elif not self.priceEnt.text().isdigit():
			errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
			return

		name = self.nameEnt.text()
		price = int(self.priceEnt.text())
		note = self.noteEnt.text()
		if int(self.monthCmb.currentText()) < 10:
			date = self.yearCmb.currentText() + '0' + self.monthCmb.currentText() + '01'
		else:
			date = self.yearCmb.currentText() + self.monthCmb.currentText() + '01'

		result_wines = []
		for wine, count in self.wines_counts:
			if not (wine.currentText() == '' or count.currentText() == '0'):
				wine_id = int(self.wine_list[wine.currentText()])
				wine_count = int(count.currentText())
				for _ in range(wine_count):
					result_wines.append(wine_id)
		
		if not self.bonusCmb.currentText() == '':
			bonus_id = int(self.wine_list[self.bonusCmb.currentText()])
		else:
			bonus_id = -1

		try:
			add_set(name, price, note, date, result_wines, bonus_id)
			self.close()
			self.parent.model = setModel()
			initTree(self.parent, 'set')
			self.parent.model.dataChanged.connect(self.parent.modify)
		except TypeError as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))
		except Exception as e:
			errorMsg(self, str(e))

class ModSet(QMainWindow, V.Ui_modSet):
	def __init__(self, parent, target_id):
		super().__init__(parent)
		self.parent = parent
		self.id = target_id

		self.setupUi(self)
		self.setFixedSize(*V.modSet_size)
		self.setWindowTitle(V.windowTitle_modSet)

		self.setComboBox()

		self.modifyBtn.clicked.connect(self.modify)

		self.show()

	def setComboBox(self):
		wineTable = make_wineTable()
		self.name_id = dict(wineTable[['pd_name', 'pd_id']].values)
		self.id_name = dict(wineTable[['pd_id', 'pd_name']].values)

		self.wines = [self.wineCmb1, self.wineCmb2, self.wineCmb3, self.wineCmb4, self.wineCmb5, self.wineCmb6]
		self.counts = [self.countCmb1, self.countCmb2, self.countCmb3, self.countCmb4, self.countCmb5, self.countCmb6]
		self.wines_counts = list(zip(self.wines, self.counts))

		# Fill Dates
		self.yearCmb.addItems(V.years)
		self.monthCmb.addItems(V.months)
		setTable = make_setTable()
		date_idx = setTable[setTable['pd_id_x'] == self.id].index
		date = pd.to_datetime(setTable.loc[date_idx, 'pd_date'].values[0])
		self.yearCmb.setCurrentIndex(self.yearCmb.findText(str(date.year)))
		self.monthCmb.setCurrentIndex(self.monthCmb.findText(str(date.month)))

		# Fill Wines
		for wine, count in self.wines_counts:
			wine.addItems(self.name_id.keys())
			wine.setMaxVisibleItems(20)
			count.addItems([str(i) for i in range(13)])
			count.setMaxVisibleItems(13)

		# Fill Bonus
		self.bonusCmb.addItems(self.name_id.keys())

		# Set ComboBoxes
		swb = make_swbTable()
		idx = swb[swb['set_id'] == self.id].index
		wines_id = swb.loc[idx, 'wine_id_x'].values[0]
		wines_name = [self.id_name[id] for id in wines_id]

		dict_wine_count = {}
		set_wineName = set(wines_name)
		for wine in set_wineName:
			dict_wine_count[wine] = wines_name.count(wine)

		for i, (wine, count) in enumerate(dict_wine_count.items()):
			wine_idx = self.wines[i].findText(wine)
			if wine_idx == -1:
				errorMsg(self, '오류: 개발자에게 문의하세요.', '목록에서 와인을 찾을 수 없습니다.')
				self.close()
				return
			self.wines[i].setCurrentIndex(wine_idx)
			self.counts[i].setCurrentText(str(count))
		for i in range(len(dict_wine_count), 6):
			self.wines[i].setCurrentIndex(-1)
		
		bonus_id = swb.loc[idx, 'wine_id_y'].values[0]
		if not bonus_id == '':
			bonus_name = self.id_name[bonus_id]
			bonus_idx = self.bonusCmb.findText(bonus_name)
			if bonus_idx == -1:
				errorMsg(self, '오류: 개발자에게 문의하세요.', '목록에서 와인을 찾을 수 없습니다.')
				self.close()
				return
			self.bonusCmb.setCurrentIndex(bonus_idx)
		else:
			self.bonusCmb.setCurrentIndex(-1)

	def modify(self):
		if int(self.monthCmb.currentText()) < 10:
			date = self.yearCmb.currentText() + '0' + self.monthCmb.currentText() + '01'
		else:
			date = self.yearCmb.currentText() + self.monthCmb.currentText() + '01'

		result_wines = []
		for wine, count in self.wines_counts:
			if not (wine.currentText() == '' or count.currentText() == '0'):
				wine_id = int(self.name_id[wine.currentText()])
				wine_count = int(count.currentText())
				for _ in range(wine_count):
					result_wines.append(wine_id)
		
		if not self.bonusCmb.currentText() == '':
			bonus_id = int(self.name_id[self.bonusCmb.currentText()])
		else:
			bonus_id = -1

		try:
			mod_set(self.id, date=date, wine_list=result_wines, bonus_id=bonus_id)
			self.close()
			self.parent.model = setModel()
			initTree(self.parent, 'set')
			self.parent.model.dataChanged.connect(self.parent.modify)
		except TypeError as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))
		except Exception as e:
			errorMsg(self, str(e))

		self.parent.updateTree()

class NewProd(QMainWindow, V.Ui_newProd):
	def __init__(self, parent, category):
		super().__init__(parent)
		self.parent = parent
		self.category = category

		self.setupUi(self)
		self.setFixedSize(*V.newProd_size)
		self.setWindowTitle(V.windowTitle_newProd)

		self.addBtn.clicked.connect(self.add)
		self.priceEnt.setValidator(QIntValidator())

		self.show()

	def add(self):
		if self.nameEnt.text() == '':
			errorMsg(self, '이름을 입력하세요.')
			return
		if self.priceEnt.text() == '':
			errorMsg(self, '가격을 입력하세요.')
			return
		elif not self.priceEnt.text().isdigit():
			errorMsg(self, '가격에는 숫자만 입력할 수 있습니다.')
			return

		try:
			if self.category == 'wine':
				add_wine(self.nameEnt.text(), int(self.priceEnt.text()), self.noteEnt.toPlainText())
				self.close()
				self.parent.model = wineModel()
				initTree(self.parent, 'wine')
				self.parent.model.dataChanged.connect(self.parent.modify)
			elif self.category == 'etc':
				add_etc(self.nameEnt.text(), int(self.priceEnt.text()), self.noteEnt.toPlainText())
				self.close()
				self.parent.model = etcModel()
				initTree(self.parent, 'etc')
				self.parent.model.dataChanged.connect(self.parent.modify)
		except Exception as e:
			errorMsg(self, '오류: 개발자에게 문의하세요.', str(e))

class NewCust(QMainWindow, V.Ui_newCust):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent

		self.setupUi(self)
		self.setFixedSize(*V.newCust_size)
		self.setWindowTitle(V.windowTitle_newCust)

		self.addBtn.clicked.connect(self.add)
		self.searchBtn.clicked.connect(lambda: SearchAddr(self))

		self.show()

	def add(self):
		if self.nameEnt.text() == '' and self.phoneEnt.text() == '':
			errorMsg(self, '이름과 전화번호 중 하나는 반드시 입력되어야 합니다.')
			return
		try:
			add_cust(self.nameEnt.text(), self.infoEnt.text(), self.phoneEnt.text(), self.addr1Ent.toPlainText()+' '+self.addr2Ent.text(), self.noteEnt.toPlainText())
			self.close()
			if isinstance(self.parent, CustPage):
				self.parent.model = custModel()
				initTree(self.parent, 'cust')
				self.parent.model.dataChanged.connect(self.parent.modify)
		except Exception as e:
			errorMsg(self, str(e))

class CustRecord(QMainWindow, V.Ui_custRecord):
	def __init__(self, parent, cust_id):
		super().__init__(parent)

		self.setupUi(self)
		self.setFixedSize(*V.custRecord_size)
		self.setWindowTitle(V.windowTitle_custRecord)

		self.model = recordModel(cust_id)
		initTree(self, 'rec')
		self.tree.header().setDefaultAlignment(Qt.AlignCenter)

		self.show()

class SearchAddr(QMainWindow, V.Ui_searchAddr):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setupUi(self)
		self.setFixedSize(*V.searchAddr_size)
		self.setWindowTitle(V.windowTitle_searchAddr)

		self.searchEnt.returnPressed.connect(self.searchAddr)
		self.searchBtn.clicked.connect(self.searchAddr)
		self.list.itemDoubleClicked.connect(lambda: self.enterAddr(parent))

		self.show()

	def searchAddr(self):
		self.list.clear()

		url = 'http://www.juso.go.kr/addrlink/addrLinkApi.do'
		keyword = self.searchEnt.text()
		queryParams = '?' + urlencode({ quote_plus('currentPage') : '1' , quote_plus('countPerPage') : '1000', quote_plus('resultType') : 'json', quote_plus('keyword') : keyword, quote_plus('confmKey') : 'bGk3MHZtMWJ2anNkODIwMTQwOTEyMTg0NDI2' })

		request = Request(url + queryParams)
		request.get_method = lambda: 'GET'
		response_body = urlopen(request).read()

		root_json = json.loads(response_body)

		if root_json['results']['common']['errorCode'] != '0': # 에러가 발생한 경우
			errorMsg(self, root_json['results']['common']['errorMessage'])
		elif root_json['results']['juso'] == []: # 에러는 아니지만 검색 결과가 없는 경우
			errorMsg(self, '검색어를 확인해주세요.')
		else:
			result = []
			for child in root_json['results']['juso']:
				result.append(child['roadAddr'])
				result.append(child['jibunAddr'])
			self.list.addItems(result)

	def enterAddr(self, parent):
		parent.addr1Ent.setPlainText(self.list.currentItem().text())
		self.close()

class MainWindow(QMainWindow, V.Ui_menu):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		# 메뉴 셋업
		self.setupUi(self)
		self.menu_btns = {'sale': self.menu_sale, 'set': self.menu_set, 'wine': self.menu_wine, 'etc': self.menu_etc, 'cust': self.menu_cust}
		self.menu_sale.clicked.connect(lambda: self.goto('sale'))
		self.menu_set .clicked.connect(lambda: self.goto('set'))
		self.menu_wine.clicked.connect(lambda: self.goto('wine'))
		self.menu_etc .clicked.connect(lambda: self.goto('etc'))
		self.menu_cust.clicked.connect(lambda: self.goto('cust'))

		menuBtnStyle = '''
						QPushButton {
							color: rgb(255, 255, 255);
							border: 0px, solid;
						}
						QPushButton[curr_page = '1'] {
							background-color: rgb(0, 0, 0)
						}
						QPushButton[curr_page = '0'] {
							background-color: rgb(70, 70, 70);
						}
						QPushButton:hover {
							background-color: rgb(64, 86, 139);
						}
						'''

		for btn in self.menu_btns.values():
			btn.setStyleSheet(menuBtnStyle)

		# Stacked Widget 설정
		self.pages = {}

		self.register(SalePage(), 'sale')
		self.register( SetPage(), 'set')
		self.register(WinePage(), 'wine')
		self.register( EtcPage(), 'etc')
		self.register(CustPage(), 'cust')

		self.goto(V.HomePage)

		self.setGeometry(*V.mainwindow_geometry)
		# self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowIcon(QIcon(os.path.abspath('ui') + '\\wine.png'))
		self.showMaximized() ########################################################### 창 띄우기

	def register(self, widget, name):
		self.pages[name] = widget
		self.stacked_widget.addWidget(widget)
		if isinstance(widget, PageSwitch):
			widget.gotoSignal.connect(self.goto)

	@Slot(str)
	def goto(self, name):
		if name in self.pages:
			widget = self.pages[name]
			self.stacked_widget.setCurrentWidget(widget)
			self.setWindowTitle(widget.windowTitle())

			# CSS Setting / 현재 메뉴를 검정색으로 변경
			for btn in self.menu_btns.values():
				btn.setProperty('curr_page', '0')
			self.menu_btns[name].setProperty('curr_page', '1')
			for btn in self.menu_btns.values():
				btn.style().polish(btn)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())