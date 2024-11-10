from concurrent.futures.thread import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from datetime import datetime,timedelta
from email.mime.text import MIMEText
from requests.packages import target
from bs4 import BeautifulSoup
from time import sleep
import requests
import smtplib
import queue
import time
import re
#**********************邮件发送***********************
msg = MIMEMultipart()        #创建一个邮件对象
msg['From'] = ''        #发送邮件的地址
msg['To'] = ''        #接收邮件的地址
# SMTP服务器配置
smtp_server = ''        #发送邮件邮箱的smtp服务器地址
port =               #对应服务器的端口号
username = ''        #发送邮件的地址
password = ''        #smtp服务的邮箱密码
#*************************提取元素********************
pattern = r'id=(\d+)&pprid=(\d+)'        #正则表达式提取提取
def wait_until(target_time):        #抢讲座的时间
    #让程序休眠到指定时间10秒之前
    time_difference=target_time-datetime.now();
    time_diff_sec=time_difference.total_seconds();
    sleep(time_diff_sec-10)
    #指定时间后300毫秒内退出循环
    target_time+=timedelta(milliseconds=300)
    while datetime.now()<target_time:
        sleep(0.1)

def send_email(lecture_info_list):        #把讲座信息发送到指定邮箱
    subject="讲座信息"
    body="讲座信息\n\n"
    for info in lecture_info_list:
        body += f"""讲座名称：{lecture['lecture_name']}
        批次：{lecture['batch']}
        地点：{lecture['location']}
        开始时间：{lecture['start_time']}
        结束时间：{lecture['end_time']}
        责任教师：{lecture['teacher']}
        简介：{lecture['description']}
        \n------------------------\n"""
    try:
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(username, password)
        server.send_message(msg)
        print("邮件发送成功")
    except Exception as e:
        print(f"发送邮件失败: {e}")
    finally:
        server.quit()

def get_params_list(params_list):        #获取全部的讲座请求id
    cookies = {}
    params = {}
    headers = {}
    response = requests.get()
    matches = re.findall(pattern, response.text)
    for match in matches:
        id_val,pprid_val=match
        params={
            'id':id_val,
            'pprid':pprid_val
        }
        params_list.append(params)

def fetch_lecture(params,sleep_time_s):        #抢讲座
    cookies = {}
    headers = {}
    while True:
        response = requests.get()
        soup = BeautifulSoup(response.text, 'html.parser')
        scriptes = soup.find_all('script')
        for script in scriptes:
            text = script.get_text()
            if 'ds.dialog.alert("该活动批次接纳人数已达上限，请选择其他批次!")' in text:
                print('该活动批次接纳人数已达上限，请选择其他批次!')
            elif 'ds.dialog.alert("该活动不对您所在的专业、年级开放!")' in text:
                print('该活动不对您所在的专业、年级开放!')
            elif '预约成功' in text:
                print("已抢到")
                send_email()
                break
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
        time.sleep(sleep_time_s)

def get_lecture_info(soup):        #获取讲座信息
    lecture_info_list=[]
    rows=soup.select("table.tablelist tr")[2:]
    for row in rows:
        columns=row.find_all("td")
        if columns:
            lecture_info={
                "lecture_name":columns[0].get_text(strip=True),
                "batch":columns[1].get_text(strip=True),
                "location":columns[2].get_text(strip=True),
                "start_time":columns[3].get_text(strip=True),
                "end_time":columns[4].get_text(strip=True),
                "teacher":columns[5].get_text(strip=True),
                "description":columns[7].get_text(strip=True)
            }
            lecture_info_list.append(lecture_info)
    return lecture_info_list

if __name__ == '__main__':
    params_list=list();
    get_params_list(params_list);
    threads_number=len(params_list);
    target_time=datetime(2024,11,9,23,26,0)        #输入设定的抢讲座的时间
    wait_until(target_time)
    with ThreadPoolExecutor(max_workers=threads_number) as executor:
        for i in range(threads_number):
            executor.submit(fetch_lecture,params_list[i],0.01)
