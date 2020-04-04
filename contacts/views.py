from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Contacts

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = Contacts.objects.all().filter(listing_id=listing_id, user_id=user_id)
        if has_contacted:
            messages.error(request, "You have already made an inquiry for this listing")
            return redirect('/listings/'+listing_id)
    
    contact = Contacts(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

    contact.save()

    # Send Email
    send_mail(
        'Property Listing Inquiry for "' + listing + '".',
        'There has been an inquiry for "' + listing + '". Sign into the admin panel for more info',
        'darshit1997d@gmail.com',
        [realtor_email, 'darshit@intricare.net'],
        fail_silently=False
    )

    messages.success(request, "Your Inquiry Successfully Submitted, a Realtor will get back to you soon")

    return redirect('/listings/'+listing_id)
