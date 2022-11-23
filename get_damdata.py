import requests
from bs4 import BeautifulSoup

from datetime import date, timedelta
import time, re
# v1.01

def get_dam_data(year,month,day,dam_ID):
    # time.sleep(0.1)
    #dam_ID='1368010332520'

    year=str(year)
    month='{0:02d}'.format(month)
    day='{0:02d}'.format(day)

    start_date=year+month+day
    end_date=year+month+day

    url='http://www1.river.go.jp/cgi-bin/DspDamData.exe?KIND=1&ID={0}&BGNDATE={1}&ENDDATE={2}&KAWABOU=NO'.format(dam_ID,start_date,end_date)
    print(url)
    response = requests.get(url)

    # print(response.text)

    soup=BeautifulSoup(response.text,"html.parser")

    elem1=soup.find("iframe")

    response = requests.get('http://www1.river.go.jp'+elem1['src'])

    # print(response.text)

    soup=BeautifulSoup(response.text,"html.parser")
    one_day=soup.find_all('tr')

    oneline=[]
    result=[]
    for one_hour in one_day:
        for i in one_hour.find_all('td'):
            isnum=re.sub(r'[:|\.|/]','',i.text)
            if(isnum.isnumeric()):
                oneline.append(i.text)
            else:
                oneline.append('')
        result.append([i for i in oneline])
        oneline=[]

    middle_num=int((result[-1][1]).split(':')[0])+1
    while(True):
        if(result[-1][1]=='24:00'):
            break
        year='{0}/{1}/{2}'.format(year,month,day)
        hour='{0:02d}:00'.format(middle_num)
        result.append([year,hour,'','','','',''])
        middle_num+=1
         
    return result

# csv_result=get_dam_data(input(),input(),input())
# print(csv_result)
csv_result=[]

print('dam ID : ')
dam_ID=input()
if(dam_ID==''):
    dam_ID='1368010332520'
print('start year : ')
start_year=int(input())
print('start month : ')
start_month=int(input())
print('start day : ')
start_day=int(input())
print('end year : ')
end_year=input()
if(end_year==''):
    end_year=start_year
end_year=int(end_year)
print('end month : ')
end_month=int(input())
print('end day : ')
end_day=int(input())

d1=date(start_year,start_month,start_day)
d2=date(end_year,end_month,end_day)

target_year=d1.year
for i in range((d2-d1).days+1):
    date=d1+timedelta(i)
    print(date)
    if(target_year!=date.year):
        with open('damdata_{0}.csv'.format(target_year),'w',encoding='utf-8') as f:
            for line in csv_result:
                    f.write(','.join(line))
                    f.write('\n')
        csv_result=[]

    csv_result=csv_result + get_dam_data(date.year,date.month,date.day,dam_ID)
    
    target_year=date.year
with open('damdata_{0}.csv'.format(date.year),'w',encoding='utf-8') as f:
    for line in csv_result:
            f.write(','.join(line))
            f.write('\n')

