from django.utils import timezone
from django.shortcuts import  get_object_or_404, render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post

#FILE PATHS
header_path = 'thinkers/header.html'
register_path ='thinkers/register.html'
login_path = "thinkers/login.html"
home_path =  "thinkers/home.html"
cinema_path = "thinkers/cinema.html"
book_path =  "thinkers/book.html"
travel_path = "thinkers/travel.html"
food_path = "thinkers/food.html"
profile_path = "thinkers/profile.html"
post_edit_path = 'thinkers/post_edit.html'
post_detail_path = 'thinkers/post_detail.html'

#INDEX
def index(request):
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)
    return render(request, header_path, context={'login_form':login_form, "register_form":register_form})

#REGISTER
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f"Registration successful. Welcome {username}" , extra_tags="register_success")
            return redirect('index')
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags="register")
    form = NewUserForm()
    return render (request=request, template_name=register_path, context={"register_form":form})

#LOGIN
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.",extra_tags="login")
        else:
            messages.error(request,"Invalid username or password.",extra_tags="login")
    form = AuthenticationForm()
    return render(request=request, template_name=login_path, context={"login_form":form})

#LOGOUT
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("index")    

#MENU BAR FUNCTIONS
def home(request):
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    posts =  Post.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)
    return render(request, home_path, context={'login_form':login_form, "register_form":register_form, 'posts': posts})

def cinema(request):
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    posts = Post.objects.filter(category=2) #category cinema
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)    
    return render(request, cinema_path, context={'login_form':login_form, "register_form":register_form, 'posts': posts})

def book(request):
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    posts = Post.objects.filter(category=1) #category book
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)    
    return render(request, book_path, context={'login_form':login_form, "register_form":register_form, 'posts': posts})

def travel(request):
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    posts = Post.objects.filter(category=4) #category travel
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)    
    return render(request, travel_path, context={'login_form':login_form, "register_form":register_form, 'posts': posts})

def food(request):
    posts = Post.objects.filter(category=3) #category food
    login_form = AuthenticationForm()
    register_form = NewUserForm()
    if 'Loginpagebutton' in request.POST:
          login_request(request)
    elif 'Registerbutton' in request.POST:
          register_request(request)    
    return render(request, food_path, context={'login_form':login_form, "register_form":register_form, 'posts': posts}) 

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    return render(request, profile_path,{'user': user,'posts':posts})


#POST FUNCTIONS
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, post_edit_path, {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, post_detail_path, {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, post_edit_path, {'form': form})    