from django.db import models
from django.contrib.auth.models import User


# List of college names and codes
COLLEGES = (
    ('MAN', 'Mansfield'),
    ('IMP', 'Imperial'),
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


class College(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')

    def __str__(self):
        return self.name


class Challenge(models.Model):
    text = models.CharField(max_length=1000)
    answer = models.CharField(max_length=200)  # TODO foreign key in an Answer model?
    difficulty = models.IntegerField(choices=DIFFICULTIES)
    college = models.ForeignKey(College)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    college = models.ForeignKey(College)

    def __str__(self):
        return self.user.__str__()


class ChallengeCompletion(models.Model):
    user = models.ForeignKey(UserProfile)
    challenge = models.ForeignKey(Challenge)
    time = models.DateField()  # TODO add auto_now?

    def __str__(self):
        return self.user.__str__() + " " + self.challenge.__str__() + " " + self.time


