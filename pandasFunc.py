import os
import pandas as pd
import numpy as np
from datetime import date

filePath = os.path.abspath('data') + '\\'
fileName = {'sale': 'sale.csv',
			'prod': 'prod.csv',
			'cust': 'cust.csv',
			'sw'  : 's_w.csv',
			'sb'  : 's_b.csv',
			'sp'  : 's_p.csv'}

def readfile():
	global filePath
	global fileName

	df = {}

	dtype_sale = {'sale_id': np.int64, 'cust_id': np.int64, 'sale_deliv': np.int64, 'sale_hs': np.int64, 'sale_bis': np.int64, 'sale_tax': bool}
	dtype_prod = {'pd_id': np.int64, 'pd_price': np.int64, 'pd_cat': 'category', 'pd_avail': bool}
	dtype_cust = {'cust_id': np.int64}
	dtype_sw   = {'set_id': np.int64, 'wine_id': np.int64}
	dtype_sb   = {'set_id': np.int64, 'wine_id': np.int64}
	dtype_sp   = {'sale_id': np.int64, 'pd_id': np.int64}

	try:
		df['sale'] = pd.read_csv(filePath + fileName['sale'], sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_sale, parse_dates=['sale_date'])
		df['prod'] = pd.read_csv(filePath + fileName['prod'], sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_prod, parse_dates=['pd_date'])
		df['cust'] = pd.read_csv(filePath + fileName['cust'], sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_cust)
		df['sw']   = pd.read_csv(filePath + fileName['sw'],   sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_sw)
		df['sb']   = pd.read_csv(filePath + fileName['sb'],   sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_sb)
		df['sp']   = pd.read_csv(filePath + fileName['sp'],   sep='|', keep_default_na=False, encoding='CP949', dtype=dtype_sp)
		return df
	except:
		raise Exception('Failed to read CSV files.')

df = readfile()

def writefile():
	global filePath
	global fileName

	try:
		df['sale'].to_csv(filePath + fileName['sale'], sep='|', index=False, encoding='CP949')
		df['prod'].to_csv(filePath + fileName['prod'], sep='|', index=False, encoding='CP949')
		df['cust'].to_csv(filePath + fileName['cust'], sep='|', index=False, encoding='CP949')
		df['sw']  .to_csv(filePath + fileName['sw'],   sep='|', index=False, encoding='CP949')
		df['sb']  .to_csv(filePath + fileName['sb'],   sep='|', index=False, encoding='CP949')
		df['sp']  .to_csv(filePath + fileName['sp'],   sep='|', index=False, encoding='CP949')
	except:
		raise Exception('Failed to write CSV files.')

def list_pdname(string):
	if len(string) == 1:
		return string
	elif len(string) > 1:
		data = list(string)
		sett = set(data)
		result = ''
		for wine in sett:
			result += wine + ' ' + str(data.count(wine)) + '병, '
		return result[:-2]
	else:
		raise TypeError('Cannot join product names.')

def make_saleTable(record_option=None):
	sale_pd = pd.merge(df['sale'], df['sp'], on='sale_id')
	sale_pd = sale_pd.merge(df['prod'][['pd_id', 'pd_name', 'pd_price']], on='pd_id')
	sale_pd['pd_id'] = sale_pd['pd_id'].apply(str)
	sale_pd = sale_pd.groupby(['sale_id', 'cust_id', 'sale_date', 'sale_deliv', 'sale_note', 'sale_hs', 'sale_bis', 'sale_tax'], as_index=False)
	sale_pd = sale_pd.agg({'pd_id': ','.join, 'pd_name': list_pdname, 'pd_price': sum})
	if record_option == 1:
		return sale_pd
	else:
		sale_pd_cust = sale_pd.merge(df['cust'][['cust_id', 'cust_name', 'cust_info', 'cust_phone']], on='cust_id')
		return sale_pd_cust

def make_setTable(): # TODO make table중에 left join이 필요한 경우가 더 있나 찾아보고 수정하기 // 일단은 필요한 경우 없음
	set_list = df['prod'][df['prod']['pd_cat'] == 'set'].copy()
	set_wine = pd.merge(set_list, df['sw'], left_on='pd_id', right_on='set_id')
	set_wine = set_wine.merge(df['prod'][['pd_id', 'pd_name', 'pd_price']], left_on='wine_id', right_on='pd_id')
	set_wine['wine_id'] = set_wine['wine_id'].apply(str)
	set_wine = set_wine.groupby(['pd_id_x', 'pd_name_x', 'pd_price_x', 'pd_note', 'pd_date', 'pd_avail'], as_index=False)
	set_wine = set_wine.agg({'wine_id': ','.join, 'pd_name_y': list_pdname, 'pd_price_y': sum})
	set_wine = set_wine.merge(df['sb'], how='left', left_on='pd_id_x', right_on='set_id')
	set_wine = set_wine.merge(df['prod'][['pd_id', 'pd_name']], how='left', left_on='wine_id_y', right_on='pd_id').fillna('')
	set_wine = set_wine.drop(columns=['set_id', 'pd_id'])
	set_wine.sort_values(by='pd_date', ascending=False, inplace=True)
	return set_wine

def make_wineTable():
	wine_list = df['prod'][df['prod']['pd_cat'] == 'wine'].copy()
	wine_list.sort_values(by=['pd_avail', 'pd_id'], ascending=False, inplace=True)
	return wine_list

def make_etcTable():
	ect_list = df['prod'][df['prod']['pd_cat'] == 'etc'].copy()
	ect_list.sort_values(by=['pd_avail', 'pd_id'], ascending=False, inplace=True)
	return ect_list

def make_custTable():
	cust_list = df['cust'].copy()
	sale_pr = pd.merge(df['sale'][['sale_id', 'cust_id']], df['sp'], on='sale_id')
	sale_pr = sale_pr.merge(df['prod'][['pd_id', 'pd_price']], on='pd_id')
	cust_list['total'] = cust_list['cust_id'].apply(lambda x: sale_pr[sale_pr['cust_id'] == x]['pd_price'].sum())
	return cust_list

def make_swbTable():
	set_list = df['prod'][df['prod']['pd_cat'] == 'set'].copy()[['pd_id']]
	set_wine = pd.merge(set_list, df['sw'], left_on='pd_id', right_on='set_id')[['set_id', 'wine_id']]
	set_wine = set_wine.groupby(['set_id'], as_index=False)
	set_wine = set_wine.agg({'wine_id': list})
	set_wine_bonus = set_wine.merge(df['sb'], how='left', on='set_id').fillna('')
	return set_wine_bonus

def newId(df_name):
	col = {'sale': 'sale_id', 'prod': 'pd_id', 'cust': 'cust_id'}
	if not df_name in col.keys():
		raise NameError('Check df name.')
	else:
		lastindex = len(df[df_name]) - 1
		newId = df[df_name][col[df_name]].loc[lastindex] + 1
		return newId

def idxById(df_name, id):
	col = {'sale': 'sale_id', 'prod': 'pd_id', 'cust': 'cust_id'}
	if not df_name in col.keys():
		raise NameError('Check df name.')
	else:
		return df[df_name][df[df_name][col[df_name]] == id].index

def add_sale(cust_id: int, date, deliv: int, note, hs: int, bis: int, tax: bool, pd_list: list): # pd_list: list of ints
	# Parameter TypeError
	if not isinstance(cust_id, int):
		raise TypeError('add_sale cust ID TypeError')
	if not isinstance(deliv, int):
		raise TypeError('add_sale delivery cost TypeError')
	if not isinstance(hs, int):
		raise TypeError('add_sale HS TypeError')
	if not isinstance(bis, int):
		raise TypeError('add_sale BIS TypeError')
	if not isinstance(tax, bool):
		raise TypeError('add_sale tax TypeError')
	if not isinstance(pd_list, list):
		raise TypeError('add_sale product list TypeError')

	sale_id = newId('sale')
	data = [sale_id, cust_id, pd.to_datetime(date), deliv, note, hs, bis, tax]
	data = pd.DataFrame([data], columns=df['sale'].columns)
	df['sale'] = df['sale'].append(data, ignore_index=True)

	for ids in pd_list:
		df['sp'] = df['sp'].append(pd.DataFrame([[sale_id, ids]], columns=df['sp'].columns), ignore_index=True)

	writefile()

def mod_sale(id: int, date=None, deliv: int=None, note=None, hs: int=None, bis: int=None, tax: bool=None):
	# Parameter TypeError
	if id is not None and not isinstance(id, int):
		raise TypeError('mod_set sale ID TypeError')
	if deliv is not None and not isinstance(deliv, int):
		raise TypeError('mod_set delivery cost TypeError')
	if hs is not None and not isinstance(hs, int):
		raise TypeError('mod_set HS TypeError')
	if bis is not None and not isinstance(bis, int):
		raise TypeError('mod_set BIS TypeError')
	if tax is not None and not isinstance(tax, bool):
		raise TypeError('mod_set tax TypeError')

	idx = idxById('sale', id)

	if date is not None:
		df['sale'].loc[idx, 'sale_date'] = pd.to_datetime(date)
	if deliv is not None:
		df['sale'].loc[idx, 'sale_deliv'] = deliv
	if note is not None:
		df['sale'].loc[idx, 'sale_note'] = note
	if hs is not None:
		df['sale'].loc[idx, 'sale_hs'] = hs
	if bis is not None:
		df['sale'].loc[idx, 'sale_bis'] = bis
	if tax is not None:
		df['sale'].loc[idx, 'sale_tax'] = tax

	writefile()

def add_set(name, price: int, note, date, wine_list: list, bonus_id: int): # wine_list: list of ints
	# Parameter TypeError
	if not isinstance(price, int):
		raise TypeError('add_set price TypeError')
	if not isinstance(wine_list, list):
		raise TypeError('add_set wine list TypeError')
	if not isinstance(bonus_id, int):
		raise TypeError('add_set bonus ID TypeError')
	if len(wine_list) == 0:
		raise Exception('상품을 아무것도 선택하지 않았습니다.')

	set_id = newId('prod')
	data = [set_id, name, price, note, pd.to_datetime(date), 'set', True]
	data = pd.DataFrame([data], columns=df['prod'].columns)
	df['prod'] = df['prod'].append(data, ignore_index=True)

	for ids in wine_list:
		df['sw'] = df['sw'].append(pd.DataFrame([[set_id, ids]], columns=df['sw'].columns), ignore_index=True)

	if bonus_id != -1:
		df['sb'] = df['sb'].append(pd.DataFrame([[set_id, bonus_id]], columns=df['sb'].columns), ignore_index=True)

	writefile()

def mod_set(id, name=None, price: int=None, note=None, date=None, wine_list: list=None, bonus_id: int=None, available: bool=None):
	if price is not None and not isinstance(price, int):
		raise TypeError('mod_wine price TypeError')
	if wine_list is not None and not isinstance(wine_list, list):
		raise TypeError('mod_wine wine list TypeError')
	if bonus_id is not None and not isinstance(bonus_id, int):
		raise TypeError('mod_wine bonus ID TypeError')
	if available is not None and not isinstance(available, bool):
		raise TypeError('mod_wine available TypeError')
	if wine_list is not None and len(wine_list) == 0:
		raise Exception('상품을 아무것도 선택하지 않았습니다.')

	idx = idxById('prod', id)

	if name is not None:
		df['prod'].loc[idx, 'pd_name'] = name
	if price is not None:
		df['prod'].loc[idx, 'pd_price'] = price
	if note is not None:
		df['prod'].loc[idx, 'pd_note'] = note
	if date is not None:
		df['prod'].loc[idx, 'pd_date'] = pd.to_datetime(date)
	if available is not None:
		df['prod'].loc[idx, 'pd_avail'] = available

	if wine_list is not None:
		df['sw'] = df['sw'].drop(df['sw'][df['sw']['set_id'] == id].index)
		for ids in wine_list:
			df['sw'] = df['sw'].append(pd.DataFrame([[id, ids]], columns=df['sw'].columns), ignore_index=True)

	if bonus_id is not None and bonus_id != -1:
		df['sb'] = df['sb'].drop(df['sb'][df['sb']['set_id'] == id].index)
		df['sb'] = df['sb'].append(pd.DataFrame([[id, bonus_id]], columns=df['sb'].columns), ignore_index=True)

	writefile()

def add_wine(name, price: int, note):
	# Parameter TypeError
	if not isinstance(price, int):
		raise TypeError('add_wine price TypeError')

	data = [newId('prod'), name, price, note, date.today(), 'wine', True]
	data = pd.DataFrame([data], columns=df['prod'].columns)
	df['prod'] = df['prod'].append(data, ignore_index=True)

	writefile()

def add_etc(name, price: int, note):
	# Parameter TypeError
	if not isinstance(price, int):
		raise TypeError('add_etc price TypeError')

	data = [newId('prod'), name, price, note, date.today(), 'etc', True]
	data = pd.DataFrame([data], columns=df['prod'].columns)
	df['prod'] = df['prod'].append(data, ignore_index=True)

	writefile()

def mod_prod(id, name=None, price: int=None, note=None, available: bool=None):
	# Parameter TypeError
	if price is not None and not isinstance(price, int):
		raise TypeError('mod_prod price TypeError')
	if available is not None and not isinstance(available, bool):
		raise TypeError('mod_prod available TypeError')

	idx = idxById('prod', id)

	if name is not None:
		df['prod'].loc[idx, 'pd_name'] = name
	if price is not None:
		df['prod'].loc[idx, 'pd_price'] = price
	if note is not None:
		df['prod'].loc[idx, 'pd_note'] = note
	if available is not None:
		df['prod'].loc[idx, 'pd_avail'] = available

	writefile()

def add_cust(name, info, phone, address, note):
	if phone in list(df['cust']['cust_phone']):
		raise Exception('중복되는 전화번호가 있습니다.')

	data = [newId('cust'), name, info, phone, address, note]
	data = pd.DataFrame([data], columns=df['cust'].columns)
	df['cust'] = df['cust'].append(data, ignore_index=True)

	writefile()

def mod_cust(id, name=None, info=None, phone=None, address=None, note=None):
	idx = idxById('cust', id)

	if name is not None:
		df['cust'].loc[idx, 'cust_name'] = name
	if info is not None:
		df['cust'].loc[idx, 'cust_info'] = info
	if address is not None:
		df['cust'].loc[idx, 'cust_addr'] = address
	if note is not None:
		df['cust'].loc[idx, 'cust_note'] = note
	if phone is not None:
		if phone != df['cust'].loc[idx, 'cust_phone'].values[0]:
			if phone in list(df['cust']['cust_phone']):
				raise Exception('중복되는 전화번호가 있습니다.')
		df['cust'].loc[idx, 'cust_phone'] = phone

	writefile()

def del_data(page, id):
	# Sale Page
	if page == 'sale':
		del_idx = idxById('sale', id)
		df['sale'] = df['sale'].drop(del_idx)
		df['sp'] = df['sp'].drop(df['sp'][df['sp']['sale_id'] == id].index)

	# Set Page
	elif page == 'set':
		if id in list(df['sp']['pd_id']):
			raise Exception('상품이 판매내역과 연결되어 있어 삭제할 수 없습니다.')

		del_idx = idxById('prod', id)
		df['prod'] = df['prod'].drop(del_idx)
		df['sw'] = df['sw'].drop(df['sw'][df['sw']['set_id'] == id].index)
		df['sb'] = df['sb'].drop(df['sb'][df['sb']['set_id'] == id].index)

	# Wine Page
	elif page == 'wine':
		if id in list(df['sp']['pd_id']):
			raise Exception('상품이 판매내역과 연결되어 있어 삭제할 수 없습니다.')
		if id in list(df['sw']['wine_id']):
			raise Exception('상품이 세트와 연결되어 있어 삭제할 수 없습니다.')

		del_idx = idxById('prod', id)
		df['prod'] = df['prod'].drop(del_idx)

	# Etc Page
	elif page == 'etc':
		if id in list(df['sp']['pd_id']):
			raise Exception('상품이 판매내역과 연결되어 있어 삭제할 수 없습니다.')

		del_idx = idxById('prod', id)
		df['prod'] = df['prod'].drop(del_idx)

	# Cust Page
	elif page == 'cust':
		if id in list(df['sale']['cust_id']):
			raise Exception('고객이 판매내역과 연결되어 있어 삭제할 수 없습니다.')

		del_idx = idxById('cust', id)
		df['cust'] = df['cust'].drop(del_idx)

	else:
		raise Exception(f'{page}: 페이지 입력이 잘못되었습니다.')

	writefile()



# print(df['cust'])