# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from permissions.fields import CommaSeparatedUserField
from permissions.models import Permission, VISIBILITY, PROTECTION

class PermissionForm(forms.Form):
    """
    A form to create a permission object
    """
    visibility = forms.ChoiceField(widget=forms.Select(), choices=VISIBILITY,
                                       initial="1",) 
    can_read = CommaSeparatedUserField(label=_(u"can_read"), required=False)
    protection = forms.ChoiceField(widget=forms.Select(), choices=PROTECTION,
                                       initial="3",)
    can_write = CommaSeparatedUserField(label=_(u"can_write"), required=False)    
    error_css_class = "error"
    
    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['visibility'].widget.attrs['class'] = 'visibility_check'        
        self.fields['can_read'].widget.attrs['class'] = 'visibility'                                
        self.fields['protection'].widget.attrs['class'] = 'protection_check'        
        self.fields['can_write'].widget.attrs['class'] = 'protection' 
        
    def clean_can_write(self):
        """
        Check that if cal_protection is set to semi-protected, the user should fill
        the can_write
        """
        if self.cleaned_data['protection'] == "2":
            if not self.cleaned_data['can_write']:
                raise forms.ValidationError(_("You should indicate people who could write on this article."))
            return self.cleaned_data['can_write']                                                                             
    
    def clean_can_read(self):
        """
        Check that if cal_visibility is set to semi-public, the user should fill
        the can_read
        """
        if self.cleaned_data['visibility'] == "2":
            if not self.cleaned_data['can_read']:
                raise forms.ValidationError(_("You should indicate people who could read this article."))
            return self.cleaned_data['can_read']
    
    def save(self, slug, request_user):        
        permissions = Permission(permission_name='%s_perms' % slug,
                                             visibility=self.cleaned_data['visibility'],
                                             protection=self.cleaned_data['protection'])
        permissions.save(commit=False)          
        permissions.can_write.add(request_user)
        permissions.can_read.add(request_user)
        if self.cleaned_data['protection'] == "2":
            for user in self.cleaned_data['can_write']:                    
                permissions.can_write.add(user)
        if self.cleaned_data['visibility'] == "2":
            for user in self.cleaned_data['can_read']:                    
                permissions.can_read.add(user)
        permissions.save(commit=True)
        return permissions
                    
