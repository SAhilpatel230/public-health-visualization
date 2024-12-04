from django.contrib import admin
from .models import LifeExpectancy, ImmunizationCoverage, MortalityRate

@admin.register(LifeExpectancy)
class LifeExpectancyAdmin(admin.ModelAdmin):
    list_display = ('state', 'county', 'census_tract', 'life_expectancy', 'standard_error')
    search_fields = ('state', 'county', 'census_tract')
    list_filter = ('state',)
    ordering = ('state', 'census_tract')

@admin.register(ImmunizationCoverage)
class ImmunizationCoverageAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'dose', 'geography', 'birth_year', 'estimate', 'sample_size')
    search_fields = ('vaccine', 'geography', 'birth_year')
    list_filter = ('vaccine', 'dose')
    ordering = ('vaccine', 'geography', 'birth_year')

@admin.register(MortalityRate)
class MortalityRateAdmin(admin.ModelAdmin):
    list_display = ('year', 'cause_name', 'state', 'deaths', 'age_adjusted_rate')
    search_fields = ('cause_name', 'state', 'year')
    list_filter = ('year', 'state')
    ordering = ('year', 'state')
