#-*- coding: utf-8 -*-
import ask_util
import json
import os, sys
import re
import requests
import time

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

# if __name__ == '__main__':
# 	inter = ParkReview()
# 	print(inter.get("348910874"))
# 	review_list = inter.get("348910874")
# 	print(len(review_list))


	


