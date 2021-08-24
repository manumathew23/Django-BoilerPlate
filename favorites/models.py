from django.db import models

from .constants import PLANETS,FILMS, PEOPLE, STARSHIPS

class Customization(models.Model):
	CATEGORY_CHOICES = (
    	(PLANETS, "planets"),
    	(FILMS, "films"),
    	(PEOPLE, "people"),
    	(STARSHIPS, "starships")
    )

	user_id=models.IntegerField()
	item_id=models.IntegerField()
	name=models.CharField(max_length=250)
	is_favorite=models.BooleanField(default=False)
	category=models.IntegerField(
        choices=CATEGORY_CHOICES,
    )