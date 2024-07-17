from django.urls import path
from .views import  ProfileView, ProfileEditView, UserListView, UserCreateView, UserEditView, UserListJsonView, UserDetailJsonView, UserToggleStatusView

app_name = 'user'

urlpatterns = [
    path('profile',                  (ProfileView.as_view()),                name='profile'),
    path('profile/edit',             (ProfileEditView.as_view()),            name='profile_edit'),
    path('list',                     (UserListView.as_view()),               name='list'),
    path('create',                   (UserCreateView.as_view()),             name='create'),
    path('edit/<int:user_id>/',      ( UserEditView.as_view()),              name='edit'),
    path('api/users',                (UserListJsonView.as_view()),           name='get_users'),
    path('api/user/',                (UserDetailJsonView.as_view()),         name='get_user'),
    path('api/user/toggle_status/',  (UserToggleStatusView.as_view()),       name='toggle_status_user'),

]



