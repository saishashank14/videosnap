from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def home(request):
    return render(request, "landing page/index.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("signup")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")

    return render(request, "accounts/signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

  
  
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            next_url = request.GET.get("next")
            return redirect(next_url or "home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

@login_required
def dashboard_view(request):
    return render(request, "dashboard/index.html")

dashboard = dashboard_view

def add(request):
    c = a_value = b_value = ""
    if request.method == "POST":
        a_value = request.POST.get("a_value", "")
        b_value = request.POST.get("b_value", "")
        c = int(a_value) + int(b_value)
    return render(request, "accounts/add.html", {"c": c, "a_value": a_value, "b_value": b_value})

def sub(request):
    c = a_value = b_value = ""
    if request.method == "POST":
        a_value = request.POST.get("a_value", "")
        b_value = request.POST.get("b_value", "")
        c = int(a_value) - int(b_value)
    return render(request, "accounts/sub.html", {"c": c, "a_value": a_value, "b_value": b_value})

def div(request):
    c = a_value = b_value = ""
    if request.method == "POST":
        a_value = request.POST.get("a_value", "")
        b_value = request.POST.get("b_value", "")
        c = int(a_value) / int(b_value)
    return render(request, "accounts/div.html", {"c": c, "a_value": a_value, "b_value": b_value})

def multi(request):
    c = a_value = b_value = ""
    if request.method == "POST":
        a_value = request.POST.get("a_value", "")
        b_value = request.POST.get("b_value", "")
        c = int(a_value) * int(b_value)
    return render(request, "accounts/multi.html", {"c": c, "a_value": a_value, "b_value": b_value})

def modulus(request):
    c = a_value = b_value = ""
    if request.method == "POST":
        a_value = request.POST.get("a_value", "")
        b_value = request.POST.get("b_value", "")
        c = int(a_value) % int(b_value)
    return render(request, "accounts/modulus.html", {"c": c, "a_value": a_value, "b_value": b_value})