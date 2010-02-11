# -*- coding: utf-8 -*-

from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.conf import settings
from models import Entry, Voter, Vote, Voting
from django_phpbb.models import PhpbbUser
from random import shuffle
from datetime import datetime
import re
import logging

def vote(request):
    voted = []

    if request.method == 'POST':
        if 'votecode' in request.POST:
            request.session.clear()
            votecode = request.POST['votecode']
            try:
                v = Voting.objects.get(hash=votecode)
                voted = [n.entry for n in v.vote_set.order_by('position')]
                request.session['votecode'] = votecode
            except Voting.DoesNotExist:
                return direct_to_template(request, 'message.html', {
                        'title': "Okänd röstningskod",
                        'message': "Den angivna röstningskoden kunde " + \
                            "tyvärr inte hittas."})
        else:
            if 'votecode' in request.session:
                votecode = request.session['votecode']
            else:
                votecode = None

            # (In)sanity checks
            assert votecode or request.user.is_authenticated()
            votedata = request.POST['votes']
            votes = re.split("^e_([0-9]+)&e_([0-9]+)&e_([0-9]+)$", votedata)
            votes = [int(votes[n]) for n in [1,2,3]]
            assert len(votes) == len(set(votes)) and len(votes) == 3
            votes = [Entry.objects.get(id=n) for n in votes]
        
            # Everything looks ok, let's continue
            request.session['votes'] = '&'.join([str(n.id) for n in votes])
            return redirect_to(request, reverse('confirm'))

    assert len(voted) == 3 or request.user.is_authenticated()

    # Users registered after contest announcement are not allowed to vote
    if request.user.is_authenticated():
        try:
            bbuser = PhpbbUser.objects.get(username=request.user.username)
            if bbuser.user_regdate() >= \
                    datetime.datetime.strptime(settings.EFVOTE_REG_LIMIT):
                return direct_to_template(request, 'message.html', {
                        'title': 'Tyvärr...',
                        'message': 'Endast medlemmar registrerade före ' + \
                            'tävlingens tillkännagivande (%s) ' + \
                            'är tillåtna att rösta i tävlingen.' \
                            % settings.EFVOTE_REG_LIMIT})
        except PhpbbUser.DoesNotExist:
            # Authenticated with unknown backend
            pass

        if Voter.has_voted(request.user):
            return direct_to_template(request, 'already_voted.html')

    entries = list(Entry.objects.all())
    
    if len(voted) == 0 and 'votes' in request.session:
        votes = str(request.session['votes']).split('&')
        for vote in votes:
            voted.append(Entry.objects.get(id=vote))

    for entry in voted:
        entries.remove(entry)

    shuffle(entries)
    return direct_to_template(request, 'vote.html', {'entries': entries,
                                                     'voted': voted})

def confirm(request):
    if 'votecode' in request.session:
        votecode = request.session['votecode']
    else:
        votecode = None

    if not request.user.is_authenticated() and not votecode:
        return redirect_to(request, reverse('home'))

    if 'confirm' in request.POST:
        votes = str(request.session['votes']).split('&')
        votes = [Entry.objects.get(id=n) for n in votes]
        
        # Make sure to prevent any double-voting
        if not votecode:
            user = request.user
            logout(request)
        else:
            del request.session['votecode']
        
        if not votecode:
            v = Voting()
            v.save()
        else:
            v = Voting.objects.get(hash=votecode)
            v.vote_set.all().delete()

        position = 1
        for entry in votes:
            Vote(voting=v, entry=entry, position=position).save()
            position += 1
        
        if not votecode:
            Voter(userid=user.id, username=user.username).save()

        return direct_to_template(request, 'thanks.html', {'hash': v.hash,
                                                           'votecode': votecode})

    votes = request.session['votes'].split('&')
    assert len(votes) == 3
    voteobjects = [Entry.objects.get(id=n) for n in votes]
    return direct_to_template(request, 'confirm.html', {'votes': voteobjects})
