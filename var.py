import os
from PySide6.QtUiTools import loadUiType

path = os.path.abspath('ui') + '\\'

Ui_menu = loadUiType(path + 'menu.ui')[0]
Ui_sale = loadUiType(path + 'page_sale.ui')[0]
Ui_set  = loadUiType(path + 'page_set.ui')[0]
Ui_wine = loadUiType(path + 'page_wine.ui')[0]
Ui_etc  = loadUiType(path + 'page_etc.ui')[0]
Ui_cust = loadUiType(path + 'page_cust.ui')[0]

Ui_newSale = loadUiType(path + 'window_newSale.ui')[0]
Ui_selectPd = loadUiType(path + 'window_selectPd.ui')[0]
Ui_newSet = loadUiType(path + 'window_newSet.ui')[0]
Ui_modSet = loadUiType(path + 'window_modSet.ui')[0]
Ui_newProd = loadUiType(path + 'window_newProd.ui')[0]
Ui_newCust = loadUiType(path + 'window_newCust.ui')[0]
Ui_custRecord = loadUiType(path + 'window_custRecord.ui')[0]
Ui_searchAddr = loadUiType(path + 'window_searchAddr.ui')[0]

newSale_size = (1921, 1000)
selectPd_size = (461, 580)
newSet_size = (441, 480)
modSet_size = (441, 390)
newProd_size = (281, 200)
newCust_size = (381, 285)
custRecord_size = (1301, 901)
searchAddr_size = (501, 450)

mainwindow_geometry = (0, 0, 1920, 1020)


windowTitle_sale = '해성와인 - 판매내역'
windowTitle_set  = '해성와인 - 세트목록'
windowTitle_wine = '해성와인 - 와인목록'
windowTitle_etc  = '해성와인 - 기타상품'
windowTitle_cust = '해성와인 - 고객명단'

windowTitle_newSale = '판매내역 추가'
windowTitle_selectPd = '상품 선택'
windowTitle_newSet = '세트 추가'
windowTitle_modSet = '날짜/구성/증정 수정'
windowTitle_newProd = '상품 추가'
windowTitle_newCust = '고객 추가'
windowTitle_custRecord = '구매 내역'
windowTitle_searchAddr = '주소 검색'

HomePage = 'sale'

sale = 'sale'
set  = 'set'
wine = 'wine'
etc  = 'etc'
cust = 'cust'

colSetting =   {
	sale:  ({'num':  0, 'width': 100, 'name': 'sale_id'},
			{'num':  1, 'width': 100, 'name': 'cust_id'},
			{'num':  2, 'width': 120, 'name': '날짜'},
			{'num':  3, 'width':  80, 'name': '택배비'},
			{'num':  4, 'width': 100, 'name': '비고'},
			{'num':  5, 'width':  80, 'name': '해성'},
			{'num':  6, 'width':  80, 'name': 'BIS'},
			{'num':  7, 'width':  50, 'name': '전세계'},
			{'num':  8, 'width': 100, 'name': 'pd_id'},
			{'num':  9, 'width': 500, 'name': '상품'},
			{'num': 10, 'width': 100, 'name': '가격'},
			{'num': 11, 'width': 100, 'name': '이름'},
			{'num': 12, 'width': 150, 'name': '설명'},
			{'num': 13, 'width': 120, 'name': '전화번호'},
			{'num': 14, 'width':  50, 'name': '번호'}),
	set:   ({'num':  0, 'width':  60, 'name': '상품번호'},
			{'num':  1, 'width': 200, 'name': '이름'},
			{'num':  2, 'width': 100, 'name': '가격'},
			{'num':  3, 'width': 100, 'name': '비고'},
			{'num':  4, 'width': 120, 'name': '날짜'},
			{'num':  5, 'width':  60, 'name': '판매중'},
			{'num':  6, 'width': 100, 'name': 'wine_id_x'},
			{'num':  7, 'width': 500, 'name': '구성'},
			{'num':  8, 'width': 100, 'name': '정가'},
			{'num':  9, 'width': 100, 'name': 'wine_id_y'},
			{'num': 10, 'width': 150, 'name': '보너스와인'}),
	wine:  ({'num':  0, 'width':  80, 'name': '상품번호'},
			{'num':  1, 'width': 300, 'name': '이름'},
			{'num':  2, 'width': 150, 'name': '가격'},
			{'num':  3, 'width': 100, 'name': '비고'},
			{'num':  4, 'width': 100, 'name': '날짜'},
			{'num':  5, 'width': 100, 'name': '분류'},
			{'num':  6, 'width':  60, 'name': '판매중'}),
	etc:   ({'num':  0, 'width':  80, 'name': '상품번호'},
			{'num':  1, 'width': 300, 'name': '이름'},
			{'num':  2, 'width': 150, 'name': '가격'},
			{'num':  3, 'width': 100, 'name': '비고'},
			{'num':  4, 'width': 100, 'name': '날짜'},
			{'num':  5, 'width': 100, 'name': '분류'},
			{'num':  6, 'width':  60, 'name': '판매중'}),
	cust:  ({'num':  0, 'width':  80, 'name': '고객번호'},
			{'num':  1, 'width': 100, 'name': '이름'},
			{'num':  2, 'width': 200, 'name': '설명'},
			{'num':  3, 'width': 150, 'name': '전화번호'},
			{'num':  4, 'width': 600, 'name': '주소'},
			{'num':  5, 'width': 100, 'name': '비고'},
			{'num':  6, 'width': 120, 'name': '총 구매금액'}),
	'rec': ({'num': 0, 'width':  50, 'name': '번호'},
			{'num': 1, 'width': 100, 'name': '날짜'},
			{'num': 2, 'width': 400, 'name': '상품'},
			{'num': 3, 'width':  80, 'name': '가격'},
			{'num': 4, 'width':  70, 'name': '택배비'},
			{'num': 5, 'width':  80, 'name': '해성'},
			{'num': 6, 'width':  80, 'name': 'BIS'},
			{'num': 7, 'width':  50, 'name': '전세계'},
			{'num': 8, 'width': 100, 'name': '비고'}),

	'alignment': {
		sale: {
			'center': (2, 7, 11, 13, 14),
			'right': (3, 5, 6, 10)},
		set: {
			'center': (0, 4, 5),
			'right': (2, 8)},
		wine: {
			'center': (0, 4, 6),
			'right': (2,)},
		etc: {
			'center': (0, 4, 6),
			'right': (2,)},
		cust: {
			'center': (0, 1, 3),
			'right': (6,)},
		'rec': {
			'center': (0, 1, 7),
			'right': (3, 4, 5, 6)}
	}
}

years = [str(year) for year in range(2017, 2031)]
months = [str(month) for month in range(1, 13)]
days =[str(day) for day in range(1, 32)]
months_0 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
days_0 = months_0 + [str(day) for day in range(13, 32)]