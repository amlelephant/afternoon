from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import os
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import praw


# Create your views here.
def index(response):
    return render(response, 'main/index.html', {})

@login_required(login_url='login')
def home(request):
    try:
        profile = request.user.profile
    except: 
        return render(request, 'main/settings.html', {})
    urls = [profile.url1, profile.url2, profile.url3, profile.url4, profile.url5, profile.url6]
    
    
    reddit = praw.Reddit(client_id='OEmrqiJRAD-_WsutfE1Fww', client_secret="hwa3aLvitCrBe7qwStjKjoi0E9d_jQ", user_agent='GetTopOfSub')
    embeds = []
    for x in range(len(urls)):
        
        #reddit
        if urls[x] != None:
            
            # reddit (works)
            if urls[x].startswith('www.reddit.com/r/'):
                subreddit = reddit.subreddit(urls[x][17:])
                # get top 1 post for today
                for submission in subreddit.top('day', limit=1):
                    embeds.append("https://www.redditmedia.com" + submission.permalink + "/?ref_source=embed&amp;ref=share&amp;embed=true")

            # facebook (works)
            elif urls[x].startswith('www.facebook.com/'):
                embeds.append("https://www.facebook.com/plugins/page.php?href=" + urls[x] + "&tabs=timeline&width=640&height=500&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=true&appId")

            # youtube (works)
            elif urls[x].startswith('www.youtube.com/'):
                uname = urls[x][17:]
                embeds.append("https://www.youtube.com/embed?listType=user_uploads&list=" + uname)
            
            # instagram (works)
            elif urls[x].startswith('www.instagram.com/'):
                embeds.append("https://www.instagram.com/" + urls[x][18:] + "/embed")
            
            # twitter (does not work)
            elif urls[x].startswith('www.twitter.com/'):
                embeds.append("https://twitter.com/" + urls[x][16:] + "/embed")
            
            else:
                embeds.append(" ")
        else:
            embeds.append(" ")
    context = {'url1': embeds[0], 'url2': embeds[1], 'url3': embeds[2], 'url4': embeds[3], 'url5': embeds[4], 'url6': embeds[5]}
    return render(request, 'main/home.html', context)

def login_request(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'main/login.html', context)

def register(response):
    if response.user.is_authenticated:
        return redirect('/home')
    else:
        form = CreateUserForm()
        if response.method == 'POST':
            form = CreateUserForm(response.POST)
            

            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                Profile.objects.create(user=form.instance)
                messages.success(response, 'Account was created for ' + form.cleaned_data.get('username'))
                return redirect('/login')

    context = {'form': form}
    return render(response, 'main/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='login')
def settings(request):
    profile_form = ProfileForm(instance=request.user.profile)

    # edit user profile form
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/home')
    
    
    context={"user":request.user, "profile_form":profile_form }
    return render(request, 'main/settings.html', context)


def contact(request):
    return render(request, 'main/contact.html', {})

def mission(request):
    return render(request, 'main/ourMission.html', {})