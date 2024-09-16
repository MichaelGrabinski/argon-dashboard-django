from django import template
from django.utils.safestring import mark_safe
import markdown
import bleach

register = template.Library()

@register.filter
def markdownify(text):
    # Convert markdown to HTML with extensions
    md = markdown.Markdown(
        extensions=[
            'fenced_code',    # For fenced code blocks
            'tables',         # For tables
        ]
    )
    html = md.convert(text)

    # Define allowed tags and attributes
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
        'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote',
        'code', 'pre', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'span', 'div',
    })

    allowed_attributes = {
        **bleach.sanitizer.ALLOWED_ATTRIBUTES,
        'a': ['href', 'title'],
        'img': ['src', 'alt'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan'],
        'code': ['class'],
        'pre': ['class'],
        'span': ['class'],
        'div': ['class'],
    }

    # Clean the HTML to prevent XSS attacks
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
    )

    return mark_safe(clean_html)