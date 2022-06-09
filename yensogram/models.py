from django.db import models

from django.contrib.auth.models import AbstractUser
from dynamic_models.models import ModelSchema, FieldSchema
from django.core.validators import FileExtensionValidator
from datetime import datetime
from PIL import Image


# Create your models here.
class User(AbstractUser):

    email = models.EmailField(null=False, blank=False)# I added this because Django's default AbstractUser
                                                      # for email feild has required = False, but I want email to be required
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
   # The reason for this custom save() method is to
    # reduce the dimension of profile pictures in order
    # not to slow down the speed of loading web pages.
    def save(self, *args, **kwargs): # This method overides the default behaviour when we save() a User object
        
        super().save(*args, **kwargs) # First carry out the default save() behaviour of the parent(super()) class
                                      # so that PIL can find the image (path to the image) to edit
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300: # If height or width of image is > 300px

            output_size = (300, 300) # A tuple
            img.thumbnail(output_size)

            img.save(self.image.path)

    def __str__(self):
        return f"{self.username.capitalize()}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }





# For dynamic models
class DynamicModel(ModelSchema):
    pass

    def __str__(self):
        return f"{self.name}"

class DynamicModelField(FieldSchema):
    pass

    def __str__(self):
        return f"{self.name}"





class Post(models.Model):
    date = models.DateTimeField(default=datetime.now)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
        upload_to="post_pics"
    )

    def save(self, *args, **kwargs): # This method overides the default behaviour when we save() a User object

        super().save(*args, **kwargs) # Carry out the default save() behaviour of the parent(super()) class
        
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300: # If height or width of image is > 300px

                output_size = (300, 300) # A tuple
                img.thumbnail(output_size)
                img.save(self.image.path)

