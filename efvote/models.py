from django.db import models
import random

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"

class Entry(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    author_url = models.CharField(max_length=100)

    def __unicode__(self):
        return "'%s' by %s" % (self.title, self.author)


class Voting(models.Model):
    hash = models.CharField(max_length=10, unique=True, editable=False)
    edited = models.IntegerField(default=0)

    def save(self):
        if not self.hash:
            self.hash = "".join([random.choice(CHARS) for n in range(10)])
            self.edited = 0
        else:
            self.edited += 1
        super(Voting, self).save()

    def __unicode__(self):
        return "%s, %d edits" % (self.hash, self.edited)
        

class Vote(models.Model):
    voting = models.ForeignKey(Voting, editable=False)
    entry = models.ForeignKey(Entry)
    position = models.IntegerField()

    def __unicode__(self):
        return "%d - %s" % (self.position, self.entry.title)


class Voter(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username

    @classmethod
    def has_voted(cls, user):
        return True if cls.objects.filter(
            username=user.username).count() > 0 else False
