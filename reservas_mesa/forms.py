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

    telefono_contacto = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8}$',
                message="El teléfono debe contener exactamente 8 dígitos numéricos."
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        'placeholder': 'Ejemplo: 71234567',
        'maxlength': '8',
        'pattern': r'\d{8}',
        'title': 'Debe ingresar exactamente 8 dígitos numéricos.'
        })
    )

    nombre_contacto = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
                message="El nombre solo puede contener letras y espacios."
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de la persona que reserva',
            
        })
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Notas especiales, alergias, decoración, etc.',
        }),
        max_length=300,
        help_text="Máximo 300 caracteres."
    )

    class Meta:
        model = ReservaMesa
        fields = [
            'nombre_contacto', 'telefono_contacto',
            'mesa', 'fecha_hora', 'cantidad_personas',
            'tipo_reserva', 'observaciones',
        ]
        widgets = {
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': DateTimeLocalInput(attrs={'class': 'form-control'}),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tipo_reserva': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_hora = cleaned_data.get('fecha_hora')
        confirmar = cleaned_data.get('confirmar_reserva_urgente')
        mesa = cleaned_data.get('mesa')
        cantidad_personas = cleaned_data.get('cantidad_personas')

        # 🚫 Reserva en el pasado
        if fecha_hora and fecha_hora < timezone.now():
            raise forms.ValidationError("No es posible registrar una reserva en el pasado.")

        # 🚫 Validación de urgencia (solo reservas nuevas)
        if self.instance.pk is None and fecha_hora:
            limite = timezone.now() + timedelta(hours=5)
            if fecha_hora <= limite and not confirmar:
                raise forms.ValidationError(
                    "La reserva se está registrando con menos de 5 horas de anticipación. "
                    "Marca la casilla de confirmación para continuar."
                )

        # 🚫 Validar capacidad de la mesa (si tu modelo Mesa tiene este campo)
        if mesa and cantidad_personas:
            if hasattr(mesa, 'capacidad') and cantidad_personas > mesa.capacidad:
                raise forms.ValidationError(
                    f"La mesa seleccionada solo tiene capacidad para {mesa.capacidad} personas."
                )

        # 🚫 Evitar doble reserva de la misma mesa en el mismo horario
        if mesa and fecha_hora:
            reservas_conflictivas = ReservaMesa.objects.filter(
                mesa=mesa,
                fecha_hora__date=fecha_hora.date(),
            ).exclude(pk=self.instance.pk)

            # Comparación simplificada: misma hora exacta
            if reservas_conflictivas.filter(fecha_hora=fecha_hora).exists():
                raise forms.ValidationError(
                    "Ya existe una reserva para esta mesa en la misma fecha y hora."
                )

        return cleaned_data
