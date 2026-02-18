from django.db import models

class RentalHouse(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    district = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    beds = models.IntegerField()
    baths = models.IntegerField()
    house_type = models.CharField(max_length=100)
    
    # 🔥 Image field
    image = models.ImageField(upload_to="houses/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
