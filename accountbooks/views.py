from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from .models import AccountBook

def index(request):
    accountbooks = AccountBook.objects.all()
    context = {
        'accountbooks' : accountbooks 
    }
    return render(request, 'accountbooks/index.html', context)

def detail(request, account_book_pk):
    accountbook = AccountBook.objects.get(pk = account_book_pk)
    accountbook_dict = model_to_dict(accountbook)
    attributes = list(accountbook_dict.items())
    context = {
        'accountbook' : accountbook,
        'attributes' : attributes,
    }
    return render(request, 'accountbooks/detail.html', context)

def new(request):
    return render(request, 'accountbooks/new.html')

def create(request):
    note = request.POST.get('note')
    category = request.POST.get('category')
    amount = request.POST.get('amount')
    date = request.POST.get('date')
    description = request.POST.get('description')

    accountbook = AccountBook(note=note, category=category, amount=amount, date=date, description=description)
    accountbook.save()
    return redirect('accountbooks:detail', accountbook.pk)

def edit(request, account_book_pk):
    accountbook = AccountBook.objects.get(pk=account_book_pk)
    context = {
        'accountbook': accountbook
    }
    return render(request, 'accountbooks/edit.html', context)

def update(request, account_book_pk):
    accountbook = AccountBook.objects.get(pk=account_book_pk)
    note = request.POST.get('note')
    category = request.POST.get('category')
    amount = request.POST.get('amount')
    date = request.POST.get('date')
    description = request.POST.get('description')

    accountbook.note = note
    accountbook.category = category
    accountbook.amount = amount
    accountbook.date = date
    accountbook.description = description
    accountbook.save()
    return redirect('accountbooks:detail', accountbook.pk)

def delete(request, account_book_pk):
    accountbook = AccountBook.objects.get(pk=account_book_pk)
    accountbook.delete()
    return redirect('accountbooks:index')


def copy(request, account_book_pk):
    accountbook = get_object_or_404(AccountBook, pk=account_book_pk)
    
    note = accountbook.note
    category = accountbook.category
    amount = accountbook.amount
    date = accountbook.date
    description = accountbook.description
    
    accountbook_copy = AccountBook(note=note, category=category, amount=amount, date=date, description=description)
    accountbook_copy.save()
    
    return redirect('accountbooks:index')


def index_copy(request):
    sortkey = request.POST.get('sortkey', 'id')
    accountbooks = AccountBook.objects.all().order_by(sortkey)
    context = {
            'accountbooks': accountbooks,
    }
    return render(request, 'accountbooks/index_copy.html', context)
    
    
# def order(request):
#     sortkey = 'amount'
#     return redirect('accountbooks:index_copy', sortkey)

def category(request, account_book_pk):
    accountbooks = AccountBook.objects.all()
    accountbooks_by_category = []
    for accountbook in accountbooks:
        a = model_to_dict(accountbook)
        if a[category] == category:
            accountbooks_by_category.append(accountbook)  
    context = {
        'accountbooks':accountbooks_by_category,
    }
    return render(request, 'accountbooks/')
