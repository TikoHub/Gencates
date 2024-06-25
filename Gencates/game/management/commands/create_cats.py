from django.core.management.base import BaseCommand
from game.models import Cat

class Command(BaseCommand):
    help = 'Create initial cats'

    def handle(self, *args, **kwargs):
        # Удаляем всех существующих котов
        Cat.objects.all().delete()

        # Создаем новых котов
        cats_data = [
            {"name": "Forest Moggy", "income": 0.1, "income_multiplier": 1.0, "selling_price": 1.0, "selling_price_multiplier": 1.0, "life_span": 1.5, "fertility": 2, "max_fertility": 7, "climate": "Any", "humidity": "Any"},
            {"name": "Desert Moggy", "income": 0.1, "income_multiplier": 1.0, "selling_price": 1.0, "selling_price_multiplier": 1.0, "life_span": 1.5, "fertility": 2, "max_fertility": 7, "climate": "Any", "humidity": "Any"},
            {"name": "Siamese", "income": 1, "income_multiplier": 10.0, "selling_price": 10.0, "selling_price_multiplier": 10.0, "life_span": 3, "fertility": 2, "max_fertility": 6, "climate": "Cold", "humidity": "Dry"},
            {"name": "Persian", "income": 1.5, "income_multiplier": 15.0, "selling_price": 5.0, "selling_price_multiplier": 5.0, "life_span": 4, "fertility": 2, "max_fertility": 6, "climate": "Warm", "humidity": "Dry"},
            {"name": "Maine Coon", "income": 2.5, "income_multiplier": 25.0, "selling_price": 2.5, "selling_price_multiplier": 2.5, "life_span": 5, "fertility": 2, "max_fertility": 6, "climate": "Warm", "humidity": "Humid"},
            {"name": "Ragdoll", "income": 10, "income_multiplier": 100.0, "selling_price": 100.0, "selling_price_multiplier": 100.0, "life_span": 6, "fertility": 2, "max_fertility": 5, "climate": "Cold +", "humidity": "Dry +"},
            {"name": "Peterbald", "income": 15, "income_multiplier": 150.0, "selling_price": 50.0, "selling_price_multiplier": 50.0, "life_span": 8, "fertility": 2, "max_fertility": 4, "climate": "Warm +", "humidity": "Dry +"},
            {"name": "Serengeti", "income": 25, "income_multiplier": 250.0, "selling_price": 25.0, "selling_price_multiplier": 25.0, "life_span": 10, "fertility": 2, "max_fertility": 4, "climate": "Warm +", "humidity": "Humid +"},
            {"name": "British Shorthair", "income": 100, "income_multiplier": 1000.0, "selling_price": 1000.0, "selling_price_multiplier": 1000.0, "life_span": 12, "fertility": 2, "max_fertility": 4, "climate": "Cold ++", "humidity": "Dry ++"},
            {"name": "Bengal", "income": 150, "income_multiplier": 1500.0, "selling_price": 500.0, "selling_price_multiplier": 500.0, "life_span": 18, "fertility": 2, "max_fertility": 3, "climate": "Warm ++", "humidity": "Dry ++"},
            {"name": "Sphynx", "income": 250, "income_multiplier": 2500.0, "selling_price": 250.0, "selling_price_multiplier": 250.0, "life_span": 24, "fertility": 2, "max_fertility": 3, "climate": "Warm ++", "humidity": "Humid ++"},
            {"name": "Khao Manee", "income": 1000, "income_multiplier": 10000.0, "selling_price": 10000.0, "selling_price_multiplier": 10000.0, "life_span": 48, "fertility": 2, "max_fertility": 2, "climate": "Cold +++", "humidity": "Dry +++"},
            {"name": "Caracal", "income": 1500, "income_multiplier": 15000.0, "selling_price": 5000.0, "selling_price_multiplier": 5000.0, "life_span": 96, "fertility": 2, "max_fertility": 2, "climate": "Warm +++", "humidity": "Dry +++"},
            {"name": "Savannah", "income": 2500, "income_multiplier": 25000.0, "selling_price": 2500.0, "selling_price_multiplier": 2500.0, "life_span": 144, "fertility": 2, "max_fertility": 2, "climate": "Warm +++", "humidity": "Humid +++"},
        ]

        for cat_data in cats_data:
            Cat.objects.create(**cat_data)

        self.stdout.write(self.style.SUCCESS('Successfully created initial cats'))
