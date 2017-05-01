import inspect

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_google_maps import fields as map_fields

from watersamples.bl import Classifier as classifier_class
from watersamples.utils import (
    SOURCE_CLASSIFICATION_CHOICES, INTENSITY_CHOICES,
    STATUS_CHOICES, STATUS_NEW, STATUS_CHECKED,
)


class OrganizationInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_title = models.CharField(max_length=100)

    def __str__(self):
        return self.organization_title


class Laboratory(models.Model):
    class Meta:
        verbose_name_plural = "Laboratories"
    title = models.CharField("Laboratory title", max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return "{title} - {address}".format(title=self.title, address=self.address)


class WaterIntakePoint(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField()

    def __str__(self):
        return "{name} ({address})".format(name=self.name, address=self.address)

DEFAULT_VALUE = dict(
    validators=MinValueValidator(0),
    blank=True,
    null=True,
)


class WaterIntakeInfo(models.Model):
    user = models.ForeignKey(User)
    laboratory = models.ForeignKey("Laboratory")
    intake_point = models.ForeignKey("WaterIntakePoint")
    date_taken = models.DateTimeField(auto_now_add=True)
    date_laboratory = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES.items())

    classification = models.IntegerField(
        choices=SOURCE_CLASSIFICATION_CHOICES.items()
    )
    classification_reason_field = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    smell_20_celsium = models.IntegerField(
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )
    smell_60_celsium = models.IntegerField(
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )
    aftertaste = models.IntegerField(
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )

    color = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300)
        ]
    )

    dry_residue = models.IntegerField('Dry residue (mg/dm3)', **DEFAULT_VALUE)
    pH = models.FloatField('pH)', **DEFAULT_VALUE)
    rigidity = models.IntegerField('Dry residue (mg/dm3)', **DEFAULT_VALUE)
    nitrates = models.IntegerField(**DEFAULT_VALUE)
    chlorides = models.IntegerField(**DEFAULT_VALUE)
    sulphates = models.IntegerField(**DEFAULT_VALUE)
    iron_overall = models.FloatField(**DEFAULT_VALUE)
    manganese = models.FloatField(**DEFAULT_VALUE)
    fluorine = models.FloatField(**DEFAULT_VALUE)

    def __str__(self):
        return "Intake from {user} for {laboratory} - {classification}".format(
            user=self.user.username,
            laboratory=self.laboratory.title,
            classification=SOURCE_CLASSIFICATION_CHOICES[self.classification],
        )

    def classify(self):
        classifications = []

        for field_name, classifier in inspect.getmembers(classifier_class, predicate=inspect.ismethod):
            value = getattr(self, field_name, None)
            if not value:
                continue
            classifications.append({
                'field_name': field_name,
                'classification': classifier(value),
            })
        return max(classifications, key=lambda c: c['classification'])

    def save(self, *args, **kwargs):
        classification_data = self.classify()
        self.classification = classification_data['classification']
        self.classification_reason_field = classification_data['field_name']
        self.status = STATUS_CHECKED if all([
            self.temperature,
            self.smell_20_celsium,
            self.smell_60_celsium,
            self.aftertaste,
            self.color,
            self.dry_residue,
            self.pH,
            self.rigidity,
            self.nitrates,
            self.chlorides,
            self.sulphates,
            self.iron_overall,
            self.manganese,
            self.fluorine,
        ]) else STATUS_NEW
        super(WaterIntakeInfo, self).save(*args, **kwargs)
