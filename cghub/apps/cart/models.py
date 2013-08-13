from django.db import models
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, post_delete


class Cart(models.Model):
    session = models.OneToOneField(Session, related_name='cart')
    size = models.PositiveIntegerField(default=0)
    live_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.session.session_key


class Analysis(models.Model):
    analysis_id = models.CharField(max_length=36, db_index=True, unique=True)
    state = models.CharField(max_length=20)
    last_modified = models.CharField(max_length=20)
    files_size = models.PositiveIntegerField()

    def __unicode__(self):
        return self.analysis_id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    analysis = models.ForeignKey(Analysis)

    def __inicode__(self):
        return '%s - %s' % (
                self.cart.session.session_key, self.analysis.analysis_id)

    class Meta:
        unique_together = ('cart', 'analysis')
        ordering = ('analysis',)


def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(session=instance)

post_save.connect(create_cart, sender=Session)

def remove_cart(sender, instance, **kwargs):
    instance.cart.items.all().delete()
    instance.cart.delete()

post_delete.connect(remove_cart, sender=Session)
