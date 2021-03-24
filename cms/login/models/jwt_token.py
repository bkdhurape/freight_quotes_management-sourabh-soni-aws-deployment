from django.contrib.postgres.fields import JSONField
from django.db import models
from login.managers.jwt_token_manager import JwtTokenManager


class JwtToken(models.Model, JwtTokenManager):
    entity_type = models.CharField(choices=[('customer', 'Customer'),('vendor', 'Vendor')], default='customer', null=False, max_length=255)
    entity_id = models.IntegerField(null=False)
    token_key = models.CharField(null=False, blank=False, max_length=2048)
    token_value = JSONField(default=dict, null=False, blank=False)
    session_id = models.CharField(null=False, blank=False, max_length=1024)
    expire_timestamp = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'jwt_tokens'
        unique_together = (('entity_type', 'entity_id', 'session_id'))
