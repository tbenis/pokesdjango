from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime
from datetime import date
# Create your models here.

lettersOnly = re.compile(r'^[a-zA-Z]*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class userManager(models.Manager):

    def rValidate(self, postData):
        errors = []
        flag = False
        if not postData['name']:
            errors.append('Name field must be filled out!.')
            flag = True
        if len(postData['name']) < 3:
            errors.append('First name must be at least 3 characters.')
            flag = True
        if any(char.isdigit() for char in postData['name']):
            errors.append('Name can only contain letters.')
            flag = True
        if not postData['alias']:
            errors.append('Alias field must be filled out!')
            flag = True
        if len(postData['alias']) < 3:
            errors.append('Alias must be at least 3 characters.')
            flag = True
        if not lettersOnly.match(postData['alias']):
            errors.append('alias can only contain letters.')
            flag = True
        if not emailRegex.match(postData['email']):
            errors.append('Email address was not valid.')
            flag = True
        if not postData['email']:
            errors.append('Email must not be blank.')
            flag = True
        if not postData['password']:
            errors.append('Password must not be blank.')
            flag = True
        if postData['password'] != postData['cPassword']:
            errors.append('Passwords must match.')
            flag = True
        if len(postData['password']) < 3:
            errors.append('Password must be at least 8 characters long.')
            flag = True
        if not postData['dob']:
            errors.append('You must enter your date of birth')
            flag = True
        elif postData['dob'] >= postData['datenow']:
            errors.append('Your date of birth must be before today')
            flag = True
        if not flag:
            # Encrypt password
            hashedPw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            # Save to database
            if User.objects.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password=hashedPw,
                dateOfBirth=postData['dob']
                ):
                print "Reg success"
                user = User.objects.last()
                return(flag, user)
            else:
                print "Reg failed"
        return(flag, errors)


    def lValidate(self, postData):
        user = User.objects.get(email=postData['email'])
        password = postData['password'].encode()
        hashed = user.password.encode()

        if bcrypt.hashpw(password, hashed) == hashed:
            return (True, user)
        else:
            return (False, "Login credentials are invalid.")


class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45, )
    password = models.CharField(max_length=255)
    dateOfBirth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poker")
    poked = models.ForeignKey(User, related_name="poked")
    counter = models.IntegerField(blank=False, default=0, null=True)
    total = models.IntegerField(blank=False, default=0, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
