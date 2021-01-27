import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "after_school_fashion_talk.settings")

import django
django.setup()

from django.contrib.auth.models import User
from asft_core.models import Profile, Message
from django.utils import timezone
import random

def populate():
    message = """You can engage your readers right from the start through a number of tried-and-true ways. Posing a question, defining the key term, giving a brief anecdote, using a playful joke or emotional appeal, or pulling out an interesting fact are just a few approaches you can take. Use imagery, details, and sensory information to connect with the reader if you can. The key is to add intrigue along with just enough information so your readers want to find out more. 

One way to do this is to come up with a brilliant opening line. Even the most mundane topics have aspects interesting enough to write about; otherwise, you wouldn't be writing about them, right?
"""
    username_prefix = "sampleuser"
    password = "111111111"

    for x in range(0, 30):
        username = username_prefix + str(x)
        new_user = add_user(username, password)
        add_profile(new_user)

    all_users = User.objects.all()
    for sender in all_users:
        for reciever in all_users:
            if sender != reciever:
                send_message(sender, reciever, message)

def add_profile(user):
    designer_count = random.randrange(5, 30)
    favorite_designers = []

    for i in range(0, designer_count):
        designer_index = random.randrange(1,50)
        if designer_index not in favorite_designers:
            favorite_designers.append(designer_index)
    
    new_profile = Profile.objects.get_or_create(user=user, favorite_designers=str(favorite_designers))
    return new_profile



def add_user(username, password):
    new_user = User.objects.create_user(username, '', password)
    new_user.save()
    return new_user


def send_message(sender, reciever, message):
    message = Message.objects.get_or_create(sender=sender, reciever=reciever,
                                            content=message, created_at=timezone.now())[0]
    message.save()
    return message

if __name__ == '__main__':
    print("Populating the database...")
    populate()
    print("Finished.")