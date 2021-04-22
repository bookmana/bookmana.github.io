import os

print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_DIR = "/static_site_repo/_posts"
FULL_PATH = os.path.join(BASE_DIR,TARGET_DIR)
print("##############################")
print("BASE_DIR : ",BASE_DIR)
print("TARGET_DIR : ",TARGET_DIR)
print("FULL_PATH : ",FULL_PATH)


print("##############################")
print(os.path.isdir(FULL_PATH))
print(os.walk(FULL_PATH))
