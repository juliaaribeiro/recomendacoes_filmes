from django.db import models
from django.conf import settings

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filme_id = models.IntegerField()
    titulo = models.CharField(max_length=255, default='')
    texto = models.TextField()
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 11)], null=True, blank=True)  # 1-10, opcional
    data_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'filme_id')

    def __str__(self):
        return f'{self.usuario} - {self.titulo}'
