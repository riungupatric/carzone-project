from django.shortcuts import render, redirect
from contacts.models import Contact
from django.contrib import messages
from .models import Contact
from django.contrib.auth.models import User
from django.core.mail import send_mail


def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        car_title = request.POST['car_title']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        phone = request.POST['phone']
        message = request.POST['message']

        # prevent logged in users from making
        # multiple enquiries on the same car
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(
                user_id=user_id, car_id=car_id)
            if has_contacted:
                messages.error(
                    request, "You have already enquired about this car. Please wait!")
                return redirect('car/'+car_id)

        # save inquiries
        contact = Contact(car_id=car_id, user_id=user_id, first_name=first_name, last_name=last_name, email=email,
                          car_title=car_title, customer_need=customer_need, city=city, state=state, phone=phone, message=message)

        # send email before saving
        # get admin infor
        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            'New Car Inquiry',
            'You have a new car enquiry for '+car_title+'. Please login for more info.',
            'from@example.com',
            [admin_email, 'kaimenyiriungu@gmail.com'],
            fail_silently=False,
        )
        contact.save()
        messages.success(request, "Inquiry submitted successfully!")
        return redirect('car/'+car_id)
