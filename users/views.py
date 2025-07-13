from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cart.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserRegistrationForm, ProfileForm, UserLoginForm


def login(request):
    if request.method == 'POST':  # это проверяет, был ли отправлен post запрос или нет на фронте за это отвечает это строка
        # <form action="{% url 'user:login' %}" method="POST">
        form = UserLoginForm(data=request.POST)  # UserLoginForm создаёт объект формы, передавая в неё данные, введённые пользователем.
        # request.POST содержит введённые в форму данные password и username
        if form.is_valid():  # Если форма заполнена правильно, продолжаем вход.
            # Если форма содержит ошибки (например, пустое поле или неверный формат ввода), выполнение дальше не пойдёт.
            username = request.POST['username']  # Извлекаем введённые пользователем логин и пароль из request.POST.
            password = request.POST['password']  # Теперь username и password содержат введённые данные.
            user = auth.authenticate(username=username,password=password)  # проверяет, существует ли пользователь с такими параметрами, если нет, то user не создаётся

            session_key = request.session.session_key

            if user:
                auth.login(request,user)  # Если пользователь найден, вызываем auth.login(request, user), чтобы сохранить информацию о входе.
                messages.success(request, f"{username} Ты успешно авторизировался")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next')
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:main_page'))  # переводит нас на основную страницу
    else:
        form = UserLoginForm()  # если post запроса не найдено, то оно передаёт шаблон для заполнения в form, если это не передавать, то ошибки не будут выдаваться
    context = {
        'title': 'Вход в систему',
        'form': form,
    }
    return render(request, 'users/login.html', context)  # и тут оно даёт нашу переделанную форму если не было post

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save() # сохранение формы в бд

            session_key = request.session.session_key

            user = form.instance  # это берёт сохранённую форму в бд и присваивает её в user
            auth.login(request, user)
            messages.success(request, f"{user.username} Ты успешно зарегистрировался и авторизировался")

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse('main:main_page'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main_page'))

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES) #data это словарь со всеми данными которые мы ввели
        # request.user — это объект текущего пользователя, который уже аутентифицирован в системе, она будет загружать данные из текущего
        # профиля пользователя и использовать их для предзаполнения полей формы
        # форма подставит в поля текущие значения из модели User (например, имя, электронную почту и т. д.)
        #request.FILES — это словарь, который содержит файлы, отправленные через форму с использованием enctype="multipart/form-data".
        # Этот атрибут нужен, чтобы обработать файлы, такие как изображения, документы и прочее, нам он по сути не нужен.
        if form.is_valid():
            form.save()
            user = form.instance
            messages.success(request, f"{user.username} Ты успешно изменил профиль")
            return HttpResponseRedirect(reverse('main:main_page'))
    else:
        form = ProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(Prefetch('orderitem_set',queryset=OrderItem.objects.select_related("product"))).order_by('-id')
    context = {
        'title': 'Профиль',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)


def user_cart(request):
    context = {
        'title': 'Профиль',
    }
    return render(request, 'cart/no_name_client.html',context)


