from django.urls import path
from .views import  ProfileView, ProfileEditView, UserListView, UserCreateView, UserEditView, UserDetailsView, UserListJsonView

app_name = 'user'

urlpatterns = [
    path('profile',                  (ProfileView.as_view()),                name='profile'),
    path('profile/edit',             (ProfileEditView.as_view()),            name='profile_edit'),
    path('list',                     (UserListView.as_view()),               name='list'),
    path('create',                   (UserCreateView.as_view()),             name='create'),
    path('edit',                     (UserEditView.as_view()),               name='edit'),
    path('details',                  (UserDetailsView.as_view()),            name='details'),
    path('api/users',                (UserListJsonView.as_view()),           name='get_list'),
]



