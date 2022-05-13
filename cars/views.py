from ast import keyword
from importlib import import_module
from django.shortcuts import render, get_object_or_404
from .models import Car
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def cars(request):
    cars = Car.objects.all()

    # pagination
    # cars replaced by pages cars in the context
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

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

    # context
    data = {
        'cars': paged_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_search': body_search,
    }
    return render(request, 'cars/cars.html', data)


def car_detail(request, id):
    car = get_object_or_404(Car, pk=id)

    # add to context
    data = {
        'car': car,
    }
    return render(request, 'cars/car_detail.html', data)


def search(request):
    cars = Car.objects.all()

    # check for a search term, search box
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        # if search term is not blank
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    # Multi-field search:
    if 'model' in request.GET:
        model = request.GET['model']

        if model:
            cars = cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']

        if city:
            cars = cars.filter(city__iexact=city)
    if 'year' in request.GET:
        year = request.GET['year']

        if year:
            cars = cars.filter(year__exact=year)
    if 'body_style' in request.GET:
        body_style = request.GET['body_style']

        if body_style:
            cars = cars.filter(body_style__iexact=body_style)
    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']

        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)
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

    data = {
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_search': body_search,
    }
    return render(request, 'cars/search.html', data)
