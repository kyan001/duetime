from django.db import models


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
            raise Http404('您查找的 {t} 并不存在。（查询参数 {a} {k}）'.format(t=self.model.__name__, a=args or '', k=kwargs or ''))


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


class Notiecard(BaseModel):
    title = models.CharField(max_length=30)
    kcol = models.CharField(max_length=30)
    vcol = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
