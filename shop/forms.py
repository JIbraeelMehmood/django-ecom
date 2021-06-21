from django import forms
from .models import RATE_CHOICES,Review,Comment

# Comment
class RateForm(forms.ModelForm):
	title_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
	review_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = Review
		fields = ('title_text','review_text','rate')

class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)

	class Meta:
		model = Comment
		fields = ('body',)
