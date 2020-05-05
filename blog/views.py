from django.views import generic
from django.views.generic import DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post, Profile, Image, Comment
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit  import FormMixin
from .forms import PostModelForm, UserLoginForm, SignUpForm, ProfileForm, UserForm, ImageFormSet, PostEditForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
# from django.forms import inlineformset_factory
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


# Create your views here.

class PostList(generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.published.filter(
                Q(title__icontains=query)|
                Q(author__username=query)|
                Q(body__icontains=query)
            )
        else:
            return Post.published.all()

class PostDetail(FormMixin, DetailView):
    template_name = 'blog/post_detail.html'
    queryset = Post.objects.all()
    form_class = CommentForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, id=pk, slug=slug)
        return post

    def get_success_url(self):
        self.success_url = Post.get_absolute_url(self.object)
        return self.success_url
    


    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        is_liked = False
        is_favourite = False
        post = get_object_or_404(Post, id=pk, slug=slug)
        if post.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        if post.favourites.filter(id=self.request.user.id).exists():
            is_favourite = True
        context['is_liked'] = is_liked
        context['is_favourite'] = is_favourite
        context['total_likes'] = post.total_likes()
        context['comments'] = Comment.objects.filter(post=self.object, reply=None).order_by('-id')
        context['comment_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = self.get_form()
        if comment_form.is_valid():
            return self.form_valid(comment_form)
        else:
            return self.form_invalid(comment_form)
            

    def form_valid(self, comment_form):
        reply_id = self.request.POST.get('comment_id')
        comment_qs = None
        if reply_id:
            comment_qs = Comment.objects.get(id=reply_id)
        comment_form.instance.post = self.object
        comment_form.instance.user = self.request.user
        comment_form.instance.reply = comment_qs
        comment_form.save()
        if self.request.method == 'POST' and self.request.is_ajax():
            html = render_to_string('blog/comments.html', self.get_context_data(), request=self.request)
            data = {'form': html}
            return JsonResponse(data)

def favourite_post(request, pk, slug):
    post = get_object_or_404(Post, id=pk, slug=slug)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
        is_favourite = False
    else:
        post.favourites.add(request.user)
        is_favourite = True
    return HttpResponseRedirect(post.get_absolute_url())

class FavPostList(generic.ListView):
    template_name = 'blog/post_favourite_list.html'
    context_object_name = 'favourite_posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user
        if query:
            return user.favourites.filter(
                Q(title__icontains=query)|
                Q(author__username=query)|
                Q(body__icontains=query)
            )
        else:
            return user.favourites.all()


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourites.all()
    context = {
        'favourite_posts': favourite_posts
    }
    return render(request, 'blog/post_favourite_list.html', context)

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        data = {'form': html}
        return JsonResponse(data)
    

class ImageInline(InlineFormSetFactory):
    model = Image
    fields = ['image']

class PostCreate(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'blog/post_create.html'
    form_class = PostModelForm
    login_url = reverse_lazy('blog:user_login')
    success_message = "%(title)s was created successfully"
    

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = ImageFormSet()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                image_form=image_form
            )
        )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = ImageFormSet(self.request.POST, self.request.FILES)

        if (form.is_valid() and image_form.is_valid()):
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)
        

    def form_valid(self, form, image_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        image_form.instance = self.object
        image_form.save()
        messages.success(self.request, 'Your post was successfully created!')
        return HttpResponseRedirect(self.get_success_url())

class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'blog/post_update.html'
    form_class = PostModelForm
    login_url = reverse_lazy('blog:user_login')
    model = Post

    def get_success_url(self):
        self.success_url = Post.get_absolute_url(self.object)
        return self.success_url
    

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = PostModelForm(self.request.POST)
            context['image_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'] = PostModelForm(instance=self.object)
            context['image_form'] = ImageFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_form = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        self.object = form.save()
        image_form.instance = self.object
        image_form.save()
        messages.success(self.request, 'Your post was successfully updated!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                image_form=image_form
                )
        )


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('blog:user_profile')
    template_name = 'blog/register.html'

    def form_valid(self, form):
        to_return = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return to_return

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/user_profile.html'

class ProfileUpdateView(LoginRequiredMixin, generic.TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'blog/profile_update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)
        

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('blog:user_profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def post_delete(request, pk, slug):
    post = get_object_or_404(Post, id=pk, slug=slug)

    if request.user != post.author:
        raise Http404
    
    post.delete()
    return redirect('blog:post_list')