from django import template

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.utils.timezone import now

from raspberryio.project.models import FeaturedProject

register = template.Library()

class FeaturedProjectNode(template.Node):

    def __init__(self, num):
        self.num = num

    def render(self, context):
        featured = FeaturedProject.objects.filter(
                        featured_start_date__lte=now(),
                        project__publish_date__lte=now(),
                        project__status=CONTENT_STATUS_PUBLISHED
                        )
        context['featured_projects'] = featured[:self.num]
        return ''


@register.tag
def featured_projects(parser, token):
    try:
        tag_name, number = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    try:
        int(number)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag's argument should be an integer" % tag_name)
    return FeaturedProjectNode(number)
