from item.models import Course, Topic
from account_auth.models import User
from django.db import transaction
import csv


@transaction.atomic
def import_courses(file):
    REQUIRED_COULMNS = {
        "username", "title", "image", "description",
        "language", "topics", "price", "discount", "published"
    }
    reader = csv.DictReader(
        file.read().decode("utf-8").splitlines()
    )

    if not reader.fieldnames:
        raise ValueError("CSV file is empty.")
    missing_columns = REQUIRED_COULMNS - reader.fieldnames
    if missing_columns:
        raise ValueError(f"Missing Columns: {' ,'.join(missing_columns)}")

    imported = 0
    for row in reader:
        user = User.objects.get(username=row["username"])
        topics = []
        for topic_name in row["topics"].split(','):
            topic_name = topic_name.strip()
            topic, created = Topic.objects.get_or_create(
                name=topic_name
            )
            topics.append(topic)

        course = Course.objects.create(
            author=user,
            title=row['title'].strip(),
            image=row['image'].strip() or None,
            description=row['description'].strip(),
            language=row['language'].strip(),
            price=row['price'] or 0,
            discount=row['discount'] or 0,
            published=row['published'].lower() in {'true', 'yes', '1'}
        )
        course.topics.set(topics)
        imported += 1

    return imported
