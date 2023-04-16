from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from . import models
from .forms import UserForm, beDriverForm, SearchForm, UserRequestForm, UserSearchForm, EditCarForm
from .forms import RegisterForm
from .forms import EditForm
from .models import Ride


# Create your views here.
def index(request):
    if request.session.get('is_login') != True:
        return render(request, 'rideservice/index.html', locals())
    else:

        username = request.session.get('user_name')
        my = models.RideUser.objects.get(name=username)
        return render(request, 'rideservice/index.html',locals())


def login(request):


    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "All fields must be filled in!!!!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.RideUser.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/ride/index/')
                else:
                    message = "Incorrect Password！"
            except:
                message = "User name doesn't exist！"
        return render(request, 'rideservice/login.html', locals())

    login_form = UserForm()
    return render(request, 'rideservice/login.html', locals())


def register(request):


    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "All fields must be filled in!!!!"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            repeat_password = register_form.cleaned_data['repeat_password']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if repeat_password != password:
                message = "The two entered passwords do not match!!"
                return render(request, 'rideservice/register.html', locals())

            same_email_user = models.RideUser.objects.filter(email=email)
            if same_email_user:
                message = "The email address has been occupied,please change one!!"
                return render(request, 'rideservice/register.html', locals())

            new_user = models.RideUser.objects.create()
            new_user.name = username
            new_user.password = password
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('/ride/login/')
    register_form = RegisterForm()
    return render(request, 'rideservice/register.html', locals())


def logout(request):


    request.session.flush()
    return redirect('/ride/index/')

def my(request):

    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.method == "POST":
        if 'bepure' in request.POST:
            my.is_driver = False
            my.save()
            car = models.Vehicle.objects.get(owner=my)
            car.delete()
            ride = models.Ride.objects.filter(driver=my)
            ride.delete()
            return redirect('/ride/index/')
        elif 'confirmed_list' in request.POST:
            return redirect('/ride/d_list/')
        elif 'd_search_list' in request.POST:
            return redirect('/ride/d_search/')

        elif 'submit_ride' in request.POST:
            return redirect('/ride/riderequest/')
        elif 'u_list' in request.POST:
            return redirect('/ride/u_list/')
        else:
            return redirect('/ride/u_search/')


    return render(request,'rideservice/my.html',{'my':my})


def edit(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.method == "POST":
        edit_form = EditForm(request.POST,instance=my)
        message = "All fields must be filled in!!!!"


        if edit_form.is_valid():
            username = edit_form.cleaned_data['name']
            email = edit_form.cleaned_data['email']
            sex = edit_form.cleaned_data['sex']
            my.name = username
            my.email = email
            my.sex = sex
            my.save()
            request.session['user_name'] = username
            return redirect('/ride/index/')
    else:


        edit = EditForm(instance = my)
        return render(request, 'rideservice/edit.html', {'edit': edit,'my':my})

def editcar(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    car = my.vehicle
    if request.method == "POST":
        edit_form = EditCarForm(request.POST,instance=car)
        message = "All fields must be filled in!!!!"


        if edit_form.is_valid():
            type = edit_form.cleaned_data['type']
            license_num = edit_form.cleaned_data['license_num']
            capacity = edit_form.cleaned_data['capacity']
            otherInfo = edit_form.cleaned_data['otherInfo']
            car.type=type
            car.license_num=license_num
            car.capacity=capacity
            car.otherInfo=otherInfo
            car.save()
            return redirect('/ride/index/')
    else:


        edit = EditCarForm(instance = car)
        return render(request, 'rideservice/editcar.html', {'edit': edit,'my':my})

def bedriver(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)

    if my.is_driver==True:
        messages.error(request, 'You have been Driver,please go to index')
        return redirect('/ride/index')


    if request.method == "POST":
        be_drive = beDriverForm(request.POST)


        if be_drive.is_valid():

            type = be_drive.cleaned_data['type']
            license_num = be_drive.cleaned_data['license_num']
            capacity = be_drive.cleaned_data['capacity']
            otherInfor = be_drive.cleaned_data['otherInfo']

            car = models.Vehicle.objects.create(owner=my)


            car.owner = my
            car.type = type
            car.license_num = license_num
            car.capacity = capacity
            car.otherInfo = otherInfor
            car.save()

            my.is_driver = True
            my.save()

            #be_drive.save()
            return redirect('/ride/index/')


    else:

        be_drive = beDriverForm()
        return render(request,'rideservice/bedriver.html',{'be_drive':be_drive})


def d_viewlist(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    d_list = list(models.Ride.objects.filter(driver=my, status='confirmed').all())

    return render(request,'rideservice/dlist.html',{'d_list':d_list})

def d_viewdetail(request,ride_id):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    detail = models.Ride.objects.get(id = ride_id)

    return render(request,'rideservice/dlist_detail.html',{'d_detail':detail})

def d_viewcomplete(request,ride_id):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    detail = models.Ride.objects.get(id = ride_id)
    detail.status = 'completed'
    detail.save()

    return redirect('/ride/d_list/')

def d_search(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            capacity = search_form.cleaned_data['capacity']
            type = search_form.cleaned_data['type']
            special_info = search_form.cleaned_data['otherInfo']

            d_list = list()

            openRide = models.Ride.objects.filter(status='open').exclude(owner=my)
            openlist = list(openRide)
            for rideitem in openlist:
                if rideitem.capacity <= capacity - 1:
                    if(rideitem.special_request=='' or rideitem.special_request == special_info):
                        if(rideitem.vehicle_type == '' or rideitem.vehicle_type == type):
                            d_list.append(rideitem)

            return render(request, 'rideservice/dlist.html', {'d_list': d_list})





    search_form = SearchForm(instance = my.vehicle)
    return render(request, 'rideservice/dsearch.html', locals())

def d_viewconfirm(request,ride_id):


    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    detail = models.Ride.objects.get(id = ride_id)
    detail.status = 'confirmed'
    detail.driver = my
    detail.save()

    email_list = []
    user = detail.owner
    sharer = detail.sharer.all()
    email_list.append(user.email)
    for s in sharer:
        email_list.append(s.email)
    send_mail(
        'Your ride is confirmed',
        'Here is the message.',
        'ece568jx@outlook.com',
        email_list,
        fail_silently=False,
    )

    return redirect('/ride/d_list/')


def riderequest(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.method == "POST":
        UR_form = UserRequestForm(request.POST)

        if UR_form.is_valid():


            ride = models.Ride.objects.create(owner=my)
            ride.destination = UR_form.cleaned_data['destination']
            ride.arrival_time = UR_form.cleaned_data['arrival_time']
            ride.capacity = UR_form.cleaned_data['capacity']
            ride.vehicle_type = UR_form.cleaned_data['vehicle_type']
            ride.special_request = UR_form.cleaned_data['special_request']
            ride.is_Share = UR_form.cleaned_data['is_Share']

            if ride.arrival_time < timezone.now():
                message = "Invalid arrival time!!"
                return render(request, 'rideservice/riderequest.html', locals())

            ride.status = 'open'
            ride.save()
            return redirect('/ride/index/')
    else:
        UR_form = UserRequestForm()
    return render(request, "rideservice/riderequest.html", locals())


def u_viewlist(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    u_owner_list = list(models.Ride.objects.filter(owner=my).all())
    u_sharer_list = list(models.Ride.objects.filter(sharer=my).all())

    return render(request, "rideservice/ulist.html", context={'u_owner_list': u_owner_list, 'u_sharer_list': u_sharer_list})


def u_viewdetail(request, ride_id):
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    detail = models.Ride.objects.get(id=ride_id)
    is_owner = False
    if detail.owner == my:
        is_owner = True
    return render(request, 'rideservice/ulist_detail.html', {'u_detail': detail,'is_owner':is_owner})


def u_edit(request, ride_id):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    ride = models.Ride.objects.get(id=ride_id)


    if request.method == "POST":
        ride_form = UserRequestForm(request.POST)
        if ride_form.is_valid():
            ride.destination = ride_form.cleaned_data['destination']
            ride.arrival_time = ride_form.cleaned_data['arrival_time']
            ride.capacity = ride_form.cleaned_data['capacity']
            ride.vehicle_type = ride_form.cleaned_data['vehicle_type']
            ride.special_request = ride_form.cleaned_data['special_request']
            ride.is_Share = ride_form.cleaned_data['is_Share']
            ride.save()
            return redirect('/ride/u_list/')
    else:

        ride_form = UserRequestForm(instance=ride)

        return render(request, "rideservice/u_edit.html", {'ride_form': ride_form,'ride':ride})


def u_search(request):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)
    if request.method == "POST":
        US_form = UserSearchForm(request.POST)
        if US_form.is_valid():
            destination = US_form.cleaned_data['destination']
            early_time = US_form.cleaned_data['early_time']
            late_time = US_form.cleaned_data['late_time']
            number_you = US_form.cleaned_data['number_you']
            temp = models.Ride.objects.filter(status='open', is_Share=True, destination=destination,
                                                     arrival_time__range=(early_time, late_time),).all()


            u_list = list(temp.exclude(owner=my))



            return render(request, 'rideservice/searchlist.html', {'u_list': u_list,'number_you':number_you})
    US_form = UserSearchForm()
    return render(request, 'rideservice/usearch.html', locals())


def join(request, ride_id,number_you):
    if request.session.get('is_login') != True:
        return redirect('/ride/index/')

    ride = get_object_or_404(Ride, id=ride_id)
    username = request.session.get('user_name')
    my = models.RideUser.objects.get(name=username)

    ride.sharer.add(my)
    ride.capacity += int(number_you)
    ride.save()

    return redirect('/ride/index/')
