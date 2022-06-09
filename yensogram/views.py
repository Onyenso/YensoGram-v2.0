from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse
from django.urls import reverse

from .forms import UserRegisterForm, LoginForm, ProfileUpdateForm, PostForm
from .models import User, DynamicModel, DynamicModelField, Post
from django.contrib import messages as flash_message # For flash messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q





"""For friend request badge"""
def badges(request):
    # Get user's friends' table
    user_table = DynamicModel.objects.get(name=f"{request.user.email} friends")
    # Convert user's friends' table to a model
    User_table = user_table.as_model()
    # Friend request details
    fr_rq_details = User_table.objects.filter(declined=0, accepted=0).order_by("-time_fr")
    badge = fr_rq_details.count()

    if badge == 0:
        badge = ""

    return {"rqs": fr_rq_details, "badges": badge}





"""For unread messages"""
def unopened(request, username):

    user_messages = DynamicModel.objects.get(name=f"{request.user.email} messages")
    User_messages = user_messages.as_model()

    friend = User.objects.filter(username=username).first()
    if not friend:
        return JsonResponse({"Error": "No such username in YensoGram!"})

    unread_messages = User_messages.objects.filter(read=0, recieved=1, deleted=0, friend=friend.id).count()
    if unread_messages == 0:
        unread_messages = ""
    return JsonResponse({"unread_messages": unread_messages})






"""Index"""
@login_required
def index(request):

    user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends") # Get user's friends' table
    User_friends = user_friends.as_model() # Turn table to a model
    friends = User_friends.objects.filter(accepted=1).values("username") # Get usernames of accepted friends in table
    friends_ids = User.objects.filter(username__in=friends).values("id") # Get ids of the usernames

    unreads = {}

    # for id in friends_ids:
    #     if id not in unreads:
    #         unread[id] = unopened(request, id)

    posts = Post.objects.filter(Q(author__in=friends_ids) | Q(author=request.user)).order_by("-date") # Get posts of these ids

    # Get page requested
    page_number = request.GET.get("page")

    paginator = Paginator(posts, 10) # Show 10 posts per page.

    page_obj = paginator.get_page(page_number)

    return render(request, "yensogram/index.html", {"badges": badges(request), "page_obj": page_obj, "friends":friends, "unread": unreads})






"""Route for signing up"""
def register(request):

    if request.method == "GET":
        # New register form
        form = UserRegisterForm()
        return render(request, "yensogram/register.html", {"form": form})

    else:
        new_POST_dict = QueryDict.copy(request.POST) # I copied request.POST because
        # request.POST is not mutable and I want to capitalize() the username of the
        # new user

        new_POST_dict["username"] = new_POST_dict["username"].capitalize()

        form = UserRegisterForm(new_POST_dict)
        # If form inputs are valid
        if form.is_valid():
            new_user = form.save(commit=False) # This reason for this
            # save(commit=False) is to capitalize
            # username, so that saving usernames with the same spelling but 
            # different capitalization will not be allowed.
            new_user.username = form.cleaned_data["username"].capitalize()
            new_user.save() # Register user

            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get('username')

            # Create table for user's friends
            friends = DynamicModel.objects.create(name=f"{email} friends")

            # Fields for user's friends' table
            # 1
            friends_username =  DynamicModelField.objects.create(
                name = "username",
                data_type = "character",
                model_schema = friends,
                max_length = 255
            )
            # 2
            friends_accepted = DynamicModelField.objects.create(
                name = "accepted",
                data_type = "integer",
                model_schema = friends
            )
            # 3
            friends_time_fr = DynamicModelField.objects.create(
                name = "time_fr",
                data_type = "date",
                null=True,
                model_schema = friends
            )
            # 4
            friends_time_accepted = DynamicModelField.objects.create(
                name = "time_accepted",
                data_type = "date",
                null=True,
                model_schema = friends
            )
            # 5
            friends_declined = DynamicModelField.objects.create(
                name = "declined",
                data_type = "integer",
                model_schema = friends
            )

            friends.as_model()

            # Create table for user's messages
            messages = DynamicModel.objects.create(name=f"{email} messages")

            # Fields for user's messages' table
            # 1
            messages_message = DynamicModelField.objects.create(
                name = "message",
                data_type = "text",
                model_schema = messages
            )
            # 2
            messages_friend = DynamicModelField.objects.create(
                name = "friend",
                data_type = "integer", # forigen key to id of User table. Remeber to manually type in
                                       # the value during runtime
                model_schema = messages
            )
            # 3
            messages_sent = DynamicModelField.objects.create(
                name = "sent",
                data_type = "integer",
                null = True,
                model_schema = messages
            )
            # 4
            messages_recieved = DynamicModelField.objects.create(
                name = "recieved",
                data_type = "integer",
                null = True,
                model_schema = messages
            )
            # 5
            messages_time = DynamicModelField.objects.create(
                name = "time",
                data_type = "date",
                model_schema = messages
            )
            #6
            messages_read = DynamicModelField.objects.create(
                name = "read",
                data_type = "integer",
                model_schema = messages
            )
            #7
            messages_deleted = DynamicModelField.objects.create(
                name = "deleted",
                data_type = "integer",
                model_schema = messages
            )

            messages.as_model()

            flash_message.success(request, f'Account created! Please log in.')
            return HttpResponseRedirect(reverse("yg-login"))
        # Form inputs are not valid
        else:
            flash_message.warning(request, 'Please fix issues with your input!', "danger")
            return render(request, "yensogram/register.html", {"form": form})






"""Route for logging in"""
def login_view(request):

    if request.method == "GET":
        logout(request) # Logout existing user
        form = LoginForm()
        return render(request, "yensogram/login.html", {"form": form})

    else:
        value_next= request.POST.get('next') # Get redirect URL

        new_POST_dict = QueryDict.copy(request.POST) # I copied request.POST because
        # request.POST is not mutable and I want to capitalize() the username of the
        # old user
        new_POST_dict["username"] = new_POST_dict["username"].capitalize()
        form = LoginForm(new_POST_dict)

        # If form inputs are valid
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # Authenticate user
            user = authenticate(request, username=username.capitalize(), password=password)

            # Check if authentication was successful
            try:
                login(request, user)
                flash_message.success(request, 'Logged In!')
                if value_next:
                    return redirect(value_next)
                return HttpResponseRedirect(reverse("yg-index"))
            # Authentication failed
            except:
                flash_message.warning(request, 'Invalid Username and/or Password!', "danger")
                return render(request, "yensogram/login.html", {"form": form})
        # Form inputs are not valid
        else:
            flash_message.warning(request, 'Please fix issues with your input!')
            return render(request, "yensogram/login.html", {"form": form})






"""Route for logging out"""
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("yg-login"))





"""Route for users' account"""
@login_required
def account(request, username):

    # If username does not exist
    if not User.objects.filter(username=username.capitalize()).exists():
        return HttpResponse("The username you provided doesn't eixst")

    # Get user's details and posts
    details = User.objects.get(username=username.capitalize())
    posts = Post.objects.filter(author=details).order_by("-date")
    total = posts.count()

    # If user is the owner of the account
    if request.user.username.capitalize() == username.capitalize():

        # If request method is GET
        if request.method == "GET":

            if not details.bio:
                details.bio = "None"
                details.save()

            form = ProfileUpdateForm(instance=request.user)
            
            return render(
                        request,
                        "yensogram/user_account.html",
                        {"form": form,"badges": badges(request), "details": details, "posts": posts, "total": total}
                    )

        # If request method is POST
        else:
            new_POST_dict = QueryDict.copy(request.POST) # I copied request.POST because
            # request.POST is not mutable and I want to capitalize() the username of the
            # old user
            new_POST_dict["username"] = new_POST_dict["username"].capitalize()
            
            form = ProfileUpdateForm(new_POST_dict, request.FILES, instance=request.user)

            # If form inputs are valid
            if form.is_valid():
                form.save() # Update user's details
                flash_message.success(request, 'Account info updated!')
                return HttpResponseRedirect(reverse("yg-account", args=[request.user.username]))

            else:
                request.user.username = username.capitalize() # There's a reason for this line
                flash_message.warning(request, 'Please fix issues with your input!', "danger")
                return render(
                            request,
                            "yensogram/user_account.html",
                            {"form": form, "badges": badges(request), "details": details, "posts": posts, "total": total}
                        )
    # If user isn't the owner of the account
    else:
        """For accept/decline friend request links on the page"""
        # Get user's friends' table
        user_table = DynamicModel.objects.get(name=f"{request.user.email} friends")

        # Convert user's friends' table to a model
        User_table = user_table.as_model()
        # Check if there's a friend request from the owner of the account
        check = User_table.objects.filter(username=username.capitalize(), accepted=0, declined=0).exists()
        
        return render(
                    request,
                    "yensogram/account.html",
                    {"badges": badges(request), "details": details, "posts": posts, "total": total, "check": check}
                )







"""Route for adding a friend"""
@login_required
def add(request):

    if request.method == "GET":
        return render(request, "yensogram/add.html", {"badges": badges(request)})

    else:
        username = request.POST["username"].capitalize()
        # If username does not exist
        if not User.objects.filter(username=username).exists():
            flash_message.warning(request, 'Username is not on Yensogram!')
            return render(request, "yensogram/add.html", {
                "message": "Invalid username.",
                "badges": badges(request)
            })
        
        # If user tried adding himself as a friend
        elif username == request.user.username:
            flash_message.warning(request, "You can't add yourself as a friend.", "danger")
            return render(request, "yensogram/add.html", {
                "message": "You can't add yourself as a friend.",
                "badges": badges(request)
            })

        # Check if user already has the username as a friend
        user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends")
        User_friends = user_friends.as_model()

        if User_friends.objects.filter(username=username).exists():
            flash_message.warning(request, "You already have this user as a friend.", "danger")
            return render(request, "yensogram/add.html", {
                "message": "You already have this user as a friend.",
                "badges": badges(request),
            })
        
        else:
            # Insert friend into user's friend list
            friend = User_friends(
                username=username,
                accepted=-1, # Null(unapplicable)
                time_fr=None, # Null(unapplicable)
                time_accepted=None, # Null(unapplicable)
                declined=-1 # Null(unapplicable)
            )
            friend.save()

            # Insert user into friend's friend list, but unaccepted
            friend_friends = DynamicModel.objects.get(name=f"{User.objects.get(username=username).email} friends")
            Friend_friends = friend_friends.as_model()

            user = Friend_friends(
                username=request.user.username,
                accepted=0,
                time_fr=datetime.now(),
                time_accepted=None,
                declined=0 
            )
            user.save()
            flash_message.success(request, "Request sent!")
            return HttpResponseRedirect(reverse("yg-add"))






# Route for user's friend requests
@login_required
def friend_requests(request):
    return render(request, "yensogram/friend_rqs.html", {"badges": badges(request)})





# Route for accepting friend requests
@login_required
def friend_request_accept(request, username):
    username = username.capitalize()

    # Get user's friends' table    
    user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends")
    User_friends = user_friends.as_model()

    if not User_friends.objects.filter(username=username).exists():
        return HttpResponse("You don't have this user in your friends in order to accept.")
    
    # Update user's friend list and add friend by setting accepted to 1
    friend = User_friends.objects.get(username=username)
    friend.accepted = 1
    friend.time_accepted = datetime.now()
    friend.save()

    # Update friends's friend list and add user by setting accepted to 1
    friend_friends = DynamicModel.objects.get(name=f"{User.objects.get(username=username).email} friends")
    Friend_friends = friend_friends.as_model()
    user = Friend_friends.objects.get(username=request.user.username)
    user.accepted = 1
    user.time_accepted = datetime.now()
    user.save()

    return HttpResponseRedirect(reverse("yg-friend-requests"))






# Route for declining friend requests
@login_required
def friend_request_decline(request, username):
    username = username.capitalize()

    # Get user's friends' table
    user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends")
    User_friends = user_friends.as_model()

    if not User_friends.objects.filter(username=username).exists():
        return HttpResponse("You don't have this user in your friends in order to decline.")

    # Update user's friend list and "delete" friend by setting declined to 1
    friend = User_friends.objects.get(username=username)
    friend.declined = 1
    friend.save()

    # Update friends's friend list and "delete" user by setting declined to 1
    friend_friends = DynamicModel.objects.get(name=f"{User.objects.get(username=username).email} friends")
    Friend_friends = friend_friends.as_model()
    user = Friend_friends.objects.get(username=request.user.username)
    user.declined = 1
    user.save()

    return HttpResponseRedirect(reverse("yg-friend-requests"))





# Route for displaying the HTML for messages
@login_required
def messages(request, friend):

    friend=friend.capitalize()
    # Check if friend exists
    friend = User.objects.filter(username=friend).first()
    if not friend:
        return HttpResponse("There is no such user on YensoGram with the URL you provided.")

    # Get user's friend list
    user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends")
    User_friends = user_friends.as_model()

    # If user does not have friend in friend list
    if not User_friends.objects.filter(username=friend.username, accepted=1).exists():
        return HttpResponse(f"You are not friends with this user. Add {friend} as a friend to see your messages.")

    return render(request,
        "yensogram/messages_api.html",
        {"friend": friend, "badges": badges(request)}
    )





# Function for serializing a message object into JSON
def serialize_message(message):
        return {
            "id": message.id,
            "message": message.message,
            "friend": message.friend,
            "sent": message.sent,
            "recieved": message.recieved,
            #"timestamp": message.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "time": message.time,
            "read": message.read,
            "deleted": message.deleted
        }





# Route for fetching messages with AJAX
@csrf_exempt
@login_required
def messages_API(request, friend):

    friend=friend.capitalize()
    # Check if friend exists
    friend = User.objects.filter(username=friend).first()
    if not friend:
        return JsonResponse(
            {"Error": "There is no such user on YensoGram with the URL you provided."},
            status=400)
    # Get user's friend list
    user_friends = DynamicModel.objects.get(name=f"{request.user.email} friends")
    User_friends = user_friends.as_model()

    # If user does not have friend in friend list
    if not User_friends.objects.filter(username=friend.username, accepted=1).exists():
        return JsonResponse(
            {"Error": f"You are not friends with this user. Add {friend} as a friend to see your messages."},
            status=400)

    # Get user's messages
    user_messages = DynamicModel.objects.get(name=f"{request.user.email} messages")
    User_messages = user_messages.as_model()

    if request.method == "GET":
        # Get read messages between user and friend
        read_messages = User_messages.objects.filter(friend=friend.id, deleted=0, read=1)

        # This update() method returns updates the messages to read and returns
        #  the number of rows updated, i.e 0 in this case
        read_messages_count = read_messages.update(read=1)

        # Set all messages between user and friend to read and get the number of rows updated
        messages = User_messages.objects.filter(friend=friend.id, deleted=0).update(read=1)

        # This is the number of unread messages (the number of rows converted from unread to read)
        unread_messages_count = messages - read_messages_count
        
        # Get unread messages between user and friend by getting the rows towards the end of the table
        # The basic syntax is: Model.objects.all()[x:y] => SQL OFFSET and LIMIT CLAUSE
        # This means OFFSET x LIMIT y i.e get the (x + 1)th - yth item
        unread_messages = User_messages.objects.filter(friend=friend.id, deleted=0).all()[read_messages.count()-unread_messages_count:]

        return JsonResponse(
            {
                "read_messages": [serialize_message(read_message) for read_message in read_messages],
                "unread": [serialize_message(unread_message) for unread_message in unread_messages],
                "friend": friend.serialize(),
            },
            status=200
        )
    else:
        message = json.loads(request.body)
        message = message.get("message")

        # Insert message into user's messages
        User_messages.objects.create(
            message=message,
            friend=friend.id,
            sent=1,
            recieved=0,
            time=datetime.now(),
            read=1,
            deleted=0
        )

        # Insert message into friends's messages
        friend_messages = DynamicModel.objects.get(name=f"{friend.email} messages")
        Friend_messages = friend_messages.as_model()

        Friend_messages.objects.create(
            message=message,
            friend=request.user.id,
            sent=0,
            recieved=1,
            time=datetime.now(),
            read=0,
            deleted=0
        )

        message = User_messages.objects.filter(
            message=message,
            friend=friend.id,
            sent=1,
            recieved=0,
            #time=datetime.now(),
            read=1,
            deleted=0
        ).last()

        return JsonResponse({"stat": "Successful", "message": serialize_message(message)})






# Route for creating a new post
@login_required
def new_post(request):
    
    if request.method == "GET":
        form = PostForm()
        return render(request, "yensogram/create_post.html", {"badges": badges(request), "legend": "New Post", "form": form})
    else:
        post = Post(author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            flash_message.success(request, 'Posted!')
            return HttpResponseRedirect(reverse("yg-index"))
        else:
            return render(request, "yensogram/create_post.html", {"badges": badges(request), "legend": "New Post", "form": form})





# Route for each individual post
@login_required
def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return HttpResponse("No such post!")

    return render(request, "yensogram/post.html", {"post": post, "badges": badges(request)})





# Route for updating a post
def update_post(request, post_id):
    pass



# Route for deleting a post
def delete_post(request, post_id):
    pass

