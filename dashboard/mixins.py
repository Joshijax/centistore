# mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    View mixin that only allows admin users.
    """

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
