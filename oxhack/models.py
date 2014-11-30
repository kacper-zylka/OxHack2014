from django.db import models
from django.contrib.auth.models import User
# from registration.signals import user_registered
# from django.dispatch import receiver

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

# @receiver(user_registered)
# def registration_active_receive_email(sender, user, request, **kwargs):
#     user_id = user.userprofile.id
#     user = UserProfile.objects.get(pk=user_id)

#     try:
#         if request.POST['college']:
#             pass
#     except:
#         user.collegeText = 'DefaultCollege'
#         user.save()

class ChallengeCompletion(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    challenge = models.ForeignKey(Challenge)
    time = models.DateTimeField()  # TODO add auto_now?

    def __str__(self):
        return self.user.__str__() + " " + self.challenge.__str__() + " " + str(self.time)


