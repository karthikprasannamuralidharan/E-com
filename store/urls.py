from django.urls import path
from . import views

urlpatterns = [
    #leave an empty string
    path('',views.scart,name='scart'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('ulogin/', views.ulogin, name='ulogin'),
    path('mens/', views.mens, name='mens'),
    path('contactus/',views.contactus, name='contactus'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('menformal/',views.menformal, name='menformal'),
    path('mencasual/',views.mencasual, name='mencasual'),
    path('mensports/',views.mensports, name='mensports'),
    path('menchappal/',views.menchappal, name='menchappal'),
    path('wcasual/',views.wcasual, name='wcasual'),
    path('wsports/',views.wsports, name='wsports'),
    path('wslippers/',views.wslippers, name='wslippers'),
    path('kcasual/',views.kcasual, name='kcasual'),
    path('ksandal/',views.ksandal, name='ksandal'),
    path('register/',views.register, name='register'),
    path('handelLogout/',views.handelLogout, name='handelLogout'),
    path('myorder/',views.myorder, name='myorder'),
    path('search/',views.search, name='search'),
]