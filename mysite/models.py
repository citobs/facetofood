from django.db import models


# Create your models here.

class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    mainphoto = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.postname


class MenuScoreAll(models.Model):
    menu = models.TextField(blank=True, null=True)
    restaurant = models.TextField(blank=True, null=True)
    happy_winter = models.FloatField(blank=True, null=True)
    happy_winter_snow = models.FloatField(blank=True, null=True)
    happy_winter_rain = models.FloatField(blank=True, null=True)
    happy_fall = models.FloatField(blank=True, null=True)
    happy_fall_rain = models.FloatField(blank=True, null=True)
    happy_summer = models.FloatField(blank=True, null=True)
    happy_summer_rain = models.FloatField(blank=True, null=True)
    happy_spring = models.FloatField(blank=True, null=True)
    happy_spring_rain = models.FloatField(blank=True, null=True)
    sad_spring_rain = models.FloatField(blank=True, null=True)
    sad_spring = models.FloatField(blank=True, null=True)
    sad_summer_rain = models.FloatField(blank=True, null=True)
    sad_summer = models.FloatField(blank=True, null=True)
    sad_fall_rain = models.FloatField(blank=True, null=True)
    sad_fall = models.FloatField(blank=True, null=True)
    sad_winter_rain = models.FloatField(blank=True, null=True)
    sad_winter = models.FloatField(blank=True, null=True)
    sad_winter_snow = models.FloatField(blank=True, null=True)
    angry_winter = models.FloatField(blank=True, null=True)
    angry_winter_snow = models.FloatField(blank=True, null=True)
    angry_winter_rain = models.FloatField(blank=True, null=True)
    angry_fall = models.FloatField(blank=True, null=True)
    angry_fall_rain = models.FloatField(blank=True, null=True)
    angry_summer = models.FloatField(blank=True, null=True)
    angry_summer_rain = models.FloatField(blank=True, null=True)
    angry_spring = models.FloatField(blank=True, null=True)
    angry_spring_rain = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_score_all'




class resultall(models.Model):
    restaurant = models.CharField(max_length=300)
    menu = models.CharField(max_length=300)
    emotion = models.CharField(max_length=300, null=True, default='')
    season = models.CharField(max_length=300, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"({self.season},{self.emotion})"


class fullist(models.Model):
    emot = models.CharField(max_length=300, null=True)
    sea = models.CharField(max_length=300, null=True)
    first= models.CharField(max_length=300, null=True)
    second= models.CharField(max_length=300, null=True)
    third = models.CharField(max_length=300, null=True)
    cr_at = models.DateTimeField(auto_now_add=True, null=True)
    fourth = models.CharField(max_length=300, null=True)
    fifth = models.CharField(max_length=300, null=True)
    wea = models.CharField(max_length=300, null=True)
    
    def __str__(self):
        return f"({self.emot},{self.sea})"

class choice(models.Model):
    res = models.CharField(max_length=300,null=True)
    menu = models.CharField(max_length=300,null=True)
    emotion = models.CharField(max_length=300,null=True)
    cr_at = models.DateTimeField(auto_now_add=True, null =True)
    weather = models.CharField(max_length=300,null=True)
    season = models.CharField(max_length=300,null=True)

    def __str__(self):
            return f"({self.res})"


