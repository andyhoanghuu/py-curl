import requests
import json
import time
import random
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Tải các biến môi trường từ tệp .env
load_dotenv()

base_url = os.getenv('BASE_URL')
course_id = os.getenv('COURSE_ID')
sesskey = os.getenv('SESSKEY')
cookies = os.getenv('COOKIES')

url_update_status = f'{base_url}/lib/ajax/service.php?sesskey={sesskey}&info=core_completion_update_activity_completion_status_manually'
url_view_course = f'{base_url}/course/view.php?id={course_id}'

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': cookies,
    'origin': base_url,
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'{base_url}/course/view.php?id={course_id}',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

while True:
    # Truy cập vào trang course để lấy data-cmid của nút "Mark as done"
    response_view = requests.get(url_view_course, headers=headers)

    if response_view.status_code == 200:
        soup = BeautifulSoup(response_view.content, 'html.parser')
        button = soup.find('button', {'data-toggletype': 'manual:mark-done', 'aria-label': lambda text: 'Mark' in text and 'as done' in text})

        if button:
            cmid = button.get('data-cmid')
            print(f'Found "Mark as done" button with data-cmid: {cmid}')

            # Cập nhật trạng thái hoàn thành cho cmid
            data = [{
                "index": 0,
                "methodname": "core_completion_update_activity_completion_status_manually",
                "args": {
                    "cmid": str(cmid),
                    "completed": True
                }
            }]

            response = requests.post(url_update_status, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                print(f'Successfully updated cmid: {cmid}')
            else:
                print(f'Failed to update cmid: {cmid}, Status Code: {response.status_code}, Response: {response.text}')

            # Thời gian chờ ngẫu nhiên từ 5 giây đến 10 giây
            sleep_time = random.uniform(5, 10)
            print(f'Waiting for {sleep_time:.2f} seconds before next request...')
            time.sleep(sleep_time)
        else:
            print('No "Mark as done" button found.')
            break
    else:
        print(f'Failed to access course page, Status Code: {response_view.status_code}, Response: {response_view.text}')
        break
