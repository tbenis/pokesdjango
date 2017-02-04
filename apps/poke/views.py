from django.shortcuts import render, redirect
from .models import User, Poke
import datetime
from django.contrib import messages
from django.db.models import Count
# Create your views here.
def index(request):

    #User.objects.all().delete()
    #Poke.objects.all().delete()
    return render(request, 'poke/login&reg.html')

def rProcess(request):
    print request.POST['dob']
    datenow = datetime.datetime.now()
    dob = datetime.datetime.strptime(str(request.POST['dob']), '%Y-%m-%d')
    postData = {
        "name": request.POST['name'],
        "alias": request.POST['alias'],
        "email": request.POST['email'],
        "password": request.POST['password'],
        "cPassword": request.POST['cPassword'],
        "dob" : dob,
        'datenow': datenow,
    }
    results = User.objects.rValidate(postData)
    # (True, [err err err])
    # (False, user obj)
    if results[0]: # There were errors
        for err in results[1]:
            print err
            messages.error(request, err) # add messages to message object
        return redirect('/')
    else:
        request.session['logged_in_user'] = results[1].id
        return redirect('/success')

def lProcess(request):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    try:
        postData = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        results = User.objects.lValidate(postData)
        if results[0]:
            request.session['logged_in_user'] = results[1].id

            return redirect('/success')
        else:
            messages.error(request, results[1])
            return redirect('/')
    except:
        messages.error(request, "Sorry! You are not an existing User. Please Register to create an account")
        return redirect('/')
def success(request):
    # User.objects.all().delete()
    # Poke.objects.all().delete()
# count the number of people that have poked logged in user
#**.. pokerpokes.count i think... **#
# count how many times a user has poked you

    number_of_pokers = Poke.objects.filter(poker=request.session['logged_in_user'])
    users = User.objects.all().exclude(id=request.session['logged_in_user'])
    pokes = Poke.objects.all()
    poke_count = User.objects.annotate(poke_count = Count('poker')).filter(poked =request.session['logged_in_user'])
    user_poke_count = Poke.objects.filter(poked =request.session['logged_in_user']).exclude
    poking_users = Poke.objects.filter(poked=request.session['logged_in_user']).exclude(id=request.session['logged_in_user'])
    list_of_users = User.objects.filter(poker__poked=request.session['logged_in_user']).annotate(num_poked = Count('poker__poked')).order_by('-num_poked')
    current_user = User.objects.get(id=request.session['logged_in_user'])
    context = {
    'current_user': current_user,
    # 'user': user,
    'poking_users':poking_users,
    'users': users,
    'pokes': pokes,
    'user_poke_count': user_poke_count,
    'list_of_users': list_of_users,
    'poked_count': poke_count
    }
    return render(request, 'poke/poke.html', context)

def counter(request, id):
    poker = User.objects.get(id=request.session['logged_in_user'])
    poked = User.objects.get(id=id)
    poke = Poke()
    poke.poker = poker
    poke.poked = poked
    poke.counter+=1
    poke.save()
    return redirect('/success')

def logout(request):
    request.session.clear()
    request.session.pop('logged_in_user', None)
    return redirect('/')
