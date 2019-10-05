from django.db import models


class Pokemon(models.Model):
    title = models.CharField('имя', max_length=200)
    image = models.ImageField('изображение', null=True, blank=True)
    description = models.TextField('описание', blank=True)
    title_en = models.CharField('имя на английском', max_length=200, blank=True)
    title_jp = models.CharField('имя на японском', max_length=200, blank=True)
    next_evolution = models.ForeignKey('self', verbose_name='в кого эволюционирует', on_delete=models.CASCADE, null=True, blank=True, related_name='previous_evolution')

    def __str__(self):
        return '{}'.format(self.title)

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='покемон', on_delete=models.CASCADE, related_name='pokemon_entities')
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    appeared_at = models.DateTimeField('когда появится', null=True, blank=True)
    disappeared_at = models.DateTimeField('когда исчезнет', null=True, blank=True)
    level = models.IntegerField('уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strength = models.IntegerField('атака', null=True, blank=True)
    defence = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)
