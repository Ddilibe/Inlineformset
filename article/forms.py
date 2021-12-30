from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Article, Add_image, Add_video, Add_body

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('publish',)
        
class Add_imageMetaForm(forms.ModelForm):
    class Meta:
        model = Add_image 
        fields = '__all__'
        
class Add_videoMetaForm(forms.ModelForm):
    class Meta:
        model = Add_video
        fields = '__all__'
        
class Add_bodyMetaForm(forms.ModelForm):
    class Meta:
        model = Add_body
        fields = '__all__'

Add_imageFormSet = inlineformset_factory(
        Article,
        Add_image,
        form = Add_imageMetaForm,
        extra=1,
)

Add_videoFormSet = inlineformset_factory(
        Article,
        Add_video,
        form = Add_videoMetaForm,
        extra=1,
)

Add_bodyFormSet = inlineformset_factory(
        Article, 
        Add_body,
        form=Add_bodyMetaForm,
        extra=1,
)
