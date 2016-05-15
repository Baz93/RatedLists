from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from time import time
from hashlib import md5

from .score_logic.logic import update


class List(models.Model):
    title = models.CharField(max_length=120)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lists:view', kwargs={'list_id': self.id})

    def get_chart_url(self):
        return reverse('lists:chart', kwargs={'list_id': self.id})

    def get_vote_url(self):
        return reverse('lists:vote', kwargs={'list_id': self.id})

    def get_add_url(self):
        return reverse('lists:new_item', kwargs={'list_id': self.id})

    def get_edit_url(self):
        return reverse('lists:edit', kwargs={'list_id': self.id})

    def get_delete_url(self):
        return reverse('lists:delete', kwargs={'list_id': self.id})


class Item(models.Model):
    title = models.CharField(max_length=500)
    suggested_by = models.ForeignKey(User, related_name='suggestions')
    modified_by = models.ForeignKey(User, related_name='modifications')
    list = models.ForeignKey(List, related_name='items')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def votes(self):
        return self.votes_as_first | self.votes_as_second

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lists:view_item', kwargs={'item_id': self.id})

    def get_edit_url(self):
        return reverse('lists:edit_item', kwargs={'item_id': self.id})

    def get_delete_url(self):
        return reverse('lists:delete_item', kwargs={'item_id': self.id})


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes')
    list = models.ForeignKey(List, related_name='votes')
    first = models.ForeignKey(Item, related_name='votes_as_first')
    second = models.ForeignKey(Item, related_name='votes_as_second')
    difference = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username + ':' + self.first.title + '&' + self.second.title


class RatersGroup(models.Model):
    list = models.ForeignKey(List, related_name='rater_groups')
    members = models.ManyToManyField(User, related_name='rater_groups')
    except_members = models.ManyToManyField(User, related_name='banned_from_rater_groups')
    last_use = models.DateTimeField(auto_now=True)
    group_hash = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    def use(self):
        self.last_use = time()
        self.save()
        update(self, Score)
        return self

    def relevant_votes(self):
        if self.members.count() > 0:
            return Vote.objects.filter(list=self.list, user__in=self.members.all())
        else:
            return Vote.objects.filter(list=self.list).exclude(user__in=self.except_members.all())

    @classmethod
    def get_or_create(cls, list_obj, members, except_members):
        assert len(members) == 0 or len(except_members) == 0, 'Incorrect raters group request.'
        m = md5()
        m.update(str([
            list_obj.id,
            [user.id for user in members],
            [user.id for user in except_members],
        ]).encode('utf-8'))
        desired_hash = m.hexdigest()
        try:
            return cls.objects.get(group_hash=desired_hash).use()
        except models.ObjectDoesNotExist:
            new_instance = cls(
                list=list_obj,
                group_hash=desired_hash,
            )
            new_instance.save()
            for user in members:
                new_instance.members.add(user)
            for user in except_members:
                new_instance.except_members.add(user)
            return new_instance.use()


class Score(models.Model):
    group = models.ForeignKey(RatersGroup, related_name='scores')
    item = models.ForeignKey(Item, related_name='scores')
    value = models.DecimalField(max_digits=8, decimal_places=5, default=0)

    def __str__(self):
        return self.item.title + ': ' + str(self.value) + ' (' + str(self.group) + ')'

    @classmethod
    def get_or_create(cls, group, item):
        try:
            return cls.objects.get(group=group, item=item)
        except models.ObjectDoesNotExist:
            new_instance = cls(group=group, item=item)
            new_instance.save()
            return new_instance

