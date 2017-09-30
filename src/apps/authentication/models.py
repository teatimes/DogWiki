import os

from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _
from django.contrib.staticfiles.templatetags.staticfiles import static

import datetime


class User(AbstractUser):

    
    def change_image_name(instance, filename): 
        ext = filename.split('.')[-1]
        new_filename = '{}.{}'.format(instance.id, ext)
        return os.path.join('profile_images/', new_filename)

    first_name = models.CharField(_("Fornavn"), max_length=50, null=True)
    last_name = models.CharField(_("Etternavn"), max_length=50, null=True)
    birth_year = models.IntegerField(_("Fødselsår"), blank=True, null=True)
    email = models.CharField(_("Epost"), max_length=50, unique=True, null=True)
    profile_image = models.ImageField(upload_to=change_image_name, default='default/default_profile_image.jpg', null=True)

    competence = models.CharField(_("Kompetanse"), max_length=300,  blank=True, null=True)
    
    REQUIRED_FIELDS = ['email']


    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    def get_age(self):
        this_year = int(datetime.datetime.now().year)

        if this_year is None:
            print("Error: self.this_year is none")

        if self.birth_year is None:
            print("Error: self.birth_year is none")
            return None
        age = this_year - int(self.birth_year)
        print("Age: ", age)

        return this_year - int(self.birth_year)


    def __str__(self):
        return self.get_full_name()


    # Show it in readable form
    def __unicode__(self):
        return self.email


class Follow(models.Model):
    following = models.ForeignKey("User", related_name="following")
    followed = models.ForeignKey("User", related_name="followed")


class Action(models.Model):
    user = models.ForeignKey("User")
    action = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
