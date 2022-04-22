from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import PIL
import Image
from tagging.fields import TagField
from tagging.models import Tag
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
# Model, ktory obsahuje informacie o pocte navstiveni stranky neregistrovanym pouzivatelom
class UnknownUser(models.Model) :
    ip_address = models.IPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    get_total = models.PositiveIntegerField()

    class Meta:
        verbose_name = "UnknownUser"
        verbose_name_plural = "UnknownUsers"
        ordering = ['created_at']

    def date_convert(self):
       return "%s" %(self.created_at.strftime("%d%m%Y"))

class UserDetail(models.Model) :
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=60)
    avatar = models.ImageField(upload_to='home/media/photos', max_length = 100, blank=True) #nahra obrazok na server
    bio = models.TextField(blank=True)
    preferences = models.CharField(max_length=255, help_text="Here write your preferences", blank = True, null = True)
    remember_me = models.BooleanField(default = True, blank = True)

#vytvorenie abstraktnej triedy pre obsah
class Author(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True, max_length=60, help_text="Nevyplnajte, hodnota sa vyplni podla mena a priezviska autora")
    def __unicode__(self):
        return "%s %s" %(self.first_name, self.last_name)
        
    class Meta:
        verbose_name_plural = "Authors"
        
    #metoda na ziskanie getURL vyhladavanie vsetkych zdrojov,
    #podla mena autora

class Source(models.Model):
    source = models.CharField(max_length=50, help_text="Sem zadajte zdroj, z ktoreho ste obsah ziskali. Priklad Tedx,...")
    slug = models.SlugField(unique=True, max_length=60, help_text="Tuto polozku nevyplnajte, priradena hodnota z pola source")

    def __unicode__(self):
        return self.source
    #metoda na getURL, zobrazenie vsetkych zdrojov, od tohto zdroju
    #podla nazvu v URL adrese podla abecedy
    

class Type(models.Model) :
    description = models.CharField(max_length=50, help_text="Uvedte prosim typ obsahu")
    slug = models.SlugField(unique=True, max_length=23, help_text="Automaticky pripradena hodnota z pola description")
    description_image = models.ImageField(upload_to='home/media/photo', help_text="Sem nahrajte ikonu typu obsahu")
    
    def __unicode__(self):
        return self.description
class TagItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class Category(models.Model) :
    slug = models.SlugField(unique=True, max_length=50, help_text="Tuto polozku nevyplnajte, zada sa sem hodnota z pola name")
    name = models.CharField(max_length=50)
    tags = TagField()

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
    def get_tags(self):
        return Tag.object.get_for_object(self)


class Content(models.Model) :
    title = models.CharField(max_length=50, help_text="Zadajte titulok obsahu")
    slug = models.SlugField(max_length=100, help_text="Nevyplnajte, automaticky pripradena hodnota z pola title")
    kind = models.ForeignKey(Type)
    category = models.ForeignKey(Category, related_name='%(class)s_related')
    author = models.ManyToManyField(Author, verbose_name="Authors")
    thumbnail = models.ImageField(upload_to='home/media/photo', blank=True, null=True, help_text="Nahrajte ikonu typu obsahu")
    video = models.URLField(blank=True, null=True, help_text="Sem zadajte URL adresu youtube videa, inak nechajte prazdne policko")
    created_at = models.DateTimeField(auto_now_add=True)
    updadet_at = models.DateTimeField(auto_now = True)
    tags = TagField(blank=True)
    recommend_by = models.ForeignKey(User, blank=True)
    visibility = models.BooleanField(default = True, blank=True, help_text="Tuto hodnotu nevyplnate")

    def __unicode__(self):
        return self.title
    class Meta:
        ordering = ['created_at']
    def get_tags(self):
        return Tag.object.get_for_object(self)
class ContentDetail(Content) :
    long_description = models.TextField(help_text="Sem zadajte popis a informacie o obsahu")
    source = models.ManyToManyField(Source, verbose_name="Sources")
    link = models.URLField(help_text="Sem zadajte odkaz na zdroj")
    start_course = models.DateTimeField(blank=True, null = True)
    start_is = models.NullBooleanField(default=True, blank = True, null = True)
    workload = models.CharField(max_length=25, blank = True, null = True )
class ContentUser(ContentDetail) :
   DONE = 'Done'
   TODO = 'ToDo'
   MY_LIST_CHOICES = (
       (DONE, 'Done'),
       (TODO, 'ToDo'),
       )
   my_list_choices = models.CharField(max_length=5, choices = MY_LIST_CHOICES, default=TODO, help_text="Tuto hodnotu vyplna pouzivatel", blank=True)
   user = models.ForeignKey(User, blank=True)
   
class Comment(MPTTModel):
    post = models.ForeignKey(ContentDetail)
    author = models.ForeignKey(User)
    comment = models.TextField()
    added  = models.DateTimeField()
    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['added']
    
    
    






    
    
    
    


