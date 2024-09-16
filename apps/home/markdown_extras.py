# home/templatetags/markdown_extras.py

from django import template
import markdown
from django.utils.safestring import mark_safe
import bleach

register = template.Library()

@register.filter
def markdownify(text):
     # Convert markdown to HTML
     html = markdown.markdown(text)

        # Clean the HTML to prevent XSS attacks
     allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote', 'code']
     allowed_attributes = {'a': ['href', 'title'], 'img': ['src', 'alt']}
     clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
         
     return mark_safe(clean_html)