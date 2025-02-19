from django.urls import path
from .views import SendSMSToUser, SendSMSToAllUsers

urlpatterns = [
    path('send-sms/', SendSMSToUser.as_view(), name='send_sms'),
    path('send-sms-all/', SendSMSToAllUsers.as_view(), name='send_sms_all'),
]
