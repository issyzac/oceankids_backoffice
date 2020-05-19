# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from app.firebase_helper import firebase
from .objects.child import Child
from .objects.parent import Parent
from typing import List
from datetime import datetime, timezone
from .firebase_helper import all_kids_list, all_parents_list, child_by_id

db = firebase.database()


# @login_required(login_url="/login/") => This enforces that the user is logged in
def index(request):
    return render(request, "index.html")


def kid_details(request, child_id):
    tokenId = request.session.get('uid')
    child = child_by_id(tokenId, child_id)
    f_name = child.setdefault("firstName", "n/a")
    l_name = child.setdefault("lastName", "n/a")

    print(child.setdefault("firstName", "n/a"))

    context = {
        "child": {
            "name": f_name+" "+l_name,
            "class": "Primary",
            "child_id": child_id
        }
    }
    return render(request, "kid-details.html", context)

# @login_required(login_url="/login/") => Enforces that the user should be logged in to view all the rest of the pages
def pages(request):

    tokenId = request.session.get('uid')

    context = {}

    if 'uid' in request.session:
        try:
            # All resource paths end in .html.
            # Pick out the html file name from the url. And load that template.
            load_template = request.path.split('/')[-1]

            if str(load_template) == 'all-kids.html':
                all_kids = all_kids_list(tokenId)
                children = []
                for key, val in all_kids.items():
                    # fire_id = val.setdefault('id', "n/a") #This child Id
                    parent_n_a = "{'id': 'n/a', 'relationship': 'n/a'}"
                    for parent in val.setdefault('parents', parent_n_a):
                        parent_id = parent['id']
                        # childs_parent = db.child('parents').child(parent_id).get(tokenId).val()
                        # print (childs_parent)

                    first_name = val.setdefault('firstName', "n/a")
                    last_name = val.setdefault('lastName', "n/a")
                    gender = val.setdefault('gender', "n/a")
                    dob = datetime.fromtimestamp((val.setdefault('dob', 1281082010992) / 1000), timezone.utc)
                    dob_formated = dob.strftime('%d-%b-%Y')
                    child_firebase_id = val.setdefault('id', 'n/a')
                    new_child = Child(first_name, last_name, gender, str(dob_formated), child_firebase_id)
                    children.append(new_child)
                context = {
                    "kids_list": children,
                }
            elif str(load_template) == 'all-parents.html':
                p_list = all_parents_list(tokenId)
                parents_list = []
                for k, v in p_list.items():
                    p_id = v.setdefault('id', 'n/a')
                    p_first_name = v.setdefault('firstName', "n/a")
                    p_last_name = v.setdefault('lastName', "n/a")
                    p_email = v.setdefault('email', "n/a")
                    p_address = v.setdefault('address', "n/a")
                    p_phone_number = v.setdefault('phoneNumber', "n/a")
                    p_relationship_to_child = v.setdefault('relationshipToChild', "n/a")
                    current_parent = Parent(p_first_name, p_last_name, p_email, p_address, p_id, p_phone_number,
                                            p_relationship_to_child)
                    parents_list.append(current_parent)
                context = {
                    "all_parents": parents_list,
                }
            elif str(load_template) == 'kid-details.html':
                kid_id = request.GET["kid_uid"]
                kid = "Jamal Makamba"
                context = {
                    "kid": kid,
                }
            else:
                context = {

                }

            print("Template is "+str(load_template))
            html_template = loader.get_template(load_template)
            return HttpResponse(html_template.render(context, request))
        
        except template.TemplateDoesNotExist:

            html_template = loader.get_template('error-404.html')
            return HttpResponse(html_template.render(context, request))

        except:
            html_template = loader.get_template('error-500.html')
            return HttpResponse(html_template.render(context, request))

    else:
        return redirect("/login/")
