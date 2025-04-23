import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from myapp.models import Restaurant

def safe_decimal(value):
    try:
        return Decimal(value.strip())
    except (InvalidOperation, ValueError, AttributeError):
        return None

class Command(BaseCommand):
    help = 'Import restaurants from hamirpur_restaurants.csv into the database'

    def handle(self, *args, **kwargs):
        count = 0
        try:
            with open(r'myapp/Restaurants_in_Hamirpur-Himachal-Pradesh_2025-04-10-21-08-35.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        name = row['Name'].strip()
                        address = row['Address'].strip()
                        phone = row['Business Phone'].strip() or row['Justdial Phone'].strip()
                        hours = row['Hours of operations'].strip()
                        rating = safe_decimal(row['Rating'])
                        review_count = row['Reviews'].replace(',', '').strip()

                        restaurant, created = Restaurant.objects.get_or_create(
                            name=name,
                            defaults={
                                'address': address,
                                'phone': phone,
                                'opening_hours': hours,
                                'rating': rating if rating is not None else 0,
                                'review_count': int(review_count) if review_count.isdigit() else 0,
                                'description': '',
                            }
                        )
                        if created:
                            count += 1
                            self.stdout.write(self.style.SUCCESS(f"Added: {name}"))
                        else:
                            self.stdout.write(f"Skipped (already exists): {name}")
                    except Exception as e:
                        self.stderr.write(f"Error processing {row.get('Name', 'Unknown')}: {e}")
        except FileNotFoundError:
            self.stderr.write("❌ CSV file not found.")
        except Exception as e:
            self.stderr.write(f"❌ Unexpected error: {e}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete. {count} new restaurants added."))
