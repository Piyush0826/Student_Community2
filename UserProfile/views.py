from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Group, Resource, Event
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .forms import UserForm, UserProfileForm
from .models import UserProfile


# Create your views here.


def index(request):
    return render(request,'index.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')  # Redirect to the index page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')  # Render the login template
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('signup')

    return render(request, 'signup.html')  # Render the signup template

def dashboard(request):
    return render(request,'dashboard.html')
def aboutus(request):
    return render(request,'aboutus.html')


@login_required
def edit_profile(request):
    # Ensure the UserProfile exists
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')  # Or wherever you want to redirect after updating

    return render(request, 'userprofile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
from django.contrib.auth import logout  # Import logout

# Logout view
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')  # Redirect to index or any page you prefer after logout


# Dashboard view
@login_required
def dashboard(request):
    # Fetch some example data for the dashboard
    groups = Group.objects.all()[:3]  # Limit to 3 for display
    resources = Resource.objects.all()[:3]  # Limit to 3 for display
    events = Event.objects.all()[:3]  # Limit to 3 for display

    return render(request, 'dashboard.html', {
        'groups': groups,
        'resources': resources,
        'events': events
    })


# Group discussion page view
@login_required
def group_discussions(request):
    groups = Group.objects.all()
    return render(request, 'userprofile/group_discussions.html', {'groups': groups})


# Document collaboration view placeholder
@login_required
def documents(request):
    return render(request, 'userprofile/documents.html')  # Template for documents collaboration


# Group join view
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'userprofile/group_detail.html', {'group': group})


# Resource detail view
@login_required
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    return render(request, 'userprofile/resource_detail.html', {'resource': resource})


from django.shortcuts import render
from django.http import JsonResponse
from .models import Message

# Simple predefined responses
PREDEFINED_RESPONSES = {
    "hello": "Hi there! How can I assist you today?",
    "how are you": "I'm just a bot, but I'm functioning as expected! How about you?",
    "bye": "Goodbye! Have a great day!",
}


def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").lower()
        # Look for a predefined response
        response = PREDEFINED_RESPONSES.get(user_message, "I'm sorry, I don't understand that.")

        # Save the conversation in the database (optional)
        if request.user.is_authenticated:
            Message.objects.create(user=request.user, message=user_message, response=response)

        return JsonResponse({"response": response})

    return render(request, "userprofile/chat.html")
