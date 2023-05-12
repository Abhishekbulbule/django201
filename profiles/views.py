from typing import Any, Dict
from django import http
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, View, UpdateView, FormView
from .forms import FormClass
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from profiles.models import Profile

# Create your views here.
class ProfileDetailView(DetailView):
    http_method_names=["get"]
    template_name='profiles/detail.html'
    model=User
    context_object_name='user'
    slug_field='username'
    slug_url_kwarg='username'
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user=self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts']=Post.objects.filter(author=user).count();
        if self.request.user.is_authenticated:
           context['you_follow'] = Follower.objects.filter(following = user, followed_by = self.request.user).exists
            
            
        context['total_followers']= Follower.objects.filter(following = user).count()
        return context
    
    
class FollowView(LoginRequiredMixin,View):
    http_method_names=['post']
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        print("DATA: ", data)
        if 'action' not in data or 'username' not in data:
            return HttpResponseBadRequest("missing data")
        try:
            other_user = User.objects.get(username = data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("missing User")

        if data['action']=='follow':
            follower, created= Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following = other_user
                )
            except Follower.DoesNotExist:
                follower = None
            if follower:
                follower.delete()
        return JsonResponse({
            'success':True,
            'wording':"Unfollow" if data['action']=='follow' else 'Follow'
        })
         
class AccountProfileView(UpdateView):
    template_name='profiles/profilepicture.html'
    model = Profile
    fields=[
        'image',
        ]
    success_url='/'
        
class AccountDetailView(FormView,UpdateView):
    template_name='profiles/account.html'
    model = User
    fields=[
            'first_name',
            'last_name',
            'email',  
    ]
    
    # form_class = FormClass
    success_url='/'
    
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['follow'] = Follower.objects.filter(
                    following=self.request.user
                    ).count()
        return context