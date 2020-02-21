import json
import bcrypt
import jwt

from .models     import Comment
from user.models import User
from user.utils import login_required

from django.views import View
from django.http  import HttpResponse, JsonResponse


class CommentView(View):
    @login_required
    def post(self, request):
        user_data   = json.loads(request.body)
        try:
            if User.objects.filter(name = user_data['name']).exists():
                Comment(
                    name    = user_data['name'],
                    comment = user_data['comment']
                ).save()
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        except KeyError:
            return HttpResponse(status=400)

    @login_required
    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'comments':list(comment_data)}, status=200)

