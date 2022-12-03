from django.forms import ModelForm
from .models import Profile,Skill,Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class UpdateProfile(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user","username"]


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields= ["username","email","password1","password2"]
        labels = {
            "username" : "UserName"
        }

class SkillCreation(ModelForm):
    class Meta:
        model=Skill
        fields=["name","body"]
    def __init__(self,*args,**kwargs):
        super(SkillCreation,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":'input'})

class MessageCreation(ModelForm):
    class Meta:
        model=Message
        fields = ["title","body"]
    def __init__(self,*args,**kwargs):
        super(MessageCreation,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({"class":"input"})