
def login_required(auth_manager):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = auth_manager.get_current_user()
            if user is None:
                print("You must be logged in to run this command.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(auth_manager):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = auth_manager.get_current_user()
            if user is None:
                print("You must be logged in to run this command.")
                return
            if user.role != "admin":
                print("You do not have permission to run this command.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator