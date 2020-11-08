from django import forms
from .models import Category

class MakeBid(forms.Form):
    amount = forms.FloatField()

class AddComment(forms.Form):
    comment = forms.CharField(max_length=500)

class EditAuction(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title...'}))
    desc = forms.CharField(max_length=500, required=True, label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control ta', 'placeholder': 'Description...'}))
    active = forms.BooleanField(label="Active", required=False, widget=forms.CheckboxInput(
        attrs={'placeholder': 'Active...', 'class': 'form-check'}))
    expires = forms.DateTimeField(label="Expires", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '1970-01-20 15:00:00'}))
    img = forms.ImageField(label="Image", required=True)

    class Meta:
        fields = ('imgsrc', 'title', 'desc', 'active', 'expires')

# Dynamic Categories
c = Category.objects.all().values_list('name', 'name')

# Category List
choice_list = []

# Adds all categories from db
for item in c:
    choice_list.append(item)

class CreateNew(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Title", widget=forms.TextInput(
        attrs={'placeholder': 'Title...'}))
    desc = forms.CharField(max_length=500, required=True, label="Description", widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': 'Description...'}))
    active = forms.BooleanField(label="Active", widget=forms.CheckboxInput(
        attrs={'placeholder': 'Active...'}))
    expires = forms.DateTimeField(label="Expires", required=True, widget=forms.TextInput(
        attrs={'placeholder': '1970-01-20 15:00:00'}))
    price = forms.CharField(label="Listed Price", required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'Listed Price...'}))
    category = forms.CharField(
        label="Category", required=True, widget=forms.Select(choices=choice_list))
    img = forms.ImageField(label="Image", required=True)

    class Meta:
        fields = ('title', 'desc', 'active', 'expires')

