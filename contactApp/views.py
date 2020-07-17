import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from contactApp.models import AppContacts, AppUser


@csrf_exempt
def sync_user_contacts(request):
    if request.method == 'POST':
        friends = list()
        json_data = json.loads(request.body)
        contacts = json_data['user_contacts']
        response = dict()
        try:
            app_user = AppUser.objects.get(app_user_phone=json_data['user_phone'])
            for contact in contacts:
                if AppUser.objects.filter(app_user_phone=contact).exists():
                    friends.append(contact)
                try:
                    app_contact = AppContacts.objects.get(app_contact_phone=contact)
                    app_contact.app_users.add(app_user)
                except AppContacts.DoesNotExist:
                    app_contact = AppContacts(app_contact_phone=contact)
                    app_contact.save()
                    app_contact.app_users.add(app_user)
            response['count'] = friends.__len__()
            response['friends'] = friends
            response['msg'] = 'Successful'
            return HttpResponse(json.dumps(response), content_type="application/json")
        except AppUser.DoesNotExist:
            response['msg'] = 'Failed: AppUser.DoesNotExist'
            return HttpResponse(json.dumps(response), content_type="application/json")
    return HttpResponse("Failed: request is not POST")


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        phone = json_data['user_phone']

        try:
            AppUser.objects.get(app_user_phone=phone)
        except AppUser.DoesNotExist:
            AppUser(app_user_phone=phone).save()

        notify_users = AppUser.objects.filter(appcontacts__app_contact_phone=phone)
        notify_users_list = list()
        for user in notify_users:
            notify_users_list.append(user.app_user_phone)
        response = dict()
        response["notif"] = notify_users_list
        return HttpResponse(json.dumps(response), content_type="application/json")

    return HttpResponse("Failed: request is not POST")
