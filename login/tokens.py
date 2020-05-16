from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.six import text_type

'''
This class generates a encrypted token based on the timestamp, user-activity and timestamp for email verification
'''
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )
account_activation_token = TokenGenerator()