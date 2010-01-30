# -*- coding: utf-8 -*-
# This file is part of django-phpbb, integration between Django and phpBB
# Copyright (C) 2007-2008  Maciej Bliziński
# 
# django-phpbb is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# django-phpbb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with django-phpbb; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

from django.db import models
from datetime import datetime

class PhpbbUser(models.Model):
    """Model for phpBB user."""
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    username_clean = models.CharField(max_length=255)
    user_password = models.CharField(max_length=40)
    user_posts = models.IntegerField()
    user_email = models.CharField(max_length=255)
    user_website = models.CharField(max_length=100)
    user_avatar_type = models.IntegerField()
    user_avatar = models.CharField(max_length=250)
    user_regdate_int = models.IntegerField(db_column="user_regdate")
    user_lastvisit_int = models.IntegerField(db_column="user_lastvisit")
    user_sig_bbcode_uid = models.CharField(max_length=8)
    user_sig_bbcode_bitfield = models.CharField(max_length=255)

    def __unicode__(self):
        return self.username

    def user_regdate(self):
        return datetime.fromtimestamp(self.user_regdate_int)

    def user_lastvisit(self):
        return datetime.fromtimestamp(self.user_lastvisit_int)

    class Meta:
        db_table = 'phpbb3_users'
        ordering = ['username']
        managed = False
