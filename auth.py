#from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
""" 
class Email(BaseBackend):
    #Get user by user_id
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
    # Authentication (email or username)
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username_exact=username) | Q(email_exact=username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
            
            """


