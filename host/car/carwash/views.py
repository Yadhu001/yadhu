from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
import razorpay
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore



# Create your views here.
def indexfun(req):
    return render(req,"index.html")
def notfound(req):
    return render(req,"404.html")
def aboutfun(req):
    return render(req,"about.html")
def bookingfun(req):
    return render(req,"booking.html")
def contactfun(req):
    return render(req,"contact.html")
def servicefun(req):
    return render(req,"service.html")
def teamfun(req):
    return render(req,"team.html")
def testfun(req):
    return render(req,"testimonial.html")

def regfun(req):
    if req.method=='POST':
        a = req.POST['name']
        b = req.POST['email']
        c = req.POST['user']
        d = int(req.POST['number'])
        e = req.POST['pass']
        f = req.POST['repass']
        if register.objects.filter(user=c).exists():
            messages.success(req,'User Exist')
        elif register.objects.filter(numbers=d).exists():
            messages.success(req,'Number Exist')
        elif register.objects.filter(email=b).exists():
            messages.success(req,'Email Exist')
        else:
            if e==f:
                register.objects.create(name=a, email=b, user=c, numbers=d ,password=e).save()
                return redirect(req,"login.html")
            else:
                messages.success(req,'password not same!')
        return render(req, "register.html")
    return render(req, "register.html")

def logfun(req):
    if req.method=='POST':
        a=req.POST['user']
        d=req.POST['pass']
        try:
            data=register.objects.get(user=a)
            if data.password==d:
                req.session['user']=a
                messages.success(req,'login successful')
                return redirect(userfun)
            else:
                messages.error(req,'incorrect pass!')
                return redirect(logfun)
        except Exception as e:
            print(e)
            if a=='admin' and d=='1234':
                req.session['admin']=a
                return redirect(adminfun)
            else:
                messages.error(req,'incorrect')
                return redirect(logfun)
    return render(req,"login.html")

def adminfun(req):
    return render(req,"admin.html")

def userfun(req):
    return render(req,"userpage.html")

def logoutfun(req):
    if 'user' in req.session or 'admin' in req.session:
        req.session.flush()
        return redirect(logfun)
    return redirect(logfun)
def addprofun(req):
    if req.method == 'POST':
        a = req.POST['name']
        b = req.POST['price']
        c = int(req.POST['quantity'])
        d = req.FILES['fil']
        product.objects.create(name=a, price=b, quantity=c, image=d).save()
    return render(req,"addpro.html")
def mpro(req):
    data = product.objects.all()
    return render(req, 'mpro.html', {'data': data})
def proup(req,u):
    data=product.objects.get(pk=u)
    data1=updateform(instance=data)
    if req.method=='POST':
        d=updateform(req.POST,req.FILES,instance=data)
        if d.is_valid():
            d.save()
            return redirect(mpro)
        return redirect(mpro)
    return render(req,'adupdate.html',{'data':data1})
def userprofun(req):
    data = product.objects.all()
    return render(req, "userpro.html",{'data': data})
def userhomefun(req):
    return render(req,'userhome.html')
def delete(req,d):
    data=product.objects.get(pk=d)
    data.delete()
    return redirect(mpro)
def addcart(req,d):
    if 'user' in req.session:
        user= register.objects.get(user=req.session['user'])
        data= product.objects.get(pk=d)
        if cart.objects.filter(product_details=data,user_details=user).exists():
            messages.error(req,'already esists')
            return redirect(userprofun)
        else:
            cart.objects.create(user_details=user,product_details=data,totalprice=data.price,quantity=data.quantity).save()
            return redirect(userprofun)
    else:
        return render(logoutfun)
def cartview(req):
    if 'user' in req.session:
        user = register.objects.get(user=req.session['user'])
        data= cart.objects.filter(user_details=user)
        total=0
        totalq=0
        for i in data:
            total+=i.totalprice
            totalq+=1
        print(total)
        return render(req,'usercart.html',{'data':data,'total':total,'quantity':totalq})
    else:
        return render(logfun)
def increment(req,d):
    if 'user' in req.session:
        data= cart.objects.get(pk=d)
        data.quantity+=1
        data.totalprice=data.quantity*data.product_details.price
        data.save()
        return redirect(cartview)
    else:
        return render(logfun)

def decrement(req,d):
    if 'user' in req.session:
        data= cart.objects.get(pk=d)
        if data.quantity<=1:
            data.delete()
            return redirect(cartview)
        else:
            data.quantity-=1
            data.totalprice = data.quantity * data.product_details.price
            data.save()
            return redirect(cartview)
    else:
        return render(logfun)
def wishview(req):
    if 'user' in req.session:
        user = register.objects.get(user=req.session['user'])
        data = wishlist .objects.filter(user_details=user)
        return render(req, 'wishlist.html', {'data': data})
    else:
        return render(logfun)
def addwish(req,d):
    if 'user' in req.session:
        user= register.objects.get(user=req.session['user'])
        data= product.objects.get(pk=d)
        if wishlist.objects.filter(product_details=data,user_details=user).exists():
            messages.error(req,'already esists')
            return redirect(userprofun)
        else:
            wishlist.objects.create(user_details=user,product_details=data).save()
            return redirect(userprofun)
    else:
        return render(logoutfun)
def rem(req,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cartview)
def wishdel(req,d):
    data=wishlist.objects.get(pk=d)
    data.delete()
    return redirect(wishview)
def payment(request, id):
    amount = id*100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment.html",{'amount':amount,'id':id})
def order(request):
    user = register.objects.get(user=request.session['user'])
    data = cart.objects.filter(user_details=user)
    import datetime
    d = datetime.datetime.now()
    for i in data:
        a=product.objects.filter(name=i.product_details.name).first()
        a.quantity=a.quantity-i.quantity
        print(a.quantity)
        a.save()
        orders.objects.create(user_details=user,product_details=a,quantity=i.quantity,amount=i.totalprice,order_date=d).save()
    data.delete()
    return render(request,"success.html")
def myorder(request):
    user = register.objects.get(user=request.session['user'])
    data = orders.objects.filter(user_details=user)
    return render(request,'myorders.html',{'data':data})
def adorder(req):
    data = orders.objects.all()
    data1=delivery_boy_register.objects.all()
    return render(req, 'adminorder.html', {'data': data,'data1':data1})
def delivery_reg(request):
    if request.method == 'POST':
        a = request.POST['name']
        b = request.POST['email']
        c = request.POST['phone']
        d = request.POST['driving_license_no']
        e = request.POST['user']
        f = request.POST['pass']
        g = request.POST['repass']
        if delivery_boy_register.objects.filter(username=e).exists():
            messages.error(request,'Username Already Exist')
        elif delivery_boy_register.objects.filter(email=b).exists():
            messages.error(request,'Email Already Exist')
        else:
            delivery_boy_register.objects.create(name=a, email=b, phone=c, driving_license_no=d, username=e, password=f).save()
            messages.success(request,'Register Successfully')
            return render(request,'delivery_boy_register.html')
    return render(request,'delivery_boy_register.html')

def delivery_login(request):
    if request.method =='POST':
        a = request.POST['b1']
        b = request.POST['b2']
        print(a,b)
        try:
            data=delivery_boy_register.objects.get(username=a)
            if data.password==b:
                if data.status == 'Accepted':
                    request.session['delivery']=a
                    messages.success(request,'Login success')
                    return redirect(delivery_home)
                else:
                    messages.error(request,'Request Pending')
                    return redirect(delivery_login)
            else:
                messages.error(request, 'Incorect password')
                return redirect(delivery_login)
        except Exception as e:
            print(e)
            messages.error(request,'Username Doesnot exists')
            return redirect(delivery_login)
    return render(request, 'delivery_boy_login.html')

def delivery_home(request):
    return render(request, 'delivery_home.html',)

def addboy(req):
    return render(req,'addeliveryboy.html')

def delivery_view(request):
    data = delivery_boy_register.objects.all()
    return render(request, 'addeliveryboy.html', {'data': data})

def history(request):
    user = delivery_boy_register.objects.get(username=request.session['delivery'])
    data = orders.objects.filter(product_status='Delivered',delivery_boy=user.username)
    return render(request,'deliveryhis.html',{'data':data})

def delivery_order(request):
    if 'delivery' in request.session:
        data=orders.objects.filter(delivery_boy=request.session['delivery'])
        return render(request,'deliveryorders.html',{'data':data})
    else:
        return redirect(logfun)

def reject(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status='Rejected'
    data.save()
    return redirect(delivery_view)

def accept(request,a):
    data = delivery_boy_register.objects.get(pk=a)
    data.status = 'Accepted'
    data.save()
    return redirect(delivery_view)

def adhome(req):
    return render(req,"adhome.html")
def profile(request):
    data = delivery_boy_register.objects.get(username=request.session['delivery'])
    return render(request,'profle.html',{'data':data})

def alert(request):
    low_stock_products = product.objects.filter(quantity__lt=5)
    return render(request, "alert.html",{'data':low_stock_products})
def choose(request,a):
    if request.method =='POST':
        b = request.POST['x1']
        data = orders.objects.get(pk=a)
        data.delivery_boy=b
        data.product_status='Out for delivery'
        data.save()
        try:
            d=delivery_boy_register.objects.get(username=b)
            d.work_status='Busy'
            d.save()
            # return redirect(booking)
        except Exception as e:
            print(e)
            messages.error(request,'Delivery Boy Doesnot Exist')
            return redirect(adorder)
        messages.success(request,f'The order has been assigned for {b}')
        return redirect(adorder)

def delivered(request,a):
    data = orders.objects.get(pk=a)
    data.product_status ='Delivered'
    data.save()
    delivery=delivery_boy_register.objects.get(username=request.session['delivery'])
    delivery.work_status='Free'
    delivery.save()
    messages.success(request,'You Have delivered the order.now you are Free')
    return redirect(delivery_order)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = register.objects.get(email=email)
        except Exception as e:
            print (e)# noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8888/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(logfun)
    return render(request, 'reset_password.html', {'token': token})