from django.http.response import HttpResponseRedirect
from django.shortcuts import  redirect , get_object_or_404
from django.urls import reverse_lazy ,reverse
from .models import BlogModel ,TagModel ,CommentModel
from .forms import CommentForm
from django.db.models import Count
from django.views.generic import View
from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin


## permissions

class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('login')

class OwnUserCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == super().get_object().user

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect('blog:blog_posts')
    
## end permissions


## post list ,show , add comment ##
class PostList(ListView):
    model = BlogModel
    paginate_by = 5
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = BlogModel.objects.filter(status='published',publish_date__lt=timezone.now()).order_by('-publish_date')
        search = self.request.GET.get('search',None)
        category = self.request.GET.get('category',None)
        tag = self.request.GET.get('tag',None)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(full_text__icontains = search ) | 
                Q(summary_text__icontains=search)
            )
        
        elif category:
             queryset = queryset.filter(category__name = category)

        elif tag:
            queryset = queryset.filter(tags__name=tag)
        
        return queryset

    def get_context_data(self):
        context = super().get_context_data()

        context['tags'] = TagModel.objects.all()[:20]

        context['category_counts'] = BlogModel.objects.values('category__name').annotate(Count('category')).order_by('-category__count')[:10]

        context['recent_posts'] =  BlogModel.objects.all()[:4]
        print('*'*100)
        return context

class PostDetail(DetailView):
    model = BlogModel
    template_name = 'blog/post_details.html'
    context_object_name = 'post'
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context.update({    
            'next_post':BlogModel.objects.filter(id__gt=super().get_object().id).order_by('id').first(),
            'prev_post':BlogModel.objects.filter(id__lt=super().get_object().id).order_by('id').last(),
            'form':CommentForm(),
            'tags':TagModel.objects.all()[:20],
            'recent_posts':BlogModel.objects.all()[:4],
            'category_counts':BlogModel.objects.values('category__name').annotate(Count('category')).order_by('-category__count')[:10]
        })

        return context

    # save comment
    def post(self, request, *args, **kwargs):
        post = super().get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.post = post
            data.save()
            return redirect('blog:post_details',slug=post.slug)
## end  post list ,show , add comment ##


class CommentDeleteView(View):
    def get(self,request,slug):
        comment = get_object_or_404(CommentModel,slug=slug)
        if comment.user == request.user:
            comment.delete()
        return redirect('blog:blog_posts')
    

class CommentDetail(LoginRequired,OwnUserCheck,UpdateView):
    model = CommentModel
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    form_class =  CommentForm

    def get_success_url(self) -> str:
        return reverse(f'blog:post_details',
                        kwargs={'slug':super().get_object().post.slug})


class CommentDelete(LoginRequired,OwnUserCheck,DeleteView):
    model = CommentModel

    def post(self,request,*args, **kwargs):
        comment  = super().get_object()
        comment.delete()
        return redirect('blog:post_details',slug=comment.post.slug)
    