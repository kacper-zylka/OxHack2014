from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # One-to-one mapping with a django.contrib.auth.models.User object
    user = models.OneToOneField(User)
    # Many-to-one mapping with a College object
    college = models.ForeignKey(College)
    # Many-to-many mapping with Challenge objects
    challenges = models.ManyToManyField(Challenge)


class College(models.Model):
    name = models.CharField(max_length=200, choices=COLLEGES)
    latitude = models.FloatField('Latitude', blank=True, null=True)
    longitude = models.FloatField('Longitude', blank=True, null=True)


class Challenge(models.Model):
    text = models.CharField(max_length=1000)
    answer = models.CharField(max_length=200)  # TODO foreign key in an Answer model?
    difficulty = models.IntegerField(choices=DIFFICULTIES)
    college = models.ForeignKey(College)


# List of college names and codes
COLLEGES = (
    ('MANSFIELD', 'MAN'),
    ('IMPERIAL', 'IMP'),
)


# Difficulty enums and dictionary
EASY = 1
MODERATE = 2
HARD = 3
DIFFICULTIES = (
    (EASY, 'Easy'),
    (MODERATE, 'Moderate'),
    (HARD, 'Hard'),
)
