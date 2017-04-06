import inspect

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_google_maps import fields as map_fields

from watersamples.bl import SurfaceClassifier, UndergroundClassifier
from watersamples.utils import SOURCE_TYPE_CHOICES, SOURCE_CLASSIFICATION_CHOICES, INTENSITY_CHOICES, \
    UNDERGROUND_SOURCE_TYPE, SURFACE_SOURCE_TYPE, STATUS_CHOICES, STATUS_NEW, STATUS_CHECKED


class OrganizationInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_title = models.CharField(max_length=100)

    def __str__(self):
        return self.organization_title


class Laboratory(models.Model):
    name = models.CharField("Laboratory's name", max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return "{name} - {address}".format(name=self.name, address=self.address)


class WaterIntakePoint(models.Model):
    name = models.CharField(max_length=200)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField()

    def __str__(self):
        return "{name} ({address})".format(name=self.name, address=self.address)


class WaterIntakeInfo(models.Model):
    user = models.ForeignKey(User)
    laboratory = models.ForeignKey("Laboratory")
    intake_point = models.ForeignKey("WaterIntakePoint")
    date_taken = models.DateTimeField(auto_now_add=True)
    date_laboratory = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField()
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES.items())
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

    dry_residue = models.IntegerField(blank=True, null=True)
    pH = models.FloatField(blank=True, null=True)
    rigidity = models.IntegerField(blank=True, null=True)
    nitrates = models.IntegerField(blank=True, null=True)
    chlorides = models.IntegerField(blank=True, null=True)
    sulphates = models.IntegerField(blank=True, null=True)
    iron_overall = models.FloatField(blank=True, null=True)
    manganese = models.FloatField(blank=True, null=True)
    fluorine = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "Проба от {user} для {laboratory} - {classification}".format(
            user=self.user.username,
            laboratory=self.laboratory.name,
            classification=SOURCE_CLASSIFICATION_CHOICES[self.classification],
        )

    def classify(self):
        classifications = []

        classifier_class = None
        if self.source_type == UNDERGROUND_SOURCE_TYPE:
            classifier_class = UndergroundClassifier
        elif self.source_type == SURFACE_SOURCE_TYPE:
            classifier_class = SurfaceClassifier

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
            self.source_type,
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
