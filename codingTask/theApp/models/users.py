from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import Permission


class RegisteredUserManager(BaseUserManager) :
    def create_user(self, name, phone_number, password = None) :
        if not name :
            raise ValueError('Users must have a name')
        
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(phone_number = phone_number)

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, phone_number, name, password) :
        user = self.create_user(phone_number = phone_number, name = name, password = password)

        user.is_superuser = True
        user.save(using=self._db)
        return user

class RegisteredUser(AbstractBaseUser, PermissionsMixin) :
    name = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 10, unique = True, validators = [MinLengthValidator(10), MaxLengthValidator(10)])
    email = models.EmailField(null = True, blank = True)

    objects = RegisteredUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name = 'user permissions',
        blank = True,
        related_name = 'registered_user_permissions',
        help_text = 'Specific permissions for this user.',
        related_query_name = 'registered_user'
    )

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_superuser
    

class Contact(models.Model) :
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 10, validators = [MinLengthValidator(10), MaxLengthValidator(10)])

    users = models.ManyToManyField('registeredUser', related_name = 'contacts', blank = True)

    def __str__(self) :
        return self.name
