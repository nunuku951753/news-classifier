from django import forms 

class PostForm(forms.Form):  
    title = forms.CharField(
                    label='標題',
                    widget = forms.TextInput(
                        attrs={
                            "class": "form-control"
                        }
                    )
    )  
    
    content = forms.CharField(
                    label='內文',
                    widget = forms.Textarea(
                        attrs={
                           "class": "form-control",
                           "rows": 20
                        }
                    )
    )
