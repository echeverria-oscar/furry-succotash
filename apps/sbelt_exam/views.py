from django.shortcuts import render, redirect
from .models import User, Quotes
from django.contrib import messages
import datetime


# Create your views here.

def index(request):

    return render(request, 'sbelt_exam/index.html')


def register(request):
    if request.method == "POST":
       form_errors = User.objects.validate(request.POST)

    if len(form_errors) > 0:
       for error in form_errors:
           messages.error(request, error)
    else:
        User.objects.register(request.POST)
        messages.success(request, "You have successfully registered! Please login to continue")

    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Not login credentials!")
            return redirect('/')
        else:
           request.session['logged_user'] = user.id
           return redirect('/quotes')

def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('/')

def quotes(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    me =  User.objects.get(id=request.session['logged_user'])
    favorites=Quotes.objects.filter(writer=me)
    quotes = Quotes.objects.exclude(id__in=favorites)
    # non_fave = Quotes.objects.get
    # user = user.objects.get()
    context = {
        'me': me,
        'quotes' : quotes,
        'favorites' : favorites,
    }
    return render(request, 'sbelt_exam/quotes.html', context)

def add_qoute(request):
    user = User.objects.get(id=request.session['logged_user'])
    get_quote=request.POST['quote']
    print get_quote
    if request.POST:
        errors = Quotes.objects.v_post(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)

        else:
            Quotes.objects.create(quoted_by=request.POST['quoted_by'], quote=request.POST['quote'], user = user)

    return redirect('/quotes')

def add_favorites(request, id):
    favorite = Quotes.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    favorite.writer.add(user)
    favorite.save()

    return redirect('/quotes')

def remove_favorites(request, id):
    favorite = Quotes.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    favorite.writer.remove()

    return redirect('/quotes')

def profile(request,id):
    if 'logged_user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=id)
    profiles = Quotes.objects.filter(user_id=user)
    count = Quotes.objects.filter(user_id=user)
    if count > 0:
        count= len(count)

    context = {
        'profiles': profiles,
        'user' : user,
        'count': count
    }

    return render(request, 'sbelt_exam/users_page.html', context)
