from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
import datetime

# mengatur permintaan HTTP dan mengembalikan tampilan yang sesuai
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'all':
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)

    # dictionary data
    context = {
        'npm' : '2406346693',
        'name' : 'Waldan Rafid',
        'class' : 'PBP F',
        'news_list' : news_list,
        'last_login' : request.COOKIES.get('last_login', 'Never'),
    }
    # me-request render tampilan pada template "main.html" dengan data
    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        news_entry =  form.save(commit = False) #commit false agar django tidak langsung menyimpan objek hasil form ke database (punya kesempatan untuk modif sblm disimpan)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "edit_news.html", context)

def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {'news': news}
    return render(request, "news_detail.html", context)



# serialize untuk mengubah format model sebelumnya menjadi format yang dibutuhkan (XML atau JSON)
def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml",  news_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, news_id):
    try:
        news_item = News.objects.filter(pk=news_id)
        xml_data = serializers.serialize("json", [news_item])
        return HttpResponse(xml_data, content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)
    
#fungsi REGISTER, LOGIN, LOGOUT
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

