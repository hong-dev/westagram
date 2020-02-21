import jwt
import json

from user.models import User

from django.http import JsonResponse

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        if access_token:
            try:
                decode = jwt.decode(access_token, 'SECRET_KEY', algorithms=['HS256'])
             #   user_id = decode.get('user', None)
                user = User.objects.get(id=decode['id'])
                request.user = user

            except jwt.DecodeError:
                return JsonResponse({"message" : "잘못된 토큰"}, status = 403)
            except  User.DoesNotExist:
                return JsonResponse({"message" : "존재하지 않는 아이디"}, status = 401)

            return func(self, request, *args, **kwargs)

        return JsonResponse({"message" : "로그인이 필요합니다"}, status = 401)

    return wrapper
