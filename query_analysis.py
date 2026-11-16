import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import Q

from requests_app.models import Category, ServiceRequest


user_model = get_user_model()
requester, _ = user_model.objects.get_or_create(username="w3_synthetic_requester")
electrical, _ = Category.objects.get_or_create(
    name="Electrical",
    defaults={"description": "Synthetic Week 3 query-analysis category"},
)
ict, _ = Category.objects.get_or_create(
    name="ICT Support",
    defaults={"description": "Synthetic Week 3 query-analysis category"},
)

ServiceRequest.objects.filter(title__startswith="W3 Synthetic - ").delete()

categories = (electrical, ict)
statuses = (
    ServiceRequest.Status.OPEN,
    ServiceRequest.Status.ASSIGNED,
    ServiceRequest.Status.IN_PROGRESS,
)

for category in categories:
    for status in statuses:
        for number in (1, 2):
            ServiceRequest.objects.create(
                requester=requester,
                category=category,
                title=f"W3 Synthetic - {category.name} - {status} - {number}",
                description="Synthetic record created only for Week 3 query analysis.",
                location="Synthetic Laboratory",
                priority=((number + len(status)) % 5) + 1,
                status=status,
            )

queryset = ServiceRequest.objects.filter(
    Q(status=ServiceRequest.Status.OPEN)
    | Q(status=ServiceRequest.Status.ASSIGNED),
    category=electrical,
).order_by("priority", "created_at")

print("DATABASE VENDOR:", connection.vendor)
print("SYNTHETIC RECORD COUNT:", ServiceRequest.objects.filter(title__startswith="W3 Synthetic - ").count())
print("QUERY RESULT COUNT:", queryset.count())
print("GENERATED SQL:")
print(queryset.query)
print("QUERY PLAN:")
print(queryset.explain())

if connection.vendor != "mysql":
    print("The displayed plan is for this configured database, not MySQL. Run this script with the lab MySQL settings to record the MySQL plan.")
