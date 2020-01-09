 # -*- coding: utf-8 -*-

import requests
from utils import shoppe
import mysql.connector
import configuration
import re

category_id = 9824
data = shoppe.getProduct(category_id, 100)

items = data['items']

string_col = 'itemid, name, price_max, price_min, price_before_discount, price, liked_count, currency, brand, status, discount, ctime, catid, shopid'
cols = [x.strip() for x in string_col.split(',')]

result = []
for item in items:

	row = []

	item['name'] = re.sub('[\W]+',' ', item['name']).strip()
	for col in cols:
		row.append(item[col])

	result.append(row)

# print(result)
# Insert
config = configuration.getConfig()

mysql_config = config['mysql']

mydb = mysql.connector.connect(
	host=mysql_config['host'],
	user=mysql_config['user'],
	passwd=mysql_config['passwd'],
	database=mysql_config['database']
)

mycursor = mydb.cursor()

sql = "INSERT INTO product (item_id, name, price_max, price_min, price_before_discount, price, liked_count, currency, brand, status, discount, create_time, category_id, shop_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

mycursor.executemany(sql, result)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
