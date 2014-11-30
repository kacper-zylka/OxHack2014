from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sendgrid
from django.shortcuts import render_to_response
from models import College, Challenge, ChallengeCompletion, UserProfile
from django.contrib.auth.models import User

@csrf_exempt
def inbound(request):

    sg = sendgrid.SendGridClient('frigaardj', 'oxhunt2014')
    from_addr = request.POST.get('from','jack.frigaard@gmail.com')
    body = request.POST.get('text','Blah')

    message = sendgrid.Mail(to=from_addr, subject="email to: " + from_addr, html=body, text=body, from_email='hunt@oxhunt.me')
    status, msg = sg.send(message)

    return HttpResponse(status)


def home(request):
    return render_to_response('oxhack/landing.html')

def rules(request):
    return render_to_response('oxhack/rules.html')

def leaderboard(request):
    # For college: all challenges sorted by number of corresponding completions

    """

    {
        'Mansfield' : { 'total_completions' : 8, 'challenge1' : 5, 'challenge2' : 2, 'challenge3' : 1 },
    }


    """

    college_names = [c.name for c in College.objects.all()]

    college_leaderboard = {}

    for name in college_names:
        college_leaderboard[name] = {}
        challenges = Challenge.objects.filter(college__name=name)
        total_completions = 0
        for challenge in challenges:
            num_completions = ChallengeCompletion.objects.filter(challenge=challenge).count()
            college_leaderboard[name][challenge.__str__()] = num_completions
            total_completions += num_completions
        college_leaderboard[name]['total_completions'] = total_completions

    # Sort college_leaderboard by total_completions
    college_leaderboard = sorted(college_leaderboard.items(), key=lambda x: x[1]['total_completions'], reverse=True)

    # For user: sort users by number of completions

    users_leaderboard = []

    users = User.objects.all()

    for u in users:
        users_leaderboard.append((u.username, ChallengeCompletion.objects.filter(user=u).count()))

    users_leaderboard = filter(lambda x: x[1] > 0, users_leaderboard)
    users_leaderboard = sorted(users_leaderboard, key=lambda x: x[1], reverse=True)

    # print users_leaderboard

    return render_to_response('oxhack/leaderboard.html', {'colleges' : college_leaderboard, 'users' : users_leaderboard})

def visualisations(request):
    return render_to_response('oxhack/visualisations.html')

def about(request):
    return render_to_response('oxhack/about.html')

def register(request):
    return render_to_response('oxhack/register.html')

