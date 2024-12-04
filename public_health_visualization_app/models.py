from django.db import models

class LifeExpectancy(models.Model):
    state = models.CharField(max_length=100)
    county = models.CharField(max_length=100, null=True, blank=True)
    census_tract = models.CharField(max_length=50, null=True, blank=True)
    life_expectancy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    standard_error = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return f"{self.state} - {self.life_expectancy}"

class ImmunizationCoverage(models.Model):
    vaccine = models.CharField(max_length=100)
    dose = models.CharField(max_length=50)
    geography = models.CharField(max_length=100)
    birth_year = models.CharField(max_length=10)
    estimate = models.DecimalField(max_digits=5, decimal_places=2)
    sample_size = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.geography} - {self.vaccine}"

class MortalityRate(models.Model):
    year = models.IntegerField()
    cause_name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    deaths = models.PositiveIntegerField()
    age_adjusted_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.state} - {self.cause_name} ({self.year})"
