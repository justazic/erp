from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your User name',
            },
            ),
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your Password',
            },
            ),
        )


from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "phone",
            "address",
            "speciality",
            "qualifications",
            "is_expert",
            ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "First name",
                },
                ),
            "last_name": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "Last name",
                },
                ),
            "username": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "Username",
                },
                ),
            "email": forms.EmailInput(attrs={
                "class": "fInput",
                "placeholder": "Email",
                },
                ),
            "phone": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "+998 90 123 45 67",
                },
                ),
            "address": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "Address",
                },
                ),
            "speciality": forms.TextInput(attrs={
                "class": "fInput",
                "placeholder": "Speciality",
                },
                ),
            "qualifications": forms.Textarea(attrs={
                "class": "fInput",
                "rows": 4,
                "placeholder": "Qualifications",
                },
                ),
            }

    def __init__( self, *args, user=None, **kwargs ):
        super().__init__(*args, **kwargs)
        self.request_user = user
        instance = self.instance
        editing = bool(instance and instance.pk)

        if "avatar" in self.fields:
            self.fields[ "avatar" ].required = False

        if editing:
            for f in [ "is_expert" ]:
                if f in self.fields:
                    self.fields[ f ].disabled = True

        if instance and instance.role != "teacher":
            for f in [ "speciality", "qualifications", "is_expert" ]:
                self.fields.pop(f, None)
        else:
            if "is_expert" in self.fields and not (user and (user.is_staff or user.is_superuser)):
                self.fields[ "is_expert" ].disabled = True

    def clean_username( self ):
        username = (self.cleaned_data.get("username") or "").strip()

        if not username:
            raise ValidationError("Username is required.")

        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("This username already exists.")

        return username

    def clean_email( self ):
        email = (self.cleaned_data.get("email") or "").strip().lower()

        if not email:
            raise ValidationError("Email is required.")

        return email

    def clean( self ):
        cleaned = super().clean()
        if self.instance and self.instance.role == "teacher":
            is_expert = cleaned.get("is_expert", getattr(self.instance, "is_expert", False))
            qualifications = (cleaned.get("qualifications") or "").strip()
            if is_expert and not qualifications:
                self.add_error("qualifications", "Qualifications are required for expert teachers.")
        return cleaned
