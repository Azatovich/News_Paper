from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'post_title',
            'post_text',
            'post_category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get('post_title')
        if post_title is None:
            raise ValidationError({
                'post_title': 'Название не может быть пустым.'
            })

        post_text = cleaned_data.get('post_text')
        if len(post_text) < 20:
            raise ValidationError({
                'post_text': 'Текст не может быть менее 20 символов.'
            })
        elif post_text == post_title:
            raise ValidationError({
                'post_text': 'Текст не может быть идентичен названию.'
            })

        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user