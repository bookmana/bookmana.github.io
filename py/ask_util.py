#-*-coding:utf-8
import datetime
import os, sys
import random
import re
import time

def dirSearch(dirname,file_name, root_path):
    filenames = os.listdir(dirname)
    # print(filenames)
    for filename in filenames:
        if filename == "askmarket_google.json":
            return os.path.join(root_path,os.path.join(dirname, filename))


def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)    

#문자열에서 숫자을 찾아 return
def getNumberFrom(str):
    return int("".join(re.findall("\\d+", str)))

def numTOwon(arg):	
	if str(type(arg)) == "<class 'int'>":		
		amount = str(arg)
	elif str(type(arg)) =="<class 'str'>":
		amount = arg.replace(',','')	
	else:
		amount = arg

	if int(amount) > 99999999:
	# print amount[0:-8],'억',amount[-8:-4],'만',amount[-4:], '원' 
		return '{0}억{1}만{2}원'.format(amount[0:-8], amount[-8:-4], amount[-4:]) 
	elif int(amount) > 9999:
	# print amount[-8:-4],'만',amount[-4:], '원' 
		return '{0}만{1}원'.format(amount[-8:-4], amount[-4:]) 
	else:
	# print amount[-4:],'원'
		return '{0}원'.format(amount[-4:])

def money(s):
	return "{:,}".format(s)

def utilTrim(s):
	pat = re.compile(r'\s+') 	
	return pat.sub('',s)

def getRandom(int1, int2):
	return random.randrange(int1,int2)

def getSqlReplace(str):
	return re.sub("\'", "",str)

def allSpacilChange(str):
	return re.sub('[^가-힝0-9a-zA-Z\\s]', '', str)
def getToDay():
	return datetime.datetime.today().strftime("%Y년%m월%d일")

def clearTitle(title_nm):
	isChange =False
	tit_nm = title_nm
	tit_len = title_nm.find(",")

	if tit_len > -1:
		tit_nm = title_nm[:tit_len]
		isChange = True
		
	tit_len2 = tit_nm.find("+")
			
	if tit_len2 > -1:
		tit_nm = tit_nm[:tit_len2]
		isChange =True
		
	if isChange:
		tit_nm +="..."
		#print(tit_nm)
		
	if len(tit_nm) > 60:
		#print(len(tit_nm))
		tit_nm = tit_nm[:  getRandom(57,len(tit_nm)-3)]+"..."		
	return tit_nm

def clearTitleTag(title_nm):
	tit_nm = title_nm
	tit_len = title_nm.find(",")

	if tit_len > -1:
		tit_nm = title_nm[:tit_len]
		isChange = True
		
	tit_len2 = tit_nm.find("+")
			
	if tit_len2 > -1:
		tit_nm = tit_nm[:tit_len2]
		isChange =True
					
	if len(tit_nm) > 40:
		#print(len(tit_nm))
		tit_nm = tit_nm[:  getRandom(37,len(tit_nm)-3)]	

	return getSqlReplace(tit_nm)

def clearXYZ(title_nm):
	pattern = re.compile(r'\s\s+')
	oldChars = '[]+/,*<>()^%$#@&=~}{_`|-\"'
	newChars = '                           '	
	n = title_nm.translate({ ord(x): y for (x, y) in zip(oldChars, newChars) })	
	rtn = re.sub(pattern,' ', n)	
	return rtn
	
def getContentTag(title_nm):	
	rtn = ''
	tag_nm = "#"+clearXYZ(getSqlReplace(str(title_nm))).strip().replace(' ', ' #')
	tag_list = tag_nm.split(' ')
	print(tag_list)
	s1 = set(tag_list)

	for i in list(s1):
		rtn+=i+" "

	return rtn

def dictFind(str, dictParam):
	return str in dictParam

def replaceBookDesc(book_text):
	isNo1 = book_text.find('1.')
	isNo2 = book_text.find('2.')
	isNo3 = book_text.find('3.')
	isNo4 = book_text.find('4.')
	isNo5 = book_text.find('5.')
	isNo6 = book_text.find('6.')
	isNo7 = book_text.find('7.')

	if isNo1 > -1 and isNo2 > -1:
		book_text = book_text.replace("1.","99999 ▶ ")
		book_text = book_text.replace("2.","99999 ▶ ")
		if isNo3 > -1:
			book_text = book_text.replace("3.","99999 ▶ ")
		if isNo4 > -1:
			book_text = book_text.replace("4.","99999 ▶ ")
		if isNo5 > -1:
			book_text = book_text.replace("5.","99999 ▶ ")
		if isNo6 > -1:
			book_text = book_text.replace("6.","99999 ▶ ")
		if isNo7 > -1:
			book_text = book_text.replace("7.","99999 ▶ ")	
	
	if book_text.find('&lt;') > -1:
		hi_max_cnt = book_text.count("&lt;")
		#print(hi_max_cnt)
		book_text = book_text.replace("&lt;","<",hi_max_cnt)	
	
	if book_text.find('&gt;') > -1:
		hi_max_cnt = book_text.count("&gt;")
		#print(hi_max_cnt)
		book_text = book_text.replace("&gt;",">",hi_max_cnt)	
	
	# if book_text.find('&') > -1:
	# 	and_max_cnt = book_text.count("&")
	# 	#print(hi_max_cnt)
	# 	book_text = book_text.replace("&"," and ",and_max_cnt)

	if book_text.find('-') > -1:
		hi_max_cnt = book_text.count("-")
		#print(hi_max_cnt)
		book_text = book_text.replace("-","99999 -",hi_max_cnt)	

	if book_text.find('·') > -1:
		rd_max_cnt = book_text.count("﻿·")
		#print(rd_max_cnt)
		book_text = book_text.replace("﻿·","99999 ﻿·",rd_max_cnt)
		
	simple_max_cnt = 0
	# print(type(book_text))
	# print(book_text.find('.') > -1)
	# print( re.findall('.', book_text))
	# print( book_text.count("1"))
	# print( book_text.count("﻿."))
	if book_text.find('...') > -1:
		simple_max_cnt +=1
		temp1 = book_text[:book_text.find('...')]+"88888 99999"
		temp2 = book_text[book_text.find('...')+3:]
		#print(book_text2)
		book_text = temp1+temp2		
		if book_text.find('...') > -1:
			simple_max_cnt +=1
			temp3 = book_text[:book_text.find('...')]+"88888 99999"
			temp4 = book_text[book_text.find('...')+3:]
			#print(book_text2)
			book_text = temp3+temp4			
			if book_text.find('...') > -1:
				simple_max_cnt +=1
				temp5 = book_text[:book_text.find('...')]+"88888 99999"
				temp6 = book_text[book_text.find('...')+3:]
				#print(book_text2)
				book_text = temp5+temp6
				if book_text.find('...') > -1:
					simple_max_cnt +=1
					temp7 = book_text[:book_text.find('...')]+"88888 99999"
					temp8 = book_text[book_text.find('...')+3:]
					#print(book_text2)
					book_text = temp7+temp8
	
	if book_text.find(".") > -1:
		point_max_cnt = book_text.count(".")
		#print(point_max_cnt)
		book_text = book_text.replace(".",".99999",point_max_cnt)

	three_max_cnt = 0
	if book_text.find("★★★") > -1:
		three_max_cnt = book_text.count("★★★")
		#print("three_max_cnt : ",three_max_cnt)
		book_text = book_text.replace("★★★",".99999 77777",three_max_cnt)

	if book_text.find("★") > -1:
		star_max_cnt = book_text.count("★")
		book_text = book_text.replace("★",".99999 ★",star_max_cnt)



	if simple_max_cnt > 0:
		print(book_text)
		print("simple_max_cnt : ",simple_max_cnt)		
		book_text = book_text.replace("88888","...",simple_max_cnt)

	if three_max_cnt > 0:
		book_text = book_text.replace("77777","★★★",three_max_cnt)

	return book_text

def repl_under(str):
	return re.sub("_", "",str)


def repl_excp(repl_text):
	if repl_text.find('_') > -1:		
		repl_text = repl_under(repl_text)
	if repl_text.find('‘') > -1:
		rd_max_cnt = repl_text.count("‘")
		repl_text = repl_text.replace("‘","",rd_max_cnt)
	if repl_text.find('’') > -1:
		rd_max_cnt = repl_text.count("’")
		repl_text = repl_text.replace("’","",rd_max_cnt)
	if repl_text.find('『') > -1:
		rd_max_cnt = repl_text.count("『")
		repl_text = repl_text.replace("『","",rd_max_cnt)
	if repl_text.find('』') > -1:
		rd_max_cnt = repl_text.count("』")
		repl_text = repl_text.replace("』","",rd_max_cnt)	
		
	if repl_text.find('°') > -1:
		rd_max_cnt = repl_text.count("°")
		repl_text = repl_text.replace("°","",rd_max_cnt)

	if repl_text.find(':') > -1:
		rd_max_cnt = repl_text.count(":")
		repl_text = repl_text.replace(":","",rd_max_cnt)
		
	if repl_text.find('=') > -1:
		rd_max_cnt = repl_text.count("=")
		repl_text = repl_text.replace("=","",rd_max_cnt)
	if repl_text.find('*') > -1:
		rd_max_cnt = repl_text.count("*")
		repl_text = repl_text.replace("*","",rd_max_cnt)
	if repl_text.find('─') > -1:
		rd_max_cnt = repl_text.count("─")
		repl_text = repl_text.replace("─","",rd_max_cnt)
	if repl_text.find('ㅡ') > -1:
		rd_max_cnt = repl_text.count("ㅡ")
		repl_text = repl_text.replace("ㅡ","",rd_max_cnt)
	if repl_text.find('\"') > -1:
		rd_max_cnt = repl_text.count("\"")
		repl_text = repl_text.replace("\"","",rd_max_cnt)
	if repl_text.find('※') > -1:
		rd_max_cnt = repl_text.count("※")
		repl_text = repl_text.replace("※","",rd_max_cnt)
	if repl_text.find('◑') > -1:
		rd_max_cnt = repl_text.count("◑")
		repl_text = repl_text.replace("◑","",rd_max_cnt)
	if repl_text.find('☜') > -1:
		rd_max_cnt = repl_text.count("☜")
		repl_text = repl_text.replace("☜","",rd_max_cnt)
	if repl_text.find('☆☆☆☆☆☆☆☆☆☆') > -1:
		rd_max_cnt = repl_text.count("☆☆☆☆☆☆☆☆☆☆")
		repl_text = repl_text.replace("☆☆☆☆☆","",rd_max_cnt)
	if repl_text.find('♡♡♡♡') > -1:
		rd_max_cnt = repl_text.count("♡♡♡♡")
		repl_text = repl_text.replace("♡","",rd_max_cnt)		
	if repl_text.find('☆☆☆☆☆☆☆☆☆') > -1:
		rd_max_cnt = repl_text.count("☆☆☆☆☆☆☆☆☆")
		repl_text = repl_text.replace("☆☆☆☆☆☆☆☆☆","☆☆☆☆☆",rd_max_cnt)
	if repl_text.find('☆☆☆☆☆☆☆☆') > -1:
		rd_max_cnt = repl_text.count("☆☆☆☆☆☆☆☆")
		repl_text = repl_text.replace("☆☆☆☆☆☆☆☆","☆☆☆☆☆",rd_max_cnt)
	if repl_text.find('~') > -1:
		rd_max_cnt = repl_text.count("~")
		repl_text = repl_text.replace("~","",rd_max_cnt)
	if repl_text.find('—') > -1:
		rd_max_cnt = repl_text.count("—")
		repl_text = repl_text.replace("—","",rd_max_cnt)
	if repl_text.find(',,,,,') > -1:
		rd_max_cnt = repl_text.count(",,,,,")
		repl_text = repl_text.replace(",,,,,",",",rd_max_cnt)
	if repl_text.find(' and gt;<br/>') > -1:
		rd_max_cnt = repl_text.count(" and gt;<br/>")
		repl_text = repl_text.replace(" and gt;<br/>",">",rd_max_cnt)
	if repl_text.find('and lt;') > -1:
		rd_max_cnt = repl_text.count("and lt;")
		repl_text = repl_text.replace("and lt;","<",rd_max_cnt)
	if repl_text.find('@@@@@') > -1:
		rd_max_cnt = repl_text.count("@@@@@")
		repl_text = repl_text.replace("@@@@@","@",rd_max_cnt)
	if repl_text.find('➖') > -1:
		rd_max_cnt = repl_text.count("➖")
		repl_text = repl_text.replace("➖","",rd_max_cnt)
	if repl_text.find('•') > -1:
		rd_max_cnt = repl_text.count("•")
		repl_text = repl_text.replace("•","",rd_max_cnt)
	if repl_text.find('   ') > -1:
		rd_max_cnt = repl_text.count("   ")
		repl_text = repl_text.replace("   "," ",rd_max_cnt)
	if repl_text.find(' -<br/> -<br/> -<br/> -<br/>') > -1:
		rd_max_cnt = repl_text.count(" -<br/> -<br/> -<br/> -<br/>")
		repl_text = repl_text.replace(" -<br/> -<br/> -<br/> -<br/>","",rd_max_cnt)
	if repl_text.find('.<br/>.<br/>.<br/>.<br/>') > -1:
		rd_max_cnt = repl_text.count(".<br/>.<br/>.<br/>.<br/>")
		repl_text = repl_text.replace(".<br/>.<br/>.<br/>.<br/>","",rd_max_cnt)
	if repl_text.find('#') > -1:
		rd_max_cnt = repl_text.count("#")
		repl_text = repl_text.replace("#","",rd_max_cnt)		
	if repl_text.find(';') > -1:
		rd_max_cnt = repl_text.count(";")
		repl_text = repl_text.replace(";","",rd_max_cnt)		
	if repl_text.find('&') > -1:
		rd_max_cnt = repl_text.count("&")
		repl_text = repl_text.replace("&","",rd_max_cnt)	
		
	return repl_text

def isStrEqual(str1, str2):		
	str1 = str1.replace("『","")
	str1 = str1.replace("[","")
	str1 = str1.replace("“","")
	str1 = str1.replace("\"","")
	str1 = str1.replace("\'","")
	str1 = str1.replace(".","")
	str1 = str1.replace(",","")
	str1 = str1.replace("★","")
	str1 = str1.replace("▶","")
	str1 = str1.replace("-","")
	str1 = str1.replace("《","")
	str1 = utilTrim(str1)

	str2 = str2.replace("『","")
	str2 = str2.replace("[","")
	str2 = str2.replace("“","")
	str2 = str2.replace("\"","")
	str2 = str2.replace("\'","")
	str2 = str2.replace(".","")
	str2 = str2.replace(",","")
	str2 = str2.replace("★","")
	str2 = str2.replace("▶","")
	str2 = str2.replace("-","")
	str2 = str2.replace("《","")		
	str2 = utilTrim(str2)
	
	if str1[:5] == str2[:5]:
		print(1)
		return True
	elif str1[:5] in (str2[:10]):
		print(2)
		return True
	else:
		return False
	

def getUrlToProductId(url):	
	startFindTxt = "prdCd="
	endFIndTxt = "&"
	sIdx = url.find(startFindTxt)
	eIdx = url.find(endFIndTxt)
	return url[sIdx+len(startFindTxt):eIdx]

def getNumber(str1):
	numbers = re.findall('\d+',str1)
	#print("numbers : ", numbers)
	rtn = ""
	for n in numbers:
		rtn+=n
	return int(rtn)

def isNone(val):
    try:
        if val:
            return val
        else:
            return val
        print(val)
    except Exception as e:
        print(e)
        return False

def getCurrentTime():
	return datetime.datetime.now()


def getDiffTimeToTime(dtTime) :
	return getCurrentTime() - dtTime
	
def isDirPath(dirPath): 
    try:
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)                
    except Exception as e:
        print(e)

def isTrue():
	isTrueInt = getRandom(1,5)
	print(isTrueInt)
	if  isTrueInt== 1:
		return True
	else:
		return False

def getImgFileName():
	return str(int(time.time()))
