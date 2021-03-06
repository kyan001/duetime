from django.contrib import admin
from main.models import *
from django.utils.html import format_html


@admin.register(CardnoteCard)  # admin.site.register(CardnoteCard)
class CardnoteCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'user', 'title', 'kcol', 'vcol', 'category', 'created', 'modified')
    search_fields = ('title', 'kcol', 'vcol')
    list_filter = ('userid', 'category')
    date_hierarchy = 'modified'


@admin.register(CardnoteItem)  # admin.site.register(CardnoteItem)
class CardnoteItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cardnotecardid', 'kword', 'val', 'created', 'modified')
    search_fields = ('kword', 'val')
    date_hierarchy = 'modified'


def make_legal(modeladmin, request, queryset):
    queryset.update(legal=True)


def make_illegal(modeladmin, request, queryset):
    queryset.update(legal=False)


def make_uncensored(modeladmin, request, queryset):
    queryset.update(legal=None)


@admin.register(ShortUrl)  # admin.site.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    def url_purified(self, obj):
        url_show = obj.url[:80] + " ..." if len(obj.url) > 80 else obj.url
        return format_html("<a href='{}' title='{}' target='_blank'>{}</a>", obj.url, obj.url, url_show)

    list_display = ('id', 'userid', 'user', 'pv', 'name', 'url_purified', 'legal', 'created', 'modified')
    search_fields = ('name', 'url', 'user')
    list_filter = ('userid', 'legal')
    date_hierarchy = 'created'
    actions = [make_legal, make_illegal, make_uncensored]
