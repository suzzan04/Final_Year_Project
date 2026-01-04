from django.db import models


#models creaed for database


class RentalHouse(models.Model):
    house_type = models.CharField(max_length=100)
    house_size = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.house_type} - {self.city}"
