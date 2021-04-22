import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = "{}{}".format(BASE_DIR, TARGET_DIR)

def create_book(bfo, review_list, row):
	now = datetime.datetime.now()
	print("now : ",now)
	print( "{} {}".format(now.strftime('%Y-%m-%d %H:%M:%S'),"+0900"))
	prd_no 			= bfo['PRD_NO']
	book_nm 		= bfo['BOOK_NM']
	price 			= bfo['PRICE']
	book_desc 		= bfo['BOOK_DESC']
	book_desc2 		= bfo['BOOK_DESC2']
	book_img_l_url  = bfo['BOOK_IMG_L_URL']
	book_img_s_url  = bfo['BOOK_IMG_S_URL']
	author 			= bfo['AUTHOR']
	isbn_no 		= bfo['ISBN_NO']
	category_id 	= bfo['CATEGORY_ID']
	category_nm 	= bfo['CATEGORY_NM']
	pub_sr 			= bfo['PUB_SR']
	pub_dt 			= bfo['PUB_DT']
	book_cd1		= bfo['BOOK_CD1']
	book_cd2		= bfo['BOOK_CD2']
	

	print('prd_no : ',prd_no)
	print('book_nm : ',book_nm)
	print('price : ',price)
	print('book_desc : ',book_desc)
	print('book_desc2 : ',book_desc2)
	print('book_img_l_url : ',book_img_l_url)
	print('book_img_s_url : ',book_img_s_url)
	print('author : ',author)
	print('isbn_no : ',isbn_no)
	print('category_id : ',category_id)
	print('category_nm : ',category_nm)
	print('pub_sr : ',pub_sr)
	print('pub_dt : ',pub_dt)

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
	print(content)

	


	rv_comment =""
	if len(review_list) > 0:
		rv_comment = """## **리뷰** \n\n"""		
		for review in review_list:
			star = review['star']
			reg_nm = review['reg_nm']
			reg_dt = review['reg_dt']
			comment = review['comment']
			rv_comment+="""%s %s %s %s <br/>""" %( star,reg_nm,comment, reg_dt)
	
	content = content+rv_comment

	print(content)
	file_path ="D:/gitpage_project/bookmana_action-main/_posts/%s-%s.md"%(now.strftime('%Y-%m-%d'),isbn_no)
	file_path = """%s/%s-%s.md""" %(FULL_PATH,now.strftime('%Y-%m-%d'),isbn_no)
	f = open(file_path ,'w', encoding='utf8')
	#f = open("./_posts/%s-%s.md"%(now.strftime('%Y-%m-%d'),isbn_no) ,'w', encoding='utf8')
	f.write(content)

# if __name__ == '__main__':
# 	now = datetime.datetime.now()	
# 	print(now.strftime('%Y-%m-%d %H:%M:%S'))
# 	print()
# 	
