import _json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Message

# Create your views here.
def index(request):
    posts = Post.objects.all()
    users = User.objects.all()
    try:
        friends = request.user.friend_list.all()

    except:
        friends = None

    # Paginate the render
    posts = posts.order_by("-timestamp").all()
    page_number = request.GET.get('page_number', 1)
    p = Paginator(posts, 2)

    return render(request, "networkext/index.html", {
        "posts": p.page(page_number),
        "users": users,
        "friends": friends,
    })


def messages(request):
    messages = Message.objects.all()
    return JsonResponse([message.serialize() for message in messages], safe=False)


def react_message_send(request, user_id):
    if request.method == "POST":
        return JsonResponse({"error": "post method is required"}, status=400)

    data = json.loads(request.body)
    body = data.get("body", "")
    receiver = User.objects.get(id=user_id)
    message = Message(author=request.user, body=body, receiver=receiver)
    message.save()
    return JsonResponse(message, safe=False)

def react_message(request):
    users = User.objects.all()
    return JsonResponse([user.serialize() for user in users], safe=False)

def react_post(request):
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def message(request):
    return HttpResponse("message")


def profile(request, user_id):
    return render(request, "networkext/profile.html")


def friend_request(request):
    if request.method == "POST":
        friend = get_object_or_404(User, pk=int(request.POST["user_id"]))
        if friend in request.user.friend_list.all():
            request.user.friend_list.remove(friend)
        else:
            request.user.friend_list.add(friend)
    return HttpResponseRedirect(reverse('index'))


def like_post(request):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=int(request.POST["post_id"]))
        if post in request.user.like_list.all():
            request.user.like_list.remove(post)
        else:
            request.user.like_list.add(post)
    return HttpResponseRedirect(reverse("index"))



def post(request):
    if request.method == "POST":
        body = request.POST["post_body"]

        try:
            user = User.objects.get(id=request.user.id)
            post = Post(author=user, body=body)
            post.save()

        except ObjectDoesNotExist:
            return render(request, "networkext/index.html", {
                "message": "Error please try again"
            })
    return HttpResponseRedirect(reverse("index"))
    


def login_view(request):
    if request.method == "POST":

        # Try to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # make sure the login was successfor
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "networkext/login.html", {
                "message": "Invalid username or password",
            })
    return render(request, "networkext/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # make sure the passwords match
        if password != confirmation:
            return render(request, "networkext/register.html", {
                "message": "Passwords must match",
            })
        
        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "networkext/register.html", {
                "message": "Username is already taken"
                })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "networkext/register.html")