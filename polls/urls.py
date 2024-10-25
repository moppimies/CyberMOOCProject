from django.urls import path

from .views import index, detail, results, vote, login_view, logout_view

app_name = 'polls'

urlpatterns = [
    path('',index,name='index'),
    path('/logout', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('<int:question_id>/', detail, name='detail'),
    path('<int:question_id>/results', results, name='results'),
    path('<int:question_id>/vote', vote, name='vote'),
]