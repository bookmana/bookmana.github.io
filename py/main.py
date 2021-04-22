#-*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ask_db
import ask_util
import json
import requests
import time
import urllib.request
import xml.etree.ElementTree as ET

from urllib.parse import parse_qs
from urllib.parse import urlparse

from inter_review import ParkReview

import make_book

#interpark_catid = ['207','208','209','210','211','214','215','216','217','201','200','203','205','206']
interpark_catid = []
interpark_catid.append('100') 	#국내도서
interpark_catid.append('101') 	#국내도서>소설
interpark_catid.append('102') 	#국내도서>시/에세이
interpark_catid.append('103') 	#국내도서>예술/대중문화
interpark_catid.append('104') 	#국내도서>사회과학
interpark_catid.append('105') 	#국내도서>역사와 문화
interpark_catid.append('107') 	#국내도서>잡지
interpark_catid.append('108') 	#국내도서>만화
interpark_catid.append('109') 	#국내도서>유아
interpark_catid.append('110') 	#국내도서>아동
interpark_catid.append('111') 	#국내도서>가정과 생활
interpark_catid.append('112') 	#국내도서>청소년
interpark_catid.append('113') 	#국내도서>초등학습서
interpark_catid.append('114') 	#국내도서>고등학습서
interpark_catid.append('115') 	#국내도서>국어/외국어/사전
interpark_catid.append('116') 	#국내도서>자연과 과학
interpark_catid.append('117') 	#국내도서>경제경영
interpark_catid.append('118') 	#국내도서>자기계발
interpark_catid.append('119') 	#국내도서>인문
interpark_catid.append('120') 	#국내도서>종교/역학
interpark_catid.append('122') 	#국내도서>컴퓨터/인터넷
interpark_catid.append('123') 	#국내도서>자격서/수험서
interpark_catid.append('124') 	#국내도서>취미/레저
interpark_catid.append('125') 	#국내도서>전공도서/대학교재
interpark_catid.append('126') 	#국내도서>건강/뷰티
interpark_catid.append('128') 	#국내도서>여행
interpark_catid.append('129') 	#국내도서>중등학습서
interpark_catid.append('200') 	#외국도서
interpark_catid.append('201') 	#외국도서>어린이
interpark_catid.append('203') 	#외국도서>ELT/사전
interpark_catid.append('205') 	#외국도서>문학
interpark_catid.append('206') 	#외국도서>경영/인문
interpark_catid.append('207') 	#외국도서>예술/디자인
interpark_catid.append('208') 	#외국도서>실용
interpark_catid.append('209') 	#외국도서>해외잡지
interpark_catid.append('210') 	#외국도서>대학교재/전문서적
interpark_catid.append('211') 	#외국도서>컴퓨터
interpark_catid.append('214') 	#외국도서>일본도서
interpark_catid.append('215') 	#외국도서>프랑스도서
interpark_catid.append('216') 	#외국도서>중국도서
interpark_catid.append('217') 	#외국도서>해외주문원서
book_code = {'100':'국내도서','101':'소설','102':'시-에세이','103':'예술-대중문화','104':'사회과학','105':'역사와문화','107':'잡지','108':'만화','109':'유아','110':'아동','111':'가정과생활','112':'청소년','113':'초등학습서','114':'고등학습서','115':'국어-외국어-사전','116':'자연과과학','117':'경제경영','118':'자기계발','119':'인문','120':'종교-역학','122':'컴퓨터-인터넷','123':'자격서-수험서','124':'취미-레저','125':'전공도서-대학교재','126':'건강-뷰티','128':'여행','129':'중등학습서','200':'외국도서','201':'어린이','203':'ELT-사전','205':'문학','206':'경영-인문','207':'예술-디자인','208':'실용','209':'해외잡지','210':'대학교재-전문서적','211':'컴퓨터','214':'일본도서','215':'프랑스도서','216':'중국도서','217':'해외주문원서'}

NV_CENTER_API = os.getenv('NV_CENTER_API')
PARK_API_KEY = os.getenv('PARK_API_KEY')
DB_INFO  = os.getenv('DB_INFO')


PARK_API_KEY = os.getenv('PARK_API_KEY')
nv_api_arr = NV_CENTER_API.split("|")	
NV_API_CID = nv_api_arr[0]
NV_API_SID = nv_api_arr[1]

dbinfo_arr = DB_INFO.split("|")
host=dbinfo_arr[0]
user=dbinfo_arr[1]
pw 	=dbinfo_arr[2]
db 	=dbinfo_arr[3]

def interParkBestSeller(catId):	
	web_url 		= "http://book.interpark.com/api/bestSeller.api?key="+PARK_API_KEY+"&categoryId="+catId
	#print("web_url : ",web_url)
	response 		= urllib.request.urlopen(web_url).read().decode('utf-8')
	#print(response)

	xtree 			= ET.fromstring(response)
	return xtree	

def bookManaOrderInsert(prdNo):
	sqlId = """ INSERT INTO BOOK_MANA_ORDER VALUES('%s')""" %(prdNo)
	print(sqlId)
	ad.insert(sqlId)

def isBookMana(prdNo):
	cnt = ad.selectOne(""" SELECT COUNT(*) FROM BOOK_MANA_ORDER WHERE PRD_NO ='%s' """ % prdNo)[0]
	if cnt==0:
		return False
	elif cnt>0:
		return True
	
def bookreviewInsert(prdNo):
	review_list = ParkReview().get(prdNo)
	if len(review_list) > 0:
		for review in review_list:
			star = review['star']
			reg_nm = review['reg_nm']
			reg_dt = review['reg_dt']
			comment = review['comment']
			sqlId = """ INSERT INTO BOOK_DESC VALUES('%s',%s,'%s','%s','%s')""" %(prdNo,star,reg_nm,reg_dt,comment)
			#print(sqlId)
			ad.insert(sqlId)



#네이버 책검색
def naverBookSearch(isbn):
	print("naverBookSearch start")
	encText = urllib.parse.quote("검색할 단어")
	url = "https://openapi.naver.com/v1/search/book_adv?d_isbn=" + isbn # json 결과		
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",NV_API_CID)
	request.add_header("X-Naver-Client-Secret",NV_API_SID)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	#print("rescode ",rescode)
	if(rescode==200):
	    response_body = response.read()		    
	    #print(type(response_body))
	    response_text = response_body.decode('utf-8')
	    #print(response_text)
	   

	    return json.loads(response_text)

	else:
	    print("Error Code:" + rescode)


if __name__  == "__main__":		
	ad = ask_db.AskDb(host, user, pw, db)
	for_cnt = 0
	cnt =0
	try:
		for ic in interpark_catid:
			for_cnt+=1
			inter_catId = ic
			print("inter_catId : ",inter_catId)			
			xtree = interParkBestSeller(inter_catId)
			book_cd1 = book_code[inter_catId]
			if inter_catId[:1]=='1':
				book_cd2 = "국내도서"
			else:
				book_cd2 = "외국도서"

			if xtree:				
				for node in xtree.findall('item'):
					cnt+=1
					print("cnt : ",str(cnt))					
					try:
						book_nm 		= node.find('title').text						
						description 	= node.find('description').text
						coverLargeUrl 	= node.find('coverLargeUrl').text
						coverSmallUrl 	= node.find('coverSmallUrl').text
						author 			= node.find('author').text
						isbn 			= node.find('isbn').text
						link 			= node.find('link').text
						translator 			= node.find('translator').text
						categoryName 			= node.find('categoryName').text
						publisher 			= node.find('publisher').text
						pubDate 			= node.find('pubDate').text						
						parts = urlparse(node.find('link').text) #http://book.interpark.com/blog/integration/product/itemDetail.rdo?prdNo=348910874&refererType=8305					
						prdNo = parse_qs(parts.query)['prdNo'][0] 
						price = node.find('priceStandard').text										
						description2 =''
						# print("isbn ",isbn)
						if isbn or not description:
							desc = naverBookSearch(isbn)['items'][0]['description']
							# print("naverBookSearch start")
							if desc:
								description2 = desc	
							if not description:
								description = "{} {}".format("● ",description2)
								description2 = ''
						# print('1 : ',description)
						# print('2 : ',author)
						# print('3 : ',isbn)

						if description:
							description = "{} {}".format("● ",description)

						if description and author and isbn:
							book_nm = ask_util.getSqlReplace(book_nm)
							description = ask_util.getSqlReplace(description)
							description2 = ask_util.getSqlReplace(description2)							
							print("insert ok gogo ",prdNo)
							print(isBookMana(prdNo))

							if not isBookMana(prdNo):
								bfo = {"PRD_NO":prdNo,"BOOK_NM":book_nm,"PRICE":price,"BOOK_DESC":description,"BOOK_DESC2":description2,"BOOK_IMG_L_URL":coverLargeUrl,
								"BOOK_IMG_S_URL":coverSmallUrl,"AUTHOR":author,"ISBN_NO":isbn,
								"CATEGORY_ID":ic,"CATEGORY_NM":categoryName,"PUB_SR":publisher,"PUB_DT":pubDate,
								"BOOK_CD1":book_cd1,"BOOK_CD2":book_cd2
								}
								
############################
								bookManaOrderInsert(prdNo)
								review_list = ParkReview().get(prdNo)
								make_book.create_book(bfo,review_list, for_cnt, cnt ) 
								if cnt > 30:
									quit()
								time.sleep(1)
###########################								
					except Exception as e:
						print(e)
						quit()
				# if for_cnt > 2:
				# 	break
	except Exception as e:		
		print(e)
		
		

	


"""
300 	음반>
301 	음반>가요
302 	음반>Pop
303 	음반>Rock
304 	음반>일본음악
305 	음반>World Music
306 	음반>Jazz
307 	음반>클래식
308 	음반>국악
309 	음반>뉴에이지/명상
310 	음반>O.S.T
311 	음반>종교음악
312 	음반>유아/아동/태교
313 	음반>수입음반
314 	음반>액세서리/관련상품
315 	음반>뮤직 DVD
314 	음반>액세서리/관련상품
315 	음반>뮤직 DVD
319 	음반>해외구매
320 	음반>LP
400 	DVD>
409 	DVD>애니메이션
411 	DVD>다큐멘터리
412 	DVD>TV시리즈
417 	DVD>건강/취미/스포츠
425 	DVD>영화
426 	DVD>해외구매
427 	DVD>기타
428 	DVD>블루레이
429 	DVD>유아동/교육DVD
430 	DVD>EBS 교육용
"""
#https://crontab.guru/
