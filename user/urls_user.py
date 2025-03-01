from django.urls import path
from .views_user import  ProfileView, ProfileEditView, UserListView, UserListJsonView, UserCreateView, UserDetailJsonView, UserEditView, UserToggleStatusView, UserDeleteView

app_name = 'user'

urlpatterns = [
    path('profile',                  (ProfileView.as_view()),                name='profile'),
    path('profile/edit',             (ProfileEditView.as_view()),            name='profile_edit'),
    
    path('list',                     (UserListView.as_view()),               name='list'),
    path('api/users',                (UserListJsonView.as_view()),           name='get_users'),
    path('create',                   (UserCreateView.as_view()),             name='create'),
    path('api/user/',                (UserDetailJsonView.as_view()),         name='get_user'),
    path('<int:user_id>/edit/',      (UserEditView.as_view()),               name='edit'),
    path('api/user/toggle_status/',  (UserToggleStatusView.as_view()),       name='toggle_status_user'),
    path('api/user/delete/',         (UserDeleteView.as_view()),             name='delete_user'),

]



