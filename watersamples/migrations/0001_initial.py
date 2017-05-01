# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 16:26
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Laboratory title')),
                ('address', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Laboratories',
            },
        ),
        migrations.CreateModel(
            name='OrganizationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_title', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WaterIntakeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('date_laboratory', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.IntegerField()),
                ('status', models.IntegerField(choices=[(0, 'New intake'), (1, 'Investigated intake')])),
                ('classification', models.IntegerField(choices=[(1, 'First class source'), (2, 'Second class source'), (3, 'Third class source'), (4, 'Unfit source')])),
                ('classification_reason_field', models.CharField(blank=True, max_length=50, null=True)),
                ('smell_20_celsium', models.IntegerField(blank=True, choices=[(0, '0 - Not found'), (1, '1 - Detected by taster'), (2, '2 - Detected by consumer'), (3, '3 - Easily detected'), (4, '4 - Strong smell and taste'), (5, '5 - Undrinkable')], null=True)),
                ('smell_60_celsium', models.IntegerField(blank=True, choices=[(0, '0 - Not found'), (1, '1 - Detected by taster'), (2, '2 - Detected by consumer'), (3, '3 - Easily detected'), (4, '4 - Strong smell and taste'), (5, '5 - Undrinkable')], null=True)),
                ('aftertaste', models.IntegerField(blank=True, choices=[(0, '0 - Not found'), (1, '1 - Detected by taster'), (2, '2 - Detected by consumer'), (3, '3 - Easily detected'), (4, '4 - Strong smell and taste'), (5, '5 - Undrinkable')], null=True)),
                ('color', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(300)])),
                ('dry_residue', models.IntegerField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0), verbose_name='Dry residue (mg/dm3)')),
                ('pH', models.FloatField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0), verbose_name='pH)')),
                ('rigidity', models.IntegerField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0), verbose_name='Dry residue (mg/dm3)')),
                ('nitrates', models.IntegerField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
                ('chlorides', models.IntegerField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
                ('sulphates', models.IntegerField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
                ('iron_overall', models.FloatField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
                ('manganese', models.FloatField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
                ('fluorine', models.FloatField(blank=True, null=True, validators=django.core.validators.MinValueValidator(0))),
            ],
        ),
        migrations.CreateModel(
            name='WaterIntakePoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('geolocation', django_google_maps.fields.GeoLocationField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='waterintakeinfo',
            name='intake_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watersamples.WaterIntakePoint'),
        ),
        migrations.AddField(
            model_name='waterintakeinfo',
            name='laboratory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watersamples.Laboratory'),
        ),
        migrations.AddField(
            model_name='waterintakeinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
