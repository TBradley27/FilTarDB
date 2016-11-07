# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm

# from django.core.urlresolvers import reverse

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contextpp(models.Model):
    mirna_name = models.CharField(db_column='miRNA_name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    transcript_id = models.CharField(db_column='transcript_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    common_name = models.CharField(db_column='common_name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_start = models.CharField(db_column='UTR_Start', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_end = models.CharField(db_column='UTR_End', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tpm = models.DecimalField(db_column='TPM', max_digits=10m decimal_places=2 blank=True, null=True) #Field name made lower case
    site_type = models.CharField(db_column='Site_Type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contextpp_score = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contextpp'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Experiments(models.Model):
    experiment_name = models.CharField(max_length=20, blank=True, null=True)
    taxonomic_id = models.CharField(db_column='taxonomic_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tissue_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiments'


class ExpressionProfiles(models.Model):
    transcript_id = models.CharField(db_column='transcript_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tpm = models.DecimalField(db_column='TPM', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expression_profiles'


class Mrnas(models.Model):
    mrna_id = models.CharField(db_column='mRNA_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.mrna_id

    class Meta:
        managed = False
        db_table = 'mRNAs'
        verbose_name_plural = 'mRNAs'


class Mirnas(models.Model):
    mirna_name = models.CharField(db_column='miRNA_name', max_length=20, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.mirna_name

    class Meta:
        managed = False
        db_table = 'miRNAs'
        verbose_name_plural = ' miRNAs'


class MusicAlbum(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'music_album'


class MusicSong(models.Model):
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    album = models.ForeignKey(MusicAlbum, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'music_song'


class Species(models.Model):
    taxonomic_id = models.CharField(db_column='taxonomic_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    species_name = models.CharField(max_length=20, blank=True, null=True)
    genome_build = models.CharField(max_length=20, blank=True, null=True)
    common_name = models.CharField(max_length=50, blank=True, null=True)
#     id = models.IntegerField(default=11, null=False, primary_key=True) 
	
    def __str__(self):
	     return self.common_name
	     
    class Meta:
        managed = False
        db_table = 'species'
        verbose_name_plural = "Species"


class Tissues(models.Model):
    tissue_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.tissue_name
        
    class Meta:
        managed = False
        db_table = 'tissues'
        verbose_name_plural = "Tissues"

class MirnaForm(ModelForm):
     mirnas = forms.ModelChoiceField(queryset = Mirnas.objects.all(), to_field_name="mirna_name")
     class Meta:
        model = Mirnas
        fields = ['mirna_name']

class Contextpp_Form(ModelForm):
    class Meta:
        model = Contextpp
        fields = ['mirna_name', 'transcript_id']