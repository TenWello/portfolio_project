from datetime import time

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from blog.models import Blog, Category, Tag, Comment
import bleach
import requests
from portfolio.models import AboutMe
from portfolios import settings
from django.contrib import messages

def truncate_html(content, length):
    allow_tags = ['p', 'b', 'i', 'u', 'a', 'br', 'strong', 'em', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h5p', 'h6']
    truncated_context = bleach.clean(content, tags=allow_tags, strip=True)
    if len(truncated_context) > length:
        truncated_context = truncated_context[:length] + '...'
    return truncated_context



class BlogListView(ListView):
    model = Blog
    template_name = 'blog-list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        blogs = Blog.objects.filter(status='published').order_by('-created_at')

        category_slug = self.request.GET.get('category')
        if category_slug:
            blogs = blogs.filter(categories__slug=category_slug)

        for blog in blogs:
            blog.truncated_content = truncate_html(blog.content, 150)
        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:5]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        return context


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog-detail.html'

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if all([name, email, message]):
            Comment.objects.create(blog=blog, name=name, email=email, message=message)
        return redirect('blog-detail', slug=blog.slug)

    # def get_queryset(self):
    #     blogs = Blog.objects.filter(status='published').order_by('-created_at')
    #
    #     category_slug = self.request.GET.get('category')
    #     if category_slug:
    #         blogs = blogs.filter(categories__slug=category_slug)
    #
    #     tag_slug = self.request.GET.get('tag')
    #     if tag_slug:
    #         blogs = blogs.filter(tag__slug=tag_slug)
    #
    #     for blog in blogs:
    #         blog.truncated_content = truncate_html(blog.content, 150)
    #
    #     return blogs

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return Blog.objects.get(slug=slug, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:5]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        context['selected_tag'] = self.request.GET.get('tag')
        context['selected_category'] = self.request.GET.get('category')
        return context

class ContactView(View):
    template_name = 'contact.html'
    def get(self, request):
        return render(request, self.template_name)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()
        context['about_me'] = about_me
        context['social_media'] = about_me.social_media if about_me else {}
        return context

    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message_contact = request.POST.get('message')

        bot_token = settings.BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        telegram_message = f"**New Contact Message:**\n\nName: {full_name}\nEmail: {email}\nMessage: {message_contact}\n"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': telegram_message,
            'parse_mode': 'Markdown',
        }
        response = requests.post(url, json=payload)

        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if response.status_code == 200:
            messages.success(request, "Your message has been sent successfully")
        else:
            messages.error(request, "Failed to send your message. Please try again later.")

        return redirect("/")






