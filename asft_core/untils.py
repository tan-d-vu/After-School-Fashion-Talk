from django.contrib.auth.models import User
from asft_core.models import Profile
from random import randint
from . import brand_set

def designer_list_conversion(designer_list):
    # Converting string of int to list of int (index of designer in brand_set)
    if designer_list:
        designer_list = str(designer_list)[1:]
        designer_list = designer_list[:-1]
        designer_list = list(designer_list.split(", "))
        for i in range(0, len(designer_list)):
            designer_list[i]=int(designer_list[i])
    
    return designer_list
    

def index_conversion(designer_list):
    # From list of index to actual desginer names
    i = 0
    for index in designer_list:
        designer_list[i] = brand_set.brand_choice[index]
        i +=1
    
    return designer_list

def get_random_suggestions(username):
    # Get 10 random sugesstions
    suggestions = []
    suggestion_count = 0
    count = Profile.objects.count()
    
    # If there are less than 10 users, recommend everyone 
    if count <= 10:
        for i in range(0, count-1):
            suggestion = Profile.objects.all()[i]
            if suggestion.username != username:
                suggestions.append(suggestion)

    # Get 10 random suggestions
    else:
        while suggestion_count <= 10:
            suggestion = Profile.objects.all()[randint(0, count-1)]
            if suggestion not in suggestions:
                suggestions.append(suggestion)
                suggestion_count+=1

    return suggestions

def get_friend_suggestions(user):
    suggestions = []
    
    suggestion_count = 0

    # Getting arg user's fav designers
    current_fav_designers =  Profile.objects.get(username=user.username).favorite_designers
    current_fav_designers = designer_list_conversion(current_fav_designers)
    
    current_fav_designers_count = len(current_fav_designers)
    # Getting all profiles, loop through to find matches
    all_profiles = Profile.objects.all()

    for profile in all_profiles:
        if profile.user != user:
            # New suggestion+ common designer for every user
            suggestion = []
            common_designer = []

            # Getting current profile's fav designers    
            profile_fav_designers = profile.favorite_designers
            profile_fav_designers = designer_list_conversion(profile_fav_designers)
        
            # Compare to arg user's fav designers
            for designer in current_fav_designers:
                if designer in profile_fav_designers:
                    # Add the common designer
                    common_designer.append(designer)

            # Add to suggestion if the common fav designers is 40% or more
            if len(common_designer)/current_fav_designers_count >= 0.4:
                common_designer = index_conversion(common_designer)
                # Add to suggestion list
                suggestion.append(profile)
                suggestion.append(common_designer)
                
                # Add the suggestion list to suggestions
                suggestions.append(suggestion)
                suggestion_count += 1
            
            if suggestion_count == 10:
                break

    return suggestions
