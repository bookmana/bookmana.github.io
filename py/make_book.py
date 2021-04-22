import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = "{}{}".format(BASE_DIR, TARGET_DIR)

def create_book(bfo, review_list,m_row, s_row):
	now = datetime.datetime.now()
	now = now+datetime.timedelta(minutes=(m_row*s_row*5))		
	prd_no 			= bfo['PRD_NO']
	book_nm 		= bfo['BOOK_NM']
	price 			= bfo['PRICE']
	book_desc 		= bfo['BOOK_DESC']
	book_desc2 		= bfo['BOOK_DESC2']
	book_img_l_url  = bfo['BOOK_IMG_L_URL']
	book_img_s_url  = bfo['BOOK_IMG_S_URL']

	try:
		book_img_l_url = book_img_l_url.replace("http:","https:")
		book_img_s_url = book_img_s_url.replace("http:","https:")
	except Exception as e:
		print(e)
		
	author 			= bfo['AUTHOR']
	isbn_no 		= bfo['ISBN_NO']
	category_id 	= bfo['CATEGORY_ID']
	category_nm 	= bfo['CATEGORY_NM']
	pub_sr 			= bfo['PUB_SR']
	pub_dt 			= bfo['PUB_DT']
	book_cd1		= bfo['BOOK_CD1']
	book_cd2		= bfo['BOOK_CD2']

	content = """---
title: "%s"
date: %s
categories: [%s, %s]
image: %s
description: %s
---

## **정보**

- **ISBN : %s**
- **출판사 : %s**
- **출판일 : %s**
- **저자 : %s**

------



## **요약**

%s

------

%s

------


%s 

------


""" %  (book_nm, "{} {}".format(now.strftime('%Y-%m-%d %H:%M:%S'),"+0900"), book_cd1, book_cd2, book_img_l_url, book_desc[:170] ,isbn_no ,pub_sr, pub_dt, author, book_desc, book_desc2, book_nm)
	#print(content)

	rv_comment =""
	if len(review_list) > 0:
		rv_comment = """## **리뷰** \n\n"""		
		for review in review_list:
			star = review['star']
			reg_nm = review['reg_nm']
			reg_dt = review['reg_dt']
			comment = review['comment']
			
			if comment.find("배송") > -1 or comment.find("주문") > -1:
				continue

			rv_comment+="""%s %s %s %s <br/>""" %( star,reg_nm,comment, reg_dt)
	
	content = content+rv_comment

	#print(content)
	file_path ="D:/gitpage_project/bookmana_action-main/_posts/%s-%s.md"%(now.strftime('%Y-%m-%d'),isbn_no)
	file_path = """%s/%s-%s.md""" %(FULL_PATH,now.strftime('%Y-%m-%d'),isbn_no)
	f = open(file_path ,'w', encoding='utf8')
	f.write(content)
