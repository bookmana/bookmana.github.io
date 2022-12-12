#-*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ask_db
import ask_util
import json
import requests
import time
import urllib.request

import string
import time

from bs4 import BeautifulSoup

import random
import tistory

# from inter_review import ParkReview

import make_book
import random
#interpark_catid = ['207','208','209','210','211','214','215','216','217','201','200','203','205','206']
book_code = {'100':'국내도서','101':'소설','102':'시-에세이','103':'예술-대중문화','104':'사회과학','105':'역사와문화','107':'잡지','108':'만화','109':'유아','110':'아동','111':'가정과생활','112':'청소년','113':'초등학습서','114':'고등학습서','115':'국어-외국어-사전','116':'자연과과학','117':'경제경영','118':'자기계발','119':'인문','120':'종교-역학','122':'컴퓨터-인터넷','123':'자격서-수험서','124':'취미-레저','125':'전공도서-대학교재','126':'건강-뷰티','128':'여행','129':'중등학습서','200':'외국도서','201':'어린이','203':'ELT-사전','205':'문학','206':'경영-인문','207':'예술-디자인','208':'실용','209':'해외잡지','210':'대학교재-전문서적','211':'컴퓨터','214':'일본도서','215':'프랑스도서','216':'중국도서','217':'해외주문원서'}

NV_CENTER_API = os.getenv('NV_CENTER_API')
nv_api_arr = NV_CENTER_API.split("|")	
NV_API_CID = nv_api_arr[0]
NV_API_SID = nv_api_arr[1]

DB_INFO = os.getenv('DB_INFO')
db_arr  = DB_INFO.split("|")
host	=db_arr[0]
user	=db_arr[1]
pw 		=db_arr[2]
db 		=db_arr[3]

def bookManaOrderInsert(isbn):
	sqlId = """ INSERT INTO BOOK_MANA_ORDER VALUES('%s',NOW())""" %(isbn)
	#print(sqlId)
	ad.insert(sqlId)

def isBookMana(isbn):
	return ad.selectOne(""" SELECT COUNT(*) FROM BOOK_MANA_ORDER WHERE ISBN ='%s' """ % isbn)[0]
	

#네이버 책검색
def naverBookSearch(isbn):
	try:
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
			response_text = response_body.decode('utf-8')
			jsonData = json.loads(response_text)
			return jsonData['items'][0]		    
		else:
		    print("Error Code:" + rescode)

	except Exception as e:
		raise e


def custUtil(f, nm):	
	try:
		return f[nm]
	except Exception as e:
		return ' '

def kbInfo(url):			
	res  = requests.get(url, timeout=25)	
	# print(res)
	return res.json()


def getRandom():
    return random.randrange(1,5)    


def kbDetailInfoGet(url):	
	res  = requests.get(url, timeout=25)	
	if res.status_code == 200:		
		return BeautifulSoup(res.text, 'html.parser')	

def getAscii():
	return random.choice(string.ascii_lowercase) 	

if __name__ == '__main__':		
	v_page = getRandom()
	print("v_page : ",v_page)
	url = f'https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/online?page={v_page}&per=100&period=001&dsplDvsnCode=000&dsplTrgtDvsnCode=001'
	ad = ask_db.AskDb(host, user, pw, db)
	try:	
		bookData = kbInfo(url)
		cnt = 0
		for i in bookData['data']['bestSeller']:
			# print("i ",i)		
			isbn 				= custUtil(i, 'cmdtCode') 
			if isBookMana(isbn) > 0:
				continue
			cnt+=1
			saleCmdtid 			= custUtil(i, 'saleCmdtid') #"saleCmdtid": "S000061863239",
			saleCmdtDvsnCode	= custUtil(i, 'saleCmdtDvsnCode')  #"saleCmdtDvsnCode": "KOR",	
			if 'KOR' in saleCmdtDvsnCode:
				book_cd1 = "국내도서"

			saleCmdtClstName	= custUtil(i, 'saleCmdtClstName') #"saleCmdtClstName": "경제전망",
			book_nm 			= custUtil(i, 'cmdtName') #"cmdtName": "트렌드 코리아 2023",
			desc 				= f'''● {custUtil(i, 'inbukCntt')}''' 
			author 				= custUtil(i, 'chrcName') #"chrcName": "김난도 외",	
			link_k 				= f'''https://product.kyobobook.co.kr/detail/{saleCmdtid}'''
			translator 			= ''
			categoryName 		= ''
			publisher 			= custUtil(i, 'pbcmName')
			pubDate 			= custUtil(i, 'rlseDate')					
			price 				= custUtil(i, 'price')
			price2 				= custUtil(i, 'sapr') #교보
			rwcnt 		 		= custUtil(i, 'buyRevwRvgr') #평점			
			coverLargeUrl 		= None
						
			try:
				descItem 			= naverBookSearch(isbn)
				description			=  f'''● {custUtil(descItem,'description')}'''  
				if not description:
					description = desc
				coverLargeUrl 		= custUtil(descItem,'image')
				coverSmallUrl 		= custUtil(descItem,'image')
				link_n				= custUtil(descItem,'link')

			except Exception as e:
				description = desc			
				print("nv e : ",e)
			
			link_c 				= ''
			book_cd2 			= saleCmdtClstName

			
			
			if description and author and isbn and coverLargeUrl:
				book_nm = ask_util.getSqlReplace(book_nm)				
				description = ask_util.repl_excp(ask_util.getSqlReplace(description))		

				description2 =''
				description3 =''
				try:
					soup = kbDetailInfoGet(f'https://product.kyobobook.co.kr/detail/{saleCmdtid}')
					for item in soup.select('div.prod_detail_contents_inner'):					
						description2 = item.select_one('div.book_publish_review p').text
						description3 = item.select_one('div.book_inside p').text
						# print("description2 : ",description2)
						# print("description3 : ",description3)
						# print("==============")
						break
					description2 = ask_util.repl_excp(ask_util.getSqlReplace(description2))
					description3 = ask_util.repl_excp(ask_util.getSqlReplace(description3))
				except Exception as e:
					description2 = ask_util.repl_excp(ask_util.getSqlReplace(description2))
					description3 = ask_util.repl_excp(ask_util.getSqlReplace(description3))
					print("kbDetailInfoGet e ",e)

					

				bfo = {"BOOK_NM":book_nm,"PRICE":price,"BOOK_DESC":description,"BOOK_IMG_L_URL":coverLargeUrl,
				"BOOK_IMG_S_URL":coverSmallUrl,"AUTHOR":author,"ISBN_NO":isbn,"PUB_SR":publisher,"PUB_DT":pubDate,"BOOK_CD1":book_cd1,"BOOK_CD2":book_cd2,
				"LINK_K":link_k,"LINK_N":link_n,"BOOK_DESC2":description2,"BOOK_DESC3":description3
				}							
				
				print("cnt : ", str(cnt)," ISBN_NO : ",isbn)
				bookManaOrderInsert(isbn)
				# review_list = ParkReview().get(isbn)
				review_list = []
				try:					
					reviewInfo = kbInfo(f'https://product.kyobobook.co.kr/api/review/list?page=1&pageLimit=30&reviewSort=001&revwPatrCode=000&saleCmdtid={saleCmdtid}')
					for info in reviewInfo['data']['reviewList']:
						try:
							review_list.append({"star":'',"reg_nm":f"{getAscii()}*******","reg_dt":info['cretDttm'],"comment":ask_util.repl_excp(ask_util.getSqlReplace(info['revwCntt']))})
						except Exception as e:
							print("for e: ",e)
						
				except Exception as e:
					print("review list ",e)
				if cnt == 1 or cnt == 15:
					tis = tistory.AutoTistory()
					tis.sendTistory(bfo, review_list)					

				else:
					quit()
					make_book.create_book(bfo, review_list, cnt ) 
			else:
				bookManaOrderInsert(isbn)		
			
			if cnt > 20:
				quit()

			time.sleep(1)
	except Exception as e:
		print("e99 : ",e)
	finally:
		ad.closeConn()
		



	#https://crontab.guru/

