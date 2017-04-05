import inspect
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    market_on_map = models.CharField(max_length=200)

    def __str__(self):
        return "{market_on_map}".format(market_on_map=self.market_on_map)


class BaseClassifier:
    @classmethod
    def smell_or_taste(cls, value):
        return -1

    @classmethod
    def smell_20_celsium(cls, value):
        return cls.smell_or_taste(value)

    @classmethod
    def smell_60_celsium(cls, value):
        return cls.smell_or_taste(value)

    @classmethod
    def aftertaste(cls, value):
        return cls.smell_or_taste(value)

    @classmethod
    def dry_residue(cls, value):
        if 1000 <= value <= 1500:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def rigidity(cls, value):
        if 7 <= value <= 10:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def chlorides(cls, value):
        if value == 350:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def sulphates(cls, value):
        if value == 500:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def nitrates(cls, value):
        if value == 45:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def manganese(cls, value):
        if value > 2.0:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        if value > 1.0:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value > 0.1:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS


class SurfaceClassifier(BaseClassifier):
    @classmethod
    def smell_or_taste(cls, value):
        if value > 4:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        if value > 3:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value > 2:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS

    @classmethod
    def color(cls, value):
        if value > 200:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        if value > 120:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value > 35:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS

    @classmethod
    def temperature(cls, value):
        if 8 <= value <= 25:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def ph(cls, value):
        if 6.5 <= value <= 8.5:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def iron_overall(cls, value):
        if value > 5:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        if value > 3:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value > 1:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS

    @classmethod
    def fluorine(cls, value):
        if value > 0.5:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value >= 0.1:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        if value < 0.1:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS


class UndergroundClassifier(BaseClassifier):
    @classmethod
    def smell_or_taste(cls, value):
        if value == 2:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def color(cls, value):
        if value > 50 or value < 20:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS

    @classmethod
    def temperature(cls, value):
        if 8 <= value <= 12:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def ph(cls, value):
        if 6.0 <= value <= 9.0:
            return WaterIntakeInfo.FIRST_SOURCE_CLASS
        return WaterIntakeInfo.UNFIT_SOURCE_CLASS

    @classmethod
    def iron_overall(cls, value):
        if value > 20:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        if value > 10:
            return WaterIntakeInfo.THIRD_SOURCE_CLASS
        if value > 0.3:
            return WaterIntakeInfo.SECOND_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS

    @classmethod
    def fluorine(cls, value):
        if value > 5.0 or value < 1.5:
            return WaterIntakeInfo.UNFIT_SOURCE_CLASS
        return WaterIntakeInfo.FIRST_SOURCE_CLASS


class WaterIntakeInfo(models.Model):
    UNDERGROUND_SOURCE_TYPE = 'underground'
    SURFACE_SOURCE_TYPE = 'surface'
    SOURCE_TYPE_CHOICES = OrderedDict([
        ('underground', 'Underground'),
        ('surface', 'Surface'),
    ])

    FIRST_SOURCE_CLASS = 1
    SECOND_SOURCE_CLASS = 2
    THIRD_SOURCE_CLASS = 3
    UNFIT_SOURCE_CLASS = 4
    SOURCE_CLASSIFICATION_CHOICES = OrderedDict([
        (FIRST_SOURCE_CLASS, 'Перший клас'),
        (SECOND_SOURCE_CLASS, 'Другий клас'),
        (THIRD_SOURCE_CLASS, 'Третій клас'),
        (UNFIT_SOURCE_CLASS, 'Непридатне'),
    ])

    INTENSITY_ZERO = 0
    INTENSITY_ONE = 1
    INTENSITY_SECOND = 2
    INTENSITY_THIRD = 3
    INTENSITY_FOURTH = 4
    INTENSITY_FIFTH = 5
    INTENSITY_CHOICES = OrderedDict([
        (INTENSITY_ZERO, '0 - не виявляються'),
        (INTENSITY_ONE, '1 - виявляються дегустатором'),
        (INTENSITY_SECOND, '2 - виявляються споживачем'),
        (INTENSITY_THIRD, '3 - виявляються легко'),
        (INTENSITY_FOURTH, '4 - сильний запах і присмак'),
        (INTENSITY_FIFTH, '5 - непридатна для пиття'),
    ])

    user = models.ForeignKey(User)
    laboratory = models.ForeignKey("Laboratory")
    intake_point = models.ForeignKey("WaterIntakePoint")
    date_taken = models.DateTimeField(auto_now_add=True)
    date_laboratory = models.DateTimeField(auto_now_add=True)
    temperature = models.IntegerField()
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPE_CHOICES.items())

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
            classification=WaterIntakeInfo.SOURCE_CLASSIFICATION_CHOICES[self.classification],
        )

    def classify(self):
        classifications = []

        classifier_class = None
        if self.source_type == WaterIntakeInfo.UNDERGROUND_SOURCE_TYPE:
            classifier_class = UndergroundClassifier
        elif self.source_type == WaterIntakeInfo.SURFACE_SOURCE_TYPE:
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
        super(WaterIntakeInfo, self).save(*args, **kwargs)
