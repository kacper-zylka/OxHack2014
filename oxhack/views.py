from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sendgrid
from django.shortcuts import render_to_response

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
    return render_to_response('oxhack/leaderboard.html')

def visualisations(request):
    return render_to_response('oxhack/visualisations.html')

def about(request):
    return render_to_response('oxhack/about.html')

def register(request):
    return render_to_response('oxhack/register.html')

