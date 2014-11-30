from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from oxhack.models import College, Challenge, ChallengeCompletion, UserProfile, DIFFICULTIES
from django.contrib.auth.models import User

from django.utils import timezone

import sendgrid
from django.shortcuts import render_to_response


reply_prefix = 'Clues for college: '

@csrf_exempt
def inbound(request):

    if request.method != 'POST':
        return HttpResponseBadRequest("Must POST")

    from_address = request.POST.get('from','')
    subject = request.POST.get('subject','')
    body = request.POST.get('body','')
    userQuery = User.objects.filter(email=from_address).exclude(username='admin')

    # No account with that email exists
    if len(userQuery) != 1:
        sendUserNotEnrolledEmail(to_address=from_address)
        return HttpResponse("Email address not enrolled")

    userProfile = UserProfile.objects.get(user=userQuery[0])

    # If it has a blank subject, send them instructions on how to play
    if not subject:
        sendBlankSubjectEmail(to_address=from_address)
        return HttpResponse("Email contained blank subject")
    # If it is a reply to a clue list email, parse it for answers
    elif reply_prefix in subject:
        debug_response = ''
        # Trim off the prefix to just get the college name
        college_name = subject[len(reply_prefix):]
        college = College.objects.get(name__icontains=college_name)
        # TODO get the user from their email
        incompleted_challenges = incompletedChallengesForUserCollege(college=college, userProfile=userProfile)
        debug_response += 'incompleted_challenges: \n' + str(incompleted_challenges)
        answers = parseAnswerStringForAnswers(body)
        debug_response += '\n correct answers:\n'

        reply_email

        for ans_key, ans_value in answers.iteritems():
            # they might have since completed the challenge they are emailing about
            try:
                chall = incompleted_challenges.index(ans_key - 1)
                if chall != None and chall.answer == ans_value:
                    # make them complete the challenge
                    c = ChallengeCompletion(user=userProfile, challenge=incompleted_challenges[ans_key - 1], time=timezone.now())
                    c.save()
                    debug_response += str(c)
            except ValueError:
                pass

        return HttpResponse(debug_response)

    # Else they are probably asking for a college clue list. Check
    else:
        # find any colleges that match the Subject line
        matching_colleges = College.objects.filter(name__icontains=subject)

        # If there are multiple or no matching colleges, ask them to send again with different college name format.
        if matching_colleges.count() != 1:
            sendInvalidCollegeEmail(to_address=from_address)
            return HttpResponse("Could not match college subject.")

        # If the body is empty, send them the clue list for that college
        if not body.strip():
            text = getClueList(college=matching_colleges[0], userProfile=userProfile)
            sendEmail(from_address,reply_prefix + matching_colleges[0].name,text)
            return HttpResponse(text)

    return HttpResponse("Pass")


def incompletedChallengesForUserCollege(college, userProfile):
    all_challenges = Challenge.objects.filter(college=college)
    completed_challenges = [challComp.challenge for challComp in ChallengeCompletion.objects.filter(user=userProfile)]
    return [chall for chall in all_challenges if chall not in completed_challenges]

def sendUserNotEnrolledEmail(to_address):
    subject = "Woops - unrecognised email address!"
    body = "We didn't recognise your email address. If you haven't created an account, click here."
    return sendEmail(to_address = to_address , subject = subject, text = body)


def getClueList(college, userProfile):
    incompleted_challenges = incompletedChallengesForUserCollege(college=college, userProfile=userProfile)

    clues_list = []
    for i, chall in enumerate(incompleted_challenges):
        clues_list.append( str(i+1) + ": (" + dict(DIFFICULTIES)[chall.difficulty] + ") " + chall.text)

    body = "Here are the available clues for " + college.name + ":\n\n"
    body += '\n'.join(clues_list)
    body += "\n\nReply to this message with the following format to answer:\n\n1: Answer to question 1 \n2: Answer to question 2\netc."
    return body

def sendBlankSubjectEmail(to_address):
    subject = "Woops - blank subject!"
    body = "You didn't include a subject in your email. To get a list of clues for a college, simply send a blank email to this address with the college name as the subject line. For a list of colleges, click here."
    return sendEmail(to_address = to_address , subject = subject, text = body)


def sendInvalidCollegeEmail(to_address):
    subject = "Woops - unrecognised college!"
    body = "We didn't recognise that college name. To get a list of clues for a college, simply send a blank email to this address with the college name as the subject line. For a list of valid college names, click here."
    return sendEmail(to_address = to_address , subject = subject, text = body)


def sendEmail(to_address,subject,text):
    sg = sendgrid.SendGridClient('frigaardj', 'oxhunt2014')
    message = sendgrid.Mail(to=to_address, subject=subject, text=text, from_email='inbound@frigaardj.bymail.in')
    status, msg = sg.send(message)
    return status

def parseAnswerStringForAnswers(answer_string):
    """
    Takes a string in the '1: answer     5: answer 5 \n 4: answer4' format and returns a dictionary
    of the answer numbers and their values (all lowercase and spaces removed)
    DOES NOT WORK WITH ANSWER NUMBERS WITH 2 DIGITS. e.g. '10: answer10'
    """
    ans = ''.join(c.lower() for c in answer_string if not c.isspace())
    answers = {}

    while len(ans) > 0:
        first_colon = ans.find(':')
        i = ans[first_colon - 1]
        ans = ans[first_colon + 1 :]
        next_colon = ans.find(':')
        if next_colon == -1:
            next_colon = len(ans) + 1
        answers[int(i)] = ans[: next_colon - 1 ]
        ans = ans[ next_colon - 1 : ]
    return answers

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
