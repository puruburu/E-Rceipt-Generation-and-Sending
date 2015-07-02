from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time,re
import docx
from docx import table
import form_filling
import os
import convert_to_pdf

#print "Enter your email ID"
#email_id = raw_input(">>")
#print "Enter your password"
#password = getpass.getpass(">>")
def scrape_email(email_id,password):
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get("http://gmail.com")
	email = driver.find_element_by_id('Email')
	email.click()
	email.send_keys(email_id)
	email.send_keys(Keys.ENTER)


	time.sleep(2)
	passwd = driver.find_element_by_id('Passwd')
	passwd.click()
	passwd.send_keys(password)
	passwd.send_keys(Keys.ENTER)
	time.sleep(1)
	i=0
	while i==0:
		try:
			table_main = driver.find_element_by_id(":2f")
			i=1
		except:
			pass
	tbody = table_main.find_element_by_tag_name("tbody")
	rows = tbody.find_elements_by_tag_name("tr")
	time.sleep(1)
	results=[]
	for row in rows:
		test = row.text
		#print "email is \n" + test
		date=test.splitlines()[-1]
		requiredRegex = re.compile(r'sold for COEPMUN 2015')
		if requiredRegex.search(test)!=None:
			subList=[]
			subList.append(date)
			row.click()
			#extract email body
			nameRegex = re.compile(r'Name : (.+)')
			emailRegex = re.compile(r'Email : (.+)')
			j=0
			while j==0:
				try:
					email_body = driver.find_element_by_class_name('ii')
					j=1
				except:
					pass
			email_list = email_body.text.splitlines()
			for element in email_list:
				
				nameResults = nameRegex.search(element)
				emailResults = emailRegex.search(element)
				if nameResults!=None:
					subList.append(nameResults.group(1))
				if emailResults!=None:
					subList.append(emailResults.group(1))

			results.append(subList)

			driver.back()

	driver.close()
	return results


f = open('coep_mun.txt', 'r')
text = f.read()
split = text.splitlines()
email_id = split[0]
print email_id
password = split[1]
print password
data_obtained =  scrape_email(email_id, password)


for list_element in data_obtained:
	date = list_element[0]
	name = list_element[1]
	price = "1300"
	no = "1512000"
	form_filling.form_filling(date, name, price, no )
	convert_to_pdf.convert_to_pdf(filename)

