import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import Item, Review
import pdb
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import base64
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from functools import wraps

# Декоратор для авторизации и проверки прав пользователя
def auth_staff(func):
    @wraps(func)
    def wrapper(request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                uname, passwrd = base64.b64decode(auth[1]).decode('UTF-8').split(':')
                user = authenticate(request, username=uname, password=passwrd)
                if user is not None:
                    login(request, user)
                    if user.is_staff == True:
                        return func(request)
                    else:
                        return HttpResponse(status=403, content='Not enough autority')
                else:
                    return HttpResponse(status=401, content='Wrong password or username')
    return wrapper


# Шаблон валидации
Item_SHEMA = {
    "properties": {
        "title": {
            "type": "string",
            "maxLength": 64,
            "minLength": 1
        },
        "description": {
            "type": "string",
            'maxLength': 1024,
            "minLength": 1
        },
        "price": {
            "type": "integer",
            "maximum": 1000000,
            "minimum": 1
        },
    },
    "required": ["title", "description", "price"],
}

Review_SHEMA = {
    "properties": {
        "text": {
            "type": "string",
            'maxLength': 1024,
            "minLength": 1
        },
        "grade": {
            "type": "integer",
            "maximum": 10,
            "minimum": 1
        },
    },
    "required": ["text", "grade"],
}


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(auth_staff, name='dispatch')
class AddItemView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, Item_SHEMA)
            modl = Item(title=data['title'], description=data['description'],
                        price=data['price'])
            modl.save()
            return JsonResponse({'id': modl.id, 'name': modl.title}, status=201)
        except ValidationError:
            return JsonResponse({'errors': 'Запрос не прошёл валидацию'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Error'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            validate(data, Review_SHEMA)
            id = Item.objects.get(pk=int(item_id))
            modl = Review(text=data['text'], grade=data['grade'],
                          item=id)
            modl.save()
            return JsonResponse({'id': modl.id}, status=201)
        except ValidationError:
            return JsonResponse({'errors': 'Запрос не прошёл валидацию'}, status=400)
        except json.JSONDecodeError as er:
            return JsonResponse({'errors': er.message}, status=400)
        except Item.DoesNotExist:
            return JsonResponse({'errors': 'Товара с таким id не существует'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):
        def get(self, request, item_id):
            try:
                it = Item.objects.get(pk=int(item_id))
                list_rev = []
                data={}
                rev = Review.objects.filter(item=int(item_id)).order_by('-id')
                if 1 <= rev.count() <= 5:
                    for r in rev:
                        list_rev.append({'id': r.id, 'text': r.text, 'grade': r.grade})
                    data = {'id': it.id, 'title': it.title, 'description': it.description, 'price': it.price,
                            'reviews': list_rev}

                elif rev.count() == 0:
                    data = {'id': it.id, 'title': it.title, 'description': it.description, 'price': it.price,
                            'reviews': []}

                elif rev.count() > 5:
                    for r in rev[:2]:
                        list_rev.append({'id': r.id, 'text': r.text, 'grade': r.grade})
                    data = {'id': it.id, 'title': it.title, 'description': it.description, 'price': it.price,
                            'reviews': list_rev}
                return JsonResponse(data, status=200)
            except Item.DoesNotExist:
                return JsonResponse({'errors': 'Товара с таким id не существует'}, status=404)