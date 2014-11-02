from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from models import *
from mimetypes import guess_type
from django.contrib.auth.decorators import login_required
from django.db import transaction

def home(request):
    newss = News.objects.all()
    context = {'newss':newss}
    if not request.user.is_anonymous():
        user_more = User_More.objects.get(user=request.user)
        context['login_user'] = user_more
    return render(request, 'event/index.html', context)

def contact(request):
    context = {}
    if not request.user.is_anonymous():
        user_more = User_More.objects.get(user=request.user)
        context['login_user'] = user_more
    return render(request, 'event/contact.html', context)

@login_required
def my_events(request):
    usermore = User_More.objects.get(user=request.user)
    context = {'login_user': usermore}
    user_events = UserMore_Event.objects.filter(user_more=usermore)
    events = [user_event.event for user_event in user_events]
    context['events'] = events
    return render(request, 'event/my_events.html', context)

@login_required()
def my_friends(request):
    usermore = User_More.objects.get(user=request.user)
    context = {'login_user': usermore}
    user_events = UserMore_Event.objects.filter(user_more=usermore)
    events = [user_event.event for user_event in user_events]
    friends = {}
    for event in events:
        pairs = UserMore_Event.objects.filter(event=event)
        for pair in pairs:
            if not pair.user_more in friends:
                friends[pair.user_more] = 0
    friends.pop(usermore)
    context['friends'] = friends
    return render(request, 'event/my_friends.html', context)

@transaction.atomic
@login_required()
def publish(request):
    user_more = User_More.objects.get(user=request.user)
    context = {'login_user': user_more}
    if request.method == 'GET':
        return render(request, 'event/register.html', context)
    news = News(title=request.POST['title'], tag=request.POST['tag'], abstract=request.POST['abstract'], content=request.POST['content'], pic=request.FILES['picture'], media=request.user, check=True)
    news.save()
    return redirect('/news')

@login_required()
def all_user(request):
    user_more = User_More.objects.get(user=request.user)
    if(user_more.role != 3):
        return redirect('/news')
    context = {'login_user': user_more}
    all_users = User_More.objects.all()
    context['friends'] = all_users
    return render(request, 'event/my_friends.html', context)

@login_required()
def all_event(request):
    user_more = User_More.objects.get(user=request.user)
    if(user_more.role != 3):
        return redirect('/news')
    context = {'login_user': user_more}
    all_event = Event.objects.all()
    context['events'] = all_event
    return render(request, 'event/my_events.html', context)