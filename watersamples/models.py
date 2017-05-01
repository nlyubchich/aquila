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
    validators=[MinValueValidator(0)],
    blank=True,
    null=True,
)


class WaterIntakeInfo(models.Model):
    user = models.ForeignKey(User, editable=False)
    laboratory = models.ForeignKey("Laboratory")
    intake_point = models.ForeignKey("WaterIntakePoint")
    date_taken = models.DateField(auto_now_add=True, blank=False, null=False)
    date_laboratory = models.DateField(blank=True, null=True)
    temperature = models.IntegerField('Temperature (points)')
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
        'Smell 20 celsium (points)',
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )
    smell_60_celsium = models.IntegerField(
        'Smell 60 celsium (points)',
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )
    aftertaste = models.IntegerField(
        'Aftertaste (points)',
        blank=True,
        null=True,
        choices=INTENSITY_CHOICES.items()
    )

    color = models.IntegerField(
        'Color (degrees)',
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(300)
        ]
    )

    dry_residue = models.IntegerField('Dry residue (mg/dm3)', **DEFAULT_VALUE)
    pH = models.FloatField('Potential of hydrogen (PH)', **DEFAULT_VALUE)
    rigidity = models.IntegerField('Rigidity (mg-eq/dm3)', **DEFAULT_VALUE)
    nitrates = models.IntegerField('Nitrates (mg/dm3)', **DEFAULT_VALUE)
    chlorides = models.IntegerField('Chlorides (mg/dm3)', **DEFAULT_VALUE)
    sulphates = models.IntegerField('Sulphates (mg/dm3)', **DEFAULT_VALUE)
    iron_overall = models.FloatField('Iron (mg/dm3)', **DEFAULT_VALUE)
    manganese = models.FloatField('Manganese (mg/dm3)', **DEFAULT_VALUE)
    fluorine = models.FloatField('Fluorine (mg/dm3)', **DEFAULT_VALUE)

    def __str__(self):
        return "Intake from {intake_point} at {date} - {classification}".format(
            intake_point=self.intake_point.name,
            date=self.date_taken,
            classification=SOURCE_CLASSIFICATION_CHOICES[self.classification] if self.status == STATUS_CHECKED else 'NEW',
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
