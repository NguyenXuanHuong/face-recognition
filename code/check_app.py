from imutils.video import VideoStream
import time
import cv2
import numpy as np
from datetime import datetime
import datetime
import os
from imutils.video import FPS
import urllib.request
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from requests.packages import urllib3
import json
import concurrent.futures
cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
def AddNew():
    tmp_vr = []
    # FireBase_Com.Init()
    addMember = db.reference('addMember')
    addTab = addMember.get()
    # print(addTab)
    # json_addTab = json.dumps(addTab)
    # for key, value in addTab.items():
    #     tmp_vr.append(value)
    dbNewUsrID = db.reference('addMember/NewUsrID')
    dbappRq = db.reference('addMember/appRequest')
    NewUsrID = dbNewUsrID.get()
    appRq = dbappRq.get()
    print("NewUsrID",NewUsrID)
    print("appRequest",appRq)
    return str(addTab),NewUsrID,appRq
def ReverseDay(day = ''):
    # 2020-08-27
    ls_par = day.split('-')
    output = ''
    for i in range (0, len(ls_par)):
        if (output != ''):
            output = output + '-' + ls_par[len(ls_par)-1-i]
        else:
            output = output + ls_par[len(ls_par)-1-i]
    print(output)
    return output
def SendData(UsrID=''):
    today = ReverseDay(str(datetime.datetime.today()).split(" ")[0])
    # Send data
    diemdanh = db.reference(str('diemdanh/'+today))
    print("str('diemdanh/'+today)",str('diemdanh/'+today))
    # diemdanh = db.reference(str('diemdanh/13-08-2020'))
    rq = diemdanh.child(UsrID)
    now = datetime.datetime.now()
    timeEnter = '0'
    timeExit = '0'
    hour = int(str(now).split(' ')[1].split(':')[0])
    this_time = str(now).split(' ')[1].split('.')[0]
    print(this_time)
    # print('hour = ',hour)
    print('this time',this_time)
    if (hour > 8 and hour < 10):
        timeEnter = this_time
        result = rq.update({'timeEnter':timeEnter})
    elif (hour > 16 and hour < 18):
        timeExit = this_time
        result = rq.update({'timeExit':timeExit})
def Authen(uid = []):
    i = 0
    list_UserID = []
    list_UserRFID = []
    str_uid = str(uid)
    list_UserID,list_UserFaceID = GetAuthenData()
    print(list_UserFaceID)
    try:
        for ls in list_UserFaceID:
            cmp_stt = str(ls).find(str_uid)
            if (cmp_stt != -1):
                result = 1
                break
            else:
                result = 0
                i = i+1
        if (result == 1):
            print("ACCESS GRANTED!!!")
        else:
            print("ACESS DENIED")
        print("\ni = ",i)
        print(list_UserID)
        UsrID = list_UserID[i]
    except:
        print("       ")
        UsrID = ''
    i= 0
    return result,UsrID
def GetAuthenData():
    # FireBase_Com.Init()
    list_UserID = []
    list_UserFaceID = []
    list_UserInfo = []
    #Get data
    employees = db.reference('employees')
    dayTab = employees.get()
    json_dayTab = json.dumps(dayTab)
    for key, value in dayTab.items():
        list_UserID.append(key)
        list_UserInfo.append(value)
    for id in list_UserID:
        db_faceid = db.reference(str('employees/' + str(id) + '/faceid'))
        faceid_ = db_faceid.get()
        list_UserFaceID.append(faceid_)
    return list_UserID,list_UserFaceID
def UpdateFaceInfo(UsrID = '', FaceID = ''):
    # FireBase_Com.Init()
    employees = db.reference(str('employees/'+UsrID))
    result = employees.update({'faceid':FaceID})
def PushDataToFirebase(FaceID = ''):
    # Connect to firebase
    # cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
    # firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
    addTab,NewUsrID,appRq = AddNew()
    if (appRq == 2):
        UpdateFaceInfo(NewUsrID,FaceID)
    else:
        result,UsrID = Authen(FaceID)
        if (result == 1):
            SendData(UsrID)
            print("Access Granted")
        else:
            print("Access Denied")
    db_reset_appRq = db.reference('addMember')
    rs = db_reset_appRq.update({'appRequest':0})
def GetImageInfo():
    dbImgID = db.reference('addMember/idAnh')
    idAnh = dbImgID.get()
    dbImgUrl = db.reference('addMember/linkAnh')
    url = dbImgUrl.get()
    return idAnh,url

def check_app():
    _, _, request = AddNew()
    return request
def open_file():
    with open('danh_sach_ten.txt', 'r') as f:
        classNames = f.readline()
    classNames=list(classNames.split(','))
    if '' in classNames:
        classNames.remove('')
    # len_classNames=len(classNames)

    with open('danh_sach_text.txt', 'r') as f:
        tentxt = f.readline()
    tentxt=list(tentxt.split(','))
    if '' in tentxt:
        tentxt.remove('')
    # len_tentxt=len(tentxt)

    with open('danh_sach_id.txt', 'r') as f:
        DS_ID = f.readline()
    DS_ID=list(DS_ID.split(','))
    if '' in DS_ID:
        DS_ID.remove('')
    # len_DS_ID=len(DS_ID)
    return tentxt,  classNames, DS_ID
def write_file(ten,idAnh,new_txt):
    with open('danh_sach_ten.txt', 'a') as f:
        ten1 = ten + ','
        f.writelines(f'{ten1}')
    print('da them ten')
    # DS_ID.append(idAnh)
    # len_DS_ID = len(DS_ID)
    with open('danh_sach_id.txt', 'a') as f:
        idAnh1 = idAnh + ','
        f.writelines(f'{idAnh1}')
    print('da them txt')
    newtentxt = new_txt
    # tentxt.append(newtentxt)
    # len_tentxt = len(tentxt)
    with open('danh_sach_text.txt', 'a') as f:
        newtentxt1 = newtentxt + ','
        f.writelines(f'{newtentxt1}')
    print('da them txt path')
    # encodeListKnown= loadtxt(tentxt)
    # return len_classNames,len_DS_ID,len_tentxt,encodeListKnown
def brightness(frame):
    gamma = 0.3
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    frame = cv2.LUT(frame, lookUpTable)
    return frame
def train():
    request=check_app()
    tentxt, classNames, DS_ID=open_file()
    if request == 2:
        idAnh, url = GetImageInfo()
        ten = idAnh.split('_')[0]
        print(ten)
        print(classNames)
        if ten not in classNames:
            print('down')
            with open ('nguoi vua tai.txt','w') as f:
                f.write(idAnh)

            new_img = ten + '.jpg'
            new_txt = ten + '.txt'
            file_path = 'data'
            full_path = os.path.sep.join([file_path, new_img])
            urllib.request.urlretrieve(url, full_path)
            path = 'data'
            path_img = os.path.sep.join([path, new_img])
            Img = cv2.imread(path_img, 1)
            rgb,boxes=face_detection(Img)
            boxes1=boxes_int(boxes)
            encode = face_recognition.face_encodings(rgb, boxes1)
            np.savetxt(new_txt, encode)
            write_file(ten,idAnh,new_txt)



def face_detection(frame):
    frame=brightness(frame)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    boxes = np.array(boxes)
    return rgb,boxes
def boxes_int(boxes):
    a = int(boxes[:, 0])
    b = int(boxes[:, 1])
    c = int(boxes[:, 2])
    d = int(boxes[:, 3])
    boxes1 = [(a, b, c, d)]
    return boxes
while True:
    train()