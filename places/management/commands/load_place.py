from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Image, Place
import requests
import os


class Command(BaseCommand):
    help = 'Load a place ftom a json file'

    def add_arguments(self, parser):
        parser.add_argument('json', help='Place json url')

    def handle(self, *args, **options):
        response = requests.get(options['json'])
        response.raise_for_status()
        new_place = response.json()

        place, created = Place.objects.get_or_create(
            title=new_place['title'],
            description_short=new_place['description_short'],
            description_long=new_place['description_long'],
            latitude=new_place['coordinates']['lat'],
            longitude=new_place['coordinates']['lng'],
        )

        image_files = os.listdir('media/')
        for image in image_files:
            if image.startswith(place.title.replace(' ', '_')):
                os.remove(f'media/{image}')
        old_images_in_db = Image.objects.filter(place=place)
        old_images_in_db.delete()

        for pic_number, image_url in enumerate(new_place['imgs']):
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.objects.create(place=place)
            image.image.save(
                f'{place.title}_{pic_number}.jpg',
                ContentFile(response.content),
                save=True
            )
        if created:
            self.stdout.write(f'New place {place.title} has been loaded.')
        else:
            self.stdout.write(
                f'The place {place.title} already exists, all photos have been replaced.'
            )
