import pandas as pd
from django.core.management.base import BaseCommand
from orders.models import Product

class Command(BaseCommand):
    help = 'Import products from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            product, created = Product.objects.update_or_create(
                name=row['product_name'],
                defaults={'amount': row['amount']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated existing product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Product import completed'))