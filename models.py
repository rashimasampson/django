from django.db import models
import re
import bcrypt


# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        # checks the email 
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['first_name'] = "Your name must be at least 2 characters"
        if not email_regex.match(postData['email']):
            errors['email'] = 'Email must be valid'
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Password and Confirm PW do not match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    commment = models.TextField()
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
