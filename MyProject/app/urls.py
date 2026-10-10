from django.urls import path
from .views import home,chatbot,chatbot_message,upload_pdf


urlpatterns = [
  path("",home,name="home"),
  path("chatbot/",chatbot,name="chatbot"),
   path("chat_message/",chatbot_message,name="chatbot_message"),
    path("upload_pdf/",upload_pdf,name="upload_pdf")
]