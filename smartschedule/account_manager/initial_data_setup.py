from .models import Hobby

"""
File for creating database entries in the Hobbie table.

To populate the table in the console, you must enter:
python manage.py shell
from account_manager.initial_data_setup import populate_hobbies
populate_hobbies()

"""

hobbies_to_add = [
    {"name": "Cycling", "image_url": "https://media.istockphoto.com/id/1269161415/vector/bicycle-cycling-ride-icon-simple-vector-on-isolated-white-background.webp?s=1024x1024&w=is&k=20&c=W-in-zigYmf7utBuNUVwTym0jqrTHqFZWWZPg_13nno="},
    {"name": "Swimming", "image_url": "https://cdn.pixabay.com/photo/2017/01/31/20/36/swimming-2027088_1280.png"},
    {"name": "Painting", "image_url": "https://cdn.pixabay.com/photo/2016/03/31/17/39/art-1293813_1280.png"},
    {"name": "Reading", "image_url": "https://media.istockphoto.com/id/1464137866/vector/group-of-raised-people-hands-holding-books.webp?s=1024x1024&w=is&k=20&c=W0lkSXXVKeFwbBJbsSNylUOipgGarX1O9xSmioVR-A0="},
    {"name": "Cooking", "image_url": "https://cdn.pixabay.com/photo/2014/04/03/00/38/grilling-308914_1280.png"},
    {"name": "Photography", "image_url": "https://cdn.pixabay.com/photo/2019/03/30/20/27/camera-4091991_1280.png"},
    {"name": "Gardening", "image_url": "https://cdn.pixabay.com/photo/2022/03/24/16/30/gardener-7089417_1280.png"},
    {"name": "Yoga", "image_url": "https://cdn.pixabay.com/photo/2013/07/12/18/31/yoga-153436_1280.png"},
    {"name": "Playing Guitar", "image_url": "https://cdn.pixabay.com/photo/2014/04/03/10/01/guitar-309644_1280.png"},
    {"name": "Hiking", "image_url": "https://cdn.pixabay.com/photo/2014/04/03/10/03/climber-309729_1280.png"}
]



def populate_hobbies():
    if not Hobby.objects.exists():
        for hobby_data in hobbies_to_add:
            Hobby.objects.create(**hobby_data)
        print("Hobbies added to the database.")
    else:
        print("Hobbies table is already populated.")
