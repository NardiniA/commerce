from django import forms
from .models import Category

class MakeBid(forms.Form):
    amount = forms.FloatField()

class AddComment(forms.Form):
    comment = forms.CharField(max_length=500)

class EditAuction(forms.Form):
    imgsrc = forms.CharField(max_length=200, required=True, label="Image Source", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Image Source...'}))
    title = forms.CharField(max_length=100, required=True, label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title...'}))
    desc = forms.CharField(max_length=500, required=True, label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control ta', 'placeholder': 'Description...'}))
    active = forms.BooleanField(label="Active", widget=forms.CheckboxInput(
        attrs={'class': 'form-check', 'placeholder': 'Active...'}))
    expires = forms.DateTimeField(label="Expires", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Expires...'}))

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
        attrs={'placeholder': 'Expires...'}))
    price = forms.CharField(label="Listed Price", required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'Listed Price...'}))
    category = forms.CharField(
        label="Category", required=True, widget=forms.Select(choices=choice_list))

    class Meta:
        fields = ('title', 'desc', 'active', 'expires')

