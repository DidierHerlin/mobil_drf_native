from django.db import models

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cin = models.CharField(max_length=20)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
