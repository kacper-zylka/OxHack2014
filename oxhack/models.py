from django.db import models
from django.contrib.auth.models import User


# List of college names and codes
COLLEGES = (
    ('MAN', 'MANSFIELD'),
    ('IMP', 'IMPERIAL'),
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
        # return dict(COLLEGES)[self.name]
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
    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)
    time = models.DateTimeField()  # TODO add auto_now?

    def __str__(self):
        return self.user.__str__() + " " + self.challenge.__str__() + " " + str(self.time)


