from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
# Create your models here.

class Profile(models.Model):
    """ UserProfile Model """
    # One(Profile) to one(User) relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(upload_to='media_pfp', default='default-avatar_qdntfa.png')
    bio = models.TextField(blank=True)
    favorite_designers= models.TextField(blank=False)

    # String representation
    def __str__(self):
        return self.user.username

    # self.username is User's username
    def save(self, *args, **kwargs):
        self.username = self.user.username
        super(Profile, self).save(*args, **kwargs)

class Message(models.Model):
    """ Message Model """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    content = models.TextField(blank=False, validators=[MinLengthValidator(500)])
    created_at = models.DateTimeField(editable=False)

    def __str__(self):
        return str(self.sender.username + 'to' + self.reciever.username)