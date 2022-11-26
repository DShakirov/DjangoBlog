from django import template
from django import template
from blog.models import Post, Tag


register = template.Library()


@register.inclusion_tag('blog/recent_posts_tpl.html')
def get_recent(cnt = 3):
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('blog/tags_tpl.html')
def get_tags():
    tags = Tag.objects.all()
    return {'tags': tags}
