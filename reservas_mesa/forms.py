# reservas_mesa/forms.py
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import ReservaMesa
from django.core.validators import RegexValidator



class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class ReservaMesaForm(forms.ModelForm):
    confirmar_reserva_urgente = forms.BooleanField(
        required=False,
        label="Confirmo que esta reserva es con menos de 5 horas de anticipación",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    class Meta:
        model = ReservaMesa
        fields = [
            'nombre_contacto', 'telefono_contacto',
            'mesa', 'fecha_hora', 'cantidad_personas',
            'tipo_reserva', 'observaciones',
        ]
        widgets = {
            'nombre_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la persona que reserva',
            }),
            'telefono_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de contacto',
            }),
            'mesa': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fecha_hora': DateTimeLocalInput(attrs={
                'class': 'form-control',
            }),
            'cantidad_personas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'tipo_reserva': forms.Select(attrs={
                'class': 'form-select',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notas especiales, alergias, decoración, etc.',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_hora = cleaned_data.get('fecha_hora')
        confirmar = cleaned_data.get('confirmar_reserva_urgente')

        # 🔴 Solo aplicar la validación de las 5 horas cuando ES UNA RESERVA NUEVA
        # (self.instance.pk es None cuando aún no se ha guardado en la BD)
        if self.instance.pk is None and fecha_hora:
            limite = timezone.now() + timedelta(hours=5)
            if fecha_hora <= limite and not confirmar:
                raise forms.ValidationError(
                    "La reserva se está registrando con menos de 5 horas de anticipación. "
                    "Marca la casilla de confirmación para continuar."
                )

        return cleaned_data