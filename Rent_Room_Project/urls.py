"""Text_To_Image_Converter_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from RoomRent import views
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('resendOTP/',views.resend_OTP,name='resendOTP'),
    path('',views.home,name="home"),
    path('uactivity/',views.ActivityDetail,name="uactivity"),
    path('edit_room/(?P<roomID>[a-z0-9-]*)/$',views.EditRoom,name="edit_room"),
    path('success/',views.Payment_Detail_Save,name="success"),
    path('status/',views.ChangeStatus,name="status"),
    path('team/',views.OurTeam,name="team"),
    path('profile/',views.Profile,name="profile"),
    path('edit_profile/',views.EditProfile,name="edit_profile"),
    path('chatlist/',views.chatList,name="chatlist"),
    path('privacyterms/',views.PrivacyTerms,name="privacyterms"),
    path('contact_mail/',views.ContactMail,name="contact_mail"),
    path('payment_method/',views.Payment_Action,name="payment_method"),
    path('agreement_list/',views.AgreementList,name="agreement_list"),
    path('agreement_detail/(?P<agreement>[a-z0-9-]*)/$',views.AgreementDetail,name="agreement_detail"),
    path('lease_agreement/(?P<mail>[a-z0-9-]*)/$',views.LeaseAgreement,name="lease_agreement"),
    path('renter_sign/(?P<details>[a-z0-9-]*)/$',views.ForRenterAgreementSign,name="renter_sign"),
    path('agreement_detail_form/',views.AgreementDetailForm,name="agreement_detail_form"),
    path('chat/(?P<id>[a-z0-9-]*)/$',views.ChatApp,name="chat"),
    path('messanger/',views.MsgSender,name="messanger"),
    path('search_by_city/',views.SearchByRoomCity,name="search_by_city"),
    path('all_msg/',views.allMsg,name="all_msg"),
    path('update_token/',views.updateToken,name="update_token"),
    path('post_room/',views.Post_Room,name="post_room"),
    re_path('room_detail/(\d+)', views.Room_Detail, name='room_detail'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('signup/',views.SignUpView),
path("password-reset/", auth_views.PasswordResetView.as_view(template_name='RoomRent/password_reset.html'), name="password_reset"),
path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='RoomRent/password_reset_done.html'), name="password_reset_done"),
path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='RoomRent/password_reset_confirm.html'), name="password_reset_confirm"),
path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='RoomRent/password_reset_complete.html'), name="password_reset_complete"),


]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#path('UpdateDate/',views.UpdateDate,name="UpdateDate"),
#path('updateStage/',views.updateStage,name="updateStage"),
