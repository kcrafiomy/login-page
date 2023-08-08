from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.contrib import messages
# Create your views here.
# Home page Def
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def HomePage(request):
    # if login true Home page call
    if 'username' in request.session :
        return render(request,'home.html')
    # if login Fall login page Showing
    return redirect('login')

# sign page def 
def SignUpPage(request):
    # if session is there home page call
    if 'username' in request.session:
        return redirect('home')
    # get user name and email and password getting
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # validating starting if null again sign up page
        if not (username and email and pass1 and pass2):
            messages.info(request,"Please fill required field")
            return redirect('signup')
        # password 1 and passord 2 checking 
        elif pass1 != pass2:
            messages.info(request,"Password mismatch")
            return redirect('signup')
        # if user name already used checking
        else:
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Already Taken")
                return redirect('signup')
            # if email already used checking    
            elif User.objects.filter(email = email).exists():
                 messages.info(request,"Email Already Taken")
                 return redirect('signup')
            else:
                # if validation is done crate new session in django defalt databace 
                my_user = User.objects.create_user(username,email,pass1)
                my_user.save()
        # if all values get login page call        
        return redirect('login')
    # if there is eny error again sign up page calling
    return render(request,'signup.html')
 
@never_cache
def LoginPage(request):
    if 'username' in request.session:
        return redirect('home')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password = pass1)
        # if username and password come and check in session if true 
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('home')
        else:
            # if not true give a massage to user
            return HttpResponse("Username or Password is Incorrect!!!")
    # render again login page
    return render(request,'login.html')

# logout def for Delete session in 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache    
def LogOutPage(request):
    if 'username' in request.session:
        del request.session['username']
        logout(request)
        return redirect('login')
    
    








