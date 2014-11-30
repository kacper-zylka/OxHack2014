from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.utils import timezone

from oxhack.forms import UserForm, UserProfileForm
from oxhack.models import College, Challenge, ChallengeCompletion, UserProfile, DIFFICULTIES

import sendgrid
import secret

question_command = 'q'

@csrf_exempt
def inbound(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Must POST")

    from_address = request.POST.get('from','')
    from_address = from_address[from_address.find("<")+1:from_address.find(">")]
    subject = request.POST.get('subject','')
    body = request.POST.get('text','') # get the text before linebreak
    userQuery = User.objects.filter(email=from_address).exclude(username='admin')
    print('from_address:' +from_address)
    print('subject:' +subject)
    print('text:' +body)
    print('userQuery:' +str(userQuery))

    # No account with that email exists
    if len(userQuery) == 0:
        sendUserNotEnrolledEmail(to_address=from_address)
        return HttpResponse("Email address not enrolled")

    userProfile = UserProfile.objects.get(user=userQuery[0])

    # If it has a blank subject, send them instructions on how to play
    if subject == '':
        sendBlankSubjectEmail(to_address=from_address)
        return HttpResponse("Email contained blank subject")

    # Check if they want questions
    if body[0:len(question_command)] == question_command:
        # find any colleges that match the Subject line
        matching_colleges = College.objects.filter(name__icontains=subject.replace('RE: ','').replace('Re: ','' ))

        # If there are multiple or no matching colleges, ask them to send again with different college name format.
        if matching_colleges.count() != 1:
            sendInvalidCollegeEmail(to_address=from_address,subject= subject)
            return HttpResponse("Could not match college subject.")

        # If the body is empty, send them the clue list for that college
        text = "Here are all the clues at " + matching_colleges[0].name + " college:\n\n"
        text += getClueList(college=matching_colleges[0], userProfile=userProfile)
        text += "\n\nReply to this message with the following format to answer (write on one line):\n\n1: Answer to question 1    2: Answer to question 2     ..... \n\nIf you don't know the answer to a question, simply don't include it. You can answer questions in any order."

        sendEmail(from_address,matching_colleges[0].name,text)
        return HttpResponse(text)
    # Parse for answers
    else:
        first_line = body.split('\n')[0]
        subject = subject.replace('Re: ', '').replace('RE: ', '')

        if first_line.find(':') == -1:
            sendInvalidBodyEmail(to_address=from_address, subject=subject)
            return HttpResponse("Unrecognised email format")

        debug_response = ''
        # Trim off the prefix to just get the college name
        college_name = subject
        print('subject:' + subject)
        colleges = College.objects.filter(name__icontains=college_name)
        college = colleges[0]
        if len(colleges) == 0:
            sendInvalidCollegeEmail(to_address=from_address, subject=subject)
            return HttpResponse(subject)
        # TODO get the user from their email
        # incompleted_challenges = incompletedChallengesForUserCollege(college=college, userProfile=userProfile)
        all_challenges = Challenge.objects.filter(college=college)
        # debug_response += 'incompleted_challenges: \n' + str(all_challenges)
        answers = parseAnswerStringForAnswers(first_line)
        debug_response += '\n correct answers:\n'

        reply_email = 'Your answers:\n\n'

        for ans_key, ans_value in answers.iteritems():
            # they might have since completed the challenge they are emailing about
            try:
                chall = all_challenges[ans_key - 1]
                print(chall)
                reply_email += str(ans_key) + ': '
                reply_email += chall.text + '\n'
                reply_email += 'You answered: ' + ans_value + '\n'

                if chall != None and chall.answer == ans_value:
                    # make them complete the challenge
                    c = ChallengeCompletion(userProfile=userProfile, challenge=chall, time=timezone.now())
                    c.save()
                    debug_response += str(c)
                    reply_email += 'Correct!'
                else:
                    reply_email += 'Wrong! Try again.'

            except IndexError:
                reply_email += str(ans_key) + ': '
                reply_email += 'Invalid question number.\n'

            reply_email += '\n\n'
            reply_email += 'Your summary for ' + college_name + ' college:\n\n'
            reply_email += getClueList(college, userProfile)

        sendEmail(to_address=from_address,subject=subject,text=reply_email)

        return HttpResponse(reply_email)

    return HttpResponse("Pass")


def incompletedChallengesForUserCollege(college, userProfile):
    all_challenges = Challenge.objects.filter(college=college)
    completed_challenges = [challComp.challenge for challComp in ChallengeCompletion.objects.filter(userProfile=userProfile)]
    return [chall for chall in all_challenges if chall not in completed_challenges]

def sendUserNotEnrolledEmail(to_address):
    print('Sending unrecognised email email')
    subject = "Woops - unrecognised email address!"
    body = """<p>We didn't recognise your email address.</p><p>If you haven't created an account, click <a href="http://oxhunt.me/register">here</a>.</p>"""
    return sendEmail(to_address = to_address , subject = subject, text = body)


def getClueList(college, userProfile):
    # incompleted_challenges = incompletedChallengesForUserCollege(college=college, userProfile=userProfile)
    all_challenges = Challenge.objects.filter(college=college)
    completed_challenges = [challComp.challenge for challComp in ChallengeCompletion.objects.filter(userProfile=userProfile)]

    clues_list = []


    for i, chall in enumerate(all_challenges):
        status = '[Answered]' if chall in completed_challenges else '[Unanswered]'

        clues_list.append( status + '['+dict(DIFFICULTIES)[chall.difficulty]+'] ' + str(i+1) + ': ' + chall.text)

    body = '\n'.join(clues_list)
    return body

def sendBlankSubjectEmail(to_address):
    print('Sending blank subject email')
    subject = "Woops - blank subject!"
    body = """<p>You didn't include a subject in your email.</p> <p>To get a list of clues for a college, simply <a href="mailto:mail@oxhunt.bymail.me?subject=College&body=g">send an email to this address with the college name as the subject line and 'g' in the body. For a list of colleges, click <a href="http://oxhunt.me/leaderboard">here</a>.</p>"""
    return sendEmail(to_address = to_address , subject = subject, text = body)


def sendInvalidCollegeEmail(to_address, subject):
    print('Sending invalid college email')
    body = """<p>We didn't recognise that college name. To get a list of clues for a college,
     simply send an email to this address with the college name as the subject line and 'g' in the body.</p>
    For a list of valid college names, click <a href="http://oxhunt.me/leaderboard">here</a>."""
    return sendEmail(to_address = to_address , subject = subject, text = body)

def sendInvalidBodyEmail(to_address, subject):
    print('Sending invalid body email')
    body = """<p>There's something a bit funny about your syntax.</p><p>Request the clues by replying to this email with the letter 'q' and try again.</p>"""
    return sendEmail(to_address = to_address , subject = subject, text = body)


def sendEmail(to_address,subject,text):
    sg = sendgrid.SendGridClient(secret.EMAIL_HOST_USER, secret.EMAIL_HOST_PASSWORD)
    message = sendgrid.Mail(to=to_address, subject=subject, html=text, text=text, from_email='mail@oxhunt.bymail.in')
    status, msg = sg.send(message)
    return status

def parseAnswerStringForAnswers(answer_string):
    """
    Takes a string in the '1: answer     5: answer 5 \n 4: answer4' format and returns a dictionary
    of the answer numbers and their values (all lowercase and spaces removed)

    { 
        1: 'answer1', 2: 'answer2'
    }

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
    return render_to_response('oxhack/landing.html', {'landing': 'true'})

def rules(request):
    return render_to_response('oxhack/rules.html', {'rules': 'true'})

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

        name_img_dict={"All Souls": "all-souls.png","Balliol": "balliol.png","Blackfriars": "blackfriars.png","Brasenose": "brasenose.png","Campion Hall": "campion-hall.png","Christ Church": "christ-church.png","Coprus Christi": "corpus-christi.png","Exeter": "exeter.png","Green Templeton": "green-templeton.png","Harris Manchester": "harris-manchester.png","Hertford": "hertford.png","Jesus": "jesus.png","Keble": "keble.png","Kellog": "kellog.png","Lady Margaret": "lady-margaret-hall.png","Linacre": "linacre.png","Lincoln": "lincoln.png","Magdalen": "magdalen.png","Mansfield": "mansfield.png","Merton": "merton.png","New": "new.png","Nuffield": "nuffield.png","Oriel": "oriel.png","Pembroke": "pembroke.png","Queens": "queens.png","Regent Park": "regent-park.png","St Annes": "st-annes.png","St Anthonys": "st-antonys.png","St Benets": "st-benets-hall.png","St Catherines": "st-catherines.png","St Cross": "st-cross.png","St Edmund Hall": "st-edmund-hall.png","St Hildas": "st-hildas.png","St Hughs": "st-hughs.png","St Johns": "st-johns.png","St Peters": "st-peters.png","St Stephens": "st-stephens-house.png","Somerville": "somerville.png","Trinity": "trinity.png","University": "university.png","Wadham": "wadham.png","Wolfson":"wolfson.png","Worcester": "worcester.png","Wycliffe": "wycliffe-hall.png"}

        college_leaderboard[name]['image_name'] = "/static/oxhack/images/college-crests/" + name_img_dict[name]

    # Sort college_leaderboard by total_completions
    college_leaderboard = sorted(college_leaderboard.items(), key=lambda x: x[1]['total_completions'], reverse=True)

    # For user: sort users by number of completions

    users_leaderboard = []

    users = UserProfile.objects.all()

    for u in users:
        users_leaderboard.append((u.user.username, ChallengeCompletion.objects.filter(userProfile=u).count()))

    users_leaderboard = filter(lambda x: x[1] > 0, users_leaderboard)
    users_leaderboard = sorted(users_leaderboard, key=lambda x: x[1], reverse=True)

    # print users_leaderboard

    return render_to_response('oxhack/leaderboard.html', {'colleges' : college_leaderboard, 'users' : users_leaderboard, 'leaderboard': 'true'})




def visualisations(request):
    return render_to_response('oxhack/visualisations.html', {'visualisations': 'true'})

def about(request):
    return render_to_response('oxhack/about.html', {'about': 'true'})

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'registration/registration_form.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def getNetworkGraphJSON():
    all_chall_comps = ChallengeCompletion.objects.all()
    colleges = {}

    for chall_comp in all_chall_comps:
        user_college = chall_comp.userProfile.college
        chall_college = chall_comp.challenge.college
        # print(user_college, chall_college)
        try:
            colleges[user_college.name][chall_college.name] += 1
        except KeyError:
            colleges[user_college.name] = {chall_college.name: 1}

    print(colleges)
