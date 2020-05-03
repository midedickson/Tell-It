import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tellit.settings")
django.setup()

from faker import Faker

from blog.models import Post

from django.contrib.auth.models import User

from django.utils import timezone

def create_post(N):
    fake = Faker()
    for _ in range(N):
        id = random.randint(1, 8)
        title = fake.name()
        Post.published.create(
            title = title + " Post!!!",
            author = User.objects.get(id=id),
            slug = "-".join(title.lower().split()),
            body = fake.text(),
            created = timezone.now(),
            updated = timezone.now(),
            status = 'published',
        )

create_post(20)
print("DATA IS POPULATED SUCCESSFULLY!")