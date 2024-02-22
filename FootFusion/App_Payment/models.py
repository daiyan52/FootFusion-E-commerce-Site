from django.db import models
from django.conf import settings
# Create your models here.

class billingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billingAddress')
    city = models.CharField(blank=True, max_length=30, verbose_name='city')
    zipcode = models.CharField(blank=True, max_length=10, verbose_name='zipcode')
    country = models.CharField(blank=True, max_length=30, verbose_name='country')
    phone = models.CharField(blank=True, max_length=30, verbose_name='phone')
    address = models.CharField(blank=True, max_length=300, verbose_name='address')

    def __str__(self):
        return f'{self.user.profile.username} Billing Address'
    
    # def is_fully_filled(self):
    #     fields_name = [f.name for f in self._meta.get_fields()]

    #     for field_name in fields_name:
    #         value = getattr(self, field_name)
    #         if value is None or value == '':
    #             return False
    #     return True
    
    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]
        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is  None or value == '':
                return False
        return True


    class Meta:
        verbose_name_plural = 'Billing Addresses'