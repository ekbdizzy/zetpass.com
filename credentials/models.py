from django.db import models
from users.models import ZetUser
from access_options.models import UserIP


class Service(models.Model):
    """Service on which user saves login and password."""
    name = models.CharField(max_length=150, db_index=True)
    url = models.URLField('URL', blank=True, null=True)
    # TODO add ImageField for logo.


class Password(models.Model):
    # FIXME update max_length of encrypted_password according to encryption.
    """Password of user on service."""
    user = models.ForeignKey(ZetUser, on_delete=models.CASCADE, related_name='passwords')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='passwords')
    encrypted_login = models.CharField('Encrypted login, email or ID', max_length=100, db_index=True)
    encrypted_password = models.CharField('Encrypted password', max_length=300)


class Note(models.Model):
    """Note with private info. Text of Note is encrypted.
    It doesn't link to service and save data in text format.
    Limit: 1000 symbols."""
    user = models.ForeignKey(ZetUser, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=150, db_index=True)
    encrypted_text = models.TextField(max_length=1000)


class Links(models.Model):
    """List of private or shared links, grouped by common idea.
     It doesn't link to service and save data as list of links.
     By default is not encrypted. Public links cannot be encrypted."""
    # TODO add url_hash to generate public links (use hashlib.md5.hexdigest()[:10])
    user = models.ForeignKey(ZetUser, on_delete=models.CASCADE, related_name='links_groups')
    name = models.CharField(max_length=150)
    is_public = models.BooleanField('Is public', default=False)
    expired_public_at = models.DateTimeField(auto_now=True)
    is_encrypted = models.BooleanField(default=False)


class Link(models.Model):
    """One link from Links list."""
    links_group = models.ForeignKey(Links, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=300, blank=True)
    link = models.CharField(max_length=300)  # Used CharField instead of URLField because it can be encrypted.


class PrivateToken(models.Model):
    """Token of private or public service.
    By default access is allowed from limited IPs.
    Named PrivateToken to avoid confusion with other tokens."""
    user = models.ForeignKey(ZetUser, on_delete=models.CASCADE, related_name='tokens')
    name = models.CharField(max_length='150', db_index=True)
    encrypted_app_id = models.CharField('ID of client or app', max_length=64, blank=True)
    encrypted_token = models.CharField('Token', max_length=300)
    allowed_ips = models.ManyToManyField(UserIP, related_name='tokens')