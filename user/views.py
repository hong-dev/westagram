import json
import bcrypt
import jwt


from .models import User

from django.views import View
from django.http  import HttpResponse, JsonResponse
from django.db.models import Q


class UserView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        User(
            name     = user_data['name'],
            email    = user_data['email'],
            phone    = user_data['phone'],
            password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        ).save()

        return HttpResponse(status=200)

    def get(self, request):
        user_data = User.objects.all()
        users     = []
        for user in user_data:
            users.append({
                'name'     : user.name,
                'email'    : user.email,
                'phone'    : user.phone,
                'password' : user.password
            })

        return JsonResponse({'users':users}, status = 200)


class LoginView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        user_name  = user_data.get('name', None)
        user_email = user_data.get('email', None)
        user_phone = user_data.get('phone', None)

        try:
            if User.objects.filter(Q(name = user_name)|Q(email = user_email)|Q(phone=user_phone)).exists():
                user = User.objects.filter(Q(name = user_name)|Q(email = user_email)|Q(phone=user_phone))[0]
                if bcrypt.checkpw(user_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'id': user.id}, 'SECRET_KEY', algorithm = 'HS256').decode('utf-8')
                    return JsonResponse({"token":token}, status = 200)
                return HttpResponse(status = 401)
            return HttpResponse(status = 400)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

