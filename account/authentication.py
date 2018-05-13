from django.contrib.auth.models import User

"""Module xac thuc nguoi dung = mang xa hoi"""

class EmailAuthBackend(object):

    """Authenticate using email"""

    def authenticate(self,username = None, password = None):
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return User
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
