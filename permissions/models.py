# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

PROTECTION = (
    ("1", _("Open")),
    ("2", _("Custom")),
    ("3", _("Protected")),
    )

VISIBILITY = (
    ("1", _("Public")),
    ("2", _("Custom")),
    ("3", _("Private")),
    )

class Permission(models.Model):
    permission_name = models.CharField(max_length=255, verbose_name=_('Permission name'))
    can_write = models.ManyToManyField(User, blank=True, null=True, related_name='write',
                                       help_text=_('Select none to grant anonymous access.'))
    can_read = models.ManyToManyField(User, blank=True, null=True, related_name='read',
                                       help_text=_('Select none to grant anonymous access.'))
    protection = models.CharField(max_length=1, verbose_name=_('Protection'),
                                  choices=PROTECTION)
    visibility = models.CharField(max_length=1, verbose_name=_('Visibility'),
                                  choices=VISIBILITY)    
    def __unicode__(self):
        return self.permission_name
    
    
    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')        
        
    def can_read_obj(self, user):        
        """ Check read permissions and return True/False."""
        if self.visibility == "1":
            return True
        else:   
            perms = self.can_read.all()
            return perms.count() == 0 or perms.filter(pk__exact=user.id).count() > 0

    def can_write_obj(self, user):
        """ Check write permissions and return True/False."""        
        if self.can_read_obj(user):
            if self.protection == "1":
                return True
            else:    
                perms = self.can_write.all()
                return perms.count() == 0 or perms.filter(pk__exact=user.id).count() > 0
            
    def edit_can_write_obj(self, can_write):
        """ change permissions to users on the current cal """
        if self.protection == "2":
                old_can_write = []
                can_write_l = self.can_write.all()
                for i in can_write_l:
                    old_can_write.append(i) 
                for user in can_write: 
                    if user in old_can_write:
                        old_can_write.remove(user)
                    else:
                        self.can_write.add(user)
                    
                for user in old_can_write:                
                    self.can_write.remove(user)            
                 
    def edit_can_read_obj(self, can_read):
        """ change permissions to users on the current cal """
        if self.visibility == "2":
                old_can_read = []            
                can_read_l = self.can_read.all()            
                for i in can_read_l:
                    old_can_read.append(i)                
                for user in can_read:         
                    if user in old_can_read:          
                        old_can_read.remove(user)
                    else:                                            
                        self.can_read.add(user)
                for user in old_can_read:
                    self.can_read.remove(user)                
       
            
            
