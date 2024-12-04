import csv
from django.core.management.base import BaseCommand
from public_health_visualization_app.models import LifeExpectancy
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Clean and populate Life Expectancy data'

    def handle(self, *args, **kwargs):
        with open('static/data/usa_life_expectancy.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            print("CSV Headers:", headers)  # Debug statement to print headers

            normalized_rows = [{key.strip(): value for key, value in row.items()} for row in reader]
            # Sort by 'Census Tract Number' and get the top 3,000 entries
            normalized_rows = sorted(normalized_rows, key=lambda x: x.get('Census Tract Number', ''), reverse=True)[:3000]

            for row in tqdm(normalized_rows, desc="Processing rows"):
                state = row.get('State')
                if state is None:
                    print("Row with missing 'State':", row)  # Debug statement for missing 'State'
                    continue

                county = row.get('County') if row.get('County') != "(blank)" else None
                census_tract = row.get('Census Tract Number')
                life_expectancy = row.get('Life Expectancy')
                standard_error = row.get('Life Expectancy Standard Error')

                # Handle missing and invalid values
                if life_expectancy:
                    life_expectancy = round(float(life_expectancy), 2)
                else:
                    life_expectancy = None

                if standard_error:
                    standard_error = round(float(standard_error), 3)
                else:
                    standard_error = None

                LifeExpectancy.objects.update_or_create(
                    state=state,
                    census_tract=census_tract,
                    defaults={
                        'county': county,
                        'life_expectancy': life_expectancy,
                        'standard_error': standard_error,
                    }
                )
        self.stdout.write(self.style.SUCCESS("Life Expectancy data populated successfully!"))