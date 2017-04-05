from django.contrib.auth.models import User
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


class WaterIntakeInfo(models.Model):
    info = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    laboratory = models.ForeignKey("Laboratory")
    intake_point = models.ForeignKey("WaterIntakePoint")
    date_taken = models.DateTimeField(auto_now_add=True)
    date_laboratory = models.DateTimeField(auto_now_add=True)
    temperature = models.CharField(max_length=200)

    smell_20_celsium = models.CharField(max_length=200, blank=True, null=True)
    smell_60_celsium = models.CharField(max_length=200, blank=True, null=True)
    aftertaste = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)

    dry_residue = models.CharField(max_length=200, blank=True, null=True)
    pH = models.CharField(max_length=200, blank=True, null=True)
    rigidity = models.CharField(max_length=200, blank=True, null=True)
    nitrates = models.CharField(max_length=200, blank=True, null=True)
    chlorides = models.CharField(max_length=200, blank=True, null=True)
    sulphates = models.CharField(max_length=200, blank=True, null=True)
    iron_overall = models.CharField(max_length=200, blank=True, null=True)
    manganese = models.CharField(max_length=200, blank=True, null=True)
    fluorine = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "проба от {user} для {laboratory}".format(user=self.user.username, laboratory=self.laboratory.name)
