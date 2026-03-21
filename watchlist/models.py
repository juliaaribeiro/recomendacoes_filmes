from django.db import models
from django.conf import settings

class Watchlist(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filme_id = models.IntegerField()
    titulo = models.CharField(max_length=255, default='')
    poster = models.CharField(max_length=500, default='', blank=True)
    assistido = models.BooleanField(default=False)
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'filme_id')

    def __str__(self):
        return f'{self.usuario} - {self.titulo}'
