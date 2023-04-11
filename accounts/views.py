from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

# Create your views here.

# def login_view(request):
#     if request.method == 'POST':
#         username= request.POST.get('username')
#         password= request.POST.get('password')
#         #remove this!!! for security reasons
#         print(username, password)

#         user= authenticate(request,username=username, password=password)
#         if user is None:
#             context = {"error": "Invalid username or Password"}
#             return render(request,"accounts/login.html",context)
        
#         login(request,user)
#         #yha pe ek alert message dalna hai
#         return redirect('/')
#     return render(request,"accounts/login.html",{})

#another way to login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
             user=form.get_user()
             login(request,user)
        #yha pe ek alert message dalna hai
             return redirect('/')
    else:
        form=AuthenticationForm(request)
    context={
        'form':form
    }
    return render(request,"accounts/login.html",context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')
    return render(request,"accounts/logout.html",{})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {'form':form}
    return render(request,"accounts/register.html",context)