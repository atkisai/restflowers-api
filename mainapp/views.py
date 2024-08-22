# from django.contrib.auth import authenticate, login, logout
# from django.core.mail import EmailMessage
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.http import HttpResponseRedirect, HttpResponse
# from django.http.response import JsonResponse
# from django.shortcuts import render
# from contacts.models import Contacts
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic.base import View
# from logs.models import Logs
# from mainapp.utils import *
# import ast
# import json

from .models import *
from .serializers import *
from orders.serializers import *
from orders.models import *

from django.conf import settings as s
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cgitb import enable
from email.mime import image
from unicodedata import name
from rest_framework.pagination import CursorPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from cursor_pagination import CursorPaginator


@api_view(["POST"])
def get_pag_data(request):
    # filter = request.data.get('filter')
    data_price = request.data.get('data_price')
    print(data_price)
    flowers = Flowers.objects.filter(enable=True)
    print('0')
    paginator = CursorPaginator(flowers, ordering=(data_price, '-id'))
    print('1')
    page = paginator.page(first=30)
    print('2')
    data = {
        'flowers': FlowersSer(page, many=True).data,
        'next': paginator.cursor(page[2]),
        'last': paginator.cursor(page[-1])
    }
    return Response(data)


class MyCursorPagination(CursorPagination):
    page_size = 30
    ordering = '-date_time'
class GetData2(ListAPIView):
    # def get(self, request):
    #     data = request.GET.get('ordering')
    #     print(data)
    #     flowers = Flowers.objects.filter(enable=True)
    #     # flowers = MyCursorPagination(flowers)
    #     flowers = FlowersSer(flowers, many=True)
    #     return Response(flowers)
    queryset = Flowers.objects.filter(enable=True)
    serializer_class = FlowersSer
    pagination_class = MyCursorPagination


@api_view(["POST"])
def get_data1(request):
    categorys = CategorySer(Category.objects.all(), many=True).data
    povods = PovodsSer(Povods.objects.all(), many=True).data
    return Response({'categorys': categorys, 'povods': povods})
    
@api_view(["POST"])
def get_data(request):
    # for i in range(400):
    #     try:
    #         flower = Flowers.objects.get(id=i)
    #         # if flower.description=="В наши букеты вложено много любви и труда. Флористы Royal Flowers используют всегда свежие цветы и максимум фантазии. Надеемся, вы оцените наши труды!":
    #         #     flower.description=""
    #         #     flower.save()
    #         # if flower.description==flower.name:
    #         #     flower.description=""
    #         #     flower.save()
    #     except:
    #         pass
    state = request.data.get('state')
    if state == '1':
        categorys = CategorySer(Category.objects.all(), many=True).data
        povods = PovodsSer(Povods.objects.all(), many=True).data
        # citys = CitySer(City.objects.filter(city_flowers__pk__isnull=False).distinct(), many=True).data
        flowers = FlowersSer(Flowers.objects.filter(enable=True)[0:30], many=True, context={'request':request}).data
        return Response({'categorys':categorys,'povods':povods,'flowers':flowers})
    else:
        return Response(FlowersSer(Flowers.objects.filter(enable=True)[30:], many=True, context={'request':request}).data)
    # state = request.data.get('state')
    # print(state)
    # categorys = CategorySer(Category.objects.all(), many=True).data
    # povods = PovodsSer(Povods.objects.all(), many=True).data
    # citys = CitySer(City.objects.filter(city_flowers__pk__isnull=False).distinct(), many=True).data
    # flowers_q = Flowers.objects.filter(enable=True)[0:20]
    # flowers = FlowersSer(flowers_q, many=True).data
    # return Response({'categorys':categorys,'povods':povods,'flowers':flowers,'citys':citys})
 
    # set = SetsExtraProducts.objects.get(id=2)
    # for i in range(340):
    #     try:
    #         fl = Flowers.objects.get(id=i+1)
    #         fl.set_dops = set
    #         fl.save()
    #         print(i+1)
    #     except:
    #         print(str(i)+'- err')
    

@api_view(["POST"])
def registration(request):
    data=request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    is_exists = User.objects.filter(username=username).exists()
    is_email_exists = Users.objects.filter(email=email).exists()
    if is_exists:
        return Response('Такой пользователь уже есть')
    if is_email_exists:
        return Response('Такой email уже есть')
    else:
        django_user = User.objects.create(username=username,password=password,email=email)
        Users.objects.create(user=django_user,work='Клиент',name=data.get('name'),email=data.get('email'),phone=data.get('phone'))
        return Response('Успешно')


@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username,password=password)
    is_exists = User.objects.filter(username=username).exists()
    if not is_exists:
        return Response('Пользователь не существует')

    if user is not None:
        if user.is_active:
            user = Users.objects.get(user=user)
            return Response(['Успешно',user.work,user.name])
        else:
            return Response('Пользователь не актвен')
    else:
        return Response('Пароль не верный')


@api_view(["POST"])
def forgot(request):
    email=request.data.get('email')
    try:
        password = User.objects.make_random_password()
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save(update_fields=['password'])
        send_mail('Восстановление пароля','Новый пароль - '+str(password),s.SERVER_EMAIL,[email],fail_silently=False)
        return Response('Пароль отправлен на email!')
    except:
        return Response('Такого email нет в системе!')


@api_view(["GET"])
def crm_orders(request):
    return Response(OrdersSer(Order.objects.all(),many=True).data)


@api_view(["GET"])
def crm_orders_stats(request):
    from datetime import date
    now_year = date.today().year

    dataList = []
    for i in range(10):
        year = now_year-i
        orders = Order.objects.filter(date_add__year=year)
        if orders:
            print('==================================='+str(year)+'===================================')
            print(orders)
            list_of_orders=[]
            list_of_sums=[]
            for i in range(12):
                mounth = i+1
                orders = Order.objects.filter(date_add__month=mounth,date_add__year=year,status='Новый')
                print(mounth)
                print(orders)
                list_of_orders.append(len(orders))
                result = 0
                for i in orders:
                    result+=i.sum_result
                list_of_sums.append(result)

            dataList.append({
                'name':year,
                'labels': ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
                'datasets': [
                    {
                    'label': 'Заказы',
                    'backgroundColor': '#EC407A',
                    'yAxisID': 'y-axis-1',
                    'data': list_of_orders
                    }, 
                    {
                    'label': 'Общая сумма',
                    'backgroundColor': '#78909C',
                    'yAxisID': 'y-axis-2',
                    'data': list_of_sums
                    }
                ]   
            })
        else:
            break

    dataList.append({
        'name':2021,
        'labels': ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        'datasets': [
            {
            'label': 'Заказы',
            'backgroundColor': '#EC407A',
            'yAxisID': 'y-axis-1',
            'data': [4,0,0,0,1,8,10,3,0,0,0,0]
            }, 
            {
            'label': 'Общая сумма',
            'backgroundColor': '#78909C',
            'yAxisID': 'y-axis-2',
            'data': [40000,0,0,0,10000,80000,10000,30000,0,0,0,0]
            }
        ]   
    })

    return Response(dataList)


@api_view(["GET"])
def crm_products(request):
    categorys = CategorySer(Category.objects.all(), many=True).data
    povods = PovodsSer(Povods.objects.all(), many=True).data
    flowers = FlowersSer(Flowers.objects.all(),many=True).data
    return Response({'categorys':categorys,'povods':povods,'flowers':flowers})


@api_view(["POST"])
def crm_add_img(request):
    image=request.data.get('image')
    id=request.data.get('id')
    flower=Flowers.objects.get(id=id)
    FlowerImages.objects.create(flower=flower,image=image)
    return Response(FlowersSer(flower,many=False).data)


@api_view(["POST"])
def crm_del_img(request):
    id_image=request.data.get('id_image')
    id=request.data.get('id')
    image = FlowerImages.objects.get(id=id_image)
    image.image.delete(save=True)
    image.delete()
    return Response(FlowersSer(Flowers.objects.get(id=id),many=False).data)


@api_view(["POST"])
def crm_product(request):
    def d(x):return request.data.get(x)

    def cat_pov(flower, categorys, povods):
        if d('categorys')!=['']:
            for cat in categorys:
                flower.category.add(Category.objects.get(id=cat.get('id')))
        if d('povods')!=['']:
            for pov in povods:
                flower.povod.add(Povods.objects.get(id=pov.get('id')))

    if d('state')=='update':
        flower=Flowers.objects.get(id=d('id'))
        flower.category.clear()
        flower.povod.clear()
        cat_pov(flower, d('categorys'), d('povods'))
        Flowers.objects.filter(id=d('id')).update(name=d('name'),description=d('description'),price=d('price'),enable=d('enable'))
        return Response('OK')
    elif d('state')=='create':
        if (d('enable')=="true"):enable=True 
        else:enable=False
        flower = Flowers(name=d('name'),description=d('description'),price=d('price'),enable=enable,count_in=Counts_Flowers.objects.get(id=1),percent_stock='0',)
        flower.save()
        cat_pov(flower, eval(d('categorys')), eval(d('povods')))
        FlowerImages.objects.create(flower=flower,image=d('image'))
        return Response(FlowersSer(flower, many=False).data)
    elif d('state')=='delete':
        Flowers.objects.get(id=d('id')).delete()
        return Response('OK')
    # elif d('state')=='in_arhive':
    #     Flowers.objects.filter(id=d('id')).update(enable=False)
    #     return Response('OK')
    # elif d('state')=='out_arhive':
    #     Flowers.objects.filter(id=d('id')).update(enable=True)
    #     return Response('OK')
    else:
        return Response('LOL')
    


# @api_view(["POST"])
# def crm_product_save(request):
#     def d(x):return request.data.get(x)
#     flower=Flowers.objects.get(id=d('id'))
#     flower.category.clear()
#     if d('categorys')!=['']:
#         for cat in d('categorys'):
#             flower.category.add(Category.objects.get(id=cat.get('id')))
#     flower.povod.clear()
#     if d('povods')!=['']:
#         for pov in d('povods'):
#             flower.povod.add(Povods.objects.get(id=pov.get('id')))
#     Flowers.objects.filter(id=d('id')).update(name=d('name'),description=d('description'),price=d('price'),enable=d('enable'))
#     return Response('OK')


# @api_view(["POST"])
# def registration(request):
#     return Response()


# @api_view(["POST"])
# def registration(request):
#     return Response()

        
# class DeliveryView(CityMixin, View):
#     def get(self, request, city):
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         delivery = Delivery.objects.filter(city=self.city).first

#         return render(request, 'main/delivery-pay.html', locals())


# class AllFlowersView(CityMixin, View):
#     def get(self, request, city, sort='price'):
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         object_list = Flowers.objects.filter(city__in=self.cities_qs, enable=True)
#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         page = request.GET.get('page')
#         paginator = Paginator(object_list, 20)
        
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         if paginator.num_pages>12:
#             do_it = 'yes'
#         return render(request, 'main/all_products.html', locals())


# class CompositionView(CityMixin, View):
#     def get(self, request, city, sort='price'):
#         comp = True
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         object_list = Flowers.objects.filter(city__in=self.cities_qs, comp=True, enable=True)

#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         return render(request, 'main/all_products.html', locals())


# class ReadyView(CityMixin, View):
#     def get(self, request, city, sort='price'):
#         ready = True
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()

#         object_list = Flowers.objects.filter(city__in=self.cities_qs,  ready=True, enable=True)
#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         return render(request, 'main/all_products.html', locals())


# class StockView(CityMixin, View):
#     def get(self, request,city, sort='price'):
#         stock = True
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         object_list = Flowers.objects.filter(
#             city__in=self.cities_qs,  stock=True, enable=True)

#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         return render(request, 'main/all_products.html', locals())


# class ValentineView(CityMixin, View):
#     def get(self, request, city, sort='price'):
#         valentine = True
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()

#         object_list = Flowers.objects.filter(
#             city__in=self.cities_qs,  valentine=True, enable=True)
#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list =  object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         return render(request, 'main/all_products.html', locals())


# class CategoryView(CityMixin, View):
#     def get(self, request, city, category_id, sort='price'):

#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         category = Category.objects.get(id=category_id)
#         object_list = Flowers.objects.filter(city__in=self.cities_qs,  category=category, enable=True)

#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:

#             flowers = paginator.page(paginator.num_pages)
#         return render(request, 'main/all_products.html', locals())


# class PovodsView(CityMixin, View):
#     def get(self, request, city, povod_id, sort='price'):
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         povod = Povods.objects.get(id=povod_id)
#         object_list = Flowers.objects.filter(city__in=self.cities_qs, povod=povod, enable=True)
#         if sort:
#             if sort == 'price':
#                 object_list = object_list.order_by('price')
#             if sort == 'price-desc':
#                 object_list = object_list.order_by('-price')
#             if sort == 'data':
#                 object_list = object_list.order_by('date_time')
#             if sort == 'data-desc':
#                 object_list = object_list.order_by('-date_time')

#         paginator = Paginator(object_list, 20)
#         page = request.GET.get('page')
#         try:
#             flowers = paginator.page(page)
#         except PageNotAnInteger:
#             flowers = paginator.page(1)
#         except EmptyPage:
#             flowers = paginator.page(paginator.num_pages)
#         # for flower in flowers:
#         #     if flower.stock:
#         #         new

#         return render(request, 'main/all_products.html', locals())


# class LoginView(CityMixin, View):
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request,username=username,password=password)
#         is_exists = User.objects.filter(username=username).exists()
#         if not is_exists:
#             return HttpResponseRedirect('{}?no_account=True'.format(reverse('index', kwargs={'city': self.city_url})))

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('{}?success=True'.format(reverse('index', kwargs={'city': self.city_url})))
#             else:
#                 return HttpResponseRedirect('{}?password_error=True'.format(reverse('index', kwargs={'city': self.city_url})))
#         else:
#             return HttpResponseRedirect('{}?password_error=True'.format(reverse('index', kwargs={'city': self.city_url})))


# class LogoutView(CityMixin, View):
#     def get(self, request):
#         logout(request)
#         return HttpResponseRedirect('{}?success_log_out=True'.format(reverse('index', kwargs={'city': self.city_url})))


# class RegistrationView(CityMixin, View):
#     def get(self, request):

#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         user_exists = request.GET.get('user_exists', False)
#         is_email_exists = request.GET.get('is_email_exists', False)
#         return render(request, 'main/registration.html', locals())

#     def post(self, request):
#         password = request.POST['password']
#         username = request.POST['username']
#         email = request.POST['email']
#         is_exists = User.objects.filter(username=username).exists()
#         is_email_exists = User.objects.filter(email=email).exists()
#         if is_exists:
#             return HttpResponseRedirect('{}?user_exists=True'.format(reverse('registartionview')))

#         if is_email_exists:
#             return HttpResponseRedirect('{}?is_email_exists=True'.format(reverse('registartionview')))
#         else:
#             current_user = User()
#             current_user.username = request.POST['username']
#             current_user.email = request.POST['email']
#             current_user.set_password(password)
#             current_user.save()
#             users = Users()
#             users.user = current_user
#             users.work = 'Клиент'
#             users.save()
#         return HttpResponseRedirect(reverse('BasicLogin', args=[current_user.id, password]))


# class BasicLogin(CityMixin, View):
#     def get(self, request, id, password):
#         user = User.objects.get(id=id)
#         current_user = authenticate(request,username=user.username,password=password)
#         login(request, current_user)
#         return HttpResponseRedirect('{}?success_regist=True'.format(reverse('index', kwargs={'city': self.city_url})))


# class ProfileView(CityMixin, View):
#     def get(self, request):
#         user = request.user
#         orders = Order.objects.filter(user=user)
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         return render(request, 'main/personal.html', locals())


# class FlowerDetail(CityMixin, View):
#     def get(self, request, city, id):
#         flower = Flowers.objects.get(id=id)
#         price=flower.price
#         extraproducts = ExtraProducts.objects.all()
#         categorys = Category.objects.all()
#         povods = Povods.objects.all()
#         try:
#             delivery = Delivery.objects.get(city=self.city).price
#         except:
#             delivery = 0
#         return render(request, 'main/product-detail.html', locals())


# class Profile_edit(View):
#     def post(self, request):
#         if request.POST['newPassword'] == request.POST['newPasswordConfirm']:
#             user_id = request.user.id
#             user = User.objects.get(id=user_id)

#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.username = request.POST['username']
#             user.set_password(request.POST['newPassword'])
#             user.save()
#         else:
#             user_id = request.user.id
#             user = User.objects.get(id=user_id)
#         return HttpResponseRedirect(reverse('BasicLogin', args=[user.id, request.POST['newPassword']]))


# # class ContactsView(CityMixin, View):
# #     def get(self, request):

# #         categorys = Category.objects.all()
# #         povods = Povods.objects.all()
# #         contacts = Contacts.objects.first()

# #         return render(request, 'main/contacts.html', locals())


# class SearchView(CityMixin, View):
#     def get(self, request, city):
#         query = request.GET.get('query', False)
#         #
#         cities = City.objects.all()
#         curent_city = int(request.session.get('city_id', 1))
#         cities_qs = City.objects.filter(id=curent_city)
#         #Flowers.objects.filter(city__in=cities_qs, enable=True)
#         #
#         flowers = Flowers.objects.filter(
#             city__in=cities_qs,  name__icontains=query, enable=True)

#         categorys = Category.objects.all()
#         povods = Povods.objects.all()

#         return render(request, 'main/all_products.html', locals())


# @method_decorator(csrf_exempt, name='dispatch')
# class CallBackTarlan(View):
#     def get(self, request):
#         a = []
#         for i in request.GET:
#             a.append(i)
#         for i in a:
#             print(f'{i}:{request.GET[f"{i}"]}')

#         return HttpResponse('Callback')

#     def post(self, request):
#         import json
#         req = request.POST
#         data = json.loads(request.body)
#         order_id = data['reference_id']
#         status = data['status']
#         order = Order.objects.get(id=int(order_id))
#         html_template = 'main/message.html'

#         html_message = render_to_string(html_template,{'order': order})
#         message = EmailMessage('Спасибо за заявку!', html_message, settings.EMAIL_HOST_USER,[f'{order.email}'])
#         message.content_subtype = 'html'
#         if int(status) == 1:
#             order.status = 'Оплачен'
#             order.save()
#             message.send()
#         elif int(status) == 6:
#             order.status = 'Не оплачен'
#             order.save()
#         srt = f'{order} {status}'

#         return HttpResponse('Success')


# class RequestTarlan(View):
#     def get(self, request, id):
#         new_id = int(id)
#         order = Order.objects.get(id=new_id)

#         return render(request, 'main/status_order.html', locals())


# class Forget_passwordView(CityMixin, View):
#     def get(self, request):
#         not_user_exists = request.GET.get('not_user_exists', False)
#         success = request.GET.get('success', False)
#         return render(request, 'main/forget_password.html', locals())

#     def post(self, request):
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#         except:
#             user = None
#         print(user)
#         if user == None:
#             return HttpResponseRedirect('{}?not_user_exists=True'.format(reverse('forget_password')))
#         else:
#             full_url = ''.join(
#                 ['https://', 'www.royalflowers.kz/forget_password_new/', str(user.id), '/'])
#             # full_url = ''.join(['http://', '127.0.0.1:8888/forget_password_new/',str(user.id),'/'])
#             body = 'Изменить пароль <a href="{}">Ссылка для изменение статуса</a>'.format(
#                 full_url)
#             message = EmailMessage('Вы можете изменить пароль!', body, settings.EMAIL_HOST_USER,
#                                    [email])
#             message.content_subtype = 'html'
#             message.send()
#             return HttpResponseRedirect('{}?success=True'.format(reverse('forget_password')))


# class Forget_password_newView(CityMixin, View):
#     def get(self, request, id):
#         id = int(id)
#         user = User.objects.get(id=id)
#         error_password = request.GET.get('error_password', False)
#         return render(request, 'main/forget_password_new.html', locals())

#     def post(self, request, id):
#         password = request.POST['password']
#         passwordConfirm = request.POST['passwordConfirm']

#         id = int(id)
#         user = User.objects.get(id=id)
#         if password == passwordConfirm:
#             user.set_password(password)
#             user.save()
#             return HttpResponseRedirect('{}?success_change=True'.format(reverse('index', kwargs={'city': self.city_url})))
#         else:
#             return HttpResponseRedirect('{}?error_password=True'.format(reverse('forget_password_new', args=[user.id])))


# class ChangeCity(View):
#     def post(self, request):
#         city = int(request.POST['city_id'])
#         request.session['city_id'] = city
#         city=City.objects.get(id=city).url_name
#         # url = "{1}".format(request.META.get('HTTP_REFERER', '/'), city)
#         # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#         # return HttpResponseRedirect(url)
#         return redirect('index', city=city)


# class IndexRedirect(CityMixin, View):
#     def get(self, request):
#         return redirect('index', city=self.city_url)