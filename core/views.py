from core.models import Comments, User
from core.forms import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
 
import redis
 
@login_required
def home(request):
    #comments = Comments.objects.select_related().all()[0:100]
    #return render(request, 'index.html', locals())
    lst = Comments.objects.order_by().values('channel').distinct()
    return render_to_response('home.html',{ 'user': request.user ,'room' : lst})
    
@csrf_exempt
def node_api(request):
    try:
        #Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)
 
        #Create comment
        Comments.objects.create(user=user, text=request.POST.get('comment'), channel= request.POST.get('channel'))
        
        #Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', request.POST.get('channel') +"~"+ user.username  + ': ' + request.POST.get('comment'))
        
        return HttpResponse("Everything worked :)")
    except Exception as e:
        return HttpResponseServerError(str(e))
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def homes(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )
def channel(request, chatroom):
    comments = Comments.objects.filter(channel__contains = chatroom)[0:100]
    chat = chatroom
    return render(request, 'index.html', locals())