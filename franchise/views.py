from franchise.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def Franchise(request):
    print(request.POST['fio'])
    Order.objects.create(email=request.POST['email'],fio=request.POST['fio'],phone=request.POST['phone'],city=request.POST['city'],city_fr=request.POST['city_fr'],brend=request.POST['brand'],kapital=request.POST['capital'],opit=request.POST['experience-1'],obopite=request.POST['experience-2'],velbiznes=request.POST['biznes'],pochemu=request.POST['why'])
    # html_template = 'main/fast_order_message.html'
    # html_message = render_to_string(html_template,{'order': order, })
    # message = EmailMessage('Поступила новая заявка (купить в один клик)!', html_message, settings.EMAIL_HOST_USER,['royalflowersproject@gmail.com'])
    # message.content_subtype = 'html'
    # message.send()
    return Response("OK")
