# -*- coding: utf-8 -*- 
# 数据操作层

import sqlite3, models, datetime
from models import SellRecord, Product, Buyer

# 查询所有售出记录的sql语句
SQL_SELECT_SELLS = "select sell_record.uid, product_class, product_type, " \
				   "deal_unit_price, amount, buyer, deal_price, deal_date, paid, " \
				   "buyer_name from sell_record, buyer where sell_record.buyer = buyer.uid order by sell_record.uid"
# 插入售出记录
SQL_INSERT_SELL = "insert into sell_record (product_class, product_type, " \
				  "deal_unit_price, amount, buyer, deal_price, paid, deal_date) VALUES" \
				  "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
# 删除售出记录
SQL_DELETE_SELL = "delete from sell_record where uid = '%s'"
# 更新售出记录
SQL_UPDATE_SELL = "update sell_record set product_class = %s, product_type = '%s', " \
				  "deal_unit_price = %s, amount = %s, buyer = %s, deal_price = %s," \
				  "paid = %s, deal_date = '%s' where uid = %s" \

# 查询所有的产品信息
SQL_ALL_PRODUCT = "select class, type, length, width, height, per_weight, price from product"
# 插入产品数据
SQL_INSERT_PRODUCT = "insert into product (class, type, length, width, height, per_weight, price) VALUES "\
					 "(%s, '%s', %s, %s, %s, %s, %s)"
# 删除产品数据
SQL_DELETE_PRODUCT = "delete from product where class = %s and type = '%s'"
# 查询所有的买家
SQL_ALL_BUYERS = "select uid, buyer_name, phone1, phone2, phone3, email from buyer"
#更新买家数据
SQL_UPDATE_BUYER = "update buyer set buyer_name = '%s', phone1 = '%s', phone2 = '%s', phone3 = '%s', email = '%s' where uid = %s"
# 插入买家信息
SQL_INSERT_BUYER = "insert into buyer (buyer_name, phone1, phone2, phone3, email) VALUES ('%s', '%s', '%s', '%s', '%s')"
db_conn = sqlite3.connect("depot.sqlite")


def GetAllSellRecords():
	"""获取所有的售出记录"""
	db_cur    = db_conn.cursor()
	db_cur.execute(SQL_SELECT_SELLS)
	all_sells = {}
	for row in db_cur:
		rec                 = SellRecord()
		rec.uid             = str(row[0])
		rec.product_class   = str(row[1])
		rec.product_type    = row[2]
		rec.deal_unit_price = str(row[3])
		rec.amount          = str(row[4])
		rec.buyer           = str(row[5])
		rec.deal_price      = str(row[6])
		rec.deal_date       = row[7] # datetime.datetime.strptime(row[7], "%Y-%m-%d").strftime("%Y-%m-%d")
		rec.paid            = str(row[8])
		rec.buyer_name      = row[9]
		
		rec.total_price     = str(float(rec.deal_unit_price) * float(rec.amount))
		rec.unpaid          = str(float(rec.deal_price) - float(rec.paid))
		all_sells[rec.uid]  = rec

	return all_sells

def GetAllProducts():
	"""获取所有的产品数据"""
	db_cur    = db_conn.cursor()
	db_cur.execute(SQL_ALL_PRODUCT)
	all_products = {}
	for category in models.ALL_PRODUCT_TYPE.values():
		all_products[category] = {}
	for row in db_cur:
		rec            = Product()
		rec.category   = str(row[0])
		rec.type       = row[1]
		rec.length     = str(row[2])
		rec.width      = str(row[3])
		rec.height     = str(row[4])
		rec.per_weight = str(row[5])
		rec.price      = str(row[6])
		all_products[rec.category][rec.type] = rec
	return all_products

def GetAllBuyers():
	"""获取所有的买家数据"""
	db_cur    = db_conn.cursor()
	db_cur.execute(SQL_ALL_BUYERS)
	all_buyers = {}
	for row in db_cur:
		rec            = Buyer()
		rec.uid        = str(row[0])
		rec.buyer_name = row[1]
		rec.phone1     = row[2]
		rec.phone2     = row[3]
		rec.phone3     = row[4]
		rec.email      = row[5]

		all_buyers[rec.buyer_name] = rec
	return all_buyers

def InsertSellRecord(sell_rec):
	db_cur = db_conn.cursor()
	sql = SQL_INSERT_SELL % (sell_rec.product_class, 
							 sell_rec.product_type,
							 sell_rec.deal_unit_price,
							 sell_rec.amount,
							 sell_rec.buyer,
							 sell_rec.deal_price,
							 sell_rec.paid,
							 sell_rec.deal_date
							 )
	db_cur.execute(sql)
	db_conn.commit()
	db_cur = db_conn.cursor()
	db_cur.execute("select max(uid) from sell_record")
	sell_rec.uid = db_cur.next()[0]
	return sell_rec

def DeleteSellRecord(sell_uid):
	db_cur = db_conn.cursor()
	sql    = SQL_DELETE_SELL % (sell_uid)
	db_cur.execute(sql)
	db_conn.commit()

def UpdateSellRecord(sell_rec):
	db_cur = db_conn.cursor()
	sql    = SQL_UPDATE_SELL % (sell_rec.product_class, 
								sell_rec.product_type, 
								sell_rec.deal_unit_price,
								sell_rec.amount,
								sell_rec.buyer,
								sell_rec.deal_price,
								sell_rec.paid,
								sell_rec.deal_date,
								sell_rec.uid)
	db_cur.execute(sql)
	db_conn.commit()

def UpdateBuyer(buyer_rec):
	db_cur = db_conn.cursor()
	sql    = SQL_UPDATE_BUYER % (buyer_rec.buyer_name, 
								 buyer_rec.phone1, 
								 buyer_rec.phone2,
								 buyer_rec.phone3,
								 buyer_rec.buyer,
								 buyer_rec.email,
								 buyer_rec.uid)
	db_cur.execute(sql)
	db_conn.commit()

def InsertBuyer(buyer_rec):
	db_cur = db_conn.cursor()
	sql    = SQL_INSERT_BUYER % (buyer_rec.buyer_name, 
								 buyer_rec.phone1, 
								 buyer_rec.phone2,
								 buyer_rec.phone3,
								 buyer_rec.buyer,
								 buyer_rec.email)
	db_cur.execute(sql)
	db_conn.commit()	

def InsertProduct(product_rec):
	db_cur = db_conn.cursor()
	sql    = SQL_INSERT_PRODUCT % (product_rec.category, 
								   product_rec.type, 
								   product_rec.length,
								   product_rec.width,
								   product_rec.height,
								   product_rec.per_weight,
								   product_rec.price)
	db_cur.execute(sql)
	db_conn.commit()

def DeleteProduct(product_rec):
	db_cur = db_conn.cursor()
	sql    = SQL_DELETE_PRODUCT % (product_rec.category, product_rec.type)
	db_cur.execute(sql)
	db_conn.commit()
