from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)



def index(request):
    return render(request, "friends_app/index.html")



def register(request):
    if request.method == "POST":
        errors = User.objects.validate_registration(request.POST)

        if not errors:
            hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())

            user = User.objects.create(name=request.POST["name"], alias=request.POST["alias"], email=request.POST["email"], password=
                hash_pw, birthdate = request.POST["birthdate"])

            request.session['id'] = user.id

            return redirect("/friends")

        flash_errors(errors, request)

    return redirect('/')



def login(request):
    if request.method =="POST":
        check = User.objects.validate_login(request.POST)
        if "user" in check:
            request.session["id"] = check["user"].id
            return redirect("/friends")
        flash_errors(check["errors"], request)

    return redirect("/")



def friends(request):
    user = User.objects.get(id=request.session['id'])
    friends = user.friends.all()
    non_friends = User.objects.exclude(id__in=friends).exclude(id=request.session["id"])
    context = {
        "all_friends": friends,
        "user": user,
        "all_non_friends": non_friends
    }
    
    return render(request, "friends_app/dashboard.html", context)



def add_friend(request):
    print request.POST["friend_id"]

    this_friend = User.objects.get(id=request.POST["friend_id"])
    this_user = User.objects.get(id=request.session["id"])
    this_friend.friends.add(this_user)

    return redirect("/friends")
    


def show(request, id):
    context = {
        "user": User.objects.get(id=id)
    }
    return render(request, "friends_app/profile.html", context)



def destroy(request, id):
    user = User.objects.get(id=request.session["id"])
    friend_to_destroy = User.objects.get(id=id)
    user.friends.remove(friend_to_destroy)
    

    return redirect("/friends")



def clear(request):
    request.session.flush()
    return redirect("/")