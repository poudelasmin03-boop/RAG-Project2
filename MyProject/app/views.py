from django.shortcuts import render
from django.http import JsonResponse
from .bot import create_Database
from .rag import get_input
# Create your views here.
def home(request):
  return render(request,"home.html")


def chatbot(request):
  return render(request,"chatbot.html")


def chatbot_message(request):
  if request.method == "POST":
    user_input = request.POST.get("message").strip()
    print(f"User input  {user_input} this is enput")

    if not user_input :
      return JsonResponse({
        "success":False,
        "message":"Please enter some input."}
      )

    try:
       response = get_input(user_input)
       print(response)
       return JsonResponse({
         "success":True,
        "message":response
       })
       

    except Exception as e:
      return JsonResponse({
        "success":False,
        "message":str(e)
      })   


  return JsonResponse({
      "success":False,
      "message":"Invalid"
    })



def upload_pdf(request):
  if request.method == "POST":
    pdf_file = request.FILES.get("pdf_file")


    if pdf_file is None:
       return JsonResponse({
              "success":False,
              "message":"Please enter some input."}
            )
    response = create_Database(pdf_file)
    print("PDF received:", pdf_file.name)

    return JsonResponse({
            "success": True,
            "message": "PDF uploaded successfully."
        })

  return JsonResponse({
        "success": False,
        "message": "Invalid request."
    })
      
  


    
    