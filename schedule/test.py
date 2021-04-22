import os

print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = os.path.join(BASE_DIR,TARGET_DIR)
FULL_PATH2 = "{}{}".format(BASE_DIR, TARGET_DIR)

print("############################## BASE_DIR")
print("BASE_DIR : ",BASE_DIR)
print("TARGET_DIR : ",TARGET_DIR)
print("FULL_PATH : ",FULL_PATH)
print("FULL_PATH : ",FULL_PATH2)


print("############################## FULL_PATH")
print(os.path.isdir(FULL_PATH))
for wa in os.walk(FULL_PATH):
	file = wa[2]
	file_cnt = len(wa[2])
	print(file," - ",str(file_cnt))

print("##############################FULL_PATH2")
print(os.path.isdir(FULL_PATH2))
for wa in os.walk(FULL_PATH2):
	file = wa[2]
	file_cnt = len(wa[2])
	print(file," - ",str(file_cnt))
