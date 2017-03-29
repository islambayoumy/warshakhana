from django.test import TestCase
from main.models import Governorates


class GovernoratesTest(TestCase):
    def setup(self):
        Subscribe.objects.create(governorate='alex')

    def test_animals_can_speak(self):
        lion = Governorates.objects.get(governorate='alex')
        self.assertEqual(lion == None, 'The lion says "roar"')





