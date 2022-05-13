from django.shortcuts import render, redirect
from pages.models import Team
from cars.models import Car
from django.core.mail import send_mail
from django.contrib import messages


def home(request):
    team = Team.objects.all()
    featured_cars = Car.objects.filter(is_featured=True)
    cars = Car.objects.all()
    # Multi-search fields
    # the meta ordering doesn't apply here, order_by() must be used
    # return unique values only
    model_search = Car.objects.order_by(
        'model').values_list('model', flat=True).distinct()
    city_search = Car.objects.order_by(
        'city').values_list('city', flat=True).distinct()
    year_search = Car.objects.order_by(
        '-year').values_list('year', flat=True).distinct()
    body_search = Car.objects.order_by('body_style').values_list(
        'body_style', flat=True).distinct()
    # search_fields = Car.objects.values('model', 'city', 'year', 'body_style')
    # * model_search, city_search, year_search, body_search are lists, NOT objects
    # context
    data = {
        'team': team,
        'featured_cars': featured_cars,
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_search': body_search,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    team = Team.objects.all()
    # context
    context = {
        'team':  team,
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']

        # send email
        message_body = 'Name : ' + name + '. \n Email : ' + email + \
            '. \n Phone : ' + phone+'.\n Message : ' + message
        send_mail(
            subject,
            message_body,
            'info@carzone.com',
            ['riungufx@gmail.com', 'kaimenyiriungu@gmail.com'],
            fail_silently=False,
        )
        messages.success(
            request, "Thank you for contacting us. Your message has been received successfully!")
        return redirect('contact')
    return render(request, 'pages/contact.html')


def services(request):
    return render(request, 'pages/services.html')
