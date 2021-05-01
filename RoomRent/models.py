from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
STATUS = (
    ('vacant','Vacant'),
    ('occupied', 'Occupied')
)

class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()

class Post_Ad_For_Room(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_primary_key=models.CharField(max_length = 100,default='none')
    date=models.DateTimeField(auto_now=True)
    owner_name=models.CharField(max_length = 100,default='none')
    owner_mobile_number=models.CharField(max_length = 100,default='none')
    owner_email=models.CharField(max_length = 50)
    room_in_state=models.CharField(max_length = 50)
    room_in_city=models.CharField(max_length = 50)
    room_pin=models.CharField(max_length = 10)
    room_description=models.TextField(default='none')
    room_rent=models.IntegerField()
    room_desposite=models.IntegerField()
    room_floor=models.SmallIntegerField()
    total_floor=models.SmallIntegerField()
    total_room=models.SmallIntegerField(default='1')
    Bathroom=models.CharField(max_length = 50)
    House_Type=models.CharField(max_length = 50)
    Available=models.CharField(max_length = 50)
    Address=models.TextField()
    Landmark=models.CharField(max_length = 100)
    status = models.CharField(max_length=6, choices=STATUS, default='vacant')
    full_location=models.CharField(max_length=100,default='NA')
    near_by_hospital=models.CharField(max_length = 500,default='none')
    near_by_school=models.CharField(max_length = 500,default='none')
    near_by_company=models.CharField(max_length = 500,default='none')
    near_by_hotel=models.CharField(max_length = 500,default='none')
    near_by_shop=models.CharField(max_length = 500,default='none')
    location_map=models.CharField(max_length = 500,default='none')
    buildingName=models.CharField(max_length = 100,default='none')




class Room_Image(models.Model):
    room_id=models.ForeignKey(Post_Ad_For_Room,on_delete=models.CASCADE,related_name='photos')
    image=models.FileField(max_length=255)




class ChatRoom(models.Model):
    Sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='chatWith')
    ReceiverEnd=models.IntegerField()
    whole_msg_buffer = models.TextField(default=None)
    sender_side_msg=models.TextField(blank=True,default='none')
    msg_token=models.IntegerField(default=0)
    session_chat_token=models.TextField(blank=True,default='none')




from rest_framework import serializers

clas s ChatRoomSerializer(serializers.Serializer):
    Sender=serializers.CharField(max_length=100)
    ReceiverEnd=serializers.IntegerField()
    whole_msg_buffer = serializers.CharField(max_length=100)
    sender_side_msg=serializers.CharField(max_length=100)


class Agreement(models.Model):
    ownerID=models.CharField(max_length=100,default='None')
    renterName=models.CharField(max_length=100,default='None')
    renterEmail=models.CharField(max_length=100,default='None')
    ownerEmail=models.CharField(max_length=100,default='None')
    roomId=models.ForeignKey(Post_Ad_For_Room,on_delete=models.CASCADE,related_name='roomID')
    monthlyDateOfRent=models.CharField(max_length=100,default='None')
    startDateOfRent=models.CharField(max_length=100,default='None')
    period=models.CharField(max_length=100,default='None')
    endDateOfRent=models.CharField(max_length=100,default='None')
    esignOwner=models.CharField(max_length=100,default='None')
    esignRenter=models.CharField(max_length=100,default='None')




class Payment(models.Model):
    email_of_payment_sender=models.CharField(max_length=100,default='None')
    email_of_payment_receiver=models.CharField(max_length=100,default='None')
    name_of_receiver=models.CharField(max_length=100,default='None')
    room_id=models.ForeignKey(Post_Ad_For_Room,on_delete=models.CASCADE,related_name='room_id')
    payment_done=models.BooleanField(default=False)
    message=models.CharField(max_length=100,default='None')
    amount_to_pay=models.CharField(max_length=100,default='None')
    payment_id=models.CharField(max_length=100,default='None')



























"""class Text(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='text')
    body=models.TextField(default="",)
    created=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('created',)


class ImageGAN(models.Model):
    image =models.ImageField(upload_to='picture',max_length=100,null=True)
    text=models.TextField(default="")
    addedOn=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('addedOn',)
"""
