from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import random
from django.core.files.storage import FileSystemStorage
from RoomRent.forms import *
from .models import UserOTP,Post_Ad_For_Room,Room_Image,ChatRoom,ChatRoomSerializer,Agreement,Payment
from django.conf import settings
import re
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from math import ceil
from geopy.geocoders import Nominatim
import json
import online_users.models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import razorpay
from django.contrib import messages
senderObject=None
receiverObject=None



def EditRoom(request,roomID=None):
    if request.method=='POST':
        roomid=request.POST.get('roomid')
        buildingName=request.POST.get('buildingName')
        name=request.POST.get('name')
        mobile_no=request.POST.get('mobile_no')
        State=request.POST.get('State')
        City=request.POST.get('city')
        pin=request.POST.get('pin')
        Monthly_Rent=request.POST.get('Monthly_Rent')
        Deposite=request.POST.get('Deposite')
        floor=request.POST.get('floor')
        total_floor=request.POST.get('total_floor')
        total_room=request.POST.get('total_room')
        Address=request.POST.get('Address')
        Landmark=request.POST.get('Landmark')
        Description=request.POST.get('Description')
        Bathroom=request.POST.getlist('Bathroom')
        Room_Type=request.POST.getlist('Room_Type')
        Available_For=request.POST.getlist('Available_For')




        # Object of Post_Ad_For_Room
        geolocator = Nominatim(user_agent="geoapiExercises")
        Room=Post_Ad_For_Room.objects.get(id=int(roomid))
        Room.buildingName=buildingName
        Room.owner_mobile_number=mobile_no
        Room.room_in_state=State
        Room.room_in_city=City
        Room.room_pin=pin
        Room.room_description=Description
        Room.room_rent=int(Monthly_Rent)
        Room.room_desposite=int(Deposite)
        Room.room_floor=int(floor)
        Room.total_floor=int(total_floor)
        Room.total_room=int(total_room)
        Room.Bathroom=Bathroom[0]
        Room.House_Type=Room_Type[0]
        Room.Available=Available_For[0]
        Room.Address=Address
        location = geolocator.geocode(pin)
        Room.full_location=location
        Room.Landmark=Landmark
        Room.owner_name=name
        Room.user_primary_key=str(request.user.id)
        Room.save()
        return HttpResponseRedirect('room_detail/'+roomid)


    try:
        room=Post_Ad_For_Room.objects.get(id=int(roomID))
        return render(request,'RoomRent/edit_room.html',{'room':room})
    except:
        return render(request,'RoomRent/home.html')




def ChangeStatus(request):
    id=request.GET.get('id')
    room=Post_Ad_For_Room.objects.get(id=id)
    s=room.status
    if s=='vacant':
        room.status='occupied'
        s='occupied'
    else:
        room.status='vacant'
        s='vacant   '
    s=id+","+s
    room.save()

    return HttpResponse(s)





def EditProfile(request):
    if request.method=='POST':
        username=request.POST.get('username')
        first=request.POST.get('first')
        last=request.POST.get('last')
        user=User.objects.get(email=request.user.email)
        user.username=username
        user.first_name=first
        user.last_name=last
        user.save()
        return render(request,'RoomRent/Profile.html',{'user':user})
    user=User.objects.get(email=request.user.email)
    return render(request,'RoomRent/edit_profile.html',{'user':user})


def Profile(request):
    user=User.objects.get(email=request.user.email)
    return render(request,'RoomRent/Profile.html',{'user':user})


def PrivacyTerms(request):
    return render(request,'RoomRent/privancy_policy.html')


def OurTeam(request):
    return render(request,'RoomRent/our_team.html')

def ContactMail(request):

    phone=request.GET.get('phone')
    mail=request.GET.get('email')
    omail=request.GET.get('oemail')
    rid=request.GET.get('rid')
    owner=User.objects.get(email=omail)
    roomies=User.objects.get(email=mail)
    room=Post_Ad_For_Room.objects.filter(id=int(rid))
    print("#"*100,room)

    html_content=render_to_string('RoomRent/contact_owner.html',{'phone':phone,'mail':mail,'omail':omail,'owner':owner,
    'roomies':roomies,'room':room[0]})
    text_content=strip_tags(html_content)
    email=EmailMultiAlternatives(
    'Roomies want to Contact You!',
    text_content,
    settings.EMAIL_HOST_USER,
    [omail]
    )
    email.attach_alternative(html_content,'text/html')
    email.send()
    return HttpResponse("Done")






from django.db.models import Q
def SearchByRoomCity(request):
    ser=request.POST.get('ser')
    all_room=Post_Ad_For_Room.objects.filter(Q(room_in_city__iexact=ser) |Q(id__iexact=ser) | Q(room_in_state__iexact=ser) | Q(room_pin__iexact=ser))
    l=len(all_room)
    lst_of_main_image=[]
    for i in range(len(all_room)):
        Rimage=Room_Image.objects.filter(room_id=all_room[i].id).first()
        lst_of_main_image.append(Rimage)
    all_object_zip=zip(list(all_room),lst_of_main_image)
    print(all_object_zip)

    return render(request,'RoomRent/search_room.html',{'ser':ser,'all_object_zip':all_object_zip,'l':l})

from django.views.decorators.csrf import csrf_exempt
def Payment_Action(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name=request.POST.get('name')
        roomID=request.POST.get('roomID')
        amount=int(request.POST.get('amount'))*100
        msg=request.POST.get('msg')
        client=razorpay.Client(auth=("rzp_test_rvr196S61RmFdX","dYzuoaHAZZBXVg4yOloSOowt"))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        payment_obj=Payment()
        payment_obj.email_of_payment_sender=request.user.email
        payment_obj.email_of_payment_receiver=email
        payment_obj.name_of_receiver=name
        try:
            payment_obj.room_id=Post_Ad_For_Room.objects.get(id=int(roomID))
        except:
            messages.error(request, 'Please Enter correct Room Id')
            return render(request,'RoomRent/payment_gateway.html')
        payment_obj.message=msg
        payment_obj.amount_to_pay=amount
        payment_obj.payment_id=payment['id']
        payment_obj.save()
        print(email,name,roomID)
        return render(request,'RoomRent/payment_gateway.html',{'payment':payment,'email':email,'name':name,'amount':amount,'msg':msg,'roomid':roomID})
    return render(request,'RoomRent/payment_gateway.html')

@csrf_exempt
def Payment_Detail_Save(request):
    if request.method=='POST':
        a=request.POST
        order_id=""
        for k,v in a.items():
            if k== 'razorpay_order_id':
                order_id=v
                break
        user=Payment.objects.filter(payment_id=order_id).first()
        user.payment_done=True
        user.save()
        user=Payment.objects.filter(payment_id=order_id).first()
        print(user.name_of_receiver,"========================")
        lst=[]
        lst.append(user.name_of_receiver)
        lst.append(user.email_of_payment_receiver)
        lst.append(user.email_of_payment_sender)
        lst.append(user.room_id)
        lst.append(user.amount_to_pay)
        lst.append(user.payment_id)
        lst.append(user.message)
        html_content=render_to_string('RoomRent/payment_receipt_mail.html',{'name':lst[0],
        'omail':lst[1],'rmail':lst[2],'roomid':lst[3],'amount':lst[4],'pid':lst[5],'msg':lst[6]})
        text_content=strip_tags(html_content)
        email=EmailMultiAlternatives(
        'Payment for '+str(user.room_id.id)+" have been Success",
        text_content,
        settings.EMAIL_HOST_USER,
        [request.user.email,user.email_of_payment_receiver]
        )
        email.attach_alternative(html_content,'text/html')
        email.send()

    return  render(request,'RoomRent/success.html')


def AgreementDetail(request,agreement):
    agreement=Agreement.objects.get(id=int(agreement))
    room=agreement.roomId
    return render(request,'RoomRent/lease_agreement.html',{'agreement':agreement,'room':room})



def AgreementList(request):
    lst1=list(Agreement.objects.filter(ownerEmail=request.user.email))
    lst2=list(Agreement.objects.filter(renterEmail=request.user.email))
    lst1=lst1[::-1]
    lst2=lst2[::-1]
    lst=lst1+lst2
    lst_agreement=[]
    for i in lst:
        if i not in lst_agreement:
            lst_agreement.append(i)
    user=User.objects.get(id=request.user.id)
    all_room_by_user=Post_Ad_For_Room.objects.filter(user=user)
    return render(request,'RoomRent/ListOFAgreement.html',{'lst_agreement':lst_agreement,'all_room_by_user':all_room_by_user})


def ForRenterAgreementSign(request,details):
    try:
        print('In try Catch')
        if int(details) and request.method!='POST' :
            print('In try Catch')
            agreement=Agreement.objects.get(id=int(details))
            print("Agreemnet",agreement)
            room=agreement.roomId
            if agreement.esignRenter =='None':
                r=1
            else:
                r=0
            return render(request,'RoomRent/lease_agreement.html',{'agreement':agreement,'room':room,'r':r})
        else:
            print(9/0)
    except:
        if request.method=='POST':
            roomid=request.POST.get('room')
            rname=request.POST.get('rname')
            oname=request.POST.get('oname')
            remail=request.POST.get('remail')
            Id=request.POST.get('id')
            RenterSign=request.POST.get('RenterSign')
            print("==================>",roomid,rname,oname,remail)
            agreement=Agreement.objects.get(renterEmail=remail,ownerID=oname,renterName=rname,roomId=roomid,id=int(Id))
            agreement.esignRenter=RenterSign
            agreement.save()
            room=get_object_or_404(Post_Ad_For_Room,id=roomid)
            print(agreement)
            return render(request,'RoomRent/lease_agreement.html',{'agreement':agreement,'room':room})

        else:
            print(type(details))
            details=details[1:len(details)-1]
            details=details.split(",")
            lst=[]
            print('---------> ',details)
            for i in details:
                lst.append(i[i.index("'")+1:len(i)-1])
            print(lst,"------------------->")
            agreement=Agreement.objects.get(renterEmail=lst[1],ownerID=lst[3],roomId=lst[4],renterName=lst[2],id=int(lst[0]))

            room=get_object_or_404(Post_Ad_For_Room,id=lst[4])
            if agreement.esignRenter =='None':
                r=1
            else:
                r=0


            #agreement=Agreement(renterEmail=details[0])
            return render(request,'RoomRent/lease_agreement.html',{'agreement':agreement,'room':room,'r':r})


def LeaseAgreement(request,mail):
    content=mail.split(" * ")
    html_content=render_to_string('RoomRent/AgreementInviteEmail.html',{'content':content})
    text_content=strip_tags(html_content)
    email=EmailMultiAlternatives(
    'testing',
    text_content,
    settings.EMAIL_HOST_USER,
    [content[1]]
    )
    email.attach_alternative(html_content,'text/html')
    email.send()

    return render(request,'RoomRent/lease_agreement.html')

def AgreementDetailForm(request):
    if request.method=='POST':
        if request.POST.get('RenterEmail'):
            renterName=request.POST.get('RenterName')
            rentMailId=request.POST.get('RenterEmail')
            ownerName=request.POST.get('OwnerName')
            roomID=int(request.POST.get('roomId'))
            sdate=request.POST.get('start_date')
            period=request.POST.get('period')
            edate=request.POST.get('end_date')
            room=get_object_or_404(Post_Ad_For_Room,id=roomID)

            agreement=Agreement()
            agreement.ownerID=ownerName
            #u=User.objects.filter(email=rentMailId)
            #Rid=u[0].id
            agreement.renterName=renterName
            agreement.renterEmail=rentMailId
            agreement.ownerEmail=request.user.email
            agreement.roomId=room
            agreement.monthlyDateOfRent='none'
            agreement.startDateOfRent=sdate
            agreement.endDateOfRent=edate
            agreement.period=period
            agreement.save()
            roomid=room
            o=1


            #renterID=User.objects.get(email=)
            #agreement.renterID=
            return render(request,'RoomRent/lease_agreement.html',{'renterName':renterName,'renterMailID':rentMailId,'ownerName':ownerName,'room':room,
            'sdate':sdate,'period':period,'edate':edate,'o':o,'agreement':agreement
            })

        else:

            roomid=request.POST.get('room')
            rname=request.POST.get('rname')
            oname=request.POST.get('oname')
            remail=request.POST.get('remail')
            OwnerSign=request.POST.get('OwnerSign')
            Id=request.POST.get('id')
            print(roomid,rname,oname,remail)
            agreement=list(Agreement.objects.filter(renterEmail=remail,ownerID=oname,roomId=roomid,renterName=rname,id=int(Id)))
            agreement=agreement[0]
            agreement.esignOwner=OwnerSign
            agreement.save()
            room=get_object_or_404(Post_Ad_For_Room,id=roomid)
            print(agreement)
            sendAgree=1

            lst_of_detail=str(agreement.id)+" * "+remail+" * "+rname+' * '+oname+' * '+str(room.id)+' * '+room.Address+' * '+room.Landmark+' * '+room.room_in_city+' * '+room.room_in_state+' * ' +str(room.room_pin)
            return render(request,'RoomRent/lease_agreement.html',{'agreement':agreement,'room':room,'sendAgree':sendAgree,'lst_of_detail':lst_of_detail})
    return render(request,'RoomRent/agreement_details.html')


def chatList(request,f=0):
    userId=User.objects.get(id=request.user.id)
    lst=ChatRoom.objects.filter(Sender=userId)[::-1]
    dict={}
    unseen_msg=[]
    d={}


    for i in lst:
        u=User.objects.get(id=i.ReceiverEnd)
        r=ChatRoom.objects.filter(Sender=i.ReceiverEnd,ReceiverEnd=request.user.id)
        dict[u.username]=r[0]
        d[u.username]=0

        s=dict[u.username].session_chat_token[1:len(dict[u.username].session_chat_token)-1]
        unseen_msg.append(s.split(','))


    for i in range(len(unseen_msg)):
        unseen_msg[i]=len(unseen_msg[i])
    k=0
    print("Unseen Msg is  ",unseen_msg)
    for i,j in d.items():
        if unseen_msg[k]==1:
            d[i]=0
        else:
            d[i]=unseen_msg[k]
        k+=1
    print(d)
    if f==1:
        c=0
        for i,j in d.items():
            c+=int(j)

        return c



    return render(request,'RoomRent/chat_list.html',{'dict':dict,'d':d})

"""
def updateStage(request):
    s=request.GET.get('s')
    rId=53
    renterxID=2
    rid=User.objects.get(id=renterxID )
    roid=Post_Ad_For_Room.objects.get(id=rId)
    oid=User.objects.get(id=request.user.id)
    user_activity=UserActivity.objects.filter(renterID=rid,roomId=roid,ownerID=oid)
    user_activity=user_activity[0]

    user_activity.stage=str(int(s)+1)
    user_activity.meettingDone='true'
    user_activity.save()

    return HttpResponse('')



def UpdateDate(request):
    d1=request.GET.get('d1')
    d2=request.GET.get('d2')
    d3=request.GET.get('d3')
    print(d1,d2,d3)

    rId=53
    renterxID=2
    rid=User.objects.get(id=renterxID )
    roid=Post_Ad_For_Room.objects.get(id=rId)
    oid=User.objects.get(id=request.user.id)
    user_activity=UserActivity.objects.filter(renterID=rid,roomId=roid,ownerID=oid)
    user_activity=user_activity[0]
    user_activity.meettingDates=str(d1+"*"+d2+"*"+d3)
    user_activity.stage=1
    user_activity.save()
    print(user_activity.meettingDates,user_activity)
    return HttpResponse('true')
"""

def ActivityDetail(request):

    return render(request,'RoomRent/activity.html')


def updateToken(request):
    global senderObject
    global receiverObject

    m1=request.GET.get('m1')
    m2=request.GET.get('m2')



    if str(m1)!='undefined' or str(m1) != '0':
        m1=int(m1)
        l1=json.loads(senderObject.session_chat_token)
        if len(l1)!=0:
            a1=l1.index(m1)
            senderObject.session_chat_token=json.dumps(l1[a1+1:])
            senderObject.save()
    if str(m2)!='undefined' or str(m2) != '0':
        m2=int(m2)
        l2=json.loads(receiverObject.session_chat_token)
        if len(l2)!=0:
            a2=l2.index(m2)
            receiverObject.session_chat_token=json.dumps(l2[a2+1:])
            receiverObject.save()

    print(m1,m2)
    print(senderObject,receiverObject,"mill gaya he object")

    return HttpResponse('Aaygaa he update token mai chilll !!')



def Ago(id,receiverPerson):
    t=None
    ago=None
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(minutes=(60*12)))
    users = (user for user in  user_status)

    from datetime import datetime
    for u in users:
        if u.user_id==id:
            t=u.last_activity
            user_last_login=u.last_activity
            user_name=receiverPerson.Sender.username
            user_last_login=str(user_last_login).split(" ")
            date=user_last_login[0]
            time=(user_last_login[1][0:5]).split(":")
            print("R login time",time)
            h=int(time[0])
            m=time[1]
            if h>12:
                h=str(h-12)
                s=h+":"+str(m)+' pm.'
            else:
                s=str(h)+":"+str(m)+' am.'

            ago="last seen on "+s
    return ago


from django.shortcuts import redirect
def ChatApp(request,id):
    id=id
    print(id,request.user.id)
    if int(id)==int(request.user.id):
        return redirect('/')

    rsv_data=None
    sdn_data=None
    whole_msg_buffer=None

    #id=int(request.GET.get('id', ''))
    user=User.objects.get(id=request.user.id)
    rsvPer=User.objects.get(id=int(id))
    if ChatRoom.objects.filter(Sender=rsvPer,ReceiverEnd=request.user.id).exists():
        receiverPersonList=ChatRoom.objects.filter(Sender=rsvPer,ReceiverEnd=request.user.id)
        senderPersonList=user.chatWith.filter(ReceiverEnd=id)
        rsv_data=json.loads(receiverPersonList[0].sender_side_msg)
        sdn_data=json.loads(senderPersonList[0].sender_side_msg)
        whole_msg_buffer=json.loads(receiverPersonList[0].whole_msg_buffer)


    return render(request,'RoomRent/Chat.html',{'id':id,'rsv_data':rsv_data,'sdn_data':sdn_data,'whole_msg_buffer':whole_msg_buffer})

def allMsg(request):

            global senderObject
            global receiverObject
            print("*"*100)

            lst=[]
            id=int(request.GET.get('id', ''))
            user=User.objects.get(id=request.user.id)
            rsvPer=User.objects.get(id=int(id))
            #receiverPerson=ChatRoom.objects.filter(Sender=rsvPer,ReceiverEnd=request.user.id)
            receiverPersonList=ChatRoom.objects.filter(Sender=rsvPer,ReceiverEnd=request.user.id)
            senderPersonList=user.chatWith.filter(ReceiverEnd=id)


            for i in receiverPersonList:
                receiverPerson=i
                break
            for i in senderPersonList:
                senderPerson=i
                break
            user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
            users = (user for user in  user_status)
            online_user_lst=[]
            for u in users:
                if u.id==id:
                    status="online"
                else:
                    status=Ago(id,receiverPerson)
            print(status,"kkjfnjkfkfn")
            senderObject=senderPerson
            receiverObject=receiverPerson
            print(receiverPersonList,senderPersonList)
            if receiverPersonList and senderPersonList:
                l1=json.loads(senderPerson.session_chat_token)
                l2=json.loads(receiverPerson.session_chat_token)
                l3=l1+l2
                l2.sort()
                print("Let count how many time this fuction exexute at one click")
                print(l1)
                print(l2)
                print(l3)


                d={'rsv_data':json.loads(receiverPerson.sender_side_msg),'sdn_data':json.loads(senderPerson.sender_side_msg),
                'whole_msg_buffer':json.loads(receiverPerson.whole_msg_buffer),'lst':l3,'l1':l1,'l2':l2,'status':status,
                'rsv_name':rsvPer.username}
                d=json.dumps(d)
                return HttpResponse(d)
            else:
                return HttpResponse('False')







def MsgSender(request):
    global senderObject
    global receiverObject
    global allow_Or_Not
    id_of_opp_person=int(request.GET.get('id', ''))
    msg=str(request.GET.get('data', ''))
    print('#'*100)
    print(msg)
    senderPerson=ChatRoom.objects.filter(Sender=request.user,ReceiverEnd=id_of_opp_person)
    if senderPerson:
        senderPerson=senderPerson[0]
        rsvPer=User.objects.get(id=int(id_of_opp_person))
        receiverPerson=ChatRoom.objects.filter(Sender=rsvPer,ReceiverEnd=request.user.id)
        receiverPerson=receiverPerson[0]
        senderObject=senderPerson
        receiverObject=receiverPerson
        sc=senderPerson.msg_token
        rc=receiverPerson.msg_token
        mc=max(sc,rc)
        lstMsg = json.loads(senderPerson.whole_msg_buffer)
        sender_side_messsage=json.loads(senderPerson.sender_side_msg)
        session_chat_token=json.loads(senderPerson.session_chat_token)
        sender_side_messsage[mc+1]=msg
        session_chat_token.append(mc+1)
        lstMsg[mc+1]=msg
        session_token=json.dumps(session_chat_token)
        sdn_buffer=json.dumps(sender_side_messsage)
        msgStr = json.dumps(lstMsg)

        senderPerson.whole_msg_buffer=msgStr
        senderPerson.sender_side_msg=sdn_buffer
        senderPerson.session_chat_token=session_token

        receiverPerson.whole_msg_buffer=msgStr
        senderPerson.msg_token=mc+1

        #print(senderPerson.msg_token,receiverPerson.msg_token)
        senderPerson.save()
        receiverPerson.save()
    else:
        chat_room_of_sender=ChatRoom()
        chat_room_of_receiver=ChatRoom()
        chat_room_of_sender.Sender=User.objects.get(id=request.user.id)
        chat_room_of_sender.ReceiverEnd=int(id_of_opp_person)
        lst_msg_init={}
        print(chat_room_of_sender.msg_token,chat_room_of_receiver.msg_token)
        #lst_msg_init.append(msg)
        lst_msg_init[chat_room_of_sender.msg_token+1]=msg
        msg = json.dumps(lst_msg_init)
        chat_room_of_sender.whole_msg_buffer= msg
        chat_room_of_sender.sender_side_msg= msg
        chat_room_of_sender.session_chat_token=json.dumps([1])
        chat_room_of_sender.msg_token=1
        chat_room_of_receiver.Sender=User.objects.get(id=int(id_of_opp_person))
        print(chat_room_of_receiver.Sender)
        chat_room_of_receiver.ReceiverEnd=request.user.id
        chat_room_of_receiver.whole_msg_buffer=msg
        chat_room_of_receiver.session_chat_token=json.dumps([])
        l={}
        m = json.dumps(l)
        chat_room_of_receiver.sender_side_msg=m



        chat_room_of_sender.save()
        chat_room_of_receiver.save()



    return HttpResponse(1)







def home(request):
    all_room=Post_Ad_For_Room.objects.all()
    top_three=all_room.order_by('-id')[:3]
    all_room=list(all_room)[::-1]

    print(top_three)
    top_three_room_image=[]
    for i in range(len(top_three)):
        image=Room_Image.objects.filter(room_id=top_three[i].id).first()
        top_three_room_image.append(image)



    all_image=Room_Image.objects.filter(room_id=8).first()
    n=len(all_room)
    lst_of_main_image=[]
    for i in range(len(all_room)):
        Rimage=Room_Image.objects.filter(room_id=all_room[i].id).first()
        lst_of_main_image.append(Rimage)

    ns=n//4+ceil((n/4)-(n//4))
    all_object_zip=zip(list(all_room),lst_of_main_image)
    top_three_object_zip=zip(list(top_three),top_three_room_image)
    r=range(1,n)
    cl=0
    if request.user.is_authenticated:
        cl=chatList(request,1)



    return render(request,'RoomRent/home.html',{'all_room':all_room,'n':n,'ns':ns,'r':r,'all_image':all_image,
    'all_object_zip':all_object_zip,'top_three_object_zip':top_three_object_zip,'cl':cl})

import requests
import bs4
def Post_Room(request):
    geolocator = Nominatim(user_agent="geoapiExercises")
    if request.method=='POST':
            buildingName=request.POST.get('buildingName')
            name=request.POST.get('name')
            mobile_no=request.POST.get('mobile_no')
            State=request.POST.get('State')
            City=request.POST.get('city')
            pin=request.POST.get('pin')
            Monthly_Rent=request.POST.get('Monthly_Rent')
            Deposite=request.POST.get('Deposite')
            floor=request.POST.get('floor')
            total_floor=request.POST.get('total_floor')
            total_room=request.POST.get('total_room')
            Address=request.POST.get('Address')
            Landmark=request.POST.get('Landmark')
            Description=request.POST.get('Description')
            Bathroom=request.POST.getlist('Bathroom')
            Room_Type=request.POST.getlist('Room_Type')
            Available_For=request.POST.getlist('Available_For')
            Image_List=request.FILES.getlist('file[]')


            # Object of Post_Ad_For_Room
            Room=Post_Ad_For_Room()
            Room.owner_email=request.user.email
            Room.user=User.objects.get(id=request.user.id)
            Room.buildingName=buildingName
            Room.owner_mobile_number=mobile_no
            Room.room_in_state=State
            Room.room_in_city=City
            Room.room_pin=pin
            Room.room_description=Description
            Room.room_rent=int(Monthly_Rent)
            Room.room_desposite=int(Deposite)
            Room.room_floor=int(floor)
            Room.total_floor=int(total_floor)
            Room.total_room=int(total_room)
            Room.Bathroom=Bathroom[0]
            Room.House_Type=Room_Type[0]
            Room.Available=Available_For[0]
            Room.Address=Address
            Room.Landmark=Landmark
            location = geolocator.geocode(pin)
            Room.full_location=location
            Room.owner_name=name
            Room.user_primary_key=str(request.user.id)
            Room.save()


            Room.save()
            print(Image_List)
            for img in Image_List:
                    fs=FileSystemStorage()
                    file_path=fs.save(img.name,img)
                    pimage=Room_Image(room_id=Room,image=file_path)
                    pimage.save()




            hospital='hospital in '+Room.room_pin+" "+Room.room_in_city
            clg='school/collage near by '+Room.room_pin+" "+Room.room_in_city
            company='company near by '+Room.room_pin+" "+Room.room_in_city
            shop='shop near by'+Room.room_pin+" "+Room.room_in_city
            hotel='hostel near by '+Room.room_pin+" "+Room.room_in_city
            buildingViewInMap="google map of "+Room.room_pin+" "+Room.room_in_city
            lst_of_nearby=[hospital,clg,company,shop,hotel,buildingViewInMap]





            lst_of_ans=[]

            for ser in lst_of_nearby:

                url = 'https://google.com/search?q=' + ser
                request_result = requests.get(url)
                soup = bs4.BeautifulSoup(request_result.text,"html.parser")
                a = soup.find_all( 'a')
                a=list(a)
                lst=[]
                for i in a:
                    lst.append(str(i)+"")

                for i in lst:
                    if  'href="https://maps.google.com/maps?q=' in i:
                        lst_of_ans.append(i)
                        break
            lst=[]
            for i in lst_of_ans:
                s=i.find('https')
                e=i.find('>Maps</a>')
                lst.append(i[s:e-1])
            try:
                Room.near_by_hospital=lst[0]+',-105.0668&output=svembed'
                Room.near_by_school=lst[1]+',-105.0668&output=svembed'
                Room.near_by_company=lst[2]+',-105.0668&output=svembed'
                Room.near_by_shop=lst[3]+',-105.0668&output=svembed'
                Room.near_by_hotel=lst[4]+',-105.0668&output=svembed'
                Room.location_map=lst[5]+',-105.0668&output=svembed'
                Room.save()
            except:
                pass


    return render(request,'RoomRent/Post_Room_Form.html')

"""
p=True
    form=TextForm()
    lst=[]

    Image_List=ImageGAN.objects.all()
    if request.method=='POST':
        form=TextForm(request.POST)
        if form.is_valid():
            new_f=form.save(commit=False)
            new_f.user=request.user
            new_f.save()
        p=False
        lst=re.split(r'[,;]+', str(form.cleaned_data['body']))
     return render(request,'TextConverter/Output.html',{'form':form,'Image_List':Image_List,'p':p,'lst':lst})
 """


def Room_Detail(request,room_id):

    #room=Post_Ad_For_Room.objects.all().filter(id=room_id)
    room=get_object_or_404(Post_Ad_For_Room,id=room_id)
    all_image=room.photos.filter()
    imageList=[]
    for i in all_image:
        imageList.append(i.image)



    return render(request,'RoomRent/RoomDetail.html',{'room':room,'imageList':imageList})





def History(request):
        username = request.user
        lst=[]
        lst_time=[]
        q=Text.objects.all().filter(user=username)
        for i in q:
            lst.append(i.body)

        return render(request,'RoomRent/History.html',{'lst':lst})




def resend_OTP(request):
    if request.method=='GET':
        get_usr=request.GET['usr']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr=User.objects.get(username=get_usr)
            usr_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=usr,otp=usr_otp)
            mess=f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"
            send_mail(
            'Welcome to Imaginary World - Verify your Email',
            mess,
            settings.EMAIL_HOST_USER,
            [usr.email],
            fail_silently=False,
            )

            return HttpResponse('Resend')
    return HttpResponse("Can't Send")









def SignUpView(request):
    form=SignUpForm()
    username=''
    user_firstname=''
    user_lastname=''
    if request.method=="POST":

            get_otp=request.POST.get('otp')
            get_otp_form=request.POST.get('otpform')
            if get_otp_form:
                if get_otp:

                    get_username=request.POST.get('usr')
                    usr=User.objects.get(username=get_username)

                    if int(get_otp) ==UserOTP.objects.filter(user=usr).last().otp:
                        print('Account Verify success')
                        usr.is_active=True
                        usr.save()
                        otp_verify=True
                        return HttpResponseRedirect('/accounts/login/')
                    else:
                        wrg_wrong_otp=True
                        return render(request,'RoomRent/signup.html',{'otp':True,'usr':usr,'wrg_wrong_otp':wrg_wrong_otp})
                else:
                    get_username=request.POST.get('usr')
                    usr=User.objects.get(username=get_username)
                    wrg_wrong_otp=True
                    return render(request,'RoomRent/signup.html',{'otp':True,'usr':usr,'wrg_wrong_otp':wrg_wrong_otp})






            vemail=False
            error_msg='Email is already exists'
            try:

                    user_email = request.POST.get('email')
                    username = request.POST.get('username')
                    user_firstname = request.POST.get('first_name')
                    user_lastname = request.POST.get('last_name')
                    if  User.objects.filter(email=user_email).exists():
                            vemail=True
                    else:
                        vemail=False
            except:
                    vemail=False

            if vemail==True:
                return render(request,'RoomRent/signup.html',{'form':form,'v':vemail,'error_msg':error_msg,'username':username,
                'user_firstname':user_firstname,'user_lastname':user_lastname})
            else:
                pass

            v=True
            try:
                    vpassword = request.POST.get('password')
            except:
                    vpassword=False

            try:
                    vpassworda = request.POST.get('password_again')
            except:
                    vpassworda=False
            error_msg='Password Not Match'
            if vpassword and vpassworda:
                if vpassword == vpassworda:
                    v=False
                else:
                    return render(request,'RoomRent/signup.html',{'form':form,'v':v,'error_msg':error_msg,'username':username,
                    'user_firstname':user_firstname,'user_lastname':user_lastname})
            else:
                error_msg='Please check your passwaord again'
                return render(request,'RoomRent/signup.html',{'form':form,'v':v,'error_msg':error_msg,'username':username,
                'user_firstname':user_firstname,'user_lastname':user_lastname})


            form=SignUpForm(request.POST)
            if form.is_valid():
                usrname=form.cleaned_data.get('username')
                print(usrname)
                user=form.save()
                user.set_password(user.password)
                user.save()
                usr=User.objects.get(username=usrname)
                usr.is_active=False
                usr.save()


                usr_otp=random.randint(100000,999999)
                UserOTP.objects.create(user=usr,otp=usr_otp)
                mess=f"Hello {user_firstname},\nYour OTP is {usr_otp}\nThanks!"
                send_mail(
                'Welcome to Imaginary World - Verify your Email',
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False,
                )
                return render(request,'RoomRent/signup.html',{'otp':True,'usr':usr})
                #return HttpResponseRedirect('/accounts/login/')
    return render(request,'RoomRent/signup.html',{'form':form})



def User_Login(request):
    if request.method=='POST':
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
    fm=AuthenticationForm()
    return render(request,'RoomRent/login.html',{'form':fm})

def User_LogOut(request):
    logout(request)
    return HttpResponseRedirect('/')
