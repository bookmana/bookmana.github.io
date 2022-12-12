import sys, os
import time
import urllib.request
import requests
import json
import re
# import sleepTime


class AutoTistory:
	def __init__(self, app_id, access_token, blog_nm):
		self.app_id = blog_nm
		self.access_token = access_token
		self.blog_nm =blog_nm
		self.bfo = {}
		self.review_list = []
		self.book_nm = ''
		self.content = ''
		self.category = '1103858'
		print(self.blog_nm, self.app_id, self.access_token)

	def sendImg(self, imgage_path):
		try:			
			print("imgage_path : ",imgage_path)			
			dir_path = '{}/img_{}.png'.format(os.path.dirname(__file__), str(round(time.time())) )
			urllib.request.urlretrieve(imgage_path,dir_path)
			# print("dir_path : ",dir_path)
			print("img_path : ",dir_path)
			url = "https://www.tistory.com/apis/post/attach"   
			data 		= {'access_token':self.access_token, 'blogName':self.blog_nm, 'output':'json'}
			files 		= {'uploadedfile': open(dir_path, 'rb') }
			print(files)		
			print("data",data)
			response 	= requests.post(url,  files=files, params=data)	
			rescode 	= response.status_code	
			print("rescode : ",rescode)
			print("response : ",response.text)
			print("response : ",response.content)
			
			if(rescode==200):	
				item = json.loads(response.text)
				print("item : ",item)
				return item["tistory"]["replacer"]
			else:
				print("img upload error",response.text)	
				print("response : ",response.json())			
				# sqlId = """UPDATE RSS_AUTO_TISTORY SET PROCESS_YN = 'X',PROCESS_DT = NOW() WHERE ACCESS_TOKEN 	= '%s' AND POST_URL = '%s' 
				# 		""" %( self.access_token, self.post_url)
				# self.ad.update(sqlId)

				return False
		except Exception as e:
			print("sendImg err :",e)
			# self.bot.sendMsg("tis setContent fail")
			return False

	def setContent(self):

		self.book_nm 		= self.bfo['BOOK_NM']
		price 			= self.bfo['PRICE']
		book_desc 		= self.bfo['BOOK_DESC']
		book_desc2 		= self.bfo['BOOK_DESC2']
		book_desc3		= self.bfo['BOOK_DESC3']
		# book_desc2 		= bfo['BOOK_DESC2']
		book_img_l_url  = self.bfo['BOOK_IMG_L_URL']
		book_img_s_url  = self.bfo['BOOK_IMG_S_URL']
		link_k  		= self.bfo['LINK_K']
		link_n  		= self.bfo['LINK_N']


		try:
			book_img_l_url = book_img_l_url.replace("http:","https:")
			book_img_s_url = book_img_s_url.replace("http:","https:")
		except Exception as e:
			print(e)
			
		author 			= self.bfo['AUTHOR']
		isbn_no 		= self.bfo['ISBN_NO']		
		pub_sr 			= self.bfo['PUB_SR']
		pub_dt 			= self.bfo['PUB_DT']
		book_cd1		= self.bfo['BOOK_CD1']
		book_cd2		= self.bfo['BOOK_CD2']

		
		try:
			img_url 	= self.sendImg(book_img_l_url)
			print("setContent start  ###########")
			if img_url:			
				width_idx = img_url.find("width=")
				img_text = img_url[:width_idx]+"alignCenter|"+img_url[width_idx:]

				contentData = ''
				contentData += f'''<h1> {self.book_nm}</h1>'''
				contentData += f'''<p> - {book_cd1} {book_cd2}</p>'''
				contentData += """<p>%s</p>""" % img_text.replace('##_1N','##_Image')
				contentData += f'''<br/><p> - ISBN : {isbn_no}</p> '''
				contentData += f'''<p> - 출판사 : {pub_sr}</p> '''
				contentData += f'''<p> - 출판일 : {pub_dt}</p> '''
				contentData += f'''<p> - 저자 : {author}</p> '''
				contentData += f'''<p style="border-top: 1px solid #7a583a;"> **요약** </p> '''				
				contentData += f'''<p> {book_desc2.replace('다.','다.<br/>')} </p> '''
				contentData += f'''<p style="border-top: 1px solid #7a583a;"> {book_desc.replace('다.','다.<br/>')} </p> '''
				contentData += f'''<p style="border-top: 1px solid #7a583a;"> {book_desc3.replace('다.','다.<br/>')} </p> '''
				if len(self.review_list) > 0:
					rv_comment = '''<p style="border-top: 1px solid #7a583a;"> 리뷰</p> '''
					for review in self.review_list:
						star = review['star']
						reg_nm = review['reg_nm']
						reg_dt = review['reg_dt']
						comment = review['comment']
						
						if comment.find("배송") > -1 or comment.find("주문") > -1:
							continue

						rv_comment+=f'''  {reg_nm} {comment} {reg_dt} <br/>'''
				
				self.content = contentData + (rv_comment.replace('다.','다.<br/>').replace('요.','요.<br/>'))
				
				print("setContent end     ###########")
				return True
			else:
				return False

		except Exception as e:
			print("setContent : ",e)
			# self.bot.sendMsg("tis setContent fail")
			return False
	
	def send(self):
		try:		
			title = urllib.parse.quote(self.book_nm)
			contents = urllib.parse.quote(self.content)	
			tag = urllib.parse.quote(self.book_nm )	

			url = "https://www.tistory.com/apis/post/write?"
			data = "access_token="+self.access_token
			data +="&output=json"
			data +="&blogName="+self.blog_nm
			data +="&title="+title
			data +="&content="+contents
			data +="&visibility=3"
			data +="&category="+self.category
			data +="&tag="+tag
			# print("data : ", data)
			
		except Exception as e:						
			print("send setData error : ",e)
			return False

		try:
			request = urllib.request.Request(url, data=data.encode("utf-8"))	
			response = urllib.request.urlopen(request)
			print(response)	
			rescode = response.getcode()
			if(rescode==200):		
				response_body = response.read().decode('utf-8')								
				return response_body
			else:				
				print("Error Code:" + rescode, response.json())
				return False
		except urllib.error.URLError as ue:						
			print("exception urllib.error.URLErro :",ue)	
		except Exception as e:
			print(e)
			return False

	def sendTistory(self, bfo, review_list):
		self.bfo = bfo
		self.review_list = review_list
		print("setcontent start")
		isContent = self.setContent()
		print("isContent : ",isContent)
		if isContent:
			# print(self.content)						
			try:
				print("sendTistory start ###########")
				response = self.send()
				print("sendTistory end ###########")
				if response:
					jsonData = json.loads(response)
					print("send rtn status ", jsonData['tistory']['status']) 
					if jsonData['tistory']['status'] == '200':
						self.tis_post_url = jsonData['tistory']['url']
						print("send ok %s" % self.blog_nm )
					else:
						print("send fail %s" % self.blog_nm )
			except Exception as e:
				print("e : ",e)		
		else:			
			print("content 발송 실패")




	def list_of_Category(self):
		url = "https://www.tistory.com/apis/category/list"

		params = {
			'access_token': self.access_token,
			'output': 'json', # json, xml 두 가지 형식 지원
			'blogName': self.blog_nm   # ().tistory.com 또는 블로그 주소 전체
		}
		
		res = requests.get(url, params=params)

		if res.status_code == 200:
			res_json = res.json()
			print(res_json)
# 1103858
if __name__ == '__main__':
	tis = AutoTistory()
	tis.list_of_Category()
# 	tis.setContent()
# 	# sendImg('https://shopping-phinf.pstatic.net/main_3246336/32463366149.20221019151105.jpg')