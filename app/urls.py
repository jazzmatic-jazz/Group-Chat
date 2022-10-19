from django.urls import  path
from .views import index

urlpatterns = [
    # path('', index), #this url is for the buddies group name which is static
    path('<str:group_name>/', index), #this is for the dynamic group name
]
