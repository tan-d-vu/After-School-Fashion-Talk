from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.utils import timezone

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from asft_core.models import Profile, Message
from asft_core.forms import ProfileForm, MessageForm
from .untils import get_friend_suggestions, get_random_suggestions, designer_list_conversion, index_conversion
# Create your views here.

# Profile Update


def home(request):
    return render(request, 'asft_templates/home.html', {})

@login_required()
def friend_suggestions_view(request, username):
    """ Show either friend suggestions from common designers or randomly """
    random_suggestions = []
    suggestions = []
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')
        
    suggestions = get_friend_suggestions(user)

    if len(suggestions)==0:
        random_suggestions = get_random_suggestions(user.username)
        

    return render(request, 'asft_templates/friend_suggestions.html', {'suggestions' : suggestions,
                    'random_suggestions': random_suggestions})


@login_required()
def profile_update(request, username):
    """ Update profile info """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')

    profile = Profile.objects.get_or_create(user=user)[0]

    profile_form = ProfileForm({'picture': profile.picture,
                                'bio': profile.bio, 'fav_designer': profile.favorite_designers})

    designer_list = designer_list_conversion(profile.favorite_designers)
    designer_list = index_conversion(designer_list)

    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(profile_form.errors)

    return render(request, 'asft_templates/profile_create.html', {'form': profile_form, 
                    'current_user': user, 'designer_list': designer_list })

class ProfileView(LoginRequiredMixin, DetailView):
    """ Viewing profile infomation """
    template_name = 'asft_templates/profile_view.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        designer_list = designer_list_conversion(self.object.favorite_designers)
        designer_list = index_conversion(designer_list)
        context['designer_list'] = designer_list

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Sending Message from this view """
    template_name = 'asft_templates/message_create.html'
    form_class = MessageForm
    success_url = reverse_lazy('home')

    # Fill sender, reciever, created_at if message is valid
    def form_valid(self, form):
        self.reciever = get_object_or_404(
            User, username=self.kwargs['username'])

        self.sender = self.request.user
        self.created_at = timezone.now()

        form.instance.reciever = self.reciever
        form.instance.sender = self.sender
        form.instance.created_at = self.created_at
        return super().form_valid(form)

class InboxView(LoginRequiredMixin, ListView):
    """ List view of all incoming messages """
    template_name = 'asft_templates/inbox.html'
    context_object_name = 'incoming_messages'


    def get_queryset(self):
        reciever = get_object_or_404(User, username = self.kwargs['username'])
        self.message = Message.objects.filter(reciever = reciever.id)
        return Message.objects.filter(reciever = reciever.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = get_object_or_404(User, username = self.kwargs['username'])
        context['current_user']= current_user
        return context

class SentMessageView(LoginRequiredMixin, ListView):
    """ List view of all sent messages """
    template_name = 'asft_templates/sent.html'
    context_object_name = 'sent_messages'


    def get_queryset(self):
        sender = get_object_or_404(User, username = self.kwargs['username'])
        self.message = Message.objects.filter(sender = sender.id)
        return Message.objects.filter(sender = sender.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = get_object_or_404(User, username = self.kwargs['username'])
        context['current_user']= current_user
        return context

