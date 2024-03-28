from django.shortcuts import render
from django.http import  HttpResponseRedirect
from .forms import signUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
#Home view function
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts' : posts})


#About view function
def about(request):
    return render(request, 'blog/about.html')

#Contact view function
def contact(request):
    return render(request, 'blog/contact.html')

#Dashboard view function
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts' : posts, "fullname" : full_name, 'groups' : gps})
    else:
        return HttpResponseRedirect('/login/')
    
#Logout view function
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#SignUp view function
def user_signup(request):
    if request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'Author')
            user.groups.add(group)
            messages.success(request, 'Congratulations, Now you are an author')
            form = signUpForm()
    else:
        form = signUpForm()
    return render(request, 'blog/signup.html', {"form" : form})


#Login view function
def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upwd = form.cleaned_data['password']
                user = authenticate(username = uname, password = upwd)
                if user is not None:
                    login(request=request)
                    messages.success(request, "You're Logged in")
                    return HttpResponseRedirect('/dashboard')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {"form" : form})
    else:
        return HttpResponseRedirect('/dashboard')
    

#add new post
def addpost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                posts = Post(title = title, desc = desc)
                posts.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {"form" : form})
    else:
        return HttpResponseRedirect('/login/')
    

#Update new post
def updatepost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk = id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk = id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form' : form})
    else:
        return HttpResponseRedirect('/login/')
    
#delete new post
def deletepost(request, id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi = Post.objects.get(pk = id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')