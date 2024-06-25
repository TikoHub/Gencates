from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import random
import uuid


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or str(self.user_id)


class Cat(models.Model):
    CLIMATE_CHOICES = [
        ('Cold', 'Cold'),
        ('Warm', 'Warm'),
        ('Cold+', 'Cold +'),
        ('Warm+', 'Warm +'),
        ('Cold++', 'Cold ++'),
        ('Warm++', 'Warm ++'),
        ('Cold+++', 'Cold +++'),
        ('Warm+++', 'Warm +++'),
    ]

    HUMIDITY_CHOICES = [
        ('Dry', 'Dry'),
        ('Humid', 'Humid'),
        ('Dry+', 'Dry +'),
        ('Humid+', 'Humid +'),
        ('Dry++', 'Dry ++'),
        ('Humid++', 'Humid ++'),
        ('Dry+++', 'Dry +++'),
        ('Humid+++', 'Humid +++'),
    ]

    name = models.CharField(max_length=100)
    income = models.FloatField(default=0.1)
    income_multiplier = models.FloatField(default=1.0)
    selling_price = models.FloatField(default=1.0)
    selling_price_multiplier = models.FloatField(default=1.0)
    life_span = models.FloatField(default=1.5)  # Life span in hours
    fertility = models.IntegerField(default=2)
    max_fertility = models.IntegerField(default=7)
    climate = models.CharField(max_length=20, choices=CLIMATE_CHOICES, default='Any')
    humidity = models.CharField(max_length=20, choices=HUMIDITY_CHOICES, default='Any')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    cats = models.ManyToManyField(Cat, related_name='owners')
    level = models.IntegerField(default=1)
    referral_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username


class Incubator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_spawn_time = models.DateTimeField(default=timezone.now)

    def spawn_cat(self):
        now = timezone.now()
        if now - self.last_spawn_time >= datetime.timedelta(minutes=1):  # Для тестов 1 минута
            new_cat_name = random.choice(["Desert Moggy", "Forest Moggy"])
            new_cat = Cat.objects.create(name=new_cat_name, level=1, income=0.1, income_multiplier=1.0, selling_price=1.0, selling_price_multiplier=1.0, life_span=1.5, fertility=2, max_fertility=7, climate='Any', humidity='Any')
            self.user.userprofile.cats.add(new_cat)
            self.last_spawn_time = now
            self.save()


class Storage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)


class Crossbreeder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cats = models.ManyToManyField(Cat, related_name='crossbreeders')

    def breed_cats(self):
        if self.cats.count() >= 2:
            cat1, cat2 = self.cats.all()[:2]
            new_cat_name = self.determine_breed(cat1, cat2)
            new_cat = Cat.objects.create(name=new_cat_name, level=max(cat1.level, cat2.level) + 1, income=(cat1.income + cat2.income) // 2, income_multiplier=1.0, selling_price=1.0, selling_price_multiplier=1.0, life_span=1.5, fertility=2, max_fertility=7, climate='Any', humidity='Any')
            self.cats.remove(cat1, cat2)
            cat1.delete()
            cat2.delete()
            self.user.userprofile.cats.add(new_cat)

    def determine_breed(self, cat1, cat2):
        breed_chances = {
            ("Forest Moggy", "Desert Moggy"): [("Desert Moggy", 35), ("Forest Moggy", 35), ("Siamese", 10), ("Persian", 10), ("Maine Coon", 10)],
            ("Forest Moggy", "Siamese"): [("Forest Moggy", 40), ("Siamese", 40), ("Ragdoll", 20)],
            ("Forest Moggy", "Persian"): [("Forest Moggy", 45), ("Persian", 40), ("Peterbald", 15)],
            ("Forest Moggy", "Maine Coon"): [("Forest Moggy", 50), ("Maine Coon", 40), ("Serengeti", 10)],
            ("Forest Moggy", "Ragdoll"): [("Forest Moggy", 45), ("Siamese", 30), ("Ragdoll", 25)],
            ("Forest Moggy", "Peterbald"): [("Forest Moggy", 45), ("Persian", 35), ("Peterbald", 20)],
            ("Forest Moggy", "Serengeti"): [("Forest Moggy", 50), ("Maine Coon", 35), ("Serengeti", 15)],

            ("Desert Moggy", "Desert Moggy"): [("Desert Moggy", 100)],
            ("Desert Moggy", "Siamese"): [("Forest Moggy", 40), ("Siamese", 40), ("Ragdoll", 20)],
            ("Desert Moggy", "Persian"): [("Desert Moggy", 45), ("Persian", 40), ("Peterbald", 15)],
            ("Desert Moggy", "Maine Coon"): [("Desert Moggy", 50), ("Maine Coon", 40), ("Serengeti", 10)],
            ("Desert Moggy", "Ragdoll"): [("Desert Moggy", 45), ("Siamese", 30), ("Ragdoll", 25)],
            ("Desert Moggy", "Peterbald"): [("Desert Moggy", 45), ("Persian", 35), ("Peterbald", 20)],
            ("Desert Moggy", "Serengeti"): [("Desert Moggy", 50), ("Maine Coon", 35), ("Serengeti", 15)],

            ("Siamese", "Siamese"): [("Siamese", 100)],
            ("Siamese", "Persian"): [("Forest Moggy", 2.5), ("Desert Moggy", 2.5), ("Persian", 25), ("Siamese", 25), ("Ragdoll", 25), ("Peterbald", 20)],
            ("Siamese", "Maine Coon"): [("Forest Moggy", 2.5), ("Desert Moggy", 2.5), ("Siamese", 27.5), ("Maine Coon", 27.5), ("Ragdoll", 25), ("Serengeti", 15)],
            ("Siamese", "Ragdoll"): [("Forest Moggy", 5), ("Desert Moggy", 5), ("Siamese", 45), ("Ragdoll", 30), ("British Shorthair", 15)],
            ("Siamese", "Peterbald"): [("Forest Moggy", 11), ("Desert Moggy", 11), ("Siamese", 30), ("Persian", 15), ("Ragdoll", 5), ("Peterbald", 20), ("British Shorthair", 5), ("Bengal", 3)],
            ("Siamese", "Serengeti"): [("Forest Moggy", 12.5), ("Desert Moggy", 12.5), ("Siamese", 30), ("Maine Coon", 15), ("Ragdoll", 8.5), ("Serengeti", 15), ("British Shorthair", 5), ("Sphynx", 1.5)],

            ("Persian", "Persian"): [("Persian", 100)],
            ("Persian", "Maine Coon"): [("Forest Moggy", 2.5), ("Desert Moggy", 2.5), ("Persian", 30), ("Maine Coon", 30), ("Peterbald", 20), ("Serengeti", 15)],
            ("Persian", "Ragdoll"): [("Forest Moggy", 10), ("Desert Moggy", 10), ("Siamese", 17.5), ("Persian", 25), ("Ragdoll", 25), ("Peterbald", 5), ("British Shorthair", 5), ("Bengal", 2.5)],
            ("Persian", "Peterbald"): [("Forest Moggy", 12.5), ("Desert Moggy", 12.5), ("Persian", 40), ("Peterbald", 25), ("Bengal", 10)],
            ("Persian", "Serengeti"): [("Forest Moggy", 16), ("Desert Moggy", 16), ("Persian", 26), ("Maine Coon", 15), ("Peterbald", 7.5), ("Serengeti", 15), ("Bengal", 3), ("Sphynx", 1.5)],

            ("Maine Coon", "Maine Coon"): [("Maine Coon", 100)],
            ("Maine Coon", "Ragdoll"): [("Forest Moggy", 10.5), ("Desert Moggy", 10.5), ("Siamese", 17.5), ("Maine Coon", 25), ("Ragdoll", 25), ("Serengeti", 5), ("British Shorthair", 5), ("Sphynx", 1.5)],
            ("Maine Coon", "Peterbald"): [("Forest Moggy", 14), ("Desert Moggy", 14), ("Maine Coon", 25), ("Persian", 17.5), ("Serengeti", 5), ("Peterbald", 20), ("Sphynx", 1.5), ("Bengal", 3)],
            ("Maine Coon", "Serengeti"): [("Forest Moggy", 20), ("Desert Moggy", 20), ("Maine Coon", 35), ("Serengeti", 20), ("Sphynx", 5)],

            ("Ragdoll", "Ragdoll"): [("Ragdoll", 100)],
            ("Ragdoll", "Peterbald"): [("Siamese", 10), ("Persian", 10), ("Ragdoll", 40), ("Peterbald", 33.5), ("British Shorthair", 5), ("Bengal", 1.5)],
            ("Ragdoll", "Serengeti"): [("Siamese", 10), ("Maine Coon", 7.5), ("Ragdoll", 45), ("Serengeti", 30), ("British Shorthair", 5), ("Sphynx", 2.5)],

            ("Peterbald", "Peterbald"): [("Peterbald", 100)],
            ("Peterbald", "Serengeti"): [("Siamese", 10), ("Maine Coon", 7.5), ("Ragdoll", 45), ("Serengeti", 30), ("British Shorthair", 5), ("Sphynx", 2.5)],

            ("Serengeti", "Serengeti"): [("Serengeti", 100)],

            ("British Shorthair", "British Shorthair"): [("British Shorthair", 100)],
            ("Bengal", "Bengal"): [("Bengal", 100)],
            ("Sphynx", "Sphynx"): [("Sphynx", 100)],
            ("Khao Manee", "Khao Manee"): [("Khao Manee", 100)],
            ("Caracal", "Caracal"): [("Caracal", 100)],
            ("Savannah", "Savannah"): [("Savannah", 100)],
        }
        cat_pair = (cat1.name, cat2.name)
        if cat_pair in breed_chances:
            possible_breeds = breed_chances[cat_pair]
            return self.get_random_breed(possible_breeds)
        return cat1.name

    def get_random_breed(self, possible_breeds):
        total = sum(weight for breed, weight in possible_breeds)
        r = random.uniform(0, total)
        upto = 0
        for breed, weight in possible_breeds:
            if upto + weight >= r:
                return breed
            upto += weight
        return possible_breeds[0][0]


class IncomeRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_rooms')
    name = models.CharField(max_length=100)
    operational_expenditure = models.IntegerField(default=10)  # Пример значения
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class HibernationRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hibernation_rooms')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CatyCoin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance} CatyCoins"
