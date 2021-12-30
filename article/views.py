from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.views.generic import UpdateView, ListView, CreateView, TemplateView, DetailView
from django.views.generic.edit import ContextMixin
from django.urls import reverse
from django.utils.text import slugify

from .models import Article, Add_video,Add_image, Add_body
from .forms import ArticleForm, Add_imageFormSet, Add_videoFormSet, Add_bodyFormSet

class ArticleListView(ListView):
    model = Article
    template_name = 'home.html'

class ArticleDetailView(DetailView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_detail.html'
    # add_image_meta_formset = Add_imageFormSet(instance=self.get_object())
    # formset = BlogFormSet( instance=Blog')
    
    def get_form(self, form_class, **kwargs):
        form = super(ArticleDetailView, self).get_form(**kwargs)
        add_image_meta_formset = Add_imageFormSet().get_form()
        return form
    
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        # print(add_image_meta_formset)
        context.update({ 
            'article':self.form_class(instance=self.get_object()),
            # 'image':Add_imageFormSet(instance=self.form_class),
            'image':Add_imageFormSet(instance=self.form_class(pk=self.get_object())),
            'body':Add_bodyFormSet(instance=self.get_object()),
            'video':Add_videoFormSet(instance=self.get_object()),
            'object_name': self.object.title,
            'object_nam': self.object.author,
        })
        return context
        

class ArticleCreateView(CreateView):
    form_class = ArticleForm
    template_name = 'article.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        
        
        context['add_image_meta_formset'] = Add_imageFormSet()
        context['add_body_meta_formset'] = Add_bodyFormSet()
        context['add_video_meta_formset'] = Add_videoFormSet()
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.slug = slugify(form['title'])
        add_image_meta_formset = Add_imageFormSet(self.request.POST, self.request.FILES)
        add_body_meta_formset = Add_bodyFormSet(self.request.POST)
        add_video_meta_formset = Add_videoFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and add_image_meta_formset.is_valid() and add_body_meta_formset.is_valid() and add_video_meta_formset.is_valid():
            print(self.request.POST)
            return self.form_valid(form, add_image_meta_formset, add_body_meta_formset, add_video_meta_formset)
        else :
            print(self.request.POST)
            return self.form_invalid(form, add_image_meta_formset, add_body_meta_formset, add_video_meta_formset)
            
    def form_valid(self, form, add_image_meta_formset, add_body_meta_formset, add_video_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        
        print(self.request.POST)
        images_meta = add_image_meta_formset.save(commit=False)
        for img in images_meta:
            img.article = self.object
            img.save()
        bodys_meta = add_body_meta_formset.save(commit=False)
        for bod in bodys_meta:
            bod.article = self.object
            bod.save()
        videos_meta = add_video_meta_formset.save(commit=False)
        for vid in videos_meta:
            vid.article = self.object
            vid.save()
        return redirect(reverse("article:Article_list"))
        
    def form_invalid(self, form, add_image_meta_formset, add_body_meta_formset, add_video_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  add_image_meta_formset=add_image_meta_formset,
                                  add_body_meta_formset=add_body_meta_formset,
                                  add_video_meta_formset=add_video_meta_formset,
                                  )
            )


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'update_article.html'
    form_name = ArticleForm
    object = None
    
    def get_object(self, queryset=None):
        self.object = super(ArticleUpdateView, self).get_object()
        return self.object
        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        add_image_meta_formset = Add_imageFormSet(self.object)
        return self.render_to_response(
                self.get_context_data( form = ArticleForm(instance=self.object),
                                       add_image_meta_formset = add_image_meta_formset,
                                    )
                            )
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = ArticleForm(data=self.request.POST, instance=self.object)
        add_image_meta_formset = Add_imageFormSet(data=self.request.POST, instance=self.object)
        if form.is_valid() and add_image_meta_formset.is_valid():
            return self.form_valid(form, add_image_meta_formset)
        else :
            return self.form_invalid(form, add_image_meta_formset)
            
    def form_valid(self, form, add_image_meta_formset):
        self.object = form.save()
        images_meta = add_image_meta_formset.save(commit=False)
        for img in add_image_meta_formset:
            img.creator = self.profile
            img.article = self.object
            img.save()
        return reverse(redirect("article:Article_list"))
        
    def form_invalid(self, form, add_image_meta_formset):
        return self.render_to_response(
                        self.get_context_data(  form=form,
                                                add_image_meta_formset=add_image_meta_formset,
                                            )
                                )