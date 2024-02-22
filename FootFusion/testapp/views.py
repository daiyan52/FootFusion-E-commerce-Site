from django.shortcuts import render,HttpResponseRedirect
from testapp.forms import UserForm,ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from testapp.models import Profile
from django.contrib import messages
# Create your views here.

def home_view(request):
    return render(request, 'pages/home.html')

@login_required
def features_view(request):
    return render(request, 'pages/features.html')



def signup_view(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('testapp:login'))
    else:
        form = UserForm()
    return render(request, 'pages/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('App_shop:home')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return HttpResponseRedirect(reverse('App_shop:home'))
    # return render(request, 'pages/logout.html',{'msg':msg}) 
     # return HttpResponseRedirect(reverse('testapp:logout'))

                                         

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Saved Successfully")
            return redirect(reverse('App_shop:home'))
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'pages/profile.html', {'form': form})
