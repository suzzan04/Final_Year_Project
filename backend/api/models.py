from django.db import models


class RentalHouse(models.Model):
    title = models.CharField(max_length=255)


    price = models.IntegerField()
    location = models.CharField(max_length=255)

    beds = models.IntegerField()
    baths = models.IntegerField()

    house_type = models.CharField(max_length=100)


    district = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)

  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.district}"
