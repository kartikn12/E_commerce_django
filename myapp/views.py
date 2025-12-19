from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import razorpay

# Create your views here.
def index(request):
    product = Product.objects.all()
    return render(request,'index.html', {'product': product})

def cart(request):
    return render(request,'cart.html')

def detail(request):
    return render(request,'detail.html')

def shop(request):
   product = Product.objects.all()
   return render(request,'shop.html', {'product': product})

def checkout(request):
    return render(request,'checkout.html')

def contact(request):
    if request.method=="POST":
        try:
 
            name=request.POST['uname']
            subject=request.POST['usubject']
            message = request.POST['umessage']
            email_from=request.POST['uemail']
            recipient_list=[settings.EMAIL_HOST_USER,]
            # email_new=settings.EMAIL_HOST_USER

            full_message = f"Message from {name} \n {email_from}:\n\n{message}"
            send_mail(subject,full_message,settings.EMAIL_HOST_USER,recipient_list)

            msg1="Your Message sent successfully"
            return render(request,'contact.html',{'msg1':msg1})
        
        except:
            msg="somthing wrong!"
            return render(request,'contact.html',{'msg':msg})

    else:
            return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email already Exists"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    name=request.POST['name'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype']   
                )
                
                user=User.objects.get(email=request.POST['email'])
                subject='Welcome to Multi-shop'
                message = f"{user.name}! Welcome To Our Website"
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[user.email,]
                send_mail(subject,message,email_from,recipient_list)

                msg1="SIgnup Successfully"
                return render(request,'signup.html',{'msg1':msg1})
    
            else:
                msg="Password & confirm Password Does not Match"
                return render(request,'signup.html',{'msg':msg})
    
    else:
        return render(request,'signup.html')
@csrf_exempt   
def login(request):
    
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])

            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['profile']=user.profile.url
                if user.usertype=="buyer":
                    return redirect('index')
                else:
                    return redirect('sindex')

            else:
                msg="Password Does not Match"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email does not match"
            return render(request,'login.html',{'msg':msg})
        
 
    else:
         return render(request,'login.html')
            
def logout(request):
    try:
        del request.session['email']
        del request.session['profile']
        return redirect('login')
    except:
        pass
    return redirect('login')

def fpass(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1001,9999)
            subject='OTP FOR FORGOT-PASSWORD'
            message = f"{user.name}! Use this OTP to complete your login: {otp}."
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[user.email,]
            send_mail(subject,message,email_from,recipient_list)

            request.session['email']=user.email
            request.session['otp']=otp
            return render(request,'otp.html')
        
        except:
            msg="Email does not found!"
            return render(request,'fpass.html',{'msg':msg})

    else:
            return render(request,'fpass.html')

def otp(request):
    if request.method=="POST":
        try:
            otp=int(request.session['otp'])
            uotp=int(request.POST['uotp'])

            if otp==uotp:
                del request.session['otp']
                return redirect('newpass')
            else:
                msg='Invalid otp'
                return render(request,'otp.html',{'msg':msg})
            
        except KeyError as e:
            print("*",e)

    else:
        return render(request,'otp.html')
    
def newpass(request):
        if request.method=="POST":
            try:
                user=User.objects.get(email=request.session['email'])

                if request.POST['npassword']==request.POST['cnpassword']:
                    user.password=request.POST['npassword']
                    user.save()
                    del request.session['email']
                    return redirect('login')
                else:
                    msg="Password and confirm password does not match"
                    return render(request,'newpass.html',{'msg':msg})
                
            except KeyError as e:
                print(e)

        else:
            return render(request,'newpass.html')
            

def cpass(request):
    user=User.objects.get(email=request.session['email'])
    
    if request.method=="POST":
            try:

                if user.password==request.POST['opassword']:
                    if request.POST['npassword']==request.POST['cnpassword']:
                        user.password=request.POST['npassword']
                        user.save()
                        return redirect('logout')
                    else:

                        msg="Your new password and confirm new password does not match"
                        if user.usertype=="buyer":
                            return render(request,'cpass.html',{'msg':msg})
                        else:
                            return render(request,'scpass.html',{'msg':msg})

                        
                else:
                    msg="Your old password does not match"
                    if user.usertype=="buyer":
                        return render(request,'cpass.html',{'msg':msg})
                    else:
                        return render(request,'scpass.html',{'msg':msg})
                    
            except:
                pass
    else:
        if user.usertype=="buyer":
            return render(request,'cpass.html')
        else:
            return render(request,'scpass.html')
    

def uprofile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.name=request.POST['name']
        user.mobile=request.POST['mobile']
        user.address = request.POST.get('address') 

        try:
            user.profile=request.FILES['profile']
            user.save()
            request.session['profile']=user.profile.url #session update

        except:
            pass
        user.save()
        if user.usertype=="buyer":
            return redirect('index')
        else:
            return redirect('sindex')

    else:
        if user.usertype=="buyer":
            return render(request,'uprofile.html',{'user':user})
        else:
            return render(request,'suprofile.html',{'user':user})


def sindex(request):
    product = Product.objects.all()
    return render(request,'sindex.html', {'product': product})


def add(request):
    user=User.objects.get(email=request.session['email'])

    
    if request.method=="POST":
    
        try:
            Product.objects.create(
                user=user,
                pcategory=request.POST['pcategory'],
                pcompany=request.POST['pcompany'],
                pname=request.POST['pname'],
                pprice=request.POST['pprice'],
                pdesc=request.POST['pdesc'],
                pimage=request.FILES['pimage']

            )
            msg = "added"
            return redirect('sindex')
        except:
            msg = "Error in adding product."
            return render(request, 'add.html', {'msg': msg})
        
    else:
        return render(request,'add.html')
    

def view(request):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.filter(user=user)
    return render(request,'view.html',{'product':product})

def pdetails(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    return render(request,'pdetails.html',{'product':product})

def edit(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.pname=request.POST['pname']
        product.pprice=request.POST['pprice']
        product.pdesc = request.POST['pdesc']
        product.pimage=request.FILES['pimage']
        product.save()
        return redirect('view')
    else:
        return render(request,'edit.html',{'product':product})

def delete(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('view')

def addwish(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)  
    try:
        Whishlist.objects.create(
            user=user,
            product=product
        )
        return redirect('wish')
    except:
        pass


def wish(request):
    user=User.objects.get(email=request.session['email'])
    wish=Whishlist.objects.filter(user=user)
    return render(request,'wish.html',{'wish':wish})


def bpdetails(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    flag=False
    flag1=False
    try:
        wish=Whishlist.objects.get(user=user,product=product)
        flag=True
    except:
        pass
    try:
        cart=Cart.objects.get(user=user,product=product)
        flag1=True
    except:
        pass
    return render(request,'bpdetails.html',{'product':product,'flag':flag,'flag1':flag1})

def deletewish(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    wish=Whishlist.objects.get(product=product)
    wish.delete()

    return redirect('wish')

def addcart(request,pk):
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)  
    try:
        Cart.objects.create(
            user=user,
            product=product,
            total=product.pprice,
            qty=1,
            payment=False
        )
        return redirect('cart')
    except:
        pass

def cart(request):
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user,payment=False)
    net=0
    for i in cart:
        net +=int(i.total)

    if net <= 0:
        return render(request,'cart.html',{'cart':cart,'context':None,'net':net,'message': 'Cart is empty or total too low for payment.'})

    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment=client.order.create({'amount':net * 100,'currency':'INR','payment_capture':1,'notes':{'email':str(user.email)}})

    context={
        'payment':payment

            }
    return render(request,'cart.html',{'cart':cart,'context':context,'net':net})

def deletecart(request, pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)

    Cart.objects.filter(user=user, product=product).delete()

    return redirect('cart')


def success(request):
    user = User.objects.get(email=request.session['email'])
    print("*",user)
    cart = Cart.objects.filter(user=user)
    print("",cart)
    
    for i in cart:
        i.payment=True
        i.save()
        
    return render(request,'success.html',{'cart':cart})

def myorder(request):
    user = User.objects.get(email=request.session['email'])
    orders = Cart.objects.filter(user=user, payment=True)

    return render(request, 'myorder.html', {'orders': orders})
