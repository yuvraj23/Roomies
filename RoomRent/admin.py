from django.contrib import admin
from .models import *


# Register your models here.




@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','email_of_payment_sender','email_of_payment_receiver','name_of_receiver','room_id','amount_to_pay','message','payment_done','payment_id')


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display=('id','user','time_st','otp',)



@admin.register(Post_Ad_For_Room)
class Post_Ad_For_RoomAdmin(admin.ModelAdmin):
    list_display=('id','user_primary_key','user','date','owner_name','owner_email','owner_mobile_number','room_in_state','room_in_city',
    'room_pin','room_desposite','room_rent','room_desposite','room_floor','total_floor','Bathroom','buildingName','full_location',
    'House_Type','Available','Address','Landmark','room_description','status',)



@admin.register(Room_Image)
class Room_ImageAdmin(admin.ModelAdmin):
    list_display=('id','room_id','image',)


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display=('id','Sender','ReceiverEnd','whole_msg_buffer','sender_side_msg','msg_token','session_chat_token')



@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display=('id','ownerID','roomId')
