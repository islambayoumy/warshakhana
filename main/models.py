from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator


''' ............... cars_models model ............... '''
class Cars(models.Model):
    model_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.model_name


''' ............... specializations model ............... '''
class Specializations(models.Model):
    specialization = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Specializations"

    def __str__(self):
        return self.specialization


''' ............... crafts model ............... '''
class Crafts(models.Model):
    craft = models.CharField(max_length=200)
    specialization = models.ForeignKey(Specializations, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Crafts"

    def __str__(self):
        return self.craft


''' ............... governorates model ............... '''
class Governorates(models.Model):
    governorate = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Governorates"

    def __str__(self):
        return self.governorate
    


''' ............... zones model ............... '''
class Zones(models.Model):
    zone = models.CharField(max_length=150)
    governorate = models.ForeignKey(Governorates, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Zones"

    def __str__(self):
        return self.zone


''' ............... workshops model ............... '''
class Workshops(models.Model):
    name = models.CharField(max_length=250)
    owner = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    governorate = models.ForeignKey(Governorates, on_delete=models.CASCADE)
    zone = ChainedForeignKey(
        Zones, 
		chained_field="governorate",
		chained_model_field="governorate", 
		show_all=False, 
		auto_choose=True,
        sort=True
	)
    cars = models.ManyToManyField(Cars)
    specializations = models.ManyToManyField(Specializations)
    crafts = models.ManyToManyField(Crafts)
    is_visible = models.BooleanField(default=True)
    notes = models.TextField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Workshops"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


''' ............... images model ............... '''
class Images(models.Model):
    workshop = models.ForeignKey(Workshops, related_name = 'images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/uploads')

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.image.url


''' ............... contacts model ............... '''
class Contacts(models.Model):
    types = (
        ('M', 'Mobile'),
        ('T', 'Telephone'),
        ('F', 'Fax')
    )

    number = models.CharField(max_length=40, unique=True)
    num_type = models.CharField(max_length=10, choices=types, default='M')
    workshop = models.ForeignKey(Workshops, related_name = 'contacts', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.num_type + ": " + self.number


''' ............... comments model ............... '''
class Comments(models.Model):
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150)
    comment = models.TextField(max_length=255)
    workshop = models.ForeignKey(Workshops, related_name = 'comments', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment  + ': "' + str(self.is_approved) + '"'


''' ............... rates model ............... '''
class Rates(models.Model):
    ip = models.GenericIPAddressField()
    rate = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    workshop = models.ForeignKey(Workshops, related_name='rates', on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Rates"
        unique_together = ('ip', 'workshop',)

    def __str__(self):
        return str(self.rate)


''' ............... subscribe model ............... '''
class Subscribe(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    submit_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Subscribe"

    def __str__(self):
        return self.email + ': "' + str(self.is_active) + '"'



