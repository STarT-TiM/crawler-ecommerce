import requests
from bs4 import BeautifulSoup
import mysql.connector
import configuration

website = 'https://shoppe.com'

with open('file.category.html') as f:
	category_html = f.read()

start_index = category_html.find('<div class="shopee-page-wrapper">')
end_index = category_html.find('<div></div>')

sub_data = category_html[start_index:end_index]
soup = BeautifulSoup(sub_data)
# print(sub_data)

parent_cates = soup.findAll('div', {"class": "a-category--wrapper"})

result = []

for parent in parent_cates:

	parent_category = parent.find('a', {"class": "a-category__display-name"})
	name_parent_category = parent_category.getText()
	href_parent_category = parent_category['href']
	id_parent_category = href_parent_category[href_parent_category.find('.') + 1:]

	row = [id_parent_category, name_parent_category, website + href_parent_category, None, website]
	result.append(row)

	sub_category = parent.findAll('a', {"class": "a-sub-category--display-name"})

	for sub_cate in sub_category:
		name_sub_cate = sub_cate.getText()
		href_sub_cate = sub_cate['href']
		id_sub_cate = href_sub_cate[href_sub_cate.find(id_parent_category + ".") + len(id_parent_category) + 1:]

		row = [id_sub_cate, name_sub_cate, website + href_sub_cate, id_parent_category, website]
		result.append(row)

# print(result)

config = configuration.getConfig()

mysql_config = config['mysql']

mydb = mysql.connector.connect(
	host=mysql_config['host'],
	user=mysql_config['user'],
	passwd=mysql_config['passwd'],
	database=mysql_config['database']
)

mycursor = mydb.cursor()

sql = "INSERT INTO category (category_id, name, link, parent_id, website) VALUES (%s, %s, %s, %s, %s)"
mycursor.executemany(sql, result)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
