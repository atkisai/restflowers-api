import email
from tabnanny import check
from unicodedata import name
from django.conf import settings as s
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.checks.messages import Error
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.base import View

from mainapp.models import *
from orders.models import *
# from contacts.models import Contacts
from django.template.context_processors import csrf

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

CART_ID = 'CART-ID'

@api_view(["POST"])
def ProfileOrders(request):
    data = request.data
    username = data.get('username')
    user = User.objects.get(username=username)
    state = data.get('state')
    if state=='init_profile':
        orders = Order.objects.filter(user=user)
        orders = OrdersSer(orders, many=True).data
        user = Users.objects.get(user=user)
        return Response([orders,user.name,user.email,user.phone])
    if state=='change_password':
        if authenticate(username=username,password=data.get('old_password')) is not None:
            user.set_password(data.get('password'))
            user.save()
            return Response('Успешно')
        else:
            return Response('Старый пароль не верный')
    if state=='change_profile':
        user = Users.objects.filter(user=user).update(name=data.get('name'),email=data.get('email'),phone=data.get('phone'))
        return Response('Успешно')
    if state=='del_profile':
        if authenticate(username=username,password=data.get('password')) is not None:
            Users.objects.get(user=user).delete()
            user.delete()
            return Response('Пользователь удален!')
        else:
            return Response('Введенные данные не верны!')
        
        
@api_view(["POST"])
def PostFastOrder(request):
    def d(x):return request.data.get(x)
    flower=Flowers.objects.get(id=int(d("flower_id")))
    city=City.objects.get(id=d("city_id"))
    order = FasrOrder(first_name=d("first_name"),phone=d("tel"),flower=flower,city=City.objects.get(id=d("city_id")))
    if flower.filial!=None:
        order.filial=flower.filial
        if flower.filial.post!=None:
            post=flower.filial.post
        elif city.post!=None:
            post=city.post
        else:
            post=s.SERVER_EMAIL
    else:
        if city.post!=None:
            post=city.post
        else:
            post=s.SERVER_EMAIL
    order.save()
    my_dict = {csrf:csrf(request)}
    my_dict.update(locals())
    html_template = 'fast_order_message.html'
    html_message = render_to_string(html_template, my_dict,)
    message = EmailMessage('Поступила новая заявка (купить в один клик)!', html_message, s.SERVER_EMAIL,[post])
    message.content_subtype = 'html'
    message.send()


@api_view(["POST"])
def PostOrder(request):
    def d(x):return request.data.get(x)
    if d("user")=='':user = User.objects.get(username="Незарегистрированный")
    else:user = User.objects.get(username=d("user"))
    try:city = City.objects.get(id = d('city_id'))
    except:city = City.objects.get(id = 1)
    print(d('anonim'))
    order = Order(user=user,city=city,first_name=d('name'),recipient_phone=d("phone"),adres=d("address"),date=d('date'),time=d('time'),sended_phone=d('my_phone'),email=d('email'),anonim=d('anonim'),postcard=d('postcard'),comments=d('comments'),paired=d('payment'),sum_result=d('sum'))
    order.save()

    for product in d('basket'):
        product_item = Order_items(order=order,item=Flowers.objects.get(id=product.get('id')),amount=product.get('col'),total_price=product.get('total'))
        product_item.save()
        for extra in product.get('set').get('extra'):
            # print(extra.get('selected'))
            if extra.get('selected') == True:
                extra_item = Order_items_extra_items(order_item=product_item,extra=ExtraProducts.objects.get(id=extra.get('id')),amount=extra.get('col'))
                extra_item.save()

    # emails=[]
    # for id in d('basket'):
    #     flower=Flowers.objects.get(id=id)
    #     Order_items.objects.create(item = flower,quantity = '1',total_price = flower.price,order = order)
    #     if flower.filial!=None:
    #         order.filial=flower.filial
    #         if flower.filial.post!=None:
    #             email=flower.filial.post
    #         elif city.post!=None:
    #             email=city.post
    #         else:
    #             email=s.SERVER_EMAIL
    #     else:
    #         if city.post!=None:
    #             email=city.post
    #         else:
    #             email=s.SERVER_EMAIL
    #     emails.append(email)

    # extras = CartExtra.objects.filter(flower=item.flower, cart_in=cart)
    # a = []
    # for i in extras:
    #     a.append(i.extra.price*i.quantity)
    # sum = item.total
    # for i in a:
    #     sum += int(i)

    # for extra in extras:
    #     order_extra = OrderExtra()
    #     order_extra.order = order
    #     order_extra.flower = item.flower
    #     order_extra.extra = extra.extra
    #     order_extra.quantity = extra.quantity
    #     order_extra.save()
    #     extra.delete()


    # for i in range(100):
    #     try:
    #        #my code
    #         break
    #     except:
    #         continue
    
    html_template = 'order_message.html'
    my_dict = {csrf:csrf(request)}
    my_dict.update(locals())
    html_message = render_to_string(html_template,my_dict)
    message = EmailMessage('Поступила новая заявка!', html_message, s.SERVER_EMAIL,[s.SERVER_EMAIL])
    message.content_subtype = 'html'
    message.send()

    html_template = 'message.html'
    html_message = render_to_string(html_template,{'order': order})
    message = EmailMessage('Спасибо за заявку!', html_message, s.SERVER_EMAIL,[d('email')])
    message.content_subtype = 'html'
    message.send()


    if order.paired == 'Оплата через Kaspi':
        send_mail('Оплата через Kaspi!','Скопируйте и оплатите заказ по номеру карты: 4400 4301 7508 6542. После оплаты в сообщении укажите номер заказа: '+str(order.id)+'.'+' Заказ можно отслеживать в личном кабинете.',s.SERVER_EMAIL,[d('email')],fail_silently=False)
        return Response({'status':'Успех','order_id':order.id})
    elif order.paired == 'Оплата онлайн':
        import requests
        import hashlib
        import collections
        merchant_id = 538362
        passw = 'cArkxBVocFkzvked'
        sum = d('sum')
        data = {
            'pg_merchant_id': f'{merchant_id}',
            'pg_amount': int(sum),
            'pg_salt': f'Заказ {order.id}',
            'pg_order_id': order.id,
            'pg_description':  f'Заказ {order.id}',
            'pg_currency': 'KZT',
            'pg_language': 'ru',
            'pg_check_url ': 'https://royalflowers.kz/',
            'pg_request_method': 'GET',
            'pg_success_url_method': 'GET',
            'pg_failure_url_method': 'GET',
            'pg_success_url': 'https://royalflowers.kz/',
            'pg_failure_url': 'https://royalflowers.kz/',
            'pg_site_url': 'https://royalflowers.kz/',
            'pg_payment_system': 'EPAYWEBKZT',
        }
        data['pg_a'] = 'init_payment.php'
        data = collections.OrderedDict(sorted(data.items()))
        data['pg_w'] = 'cArkxBVocFkzvked'
        data = dict(data)
        a = []
        sig = ''
        for i in data:
            a.append(i)
        for i in data:
            sig = sig + f'{data[i]}' + ';'
        sig = sig[0:-1]
        result = hashlib.md5(sig.encode('utf-8')).hexdigest()
        item = data.popitem()
        data = {
            'pg_merchant_id': f'{merchant_id}',
            'pg_amount': int(sum),
            'pg_salt': f'Заказ {order.id}',
            'pg_order_id': order.id,
            'pg_description': f'Заказ {order.id}',
            'pg_currency': 'KZT',
            'pg_language': 'ru',
            'pg_check_url ': 'https://royalflowers.kz/',
            'pg_request_method': 'GET',
            'pg_success_url_method': 'GET',
            'pg_failure_url_method': 'GET',
            'pg_success_url': 'https://royalflowers.kz/',
            'pg_failure_url': 'https://royalflowers.kz/',
            'pg_site_url': 'https://royalflowers.kz/',
            'pg_payment_system': 'EPAYWEBKZT',
        }
        data['pg_sig'] = result
        print(data)
        data = collections.OrderedDict(sorted(data.items()))
        data = dict(data)
        r = requests.post(
            f'https://api.paybox.money/init_payment.php', params=data)
        import xmltodict
        import pprint
        my_xml = r.text
        pp = pprint.PrettyPrinter(indent=4)
        my_dict = xmltodict.parse(my_xml)
        status = my_dict['response']['pg_status']
        url = my_dict['response']['pg_redirect_url']
        # return redirect(url)
        return Response({'status':'Успех','url':url})
    else:
        return Response({'status':'Успех'})


    html_template = 'main/order_message.html'
    my_dict = {csrf:csrf(request)}
    my_dict.update(locals())
    html_message = render_to_string(html_template,my_dict,)
    message = EmailMessage('Поступила новая заявка!', html_message, settings.EMAIL_HOST_USER,[post])
    message.content_subtype = 'html'
    message.send()
    html_template = 'main/message.html'
    html_message = render_to_string(html_template,{'order': order, 'username': user.username, 'password': user.password, 'city':self.city_url, })
    message = EmailMessage('Спасибо за заявку!', html_message, settings.EMAIL_HOST_USER,[f'{request.POST["email"]}'])
    message.content_subtype = 'html'


    if order.paired == 'Оплата через Kaspi':
        message.send()
        return HttpResponseRedirect(reverse('kaspi', args=[order.id]))
    elif order.paired == 'Онлайн оплата':
        import requests
        import hashlib
        import collections
        merchant_id = 538362
        passw = 'cArkxBVocFkzvked'
        data = {
            'pg_merchant_id': f'{merchant_id}',
            'pg_amount': int(sum),
            'pg_salt': f'Заказ {order.id}',
            'pg_order_id': order.id,
            'pg_description':  f'Заказ {order.id}',
            'pg_currency': 'KZT',
            'pg_language': 'ru',
            'pg_check_url ': 'https://royalflowers.kz/',
            'pg_request_method': 'GET',
            'pg_success_url_method': 'GET',
            'pg_failure_url_method': 'GET',
            'pg_success_url': 'https://royalflowers.kz/',
            'pg_failure_url': 'https://royalflowers.kz/',
            'pg_site_url': 'https://royalflowers.kz/',
            'pg_payment_system': 'EPAYWEBKZT',
        }
        data['pg_a'] = 'init_payment.php'
        data = collections.OrderedDict(sorted(data.items()))
        data['pg_w'] = 'cArkxBVocFkzvked'
        data = dict(data)
        a = []
        sig = ''
        for i in data:
            a.append(i)
        for i in data:
            sig = sig + f'{data[i]}' + ';'
        sig = sig[0:-1]
        result = hashlib.md5(sig.encode('utf-8')).hexdigest()
        item = data.popitem()
        data = {
            'pg_merchant_id': f'{merchant_id}',
            'pg_amount': int(sum),
            'pg_salt': f'Заказ {order.id}',
            'pg_order_id': order.id,
            'pg_description': f'Заказ {order.id}',
            'pg_currency': 'KZT',
            'pg_language': 'ru',
            'pg_check_url ': 'https://royalflowers.kz/',
            'pg_request_method': 'GET',
            'pg_success_url_method': 'GET',
            'pg_failure_url_method': 'GET',
            'pg_success_url': 'https://royalflowers.kz/',
            'pg_failure_url': 'https://royalflowers.kz/',
            'pg_site_url': 'https://royalflowers.kz/',
            'pg_payment_system': 'EPAYWEBKZT',
        }
        data['pg_sig'] = result
        data = collections.OrderedDict(sorted(data.items()))
        data = dict(data)
        r = requests.post(
            f'https://api.paybox.money/init_payment.php', params=data)
        import xmltodict
        import pprint
        my_xml = r.text
        pp = pprint.PrettyPrinter(indent=4)
        my_dict = xmltodict.parse(my_xml)
        status = my_dict['response']['pg_status']
        url = my_dict['response']['pg_redirect_url']
        print(url)
        return redirect(url)
    else:
        # message.send()------------------------------------------------------------------------------------------------------------------------
        return HttpResponseRedirect('{}?success_order=True'.format(reverse('index', kwargs={'city': self.city_url})))


class OrderPay(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        return render(request, 'main/order-pay.html', locals())


class OrderStatusEdit(View):
    def post(self, request):
        id = request.POST['order_id']
        order = Order.objects.get(id=id)
        status = request.POST['status']
        if status == 'None':
            pass
        else:
            order.status = status
            order.save()
            html_template = 'main/status_message.html'
            html_message = render_to_string(html_template,{'order': order})
            message = EmailMessage(f'Изменен статус вашего заказа {order.id}', html_message, s.SERVER_EMAI,[order.email])
            message.content_subtype = 'html'
            message.send()
        return HttpResponseRedirect(reverse('crm_index'))


# class AllFastOrderView(CrmMixin, View):
#     def get(self, request):
#         fast_orders = self.fast_orders
#         return render(request, 'crm/allfast_orders.html', locals())


class Username_checkView(View):
    def get(self, request):
        data = {'yes': False}
        username = request.GET['username']
        is_exists = User.objects.filter(username=username).exists()
        if is_exists:
            data['yes'] = True
        else:
            data['yes'] = False
        return JsonResponse(data=data)
