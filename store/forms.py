from django import forms

class SearchForm(forms.Form):

    search_form = forms.CharField(max_length=50, label='')