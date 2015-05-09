from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# Create your models here.
class App(models.Model):
    title = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, null=True)
    secret_key = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        if self.secret_key is None:
            self.secret_key = shortuuid.uuid()
        super(Model, self).save(*args, **kwargs)


class LogEntry(models.Model):
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    link = models.URLField(max_length=255, null=True)
    app_id = models.ForeignKey('App', null=True)


    @classmethod
    def get_unread(self, app_id, user_id):
        return []

    def to_dict(self):
        return model_to_dict(self)


class LogEntryRead(models.Model):
    log = models.ForeignKey('LogEntry')
    user_id = models.TextField()
