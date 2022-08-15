from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, name=None, is_staff=False, is_superuser=False, is_active=True):
        if not phone:
            raise ValueError('کاربر باید دارای شماره موبایل باشد')
        if not password:
            raise ValueError('کاربر باید دارای رمز عبور باشد')

        user = self.model(phone = phone, name = name)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()

        return user

    def create_staffuser(self, phone, password=None):
        return self.create_user(
            phone = phone,
            password = password,
            is_staff=True
        )

    def create_superuser(self, phone, password=None):
        return self.create_user(
            phone = phone,
            password = password,
            is_staff = True,
            is_superuser = True
        )