from django.forms import ModelForm
from .models import Signature, Verify, Note


class SignatureForm(ModelForm):
    class Meta:
        model = Signature
        fields = '__all__'
        exclude = ["owner"]


class VerifyForm(ModelForm):
    class Meta:
        model = Verify
        fields = "__all__"
        exclude = ["owner", "prediction"]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = "__all__"
        exclude = ["owner", 'created', 'updated', "signature"]
