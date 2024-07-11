import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User

"""
UserView
--------

Представление, обрабатывающее запросы, связанные с пользователями.

Поддерживаемые методы HTTP:
    - GET: Возвращает список всех пользователей.
    - POST: Создает нового пользователя.
    - PUT: Обновляет информацию о существующем пользователе.
    - DELETE: Удаляет существующего пользователя.

Методы:
    dispatch(request, *args, **kwargs) -> HttpResponse:
        Переопределенный метод, который вызывается Django для обработки входящих HTTP-запросов.
        Применяет декоратор @csrf_exempt, чтобы отключить защиту от CSRF-атак.
    get(request) -> JsonResponse:
        Обрабатывает HTTP GET-запросы и возвращает список всех пользователей в формате JSON.
    post(request) -> JsonResponse:
        Обрабатывает HTTP POST-запросы, создает нового пользователя и возвращает информацию о нем в формате JSON.
    put(request, user_id) -> JsonResponse:
        Обрабатывает HTTP PUT-запросы, обновляет информацию о существующем пользователе и возвращает обновленные данные в формате JSON.
    delete(request, user_id) -> JsonResponse:
        Обрабатывает HTTP DELETE-запросы, удаляет существующего пользователя и возвращает сообщение об успешном удалении.
"""


class UserView(View):
    """ Класс представления, обрабатывает различные HTTP-запросы."""

    @csrf_exempt  # декоратор, который отключает защиту от CSRF
    def dispatch(self, request, *args, **kwargs):
        """Метод для обработки входящих HTTP-запросов."""
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """Метод возвращает список всех пользователей."""
        users = User.objects.all()
        return JsonResponse([{'id': user.id, 'username': user.username, 'email': user.email} for user in users],
                            safe=False)

    @csrf_exempt
    def post(self, request):
        """Метод для добавления нового пользователя."""
        data = json.loads(request.body)
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        user.save()
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email}, status=201)

    @csrf_exempt
    def put(self, request, user_id):
        """Метод обновляет информацию о существующем пользователе."""
        user = User.objects.get(id=user_id)
        data = json.loads(request.body)
        user.username = data['username']
        user.email = data['email']
        user.save()
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email})

    @csrf_exempt
    def delete(self, request, user_id):
        """Метод удаляет существующего пользователя."""
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'Пользователь удален'}, status=204)


@csrf_exempt
def login(request):
    """Метод регистрации и аутентификации пользователей."""
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            return JsonResponse({'message': 'Вы успешно вошли в систему'})
        else:
            return JsonResponse({'error': 'Неправильное имя пользователя или пароль'}, status=401)
    else:
        return JsonResponse({'error': 'Доступ запрещен'}, status=405)
