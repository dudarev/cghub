from django.db import models
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_delete


class Cart(models.Model):
    session = models.OneToOneField(Session, related_name='cart')
    size = models.BigIntegerField(default=0)
    live_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.session.session_key


class Analysis(models.Model):
    analysis_id = models.CharField(max_length=36, db_index=True, unique=True)
    state = models.CharField(max_length=20)
    last_modified = models.CharField(max_length=20)
    files_size = models.BigIntegerField()
    # used for sorting purpose
    aliquot_id = models.CharField(max_length=36, blank=True, null=True)
    analyte_code = models.CharField(max_length=4, blank=True, null=True)
    center_name = models.CharField(max_length=36, blank=True, null=True)
    disease_abbr = models.CharField(max_length=36, blank=True, null=True)
    legacy_sample_id = models.CharField(max_length=36, blank=True, null=True)
    library_strategy = models.CharField(max_length=36, blank=True, null=True)
    published_date = models.CharField(max_length=20, blank=True, null=True)
    participant_id = models.CharField(max_length=36, blank=True, null=True)
    platform = models.CharField(max_length=36, blank=True, null=True)
    refassem_short_name = models.CharField(max_length=36, blank=True, null=True)
    sample_accession = models.CharField(max_length=36, blank=True, null=True)
    sample_id = models.CharField(max_length=36, blank=True, null=True)
    sample_type = models.CharField(max_length=4, blank=True, null=True)
    study = models.CharField(max_length=36, blank=True, null=True)
    tss_id = models.CharField(max_length=4, blank=True, null=True)
    upload_date = models.CharField(max_length=20, blank=True, null=True)

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
    if instance.cart:
        instance.cart.items.all().delete()
        instance.cart.delete()

pre_delete.connect(remove_cart, sender=Session)
