"""
URL configuration for car project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from carwash import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexfun),
    path('404',views.notfound),
    path('about',views.aboutfun),
    path('booking',views.bookingfun),
    path('contact',views.contactfun),
    path('service',views.servicefun),
    path('team',views.teamfun),
    path('test',views.testfun),
    path('register',views.regfun),
    path('log',views.logfun),
    path('adminp',views.adminfun),
    path('user',views.userfun),
    path('logout',views.logoutfun),
    path('product',views.addprofun),
    path('managepro',views.mpro),
    path('userproduct',views.userprofun),
    path('uhome',views.userhomefun),
    path("prodelete/<int:d>",views.delete),
    path("usercart/<int:d>",views.addcart),
    path("cartv",views.cartview),
    path('increment/<int:d>',views.increment),
    path('decrement/<int:d>',views.decrement),
    path("userwish/<int:d>",views.addwish),
    path('wishlist',views.wishview),
    path('remove/<int:d>',views.rem),
    path('wishrem/<int:d>',views.wishdel),
    path('payment/<int:id>',views.payment),
    path('success',views.order),
    path('myorder',views.myorder),
    path('adorder',views.adorder),
    path('delivery_reg',views.delivery_reg),
    path('delivery_log',views.delivery_login),
    path('deliveryboy',views.delivery_view),
    path('delivery_home',views.delivery_home),
    path('reject/<int:a>',views.reject),
    path('accept/<int:a>',views.accept),
    path('orderhistory',views.history),
    path('deliveryorders',views.delivery_order),
    path('proupdate/<int:u>',views.proup),
    path('adhome',views.adhome),
    path('profile',views.profile),
    path('alert',views.alert),
    path('choose/<int:a>',views.choose),
    path('delivered/<int:a>',views.delivered),
    path('forgot', views.forgot_password),
    path('reset_password/<token>', views.reset_password)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)