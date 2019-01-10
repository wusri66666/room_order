import datetime
import hashlib
import uuid
from functools import wraps

from django.contrib.auth import authenticate, login
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from app.models import *
from app.tasks import send_html


def get_str():
    uuid_str = str(uuid.uuid4()).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()

class RegisterView(View):

    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        com_password = request.POST.get('com_password')
        email = request.POST.get('email')
        res = {
            'code':1,
            'msg':None,
            'data':None
        }
        object = MyUser.objects.filter(username=username).first()
        if object:
            res['msg'] = '用户名已存在'
        if not username or len(username)<3:
            res['msg'] = '用户名过短'
            return JsonResponse(res)
        if not phone or len(phone)!=11:
            res['msg'] = '手机号不符合格式'
            return JsonResponse(res)
        if not password or password != com_password:
            res['msg'] = '密码不对'
            return JsonResponse(res)
        res1 = get_str()
        url = 'http://127.0.0.1:8000/app/active/'+res1
        cache.set(res1,username)
        send_html.delay(url,email)
        MyUser.objects.create_user(username=username,phone=phone,email=email,password=password,is_active=0)
        res['msg'] = '注册成功,请注意邮件查收'
        return JsonResponse(res)

def active(request,active_code):
    res = cache.get(active_code)
    obj = MyUser.objects.filter(username=res).first()
    obj.is_active = 1
    obj.save()
    return redirect('/app/login/')

class LoginAPI(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            request.session['userid']=user.id
            res = {
                'code':0,
                'msg':'登陆成功',
                'data':'/app/room/'
            }
            return JsonResponse(res)
        else:
            res = {
                'code':1,
                'msg':'用户名或密码错误',
            }
            return JsonResponse(res)


def check_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        userid=request.session.get('userid')
        if not userid:
            return redirect('/app/login/')
        else:
            request.userid=userid
            return func(request,*args,**kwargs)
    return inner

@check_login
def room(request):
    if request.method=='GET':
        select_date=request.GET.get('select_date',None)
        if select_date==None:
            select_date=datetime.datetime.now().date().strftime("%Y-%m-%d")
        room_list=MeetingRoom.objects.all().values('id','name')
        time_tuple=ReserveRecord.time1
        new_dic={}
        for dic in room_list:
            new_dic[dic['id']]={
                'id':dic['id'],
                'name':dic['name'],
                'times':{
                    1:False,
                    2:False,
                    3:False,
                    4:False,
                    5:False,
                    6:False,
                    7:False,
                    8:False,
                    9:False,
                    10:False,
                }
            }
        record_list=ReserveRecord.objects.filter(data=select_date).values('room_id','timeline')
        for dic in record_list:
            new_dic[dic['room_id']]['times'][dic['timeline']]=True
        return render(request,'room_list.html',locals())
    else:
        data=dict(request.POST)
        userid=request.userid
        select_date=request.POST.get('select_date')
        print(data.items())
        for i,j in data.items():
            if i=='select_date':
                continue
            for k in j:
                ReserveRecord.objects.create(data=select_date,user_id=request.userid,room_id=i,timeline=k)
        return redirect('/app/room/?select_date=%s' %select_date)

def quit(request):
    request.session.flush()
    return redirect('/app/login/')
