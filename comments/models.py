from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filme_id = models.IntegerField()
    titulo = models.CharField(max_length=255, default='')
    texto = models.TextField()
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 11)], null=True, blank=True)  # 1-10, opcional
    data_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'filme_id')

    def clean(self):
        # Validações customizadas para o admin e qualquer formulário
        if self.nota is not None and (self.nota < 1 or self.nota > 10):
            raise ValidationError({'nota': 'A nota deve estar entre 1 e 10.'})

        if not self.titulo and not self.texto:
            raise ValidationError('Comentário deve ter título ou texto.')

    def save(self, *args, **kwargs):
        # Garante que a validação seja aplicada antes de salvar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario} - {self.titulo}'
