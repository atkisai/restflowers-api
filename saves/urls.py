from django.urls import path
from mainapp import views
# from mainapp import crm_views



urlpatterns = [
    # path('', views.IndexRedirect.as_view(), name='index_redirect'),

    path('index/', views.get_data),
    path('registration/', views.registration),
    path('login/', views.login),
    path('forgot/', views.forgot),

    # path('<str:city>/all/', views.AllFlowersView.as_view(), name='allflowers'),
    # path('<str:city>/all/<str:sort>/', views.AllFlowersView.as_view(), name='allflowers_sort'),
    # path('ajax_flowers/', views.AllFlowersJsonView.as_view(), name='ajax_flowers'),

    # path('<str:city>/composition/', views.CompositionView.as_view(), name='composition'),
    # path('<str:city>/composition/<str:sort>/', views.CompositionView.as_view(), name='composition_sort'),

    # path('<str:city>/ready/', views.ReadyView.as_view(), name='ready'),
    # path('<str:city>/ready/<str:sort>/', views.ReadyView.as_view(), name='ready_sort'),

    # path('<str:city>/womans_day/', views.ValentineView.as_view(), name='valentine'),
    # path('<str:city>/valentine/<str:sort>/', views.ValentineView.as_view(), name='valentine_sort'),

    # path('<str:city>/stock/', views.StockView.as_view(), name='stock'),
    # path('<str:city>/stock/<str:sort>/', views.StockView.as_view(), name='stock_sort'),

    # path('<str:city>/category/<int:category_id>/', views.CategoryView.as_view(), name='category_view'),
    # path('<str:city>/category/<int:category_id>/<str:sort>/', views.CategoryView.as_view(), name='category_view_sort'),

    # path('<str:city>/povod/<int:povod_id>/', views.PovodsView.as_view(), name='povods_view'),
    # path('<str:city>/povod/<int:povod_id>/<str:sort>/', views.PovodsView.as_view(), name='povods_view_sort'),

    # path('<str:city>/search/', views.SearchView.as_view(), name='Search'),

    # path('<str:city>/flower/<int:id>/', views.FlowerDetail.as_view(), name='flower_detail'),
    
    # path('<str:city>/deve/', views.DeliveryView.as_view(), name='DeliveryView'),
    # # path('contacts/', views.ContactsView.as_view(), name='contacts'), 
    # path('login/', views.LoginView.as_view(), name='loginview'),
    # path('registration/', views.RegistrationView.as_view(), name='registartionview'),
    # path('forget_password/', views.Forget_passwordView.as_view(), name='forget_password'),
    # path('forget_password_new/<str:id>/', views.Forget_password_newView.as_view(), name='forget_password_new'),
    # path('logout/', views.LogoutView.as_view(), name='logoutview'),
    # path('login_in/<int:id>/<str:password>/', views.BasicLogin.as_view(), name='BasicLogin'),

    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('profile/edit/', views.Profile_edit.as_view(), name='profile_edit'),

    # path('order_status/', views.CallBackTarlan.as_view(), name='order_status'),
    # path('request/<str:id>/', views.RequestTarlan.as_view(), name='request'),
    # path('changecity/', views.ChangeCity.as_view(), name='changecity'),

]
