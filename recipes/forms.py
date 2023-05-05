from django import forms


from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):

    error_css_class = 'error-field'
    required_css_class = 'required-field' # abhi ye required field & error field name ke liye hi set h,descriptions ke liye bhi hoti pr abhi wo commented h (ek bar view source me dekh lena)
    # name me css & html editing (par ye neeche init wale function ki wajah se overwrite ho jayege)

    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Recipe name"}))
    
    name = forms.CharField(help_text='This is your help! <a href="/contact">Contact us</a>') #form fields ko alag se template me rendering krne ke liye likha gya tha,wha pe rendering na krne pr bhi yha pe valid kaam krta

    # descriptions = forms.CharField(widget=forms.Textarea(attrs={"rows": 3})) # ek aur field (box) show krne lgta descriptions naam ka

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-crispy-forms
        for field in self.fields: # yha fields matlab , fields = ['name', 'description', 'directions']
            new_data = {
                "placeholder": f'Recipe {str(field)}', # matlab : "placeholder": f'Recipe name}',"placeholder": f'Recipe description}',"placeholder": f'Recipe directions}' ,,har loop me ek ek set hoga
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(  # yha pe new_data ki tarz pe updation ho rha h (naa samajh aaye to neeche wala commented and uncommented part dekh lo)
                new_data
            )
        # self.fields['name'].label = ''
        # self.fields['name'].widget.attrs.update({'class': 'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['directions'].widget.attrs.update({'rows': '4'})


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']
