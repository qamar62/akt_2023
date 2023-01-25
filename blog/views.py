from email import message
from django.shortcuts import redirect, render, get_list_or_404,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Like
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.


def like_post(request):
   
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
            
        like.save()
        
    return redirect('blogs')
    
class Blogs(ListView):
    model = Post
    template_name = 'blog/blogs.html'
    ordering = ['-post_created']
    

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog-detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.order_by('-id')[:4]
        context['posts'] = posts
        return context
    
   
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'


class AddCommentView(CreateView):
    model = Comment
    form_class  =  CommentForm
    template_name = 'blog/add_comment.html'
    
    
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url= reverse_lazy('blogs')
   


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'
    # fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blogs')

    
    

     