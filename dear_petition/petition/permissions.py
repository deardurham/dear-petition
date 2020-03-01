import logging
from inspect import getfullargspec
from functools import wraps

logger = logging.getLogger(__name__)


def permit_superuser(user_field_name="user"): #Decorator
    def decorator(func):
        argspec = getfullargspec(func)
        user_index = argspec.args.index(user_field_name)        
        @wraps(func)
        def add_superuser_check(*args,**kwargs):
            try:
                user=args[user_index]
            except IndexError:
                user=kwargs[user]
            return user.is_superuser or func(*args, **kwargs)     
        return add_superuser_check
    return decorator

@permit_superuser()
def is_owner(user, batch):
    return user == batch.user