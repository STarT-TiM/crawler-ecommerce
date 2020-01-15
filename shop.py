 # -*- coding: utf-8 -*-

import requests
from utils import shoppe
import mysql.connector
import configuration
import re

shop_id = 16376557

config = configuration.getConfig()

mysql_config = config['mysql']

mydb = mysql.connector.connect(
	host=mysql_config['host'],
	user=mysql_config['user'],
	passwd=mysql_config['passwd'],
	database=mysql_config['database']
)

mycursor = mydb.cursor()

mycursor.execute("SELECT shop_id FROM shop")
shop_indb = mycursor.fetchall()
shop_indb = [row[0] for row in shop_indb]

data = shoppe.getShop(shop_id)['data']

string_col = 'shopid, description, status, place, shop_location, item_count, rating_star, rating_good, rating_bad, follower_count, userid, account_id, ctime'
cols = [x.strip() for x in string_col.split(',')]

row = []
# neu da co trong database
if int(data['shopid']) not in shop_indb:

	data['name'] = re.sub('[\W]+',' ', data['name']).strip()
	data['description'] = re.sub('[\W]+',' ', data['description']).strip()
	data['account_id'] = data['account']['username']

	for col in cols:
		if col in data:
			row.append(data[col])
		else:
			row.append("")

	# Insert
	sql = "INSERT INTO shop (shop_id, description, status, place, shop_location, item_count, rating_star, rating_good, rating_bad, follower_count, user_id, account_id, create_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

	mycursor.execute(sql, row)
	mydb.commit()
	print(mycursor.rowcount, "was inserted.")
else:
	print('No insert')