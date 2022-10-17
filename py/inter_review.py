#-*- coding: utf-8 -*-
import ask_util
import json
import os, sys
import re
import requests
import time

from bs4 import BeautifulSoup

class ParkReview:	
	def get(self,prdNo):
		url = 'http://mbook.interpark.com/api/my/review/shortReviewList?sc.prdNo=%s&sc.page=1&sc.row=20' % prdNo		
		res = requests.get(url)
		#print(res.text)
		jsonData = res.json()
		#print(jsonData)
		review_list = []
		try:
			for item in jsonData['resData']['list']:
				if len(item['usedTitle']) < 3:
					continue

				star = item['avgScoreTot']
				reg_nm = item['usedMemNm']
				if len(reg_nm) ==3:
					reg_nm = reg_nm[:1]+"-"+reg_nm[2:]
				else:		
					reg_nm = reg_nm[:1]+"-"
				reg_dt = item['regDts']
				comment = ask_util.repl_excp(ask_util.getSqlReplace(item['usedTitle']))
				review_list.append({"star":star,"reg_nm":reg_nm,"reg_dt":reg_dt,"comment":comment})			
				# print("start %s, reg_nm %s, reg_dt %s, comment %s" %(star, reg_nm,reg_dt,comment))
		except Exception as e:
			print(e)

		return review_list

 # // 화면 view type code
 #        KbbJS.setOption('plugins.ui-product.type', "KOR")
 #        // 판매상품ID
 #        KbbJS.setOption('plugins.ui-product.pid', "S000061695026")
 #        // 결합상품 판매상품ID
 #        KbbJS.setOption('plugins.ui-product.combiSaleCode', "")
 #        // 상품코드(바코드)
 #        KbbJS.setOption('plugins.ui-product.barcode', "9791158741648")
 #        // 판매상품구분코드
 #        KbbJS.setOption('plugins.ui-product.salecode', "KOR")
 #        // 판매상품분류코드
 #        KbbJS.setOption('plugins.ui-product.saleClstCode', "150311")
 #        // 판매상품그룹구분코드
 #        KbbJS.setOption('plugins.ui-product.saleGrpCode', "SGK")
 #        // 판매상품 가격
 #        KbbJS.setOption('plugins.ui-product.salePrice', "16020")
 #        // 오픈마켓 입점사 ID
 #        KbbJS.setOption('plugins.ui-product.sellerId', "")
 #        // 오픈마켓 구성 ID
 #        KbbJS.setOption('plugins.ui-product.opnCode', "")
 #        // 상품 상세 접근시 최근 본 컨텐츠 추가
 #        KbbJS.addRecentlyContent({ catg: 'p', type: 'KOR', id: 'S000061695026' })
 #        // 판매제한연령
 #        KbbJS.setOption('plugins.ui-product.saleLmttAge', "0")
 #        // 컬처 구성상품 판매상품ID
 #        KbbJS.setOption('plugins.ui-product.cnfgSaleCmdtId', "")
 #        // 사은품 여부
 #        KbbJS.setOption('plugins.ui-product.isGifts', "N")
def kyouboBestInfo(url):			
	res  = requests.get(url, timeout=5)
	print("res ",res)
	print("res ",res.text)
	return res.json()
# url = 'https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/online?page=1&per=20&period=001&dsplDvsnCode=000&dsplTrgtDvsnCode=001'
# bookData = kyouboBestInfo(url)

def getBookInfoHtml(url):
	res  = requests.get(url, timeout=5)
	return BeautifulSoup(res.text, 'html.parser')

url2 = 'https://product.kyobobook.co.kr/detail/S000061695026'
bookDetailData = getBookInfoHtml(url2)
s = bookDetailData.select("div.basic_info tr")[0].text

print(s.find('ISBN'))
print(s.find('ISBN')==1)
print(s.find('ISBN')== -1)
if s.find('ISBN') > -1:	
	isbn = bookDetailData.select("div.basic_info tr td")[0].text
	print("isbn : ",isbn)
# print(s)
# print(s.select('tr'))
# product_detail_area basic_info
quit()
for i in bookData['data']['bestSeller']:	
	saleCmdtid 		= i['saleCmdtid']
	saleCmdtGrpDvsnCode 		= i['saleCmdtGrpDvsnCode']
	saleCmdtClstCode 		=i['saleCmdtClstCode']
	saleCmdtClstName = i['saleCmdtClstName']
	cmdtCode 	=i['cmdtCode']

	
	book_nm 		= i['cmdtName']
	description 	= i['inbukCntt']
	coverLargeUrl 	= ''
	coverSmallUrl 	= ''
	author 			= i['chrcName']
	isbn 			= ''
	link 			= ''
	translator 		= ''
	categoryName 	= ''
	publisher 			= i['pbcmName']
	pubDate 			= i['rlseDate']					
	price 			= i['price']
	price2 			= i['sapr'] #교보
	rwcnt 		 	= i['buyRevwRvgr'] #평점
	description2 =''
	print("{saleCmdtid : ",saleCmdtid)
	print('saleCmdtGrpDvsnCode',saleCmdtGrpDvsnCode)
	print('saleCmdtClstCode',saleCmdtClstCode)
	print('saleCmdtClstName',saleCmdtClstName)
	print('cmdtCode',cmdtCode)
	print('book_nm : ', book_nm)
	print('description : ', description)
	print('coverLargeUrl : ', coverLargeUrl)
	print('coverSmallUrl : ', coverSmallUrl)
	print('author : ', author)
	print('isbn : ', isbn)
	print('link : ', link)
	print('translator : ', translator)
	print('categoryName : ', categoryName)
	print('publisher : ', publisher)
	print('pubDate : ', pubDate)
	print('price : ', price)
	print('description2 : ', description2)
	print("===========================")

# if __name__ == '__main__':
# 	inter = ParkReview()
# 	print(inter.get("348910874"))
# 	review_list = inter.get("348910874")
# 	print(len(review_list))


	


