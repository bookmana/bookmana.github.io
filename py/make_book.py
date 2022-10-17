import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = "{}{}".format(BASE_DIR, TARGET_DIR)

def create_book(bfo, review_list, s_row):
	now = datetime.datetime.now()
	now = now+datetime.timedelta(minutes=(s_row*5))		
	# prd_no 			= bfo['PRD_NO']
	book_nm 		= bfo['BOOK_NM']
	price 			= bfo['PRICE']
	book_desc 		= bfo['BOOK_DESC']
	# book_desc2 		= bfo['BOOK_DESC2']
	book_img_l_url  = bfo['BOOK_IMG_L_URL']
	book_img_s_url  = bfo['BOOK_IMG_S_URL']
	link_k  		= bfo['LINK_K']
	link_n  		= bfo['LINK_N']
	link_c  		= bfo['LINK_C']
	

	try:
		book_img_l_url = book_img_l_url.replace("http:","https:")
		book_img_s_url = book_img_s_url.replace("http:","https:")
	except Exception as e:
		print(e)
		
	author 			= bfo['AUTHOR']
	isbn_no 		= bfo['ISBN_NO']
	# category_id 	= bfo['CATEGORY_ID']
	# category_nm 	= bfo['CATEGORY_NM']
	pub_sr 			= bfo['PUB_SR']
	pub_dt 			= bfo['PUB_DT']
	book_cd1		= bfo['BOOK_CD1']
	book_cd2		= bfo['BOOK_CD2']

	content = f'''---
title: "{book_nm}"
date: {now.strftime('%Y-%m-%d %H:%M:%S')}
categories: [{book_cd1} {book_cd2}]
image: {book_img_l_url}
description: {book_desc[:50]}...
---

## **정보**

- **ISBN : {isbn_no}**
- **출판사 : {pub_sr}**
- **출판일 : {pub_dt}**
- **저자 : {author}**

------



## **요약**

{book_desc}

------

#{book_nm}

[ 도서 구매 바로가기  [쿠팡]({link_c}) /  [교보문고]({link_k})  /  [네이버]({link_n})  ]
[쿠팡]:{link_c}
[교보문고]:{link_k}
[네이버]:{link_n}

'''
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
	file_path = f'''{FULL_PATH}/{now.strftime('%Y-%m-%d')}-{isbn_no}.md'''
	print("file_path : ",file_path)
	f = open(file_path ,'w', encoding='utf8')
	f.write(content)
