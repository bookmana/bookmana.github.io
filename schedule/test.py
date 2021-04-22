import datetime
import os

print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = "{}{}".format(BASE_DIR, TARGET_DIR)

print("############################## BASE_DIR")
print("BASE_DIR : ",BASE_DIR)
print("TARGET_DIR : ",TARGET_DIR)
print("FULL_PATH : ",FULL_PATH)



print("############################## FULL_PATH")
print(os.path.isdir(FULL_PATH))
for wa in os.walk(FULL_PATH):
	file = wa[2]
	file_cnt = len(wa[2])
	print(file," - ",str(file_cnt))


content="hellow python"

now = datetime.datetime.now()	

file_path = """%s/%s-%s.md""" %(FULL_PATH,now.strftime('%Y-%m-%d'),'1234567')
#f = open(file_path ,'w', encoding='utf8')
f = open("./_posts/%s-%s.md"%(now.strftime('%Y-%m-%d'),isbn_no) ,'w', encoding='utf8')
f.write(content)
