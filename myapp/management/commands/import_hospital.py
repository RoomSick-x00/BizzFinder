import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from myapp.models import Hospital

def safe_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        return None

class Command(BaseCommand):
    help = 'Import hospitals from justdial.csv into the database'

    def handle(self, *args, **kwargs):
        path = 'myapp/justdial.csv'  # Update path if necessary
        count = 0

        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    name = row['jsx-ee3d18659dbf4034'].strip()
                    address = row['jsx-ee3d18659dbf4034 5'].strip()
                    phone = row['jsx-ee3d18659dbf4034 9'].strip()[:20]  # Truncate to fit model max_length
                    rating = safe_decimal(row['jsx-ee3d18659dbf4034 3'])
                    review_count = row['jsx-ee3d18659dbf4034 4'].replace('Ratings', '').replace(',', '').strip()
                    specialties = ', '.join([
                        row.get('jsx-ee3d18659dbf4034 6', '').strip(),
                        row.get('jsx-ee3d18659dbf4034 7', '').strip()
                    ]).strip(', ')

                    hospital, created = Hospital.objects.get_or_create(
                        name=name,
                        defaults={
                            'address': address,
                            'phone': phone,
                            'rating': rating if rating is not None else 0,
                            'review_count': int(review_count) if review_count.isdigit() else 0,
                            'specialties': specialties,
                            'description': '',  # Optional
                        }
                    )

                    if created:
                        count += 1
                        self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
                    else:
                        self.stdout.write(f"Skipped (already exists): {name}")

                except Exception as e:
                    self.stderr.write(f"Error processing row: {e}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete. {count} new hospitals added."))