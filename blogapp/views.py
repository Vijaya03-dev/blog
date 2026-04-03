from django.shortcuts import render

from .models import Posts

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# posts= [

#     {

#         'author': 'CoreyMS',

#         'title': 'Blog Post 1',

#         'content': 'First post content',

#         'date_posted': 'August 27,2018'

#     },

#     {

#         'author': 'John Doe',

#         'title': 'Blog Post 2',

#         'content': 'Second post content',

#         'date_posted': 'September 30,2018'

#     }

# ]


# this below is a functional view

# posts = Posts.objects.all()


# def home(request):

#     return render(request,'blogapp/home.html',{'posts':posts})


# this below is a class view


class PostListView(ListView):

    model = Posts

    template_name = "blogapp/home.html"

    context_object_name = "posts"

    ordering = ["-data_posted"]

    paginate_by = 5


class UserPostListView(ListView):

    model = Posts

    template_name = "blogapp/user_post.html"

    context_object_name = "posts"

    ordering = ["-data_posted"]

    paginate_by = 5

    def get_queryset(self):

        user = get_object_or_404(User, username=self.kwargs.get("username"))

        return Posts.objects.filter(author=user).order_by("-data_posted")


class PostDetailView(DetailView):
    model = Posts


def about(request):

    return render(request, "blogapp/about.html", {"title": "About"})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form.valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    fields = ["title", "content"]

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# two type of views functional and class based

# functional views - everything is manual

# and class asbed views .they have prebuilt functionality and they are directly mapped with the modals

# DRF django Rest framework
