from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import SendSMSRequestSerializer, SendBulkSMSRequestSerializer
from .eskiz_sms import EskizSMS

class SendSMSToUser(APIView):
    @swagger_auto_schema(
        request_body=SendSMSRequestSerializer,
        responses={200: openapi.Response("Success")}
    )
    def post(self, request):

        serializer = SendSMSRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        message = serializer.validated_data['message']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        sms_service = EskizSMS()
        response_data = sms_service.send_sms(user.phone_number, message)

        return Response(response_data, status=status.HTTP_200_OK)



class SendSMSToAllUsers(APIView):

    @swagger_auto_schema(
        request_body=SendBulkSMSRequestSerializer,
        responses={200: openapi.Response("Success")},
    )
    def post(self, request):
        serializer = SendBulkSMSRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.validated_data['message']
        print(f"📩 Received message: {message}")

        sms_service = EskizSMS()
        users = User.objects.all()

        responses = []
        for user in users:
            phone_number = user.phone_number
            print(f"📞 Sending SMS to: {phone_number}")

            try:
                response_data = sms_service.send_sms(phone_number, message)
                print(f"✅ Response: {response_data}")
            except Exception as e:
                response_data = {"error": str(e)}
                print(f"❌ Error sending SMS: {e}")

            responses.append({"phone_number": phone_number, "response": response_data})

        return Response(responses, status=status.HTTP_200_OK)