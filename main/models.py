import random

from django.db import models
from django.forms.models import model_to_dict
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _


class BaseManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            raise Http404(_('The {t} you are looking for does not exist. (Request arguments {a} {k})').format(t=self.model.__name__, a=args or '', k=kwargs or ''))


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    objects = BaseManager()

    class Meta:
        abstract = True

    def toArray(self):
        self.created = self.created.isoformat(' ')
        self.modified = self.modified.isoformat(' ')
        return model_to_dict(self)


class CardnoteCard(BaseModel):
    CATEGORIES = (
        ('default', 'Default'),
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    )
    userid = models.IntegerField(blank=False, null=False)
    title = models.CharField(max_length=30)
    kcol = models.CharField(max_length=30, blank=True)
    vcol = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=20, blank=True, choices=CATEGORIES, default='default')

    @property
    def cardnoteitems(self):
        return CardnoteItem.objects.filter(cardnotecardid=self.id)

    @property
    def last_updated(self):
        return self.cardnoteitems.order_by('-modified').get().modified

    @property
    def user(self):
        return get_object_or_404(User, id=self.userid)


class CardnoteItem(BaseModel):
    cardnotecardid = models.IntegerField()
    kword = models.CharField(max_length=128, blank=True)
    val = models.CharField(max_length=512, blank=True)

    @property
    def cardnotecard(self):
        card = CardnoteCard.objects.get(id=self.cardnotecardid)
        return card


class ShortUrlManager(BaseManager):
    def isUrlLegal(self, url, exclude=None):
        """Check if a URL is already censored

        Args:
            url: [str] Target URL
            exclude: [ShortUrl] The ShortUrl which should be excluded

        Returns:
            True: Target URL is legal
            False: Target URL is illegal
            None: Target URL is uncensored
        """
        if exclude:
            precedent = self.filter(url=url).exclude(id=exclude.id).first()
        else:
            precedent = self.filter(url=url).first()
        if not precedent:
            return None
        return precedent.legal


class ShortUrl(BaseModel):
    userid = models.IntegerField()
    name = models.CharField(max_length=200, blank=True, default="")
    url = models.URLField(null=False, blank=False)
    pv = models.IntegerField(default=0)
    legal = models.NullBooleanField(default=None, null=True)
    objects = ShortUrlManager()

    @property
    def user(self):
        return get_object_or_404(User, id=self.userid)

    @property
    def uri(self):
        return "/su/{}".format(self.id)

    @property
    def short(self):
        host = "https://duetime.cn"
        return host + self.uri

    def add_pv(self):
        self.pv = self.pv + 1
        self.save()
