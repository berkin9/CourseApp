from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib import messages

def user_login(request):
    if request.user.is_authenticated and "next" in request.GET:
        return render(request, "account/login.html", {"error":"yetkiniz yok."})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Giriş başarılı")
                nextUrl = request.GET.get("next", None)
                if nextUrl is None:
                    return redirect("index")
                else:
                    return redirect(nextUrl)
            else:
                messages.add_message(request, messages.ERROR, "username ya da parola yanlış")
                return render(request, "account/login.html", {"form":form})
        else:
            return render(request, "account/login.html", {"form":form})
    else:
        form = AuthenticationForm()
        return render(request, "account/login.html", {"form":form})

# def user_register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         password = request.POST["password"]
#         repassword = request.POST["repassword"]

#         if password != repassword:
#             return render(request, "account/register.html", 
#             {
#                 "error":"parola eşleşmiyor.",
#                 "username": username,
#                 "email": email
#             })

#         if User.objects.filter(username = username).exists():
#             return render(request, "account/register.html", 
#             {
#                 "error":"username kullanılıyor.",
#                 "username": username,
#                 "email": email
#             })
        
#         if User.objects.filter(email=email).exists():
#             return render(request, "account/register.html", 
#             {
#                 "error":"email kullanılıyor.",
#                 "username": username,
#                 "email": email
#             })
        
#         user = User.objects.create_user(username=username, email=email,password=password)
#         user.save()
#         return redirect("user_login")        
#     else:
#         return render(request, "account/register.html")

def change_password(request):
    form = PasswordChangeForm(request.user)
    messages.add_message(request, messages.SUCCESS, "Şifre Değiştirildi")
    return render(request, "account/change-password.html", {"form":form})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, "parola güncellendi")
            return redirect("change_password")
        else:
            return render(request, "account/change-password.html", {"form":form})
    form = PasswordChangeForm(request.user)
    return render(request, "account/change-password.html", {"form":form})

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username,password=password)
            login(request,user)
            return redirect("index")
        else:
            return render(request, "account/register.html", {"form":form})
    else:
        form = UserCreationForm()
        return render(request, "account/register.html", {"form":form})

def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Çıkış başarılı")
    return redirect("pages_index")