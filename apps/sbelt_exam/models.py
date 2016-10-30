from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(email = post['email'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:

                return user
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name = post['name'], alias = post['alias'], email = post['email'],birthdate = post['birthdate'], password = encrypted_password )

    def validate(self, post):
        errors = []
        today = date.today()

        if len(post['name']) == 0:
            errors.append("Name is required")
        elif len(post['name']) < 2:
            errors.append("Name is too short")

        if len(post['alias']) == 0:
            errors.append("alias is required")

        if len(post['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Please enter a valid email")

        if len(post['password']) == 0:
            errors.append("must enter a password")
        elif len(post['password']) < 8:
            errors.append("password must have at least 8 characters")
        elif post['password'] != post['confirm_pass']:
            errors.append("password and confirmation must match")

        # if not post['birthdate']
        #     errors.append("Birthdate Field cannot be empty")
        #     try:
        #         travel_from = datetime.strptime(post['travel_from'], '%Y-%m-%d')
        #         if travel_from.date() < today:
        #             errors.append("From Date cannot be in the past")
        #     except:
        #         errors.append("Please enter a valid date for the From Date")

        # if len(User.objects.filter(email = post['email'])) > 0 :
        #     errors.append("Email address is unavailable!")

        return errors

class QuoteManager(models.Manager):
    def v_post(self,post):
        errors = []

        if len(post['quoted_by']) == 0:
            errors.append("Name is required")
        elif len(post['quoted_by']) < 3:
            errors.append("Name is too short")

        if len(post['quote']) == 0:
            errors.append("Quote is required")
        elif len(post['quote']) < 10:
            errors.append("Quote is too short")
        return errors

class User(models.Model):
    name = models.CharField(max_length = 45)
    alias = models.CharField(max_length = 45)
    email = models.EmailField(max_length= 60)
    birthdate = models.DateField()
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quotes(models.Model):
    user = models.ForeignKey(User)
    quoted_by = models.CharField(max_length = 30)
    quote = models.TextField(max_length = 1000)
    writer = models.ManyToManyField(User, related_name= "other_writers")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
