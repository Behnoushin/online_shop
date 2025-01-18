from .models import Template

def get_formatted_message(slug, **kwargs):
    try:
        template = Template.objects.get(slug=slug)
        return template.text.format(**kwargs)
    except Template.DoesNotExist:
        return f"پیامی با شناسه '{slug}' یافت نشد."