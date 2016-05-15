from django.contrib import admin

from .models import List, Item, Vote, RatersGroup, Score


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'created', 'updated']
    list_editable = ['title']
    search_fields = ['title']
    list_filter = ['owner', 'created', 'updated']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'suggested_by', 'modified_by', 'list', 'created', 'updated']
    list_editable = ['title']
    search_fields = ['title']
    list_filter = ['suggested_by', 'modified_by', 'list', 'created', 'updated']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'list', 'first', 'second', 'difference', 'weight', 'timestamp']
    list_editable = ['difference', 'weight']
    list_filter = ['user', 'list', 'first', 'second', 'difference', 'weight', 'timestamp']


@admin.register(RatersGroup)
class RatersGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'list', 'last_use']
    list_filter = ['list', 'last_use']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'item', 'value']
    list_filter = ['group', 'item', 'value']

