from __future__ import unicode_literals

from django.db import models

import re
import datetime
import time
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors = []
        if len(form_data["name"]) < 2:
            errors.append("Name must be valid in length")
        if len(form_data["alias"]) < 2:
            errors.append("Alias must be valid in length")
        if not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Please enter a valid Email")
        if len(form_data["password"]) == 0:
            errors.append("Must enter a password")
        if len(form_data["password"]) < 8:
            errors.append("Password must be at least 8 characters long")
        if form_data["password"] != form_data["confirm_pw"]:
            errors.append("Passwords do not match")
        current_time = time.strftime('%Y-%m-%d')
        if current_time <= form_data["birthdate"]:
            errors.append("Birthdate must be in the past")
        if not form_data["birthdate"]:
            errors.append("Must enter birthday")
        


        return errors

    def validate_login(self, form_data):
        errors = []
        if not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Please enter a valid Email")
        if len(form_data["password"]) == 0:
            errors.append("Must enter a password")
        if User.objects.filter(email=form_data["email"]).exists() == False:
            errors.append("No such email exists")

        
        user = User.objects.filter(email=form_data["email"]).first()
        if user is not None:
            if bcrypt.checkpw(form_data["password"].encode(), user.password.encode()) == False:
                errors.append("Email and Password must match")
        if user:
            if bcrypt.checkpw(form_data["password"].encode(), user.password.encode()):
                return {"user": user}

        return {"errors": errors}


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    friends = models.ManyToManyField('self')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

