from channels.db import database_sync_to_async
from mainapp.models import Profile

@database_sync_to_async
def set_online(username):
    Profile.objects.filter(user=username).update(online=True)
    return "OK"

@database_sync_to_async
def set_offline(username):
    Profile.objects.filter(user=username).update(online=False)
    return "OK"