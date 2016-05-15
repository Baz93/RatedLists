from django.conf.urls import url

from .views import (
    all_lists,
    list_create,
    list_update,
    list_delete,
    list_view,
    list_chart,
    vote,
    item_detail,
    item_create,
    item_update,
    item_delete,
)

urlpatterns = [
    url(r'^$', all_lists, name='all'),
    url(r'^new/$', list_create, name='new'),
    url(r'^(?P<list_id>\d+)/$', list_view, name='view'),
    url(r'^(?P<list_id>\d+)/edit/$', list_update, name='edit'),
    url(r'^(?P<list_id>\d+)/delete/$', list_delete, name='delete'),
    url(r'^(?P<list_id>\d+)/chart/$', list_chart, name='chart'),
    url(r'^(?P<list_id>\d+)/vote/$', vote, name='vote'),
    url(r'^(?P<list_id>\d+)/new_item/$', item_create, name='new_item'),
    url(r'^item/(?P<item_id>\d+)/$', item_detail, name='view_item'),
    url(r'^item/(?P<item_id>\d+)/edit/$', item_update, name='edit_item'),
    url(r'^item/(?P<item_id>\d+)/delete/$', item_delete, name='delete_item'),
]
