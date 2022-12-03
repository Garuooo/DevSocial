from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile,Skill,Message
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfile, CreateUser , SkillCreation , MessageCreation
from django.contrib.auth.models import User
from signatures.views import siamese_model, Verify, preprocess
from django.contrib import messages
from projects.models import Project
from signatures.models import Signature

def sign_up(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("profiles")
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user=user)
            return redirect("update_profile")
        else:
            return HttpResponse("Invalid Request")
    context = {"form": form}
    return render(request, "users/signup.html", context)

@login_required(login_url="login")
def update_profile(request):
    try:
        profile = request.user.profile
    except:
        messages.error("Profile Not Found")
        return redirect("login")
    form = UpdateProfile(instance=profile)
    if request.method == "POST":
        form = UpdateProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        messages.success(request, "Profile Saved")
        return redirect("profiles")
    context = {"form": form}
    return render(request, 'users/update_profile.html', context)

@login_required(login_url="login")
def log_out(request):
    try:
        user = request.user
    except:
        messages.error(request, "An error occured")
    logout(request=request)
    messages.success(request, "Logged out successfully")
    return redirect("profiles")

def log_in(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("profiles")
    if request.method == "POST":
        try:
            password = request.POST["password"]
            email = request.POST["email"]
            username = request.POST["username"]
        except:
            return HttpResponse("Invalid Request")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user=user)
            messages.success(request, "logged in successfuly")
            return redirect("profiles")
        else:
            messages.error(request, "Username or Password is incorrect")
            return HttpResponse("Invalid Account")
    context = {}
    return render(request, 'users/login.html', context)

def login_with_signature(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("profiles")
    if request.method == "POST":
        try:
            username = request.POST["username"]
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Account Not Found")
            return redirect("login")
        try:
            image = request.FILES["signature"]
        except:
            messages.error(request, "Invalid Image")
            return redirect("login")
        try:
            if user.profile.personal_signature.name == "":
                messages.error(request, "Invalid personal signature Image")
                return redirect("login_with_signature")
            verify = Verify.objects.create(
                owner=user.profile, first_signature=user.profile.personal_signature, second_signature=image)
        except:
            messages.error(request, "Profile signature Image is not Found")
            return redirect("login")
        first_signature = preprocess(verify.first_signature)
        second_signature = preprocess(verify.second_signature)
        prediction = siamese_model.predict((first_signature, second_signature))
        print(prediction)
        if prediction >= 0.7:
            prediction = "Valid"
            verify.prediction = prediction
            verify.save()
            login(request, user=user)
            messages.success(request, "Logged In Successfully")
            return redirect("profiles")
        else:
            prediction = "Invalid"
            verify.prediction = prediction
            verify.save()
            messages.error(request, "Incorrect Signature")
            return redirect("login")
    context = {}
    return render(request, 'users/login_with_signature.html', context)

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)

def profile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except:
        return HttpResponse("Profile Not Found")
    projects = Project.objects.filter(owner=profile)
    if request.user.profile == profile:
        signatures = Signature.objects.filter(owner=profile)
    else:
        signatures=[]
    context = {"profile": profile,
               "signatures": signatures, "projects": projects}
    return render(request, "users/profile.html", context)

def history(request):
    try:
        profile = request.user.profile
    except:
        return HttpResponse("Profile Not Found")
    verify_objects = profile.verify_set.all()
    context = {"verify_objects": verify_objects}
    return render(request, 'users/history.html', context)

@login_required(login_url="login")
def create_skill(request):
    profile = Profile.objects.get(user=request.user)
    form = SkillCreation()
    if request.method == "POST":
        form = SkillCreation(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,"Skill added successfuly")
            return redirect("profile",profile.id)
        else:
            messages.error(request,"Invalid skill information")
    context={"form":form}
    return render(request,"users/create_skill.html",context)

@login_required(login_url="login")
def delete_skill(request,pk):
    skill=Skill.objects.get(pk=pk)
    profile = skill.owner
    if request.method=="POST":
        if request.user==profile.user:
            skill.delete()
            messages.success(request,"Skill deleted successfully")
            return redirect('profile',profile.id)
        else:
            messages.error(request,"You are not the owner")
            return redirect('profile',profile.id)
    context={"skill":skill,"value":"delete"}
    return render(request,"users/create_skill.html",context)

@login_required(login_url="login")
def edit_skill(request,pk):
    skill=Skill.objects.get(pk=pk)
    form = SkillCreation(instance=skill)
    profile=skill.owner
    if request.method=="POST" and request.user==profile.user:
        form = SkillCreation(request.POST,instance=skill)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,"Skill edited successfully")
            return redirect("profile",profile.id)
        else:
            messages.error(request,"Invalid skill Information")

    context={"form":form}
    return render(request,"users/create_skill.html",context)

@login_required(login_url="login")
def all_messages(request):
    profile = request.user.profile
    receieved_messages=Message.objects.filter(reciever=profile)
    sent_messages = Message.objects.filter(sender=profile)
    unread_length=0
    for message in receieved_messages:
        if message.is_read==False:
            unread_length+=1
    print(sent_messages)
    context={"sent_messages":sent_messages,"receieved_messages":receieved_messages,"unread_length":unread_length}
    return render(request,"users/inbox.html",context)


@login_required(login_url="login")
def view_message(request,id):
    try:
        message = Message.objects.get(id=id)
        if message.reciever != request.user.profile and message.sender != request.user.profile:
            messages.error(request,"Access Denied")
            return redirect("inbox")
        if message.is_read==False:
            message.is_read=True
            message.save()
    except:
            messages.error(request,"Message Not Found")
            return redirect("inbox")
    context={"message":message}
    return render(request,"users/message.html",context)


@login_required(login_url="login")
def create_message(request,pk):
    sender=request.user.profile
    try:
        reciever = Profile.objects.get(id=pk)
    except:
        messages.error("Reciever not found")
        return redirect("profiles")
    form = MessageCreation()
    if request.method=="POST":
        message = form.save(commit=False)
        message.reciever = reciever
        message.sender = sender
        message.save()
    context={"form":form}
    return render(request,"users/create_message.html",context)    