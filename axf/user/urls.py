from django.conf.urls import url

from user import views

urlpatterns = [
    # login
    # register
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    # logout
    url(r'^logout/', views.logout, name='logout')

]