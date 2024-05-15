from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Group(models.Model):
    # Add fields to define the Group model (name, description, etc.)
    pass

class Permission(models.Model):
    # Add fields to define the Permission model (name, description, etc.)
    pass

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Agent(AbstractUser): # AGENT
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    groups = models.ManyToManyField(Group, related_name="agent_set")
    user_permissions = models.ManyToManyField(Permission, related_name="agent_permissions")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
#===============================================================================================
class ControlPoint(models.Model):
    name = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    quartier = models.CharField(max_length=255)
    agents = models.ManyToManyField(Agent, through="ControlPointByAgent")

    class Meta:
        verbose_name = "Point de contrôle"
        verbose_name_plural = "Points de contrôle"

class ControlPointByAgent(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    control_point = models.ForeignKey(ControlPoint, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Point de contrôle par agent"
        verbose_name_plural = "Points de contrôle par agents"
        unique_together = ('agent', 'control_point')

class Criteria(models.Model): #infraction
    name = models.CharField(max_length=255, verbose_name="Nom")
    description = models.CharField(max_length=255, verbose_name="Description")

    class Meta:
        verbose_name = "Critère"
        verbose_name_plural = "Critères"

class RoadControl(models.Model):
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    type_piece = models.CharField(max_length=255, verbose_name="Type de pièce")
    license_number = models.CharField(max_length=255, verbose_name="Numéro du permis ou CNI / PASSEPORT")
    type_vehicule = models.CharField(max_length=255, verbose_name="Type de véhicule")
    imatriculation = models.CharField(max_length=255, verbose_name="Imatriculation du véhicule")
    telephone_conducteur = models.CharField(max_length=255, unique=True, verbose_name="Numéro téléphone conducteur")
    criteria = models.ManyToManyField(Criteria , through="CriteriaByControl", verbose_name="Critères")
    control_point = models.ForeignKey(ControlPoint, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Contrôle routier"
        verbose_name_plural = "Contrôles routiers"

class CriteriaByControl(models.Model):

    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    road_control = models.ForeignKey(RoadControl, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Critère par contrôle"
        verbose_name_plural = "Critères par contrôle"
        unique_together = ('criteria', 'road_control')

class Almond(models.Model):
    road_control = models.ForeignKey(RoadControl, on_delete=models.CASCADE)
    montant = models.CharField(max_length=255, verbose_name="Montant")
    paid = models.BooleanField(default=False, verbose_name="Payé")

    class Meta:
        verbose_name = "Amende"
        verbose_name_plural = "Amendes"