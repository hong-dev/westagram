#from django.shortcuts import render 

import json
from .models      import User, Comment
from django.views import View
from django.http  import HttpResponse, JsonResponse

class UserView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        User(
            name     = user_data['name'],
            email    = user_data['email'],
            phone    = user_data['phone'],
            password = user_data['password']
        ).save()

        return JsonResponse({'message':'Thank you for signing up!'}, status=200)

    def get(self, request):
        user_data = User.objects.all()
        users     = []
        for user in user_data:  #하나의 객체씩 나온다.
            users.append({
                'name'     : user.name,
                'email'    : user.email,
                'phone'    : user.phone,
                'password' : user.password
            })

            return JsonResponse({'users':users}, status = 200)


class LoginView(View):
    def post(self, request):
        user_login_req = json.loads(request.body)
        user_data      = User.objects.values()
        for index in range(len(user_data)):
            if user_login_req['name'] in user_data[index]['name']:
                if user_login_req['password'] == user_data[index]['password']:
                    return JsonResponse({'message':'Welcome! '+ user_login_req['name']}, status=200)
                else:
                    return JsonResponse({'message':'Please check your password :)'}, status=200)
        return JsonResponse({'message':'Please sign up first :)'}, status=200)



class CommentView(View):
    def post(self, request):
        user_com_req   = json.loads(request.body)
        user_data      = User.objects.values()
        for index in range(len(user_data)):
            if user_com_req['name'] in user_data[index]['name']:
                Comment(
                    name    = user_com_req['name'],
                    comment = user_com_req['comment']
                ).save()
                return JsonResponse({'message':'comment saved!'}, status=200)
        return JsonResponse({'message':'Please log in first :)'}, status=200)


    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments':list(comment_data)}, status=200)


