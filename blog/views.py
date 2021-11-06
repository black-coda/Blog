from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.edit import FormView
from . models import AuthorPost
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, TemplateView, FormView)
from django.views.generic.detail import SingleObjectMixin
from . forms import CreatePostForm, RegisterForm
from django import forms
from . models import Comment
from django.contrib.auth import authenticate, get_user_model,login
User = get_user_model()
from django.contrib.auth.decorators import login_required

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_on','active','post',]

class PostListView(ListView):
    template_name   =    'blog/list_view.html'
    context_object_name = 'lists'
    queryset    = AuthorPost.published.all()

class PostDetailView(DetailView):
    template_name   =   'blog/detail_view.html'
    context_object_name = 'details'
    model = AuthorPost


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
class DetailFormView(SingleObjectMixin, FormView):
    template_name   =   'blog/detail_view.html'
    form_class = CommentForm
    model = Comment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('PostDetail', kwargs={'pk':self.object.pk})

class PostdetailView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DetailFormView.as_view()
        return view(request, *args, **kwargs)

def list_view(request):
    list = AuthorPost.objects.all()
    context = {'lists':list}
    return render(request, 'blog/list_view.html', context)

def detail_view(request, pk):
    detail = get_object_or_404(AuthorPost, id=pk)
    comments = Comment.objects.filter(active = True)
    new_comment = None
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False) #dont save directly to db
            new_comment.post = detail
            print(detail)
            new_comment.save()
        else:
            form = CommentForm()

    context = {'details':detail, 'form':form, 'new_comment':new_comment, 'comments':comments}
    return render(request,'blog/detail_view.html', context )
    
"""
def detail_view(request, pk):
    detail = get_object_or_404(AuthorPost, id=pk)
    comments = Comment.objects.filter(active = True)

    form = CommentForm(instance=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=pk)
        if form.is_valid:
            form.save()
            return redirect('PostList')
 

    context = {'details':detail, 'form':form}
    return render(request,'blog/detail_view.html', context )
"""
@login_required
def authorForm(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid:
            #post = form.save(commit=False)
            form.save()
            #post.author = request.user
            return redirect('blog:PostList')

    return render(request, 'blog/form.html', {'form':form})

class AuthorPostForm(CreateView):
    template_name = 'blog/authorpost.html'
    form_class = CreatePostForm


def AuthorRegistrationForm(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email = email, password = password)
            login(request, user)
            return redirect('blog:PostList')
        else:
            form = RegisterForm()
    return render(request, 'registration/signup.html',{'form':form})