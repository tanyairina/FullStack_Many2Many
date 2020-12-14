from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/quotes')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    loggedin_user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = loggedin_user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/quotes')

def quotes(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_quotes': Quote.objects.all(),
        'other_quotes': Quote.objects.exclude(uploaded_by=request.session['user_id'])
    }
    return render(request, 'quotes.html', context)

def create(request):
    if request.method == 'GET':
        return redirect('/quotes')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.create(
            message = request.POST['message'],
            uploaded_by = user,
        )
        context = {
            'quote': Quote.objects.last(),
        }
        user.fav_quotes.add(quote)
        return render(request, 'onequote.html', context)

def edit(request, quote_id):
        user = User.objects.get(id=request.session['user_id'])
        one_quote = Quote.objects.get(id=quote_id)
        context = {
            'quote': one_quote,
            'user': user
        }
        return render(request, 'edit.html', context)

def update(request, quote_id):
    if request.method == 'GET':
        return redirect('/quotes')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/quotes/edit/{quote_id}")
    else:
        User.objects.get(id=request.session['user_id'])
        to_update = Quote.objects.get(id=quote_id)
        to_update.title = request.POST['title']
        to_update.desc = request.POST['message']
        to_update.save()
        updated = Quote.objects.get(id=quote_id)
        request.session['quote_id'] = updated.id
        messages.success(request, "Quote successfully updated!")
        return redirect(f"/quotes/{quote_id}")

def onequote(request, quote_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    one_quote = Quote.objects.get(id=quote_id)
    context = {
        'quote':one_quote,
        'user': user
    }
    return render(request, 'onequote.html', context)

def user(request, user_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_quotes': Quote.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'user.html', context)

def others(request, user_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_books': Quote.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'others.html', context)

def favorite(request, quote_id):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Quote.objects.get(id=quote_id)
        user.fav_quotes.add(book)
        user.save()
        updated = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = updated.id
        messages.success(request, "Added to Favorite Quotes")
        return redirect(f'/quotes/{quote_id}')

def unfavorite(request, quote_id):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Quote.objects.get(id=quote_id)
        user.fav_quotes.remove(book)
        user.save()
        updated = User.objects.get(id=request.session['user_id'])
        request.session['user_id'] = updated.id
        messages.success(request, "Removed from Favorite Quotes")
        return redirect(f'/quotes/{quote_id}')


def delete(request, quote_id):
    if 'user_id' not in request.session:
        return redirect('/')
    User.objects.get(id=request.session['user_id'])
    to_delete=Quote.objects.get(id=quote_id)
    to_delete.delete()
    return redirect('/quotes')

def logout(request):
    messages.success(request, "Succefully Logout!")
    request.session.clear()
    return redirect('/')