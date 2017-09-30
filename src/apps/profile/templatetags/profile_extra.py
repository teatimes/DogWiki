from django import template

from src.apps.authentication.models import Follow, User as User

register = template.Library()

@register.simple_tag
def follow_text(following_pk, followed_pk):
    following = User.objects.get(pk=following_pk)
    followed = User.objects.get(pk=followed_pk)

    if Follow.objects.filter(following=following, followed=followed).exists():
        return "Følger"
    else:
        return "Følg"