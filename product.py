 # -*- coding: utf-8 -*-

import requests
from utils import shoppe
import mysql.connector
import configuration
import re

category_id = 9824

config = configuration.getConfig()

mysql_config = config['mysql']

mydb = mysql.connector.connect(
	host=mysql_config['host'],
	user=mysql_config['user'],
	passwd=mysql_config['passwd'],
	database=mysql_config['database']
)

mycursor = mydb.cursor()

# lay id san pham da co trong he thong boi category_id 
# --> can where theo type shop
mycursor.execute("SELECT item_id FROM product WHERE category_id = " + str(category_id))
product_indb = mycursor.fetchall()
product_indb = [row[0] for row in product_indb]

data = shoppe.getProduct(category_id, 100)

items = data['items']

string_col = 'itemid, name, price_max, price_min, price_before_discount, price, liked_count, currency, brand, status, discount, ctime, catid, shopid'
cols = [x.strip() for x in string_col.split(',')]

result = []
for item in items:

	row = []
	# neu da co trong database
	if int(item['itemid']) in product_indb:
		continue

	item['name'] = re.sub('[\W]+',' ', item['name']).strip()
	for col in cols:
		if col in item:
			row.append(item[col])
		else:
			row.append("")

	result.append(row)

if len(result) > 0:
	# Insert
	sql = "INSERT INTO product (item_id, name, price_max, price_min, price_before_discount, price, liked_count, currency, brand, status, discount, create_time, category_id, shop_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

	mycursor.executemany(sql, result)
	mydb.commit()
	print(mycursor.rowcount, "was inserted.")
else:
	print('No insert')