from django.db import models


class HelpText(models.Model):
    slug = models.SlugField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title
