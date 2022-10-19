from unicodedata import name
from django.shortcuts import render
from .models import Chat, Group
# STatic group name
# def index(request):
#     return render(request, 'app/index.html')

# Dynamic group name
def index(request, group_name):
    print('Group Name:', group_name)
    group = Group.objects.filter(name=group_name).first()
    chats = []

    if group: 
        # if it exist then we show the chats of the group
        chats = Chat.objects.filter(group=group)

    else:
    # To save the group name from the url if does not exists
        group = Group(name=group_name)
        group.save()
        
    return render(request,
         'app/index.html', 
        {
            'groupname': group_name, 
            'chats': chats
        })