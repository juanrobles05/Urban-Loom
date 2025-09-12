from django.core.management.base import BaseCommand
from catalog.models import Collection

class Command(BaseCommand):
    help = 'Load sample collections data'

    def handle(self, *args, **options):
        collections_data = [
            {
                "name": "WINTER SHADOWS",
                "season": "FW24",
                "description": "Dark aesthetics meet winter functionality",
                "pieces": 24,
                "status": "AVAILABLE",
                "is_current": True,
            },
            {
                "name": "NEON NIGHTS",
                "season": "SS24",
                "description": "Vibrant colors for the urban nightlife",
                "pieces": 18,
                "status": "LIMITED",
                "is_current": False,
            },
            {
                "name": "CONCRETE DREAMS",
                "season": "FW23",
                "description": "Industrial-inspired urban essentials",
                "pieces": 32,
                "status": "SOLD OUT",
                "is_current": False,
            },
            {
                "name": "METRO PULSE",
                "season": "SS23",
                "description": "Technical wear for city commuters",
                "pieces": 21,
                "status": "AVAILABLE",
                "is_current": False,
            },
            {
                "name": "UNDERGROUND",
                "season": "FW22",
                "description": "Raw street culture essentials",
                "pieces": 15,
                "status": "ARCHIVE",
                "is_current": False,
            },
            {
                "name": "SKYLINE",
                "season": "SS22",
                "description": "Elevated streetwear for urban heights",
                "pieces": 28,
                "status": "ARCHIVE",
                "is_current": False,
            },
        ]

        for collection_data in collections_data:
            collection, created = Collection.objects.get_or_create(
                name=collection_data['name'],
                season=collection_data['season'],
                defaults=collection_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created collection "{collection.name} - {collection.season}"'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Collection "{collection.name} - {collection.season}" already exists'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded all collections data')
        )
