from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*role_names):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            user_roles = {r.name for r in current_user.roles}
            if not user_roles.intersection(set(role_names)):
                abort(403)
            return fn(*args, **kwargs)
        return inner
    return wrapper