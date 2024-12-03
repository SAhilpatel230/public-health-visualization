import csv
from django.core.management.base import BaseCommand
from public_health_visualization_app.models import ImmunizationCoverage
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Clean and populate Immunization Coverage data'

    def handle(self, *args, **kwargs):
        # Open the file with UTF-8 encoding and handle BOM
        with open('static/data/usa_vaccination_coverage.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            print("CSV Headers:", headers)  # Debug statement to print headers

            rows = list(reader)
            # Sort by 'Birth Year/Birth Cohort' and get the top 3,000 entries
            rows = sorted(rows, key=lambda x: x.get('Birth Year/Birth Cohort', ''), reverse=True)[:3000]

            for row in tqdm(rows, desc="Processing rows"):
                vaccine = row.get('Vaccine')
                dose = row.get('Dose')
                geography = row.get('Geography')
                birth_year = row.get('Birth Year/Birth Cohort')
                estimate = row.get('Estimate (%)')
                sample_size = row.get('Sample Size')

                # Handle missing and invalid values
                if estimate:
                    estimate = round(float(estimate), 2)
                else:
                    estimate = None

                if sample_size:
                    try:
                        sample_size = int(sample_size)
                    except ValueError:
                        sample_size = None
                else:
                    sample_size = None

                ImmunizationCoverage.objects.update_or_create(
                    vaccine=vaccine,
                    dose=dose,
                    geography=geography,
                    birth_year=birth_year,
                    defaults={
                        'estimate': estimate,
                        'sample_size': sample_size,
                    }
                )
        self.stdout.write(self.style.SUCCESS("Immunization Coverage data populated successfully!"))