from django import forms


from .models import Recipe, RecipeIngredient, RecipeIngredientImage

class RecipeIngredientImageForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredientImage
        fields = ['image']
        labels = {
            "image": "Extract via Image Upload"
        }


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
                "placeholder": f'Recipe {str(field)}', # matlab : "placeholder": f'Recipe name',"placeholder": f'Recipe description}',"placeholder": f'Recipe directions}' ,,har loop me ek ek set hoga
                "class": 'form-control',

                #simply autosave ke liye likhe hai har field me change hone par,(iise easy hai form.html me hx-trigger:changed delay:500 ms se bhi ho jaayega ,yha itna likhne ki koi zaroorat nhi h,par theek h)

                #70th video me ye comment ho hi gya kyonki iska koi kaam ab hai hi nhi(pehle bhi nhi tha)
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
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
