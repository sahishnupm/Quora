from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.template import loader
from users.models import Users

def home(request):
    return render(request, 'users/login.html')


class CreateUser(View):
    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('password')

        if username and password:
            user_model = Users(name=username, password=password)
            user_model.save()

            request.session['user'] = user_model.id
            
            return JsonResponse({}, status=200)
        else:
            return JsonResponse(status=500)
    

class Login(View):
    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('password')

        if username and password:
            user = Users.objects.filter(name=username, password=password).values("id")
            if user:
                request.session['user'] = user[0]['id']
                print(request.session['user'])
                return JsonResponse({'status':True}, status=200)
            else:
                return JsonResponse({'status':False}, status=200)


        else:
            return JsonResponse(status=500)
        
class Logout(View):
    def post(self, request):
        try:
            del request.session['user']
        except KeyError:
            pass
        
        return JsonResponse({'status':True}, status=200)



