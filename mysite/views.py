from django.shortcuts import render, get_object_or_404, redirect
from mysite.models import  Post, resultall, fullist, choice
from django.utils import timezone
from django.db import connection
from django.urls import reverse
from django.views.generic import DeleteView
import pymysql
import random

# 딥러닝
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models, layers
from tensorflow.keras.models import load_model
import cv2
import numpy as np

# 날씨
import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

# 계절
import datetime

import glob
from PIL import Image

import os

count = 0
rec_count = 0
def base1(request):
    global count
    count = count + 1
    return render(request, 'mysite/base1.html', {"rec_count":rec_count, "count":count})

def blog1(request):
    return render(request, 'mysite/blog1.html')

def weather(request):
    html = requests.get('https://weather.naver.com/today/09680630?cpName=KMA')
    soup = bs(html.text, 'html.parser') 

    a = soup.find('span', {'class':'weather'}).get_text()

    return render(request, 'mysite/weather.html', {'a':a})

# # Create your views here.
def index(request):
    return render(request,'mysite/index.html')

def new_post(request):
    try:
        if request.method == 'POST':
            if request.POST.get('mainphoto'):
                new_article=Post.objects.create(
                    # postname=request.POST.get('postname'),
                    # contents=request.POST.get('contents'),
                    mainphoto= request.FILES['mainphoto'],
                )
            else:
                new_article=Post.objects.create(
                    # postname=request.POST.get('postname'),
                    # contents=request.POST.get('contents'),
                    mainphoto= request.FILES['mainphoto'],
                )

                cursor = connection.cursor()

                strSql = "SELECT * FROM mysite_post"
                result = cursor.execute(strSql)
                datas = cursor.fetchall()

                connection.commit()
                connection.close()

                arr = []
                for data in datas:
                    row = {
                        'mainphoto' : data[1]
                    }
                    arr.append(row)  

                ptlink = arr[-1]["mainphoto"]
                
                files = glob.glob('media/{}'.format(ptlink))
                for f in files:
                    title, ext = os.path.splitext(f)
                    if ext in ['.jpg', '.png']:
                        img = Image.open(f)
                        img_resize = img.resize((250, 250))
                        img_resize.save(title + ext)
            return redirect('/recommend/')
    except:
        return redirect('/file_upload/')

    return render(request, 'mysite/new_post.html' ,{"rec_count":rec_count, "count":count})

def show_post(request):
    #최신순으로 조회(-pk 역순 조회)
    postlist = Post.objects.all().order_by('-pk')
    return render(request, 'mysite/show.html', {'postlist':postlist})
#끝

#음식기록 추가코드(show_food 페이지와 연결)
def show_food(request):
    res = resultall.objects.all()
    fcount = res.count()
#끝
#사진입력 횟수를 조회하는 코드 시작
    sp = Post.objects.all()
    spcount = sp.count()        
    foodlist = resultall.objects.all().order_by('-pk')
    return render(request, 'mysite/foodlist.html', {'foodlist':foodlist, "rec_count":rec_count, "count":count})



def molar(request):
    if request.method == 'POST':
        if request.POST.get('angry'):
            a1 = 'angry'
        elif request.POST.get('happy'):
            a1 = 'happy'
        else:
            a1 = 'sad'
        
    return render(request, 'mysite/food_list1.html',{"rec_count":rec_count, "count":count})


def food_list1(request):
    if request.method == 'POST':
        if request.POST.get('angry'):
            a1 = 'angry'
            emotion = '분노한'
        elif request.POST.get('happy'):
            a1 = 'happy'
            emotion = '기쁜'
        else:
            a1 = 'sad'
            emotion = '슬픈'

    cursor = connection.cursor()

    strSql = "SELECT * FROM mysite_post"
    result = cursor.execute(strSql)
    datas = cursor.fetchall()

    connection.commit()
    connection.close()


    arr = []
    for data in datas:
        row = {
            'id' : data[0],
            'mainphoto' : data[3]
        }
        arr.append(row)  

    ptlink = arr[-1]["mainphoto"]
    
    model = load_model('g:/VGG16_BatchNor.h5') # 모델명
    
    roi = cv2.imread('media/{}'.format(ptlink)) # 파일 경로
    #roi = cv2.imread('media/{}'.format(arr[-1].mainphoto)) # 파일 경로
    
    w, h = 250, 250
    roi = cv2.resize(roi, (w,h), interpolation = cv2.INTER_AREA)
    roi = roi.astype('float') / 255.0
    # roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    # img = img.reshape(1,w,h,3)

    Prediction = model.predict(roi)

    #Prediction[0]   #감정별 백분율 (화남 0, 기쁨 1, 중립 2, 슬픔3)


    # percent = Prediction[0][np.argmax(Prediction)]

    result = np.argmax(Prediction)#백분율이 제일 높은 값

    global rec_count
    rec_count = rec_count + 1
    

    html = requests.get('https://weather.naver.com/today/09680630?cpName=KMA')
    soup = bs(html.text, 'html.parser') 

    
    data1 = soup.find('span', {'class':'weather'}).get_text()
    if data1 == '비':
        b = '_rain'
        wea = "비가 오는 바깥의"
    elif data1 == '눈':
        b = '_snow'
        wea = "눈이 오는 바깥의"
    else:
        b = ''
        wea = data1
        
    
    now = datetime.datetime.now()
    if now.month == [3, 4, 5]:
        c = '_spring'
        season = "봄"
    elif now.month == [6, 7, 8]:
        c = '_summer'
        season = "여름"
    elif now.month == [9, 10, 11]:
        c = '_fall'
        season = "가을"
    else:
        c = '_winter'
        season = "겨울"
        
    
    final = a1+b+c

    
    
    cursor2 = connection.cursor()

    strSql2 = f"SELECT * from (SELECT * FROM menu_score_all  group by menu order by  {final}  DESC, rand()) res group by restaurant order by {final} DESC;"
    result2 = cursor2.execute(strSql2)
    datas2 = cursor2.fetchall()

    connection.commit()
    connection.close()

    arr2 = []
    for data in datas2:
        row2 = {
            'menu' : data[0],
            'restaurant' : data[1]
        }
        arr2.append(row2)    
    
    menu1 = arr2[0]["menu"]     
    restaurant1 = arr2[0]["restaurant"]
    menu2 = arr2[1]["menu"]     
    restaurant2 = arr2[1]["restaurant"]
    menu3 = arr2[2]["menu"]     
    restaurant3 = arr2[2]["restaurant"]
    menu4 = arr2[3]["menu"]     
    restaurant4 = arr2[3]["restaurant"]
    menu5 = arr2[4]["menu"]     
    restaurant5 = arr2[4]["restaurant"]

    d= []
    e= []
    f=[]

    d.append(menu1)
    d.append(menu2)
    d.append(menu3)
    d.append(menu4)
    d.append(menu5)           
    e.append(restaurant1)
    e.append(restaurant2)
    e.append(restaurant3)
    e.append(restaurant4)
    e.append(restaurant5)
    for i in range(1,len(d)+1):
            i =+i
            f.append(i)
    folist = zip(f, d, e)
    resultall.objects.create(
            restaurant = e,
            menu = d,
            season = final,
            emotion = a1
        )

    return render(request, 'mysite/food_list1.html', {'arr':arr[-1],"rec_count":rec_count, "count":count, 'emotion':emotion, 'wea':wea, 'season':season ,'a1':a1,'b':b,'c':c, 'd':d, 'e':e, 'folist': folist, 'final':final})

    
def food_list(request):
    try:
        cursor = connection.cursor()

        strSql = "SELECT * FROM mysite_post"
        result = cursor.execute(strSql)
        datas = cursor.fetchall()

        connection.commit()
        connection.close()


        arr = []
        for data in datas:
            row = {
                'id' : data[0],
                'mainphoto' : data[3]
            }
            arr.append(row)  

        ptlink = arr[-1]["mainphoto"]
        
        model = load_model('g:/VGG16_BatchNor.h5') # 모델명
        
        roi = cv2.imread('media/{}'.format(ptlink)) # 파일 경로
        #roi = cv2.imread('media/{}'.format(arr[-1].mainphoto)) # 파일 경로
        
        w, h = 250, 250
        roi = cv2.resize(roi, (w,h), interpolation = cv2.INTER_AREA)
        roi = roi.astype('float') / 255.0
        # roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        # img = img.reshape(1,w,h,3)

        Prediction = model.predict(roi)

        #Prediction[0]   #감정별 백분율 (화남 0, 기쁨 1, 중립 2, 슬픔3)


        percent = round(Prediction[0][np.argmax(Prediction)]*100,2)

        result = np.argmax(Prediction)#백분율이 제일 높은 값
        
        global rec_count
        rec_count = rec_count + 1

        if result == 0:
            a = 'angry'
            emotion = "분노한"
        elif result == 1:
            a = 'happy'
            emotion = "행복한"
        elif result == 3:
            a = 'sad'
            emotion = "슬픈"
        else:
            return render(request, 'mysite/molar.html')
            


        html = requests.get('https://weather.naver.com/today/09680630?cpName=KMA')
        soup = bs(html.text, 'html.parser') 

        
        data1 = soup.find('span', {'class':'weather'}).get_text()
        if data1 == '비':
            b = '_rain'
            wea = "비가 오는 바깥의"
        elif data1 == '눈':
            b = '_snow'
            wea = "눈이 오는 바깥의"
        else:
            b = ''
            wea = data1
            
        
        now = datetime.datetime.now()
        if now.month == [3, 4, 5]:
            c = '_spring'
            season = "봄"
        elif now.month == [6, 7, 8]:
            c = '_summer'
            season = "여름"
        elif now.month == [9, 10, 11]:
            c = '_fall'
            season = "가을"
        else:
            c = '_winter'
            season = "겨울"
        
        final = a+c+b

        cursor2 = connection.cursor()

        strSql2 = f" SELECT * from (SELECT * FROM menu_score_all  group by menu order by  {final}  DESC, rand()) res group by restaurant order by {final} desc;"
        result2 = cursor2.execute(strSql2)
        datas2 = cursor2.fetchall()

        connection.commit()
        connection.close()

        arr2 = []
        for data in datas2:
            row2 = {
                'menu' : data[0],
                'restaurant' : data[1]
            }
            arr2.append(row2)    
        
        menu1 = arr2[0]["menu"]     
        restaurant1 = arr2[0]["restaurant"]
        menu2 = arr2[1]["menu"]     
        restaurant2 = arr2[1]["restaurant"]
        menu3 = arr2[2]["menu"]     
        restaurant3 = arr2[2]["restaurant"]
        menu4 = arr2[3]["menu"]     
        restaurant4 = arr2[3]["restaurant"]
        menu5 = arr2[4]["menu"]     
        restaurant5 = arr2[4]["restaurant"]

        d= []
        e= []
        f=[]

        d.append(menu1)
        d.append(menu2)
        d.append(menu3)
        d.append(menu4)
        d.append(menu5)           
        e.append(restaurant1)
        e.append(restaurant2)
        e.append(restaurant3)
        e.append(restaurant4)
        e.append(restaurant5)
        for i in range(1,len(d)+1):
                i =+i
                f.append(i)
        folist = zip(f, d, e)
        resultall.objects.create(
            restaurant = e,
            menu = d,
            season = final,
            emotion = a
        )



    except:
        connection.rollback()
        print("Failed selecting in DB")
    

    return render(request, 'mysite/food_list.html', {'arr':arr[-1],'emotion':emotion,"rec_count":rec_count, "count":count, "wea":wea, "season":season,'percent':percent,'a':a,'b':b,'c':c, 'd':d, 'e':e, 'folist': folist, 'final':final})
#지도 불러오기 함수
#고투웍
def gotowork(request):
    return render(request,'mysite/고투웍map.html',{"rec_count":rec_count, "count":count})
#구내식당
def gunae(request):
    return render(request,'mysite/구내식당map.html',{"rec_count":rec_count, "count":count})
#롤링파스타
def rol(request):
    return render(request,'mysite/롤링파스타map.html',{"rec_count":rec_count, "count":count})
#돌배기집
def dol(request):
    return render(request,'mysite/돌배기집map.html',{"rec_count":rec_count, "count":count})
#리춘식당
def lee(request):
    return render(request,'mysite/리춘시장map.html',{"rec_count":rec_count, "count":count})
#막이오름
def mak(request):
    return render(request,'mysite/막이오름map.html',{"rec_count":rec_count, "count":count})
#미정국수
def mij(request):
    return render(request,'mysite/미정국수0410map.html',{"rec_count":rec_count, "count":count})
#백스비빔밥
def bac1(request):
    return render(request,'mysite/백S비빔밥map.html',{"rec_count":rec_count, "count":count})
#백스비어
def bac2(request):
    return render(request,'mysite/백스비어map.html',{"rec_count":rec_count, "count":count})
#백철판
def bac3(request):
    return render(request,'mysite/백철판0410map.html',{"rec_count":rec_count, "count":count})
#본가
def bon(request):
    return render(request,'mysite/본가map.html',{"rec_count":rec_count, "count":count})
#분식9단
def bun(request):
    return render(request,'mysite/분식9단map.html',{"rec_count":rec_count, "count":count})
#빽다방
def bac4(request):
    return render(request,'mysite/빽다방map.html',{"rec_count":rec_count, "count":count})
#빽보이 피자
def bac5(request):
    return render(request,'mysite/빽보이피자map.html',{"rec_count":rec_count, "count":count})
#새마을 식당
def sae(request):
    return render(request,'mysite/새마을식당map.html',{"rec_count":rec_count, "count":count})
#성성식당
def sun(request):
    return render(request,'mysite/성성식당map.html',{"rec_count":rec_count, "count":count})
#역전우동
def yuk(request):
    return render(request,'mysite/역전우동0410map.html',{"rec_count":rec_count, "count":count})
#연돈볼카츠
def yeo(request):
    return render(request,'mysite/연돈볼카츠map.html',{"rec_count":rec_count, "count":count})
#원조쌈밥집
def one(request):
    return render(request,'mysite/원조쌈밥집map.html',{"rec_count":rec_count, "count":count})
#인생설렁탕
def ins(request):
    return render(request,'mysite/인생설렁탕map.html',{"rec_count":rec_count, "count":count})
#제순식당
def jes(request):
    return render(request,'mysite/제순식당map.html',{"rec_count":rec_count, "count":count})
#한신포차
def han(request):
    return render(request,'mysite/한신포차map.html',{"rec_count":rec_count, "count":count})
#홍콩반점
def hon(request):
    return render(request,'mysite/홍콩반점0410map.html',{"rec_count":rec_count, "count":count})



def map(request):
    return render(request,'mysite/map.html', {"rec_count":rec_count, "count":count})


def fchoice(request):
    fd = fullist.objects.all()
    # 전체 메뉴 조회
    global count
    count = count + 1
    f3 = []
    f1 = request.GET['choice']
    # f1.split(',')
    f3.append(f1.split(','))
    
   
    # df1 = pd.Series(f3)
    df1 =pd.DataFrame(list(f3))
    df1.reset_index
    df1 = df1.rename(columns={0:"음식명",1:"음식점",2:"감정상태", 3:"날씨",4:"계절"})
    # df1.drop([''],axis=1)
    # df1 = df1.columns["메뉴명","음식점","감정상태"]
    # df1[0] = df1[0].str.replace("0"," ", )
    # df1 =pd.DataFrame(f3).transpose()
    df1.loc[df1["음식점"]=="Back다방","음식점"] = "빽다방"
    df1.loc[df1["음식점"]=="돌배기","음식점"] = "돌배기집"
    df1.loc[df1["음식점"]=="백종원의 元祖쌈밥집","음식점"] = "원조쌈밥집"
    df1.loc[df1["음식점"]=="백철판","음식점"] = "백철판0410"
    df1.loc[df1["음식점"]=="역전우동","음식점"] = "역전우동0410"
    df1.loc[df1["음식점"]=="홍콩반점","음식점"] = "홍콩반점0410"
    df1.loc[df1["음식점"]=="빽보이","음식점"] = "빽보이피자"


      
    choice.objects.create(
        menu = str(df1["음식명"].values).replace("['","").replace("']",""),
        res = str(df1["음식점"].values).replace("['","").replace("']",""),
        emotion = str(df1["감정상태"].values).replace("['","").replace("']",""),
        weather = str(df1["날씨"].values).replace("['","").replace("']",""),
        season = str(df1["계절"].values).replace("['","").replace("']","")  
    )
 
    
    foodlist = resultall.objects.all()        
    print(type(f1))
    print(type(f3))
    print(df1.values)
    f2 = choice.objects.all().order_by('-pk')
    choice_res = str(df1["음식점"].values).replace("['","").replace("']","")
  
      
    return render(request, 'mysite/{}map.html'.format(choice_res),{'fd':fd,'f1':f1,'f2':f2 ,'count':count, 'foodlist':foodlist})


def foodview(request):
    f2 = choice.objects.all().order_by('-pk')
    # mere = RestaurantMenu.objects.all().order_by('-pk')
    return render(request, 'mysite/choice.html',{'f2':f2})
