from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CreatePostForm, EditPostForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.

class AllPostsView(PermissionRequiredMixin, TemplateView):
    permission_required = 'posts.view_post'
    template_name = 'posts/posts.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context
    
    
class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = 'posts.add_post'
    template_name = 'posts/create_post.html'
    model = Post
    form_class = CreatePostForm
    success_url = '/posts/'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Пост был успешно создан.")  # Успешное сообщение
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании поста.")  # Сообщение об ошибке
        return super().form_invalid(form)
    

class EditPost(PermissionRequiredMixin, UpdateView):
    template_name = 'posts/create_post.html'
    permission_required = 'posts.change_post'
    model = Post
    form_class = EditPostForm
    success_url = '/posts/'

    def form_valid(self, form):
        post = self.get_object()  # Получаем текущий объект поста
        new_id = form.cleaned_data['id']  # Получаем новый ID из формы

        # Получаем остальные данные из формы
        topic = form.cleaned_data['topic']
        content = form.cleaned_data['content']
        author = form.cleaned_data['author']

        # Если ID меняется, создаем новый пост и удаляем старый
        if new_id != post.id:
            Post.objects.create(id=new_id, topic=topic,  content=content, author=author)

            post.delete()  # Удаляем старый пост
            messages.success(self.request, "Пост был успешно обновлён.") 
            return redirect(self.success_url) 
        else:
            # Обновляем текущую запись
            post.topic = topic
            post.content = content
            post.author = author
            post.save()
            messages.success(self.request, "Пост был успешно обновлён.") 

        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при сохранении поста.") 
        return super().form_invalid(form)


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = 'posts.delete_post'
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        messages.success(self.request, f"Пост с id - {pk} был удален.") 
        return redirect('/posts/')


def like_post(request, post_id):
    if not request.user.has_perm('posts.view_post'):
            raise PermissionError
    else:
        post = Post.objects.get(id=post_id)
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'like':
                post.number_likes += 1
                post.save()
                messages.success(request, f"Успешно увеличено кол-во лайков на посте с id {post_id}.") 
            elif action == 'unlike':
                if post.number_likes == 0:
                    messages.warning(request, f"Лайков не может быть меньше 0.")
                else:
                    post.number_likes -= 1
                    post.save()
                    messages.success(request, f"Успешно уменьшено кол-во лайков на посте с id {post_id}.")
        return redirect('/posts/')