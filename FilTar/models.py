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
from smart_selects.db_fields import ChainedForeignKey
from django.utils.encoding import python_2_unicode_compatible


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
    experiment_name = models.CharField(max_length=20, blank=True, null=False, primary_key=True)
    species = models.ForeignKey('Species', max_length=30, blank=True, null=True) # Field name made lowercase.
    tissue = models.ForeignKey('Tissues', max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'experiments'

class Mirnas(models.Model):
    name = models.CharField(db_column='miRNA_name', max_length=20, blank=True, null=False, primary_key=True)  # Field name made lowercase.
    Species = models.ForeignKey('Species', to_field="taxonomic_id", db_column="Species", max_length=20, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'mirna_dummy'
        verbose_name_plural = ' mirna_dummy'

class ExpressionProfiles(models.Model):
     mrnas = models.ForeignKey('Mrnas', max_length=20, blank=True, null=False)  # Field name made lowercase.
     tpm = models.DecimalField(db_column='TPM', max_digits=10, decimal_places=2, blank=True, null=True)
     experiments = models.ForeignKey('Experiments', null=True, on_delete=models.CASCADE)
        # models.CharField(db_column='experiment_name', max_length=20, blank=True, null=True)# Field name made lowercase.

     class Meta:
        managed = True
        db_table = 'expression_profiles'


class Mrnas(models.Model):
    id = models.CharField(db_column='mRNA_ID', max_length=20, blank=True, null=False, primary_key=True)  # Field name made lowercase.
    genome_assembly = models.ForeignKey('GenomeAssembly', max_length=30, blank=True, null=True)
    annotation = models.CharField(max_length=30, blank=True, null=True)
    gene_name = models.CharField(db_column='Gene_Name', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = True
        db_table = 'mRNAs'
        verbose_name_plural = 'mRNAs'

class GenomeAssembly(models.Model):
    genome_assembly = models.CharField(max_length=30, blank=True, null=False, primary_key=True)
    species = models.ForeignKey('Species', max_length=30, blank=True, null=True)
    submitter = models.CharField(max_length=30, blank=True, null=True)
    assembly_level = models.CharField(max_length=30, blank=True, null=True)
    syonyms = models.CharField(max_length=30, blank=True, null=True)


    def __str__(self):
        return self.genome_assembly

    class Meta:
        managed = True
        db_table = 'GenomeAssembly'
        verbose_name_plural = 'GenomeAssembly'

    class Meta:
        db_table = 'tmodel'


class Species(models.Model):
    taxonomic_id = models.CharField(db_column='taxonomic_ID', max_length=20, blank=True, null=False,
                                    primary_key=True)  # Field name made lowercase.
    species_name = models.CharField(max_length=20, blank=True, null=True)
    genome_build = models.CharField(max_length=20, blank=True, null=True)
    common_name = models.CharField(max_length=50, blank=True, null=True)

    #     id = models.IntegerField(default=11, null=False, primary_key=True)

    def __str__(self):
        return self.common_name

    class Meta:
        managed = True
        db_table = 'species'
        verbose_name_plural = "Species"


class Tissues(models.Model):
    name = models.CharField(max_length=50, null=False, primary_key=True)
    taxonomic_ID = models.ForeignKey('Species', to_field="taxonomic_id", db_column="taxonomic_ID", max_length=20,
                                     blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'tissues'
        verbose_name_plural = "Tissues"

class ExampleFK(models.Model):
    name = models.CharField(max_length=200)

    test = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='related_test_models'
    )

    for_inline = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    species = models.ForeignKey('Species',
                                to_field="taxonomic_id",
                                db_column="Species",
                                max_length=20, blank=True,
                                null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'ExampleFK'
        verbose_name_plural = 'example'

class Location(models.Model):
    name = models.CharField(max_length=200)
    species = models.ForeignKey(Species)
    tissue = ChainedForeignKey(
        Tissues,
        chained_field="species",
        chained_model_field="taxonomic_ID",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    miRNA = ChainedForeignKey(
        ExampleFK,
        chained_field="species",
        chained_model_field="species",
        show_all=False,
        auto_choose=False,
        sort=False
    )


    def __unicode__(self):
        return str(self.pk)

    class Meta:
        managed = False

class Gene(models.Model):
    name = models.CharField(db_column='name', max_length=10, blank=True, null=False, primary_key=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Gene'
        verbose_name_plural = ' Genes'

class Contextpp(models.Model): # Target Prediction Output table
    mirna = models.ForeignKey('Mirnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mrna = models.ForeignKey('Mrnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(db_column='Species', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_start = models.CharField(db_column='UTR_Start', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_end = models.CharField(db_column='UTR_End', max_length=20, blank=True, null=True)  # Field name made lowercase.
    site_type = models.CharField(db_column='Site_Type', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contextpp_score = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contextpp'

class PITA(models.Model): # Target Prediction Output table
    mirna = models.ForeignKey('Mirnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mrna = models.ForeignKey('Mrnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(db_column='Species', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_start = models.CharField(db_column='UTR_Start', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_end = models.CharField(db_column='UTR_End', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pita_score = models.CharField(db_column="PITA_score", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pita'


class MiRanda(models.Model): # miRanda Target Prediction Output table
    mirna = models.ForeignKey('Mirnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mrna = models.ForeignKey('Mrnas', max_length=20, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(db_column='Species', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_start = models.CharField(db_column='UTR_start', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utr_end = models.CharField(db_column='UTR_end', max_length=20, blank=True, null=True)  # Field name made lowercase.
    miranda_score = models.CharField(db_column="miRanda_score", max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'miRanda'

