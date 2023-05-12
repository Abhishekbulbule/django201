from django.urls import path

from . import views
app_name='profiles'

urlpatterns = [
    path("<str:username>/",views.ProfileDetailView.as_view(), name='detail'),
    path("<str:username>/follow/",views.FollowView.as_view(), name='follow'),
    path("accountDetails/<int:pk>",views.AccountDetailView.as_view(), name='account'),
    path("account/<int:pk>",views.AccountProfileView.as_view(), name='accountProf')
]
