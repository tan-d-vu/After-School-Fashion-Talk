from django.contrib.auth.models import User
from asft_core.models import Profile
from difflib import SequenceMatcher
from random import randint

def __designer_list_conversion(designer_list):
    # Converting string of int to list of int (index of designer in brand_set)
    designer_list = str(designer_list)[1:]
    designer_list = designer_list[:-1]
    designer_list = list(designer_list.split(", "))
    for i in range(0, len(designer_list)):
        designer_list[i]=int(designer_list[i])
    return designer_list

def __short_list_compare(current_fav_designers, profile_fav_designers):
    # To compare list of less than 10 designers
    common_designers = []
    for designer in profile_fav_designers:
        if designer in current_fav_designers:
            common_designers.append(designer)

    if len(common_designers) >= round(len(current_fav_designers)/0.5):
        return "Matched"
    else:
        return "Not Matched"

def get_random_suggestions():
    suggestions = []
    suggestion_count = 0
    count = Profile.objects.count()
    
    if count <= 10:
        for i in range(0, count-1):
            suggestions.append(Profile.objects.all()[i])

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
    current_fav_designers = __designer_list_conversion(current_fav_designers)
    
    all_profiles = Profile.objects.all()

    # If user's fav designers list is short (less than 10), use __short_list_compare__
    if len(current_fav_designers) <= 10:
        for profile in all_profiles:
            if profile.user != user:
                profile_fav_designers = profile.favorite_designers
                profile_fav_designers = __designer_list_conversion(profile_fav_designers)
               
                if __short_list_compare(current_fav_designers, profile_fav_designers)=="Matched":
                    suggestions.append(profile)
                    suggestion_count += 1
                
                # Getting 10 suggestions = done
                if suggestion_count == 10:
                    break

    else:
        for profile in all_profiles:
            if profile.user != user:
                profile_fav_designers = profile.favorite_designers
                profile_fav_designers = __designer_list_conversion(profile_fav_designers)
                
                if len(profile_fav_designers) <= 10:
                    if __short_list_compare(current_fav_designers, profile_fav_designers)=="Matched":
                        suggestions.append(profile)
                        suggestion_count += 1
                else:
                    similarity = SequenceMatcher(None, current_fav_designers, profile_fav_designers)
                    if similarity.ratio() > 0.03:
                        suggestions.append(profile)
                        suggestion_count += 1

                if suggestion_count == 10:
                    break

    return suggestions
