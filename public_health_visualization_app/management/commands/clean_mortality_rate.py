import csv
from django.core.management.base import BaseCommand
from public_health_visualization_app.models import MortalityRate
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Clean and populate Mortality Rate data'

    def handle(self, *args, **kwargs):
        # Open the file with UTF-8 encoding and handle BOM
        with open('static/data/usa_mortality.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            print("CSV Headers:", headers)  # Debug statement to print headers

            rows = list(reader)
            # Sort by 'Year' and get the top 3,000 entries
            rows = sorted(rows, key=lambda x: x.get('Year', ''), reverse=True)[:3000]

            for row in tqdm(rows, desc="Processing rows"):
                year = row.get('Year')
                cause_name = row.get('Cause Name')
                state = row.get('State')
                deaths = row.get('Deaths')
                age_adjusted_rate = row.get('Age-adjusted Death Rate')

                # Handle missing and invalid values
                if year:
                    year = int(year)
                else:
                    continue  # Skip rows without year

                if deaths:
                    deaths = int(deaths)
                else:
                    deaths = None

                if age_adjusted_rate:
                    age_adjusted_rate = round(float(age_adjusted_rate), 2)
                else:
                    age_adjusted_rate = None

                MortalityRate.objects.update_or_create(
                    year=year,
                    cause_name=cause_name,
                    state=state,
                    defaults={
                        'deaths': deaths,
                        'age_adjusted_rate': age_adjusted_rate,
                    }
                )
        self.stdout.write(self.style.SUCCESS("Mortality Rate data populated successfully!"))