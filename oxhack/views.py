from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sendgrid

@csrf_exempt
def inbound(request):

    sg = sendgrid.SendGridClient('frigaardj', 'oxhunt2014')
    from_addr = request.POST.get('from','jack.frigaard@gmail.com')
    body = request.POST.get('text','Blah')

    message = sendgrid.Mail(to=from_addr, subject="email to: " + from_addr, html=body, text=body, from_email='hunt@oxhunt.me')
    status, msg = sg.send(message)

    return HttpResponse(status)

