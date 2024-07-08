from django.db.models.signals import post_migrate
from django.dispatch import receiver
from jobs.models import CategoryJobModel


TOP_LINKEDIN_CATEGORIES = [
    'Corporate Services',
    'Computer Software',
    'Information Technology and Services',
    'Internet',
    'Marketing and Advertising',
    'Accounting',
    'Hospital & Health Care',
    'Human Resources',
    'Financial Services',
    'Telecommunications',
    'Education Management',
    'Computer & Network Security',
    'Computer Hardware',
    'Management Consulting',
    'Banking',
    'Consumer Goods',
    'Retail',
    'Law Practice',
    'Insurance',
    'Real Estate',
]

@receiver(post_migrate)
def add_top_category(sender, **kwargs):
    if sender.name == 'jobs': 
        for category in TOP_LINKEDIN_CATEGORIES:
            obj, created = CategoryJobModel.objects.get_or_create(name=category)
            if created:
                print(f'Created:{category}')
            elif obj:
                print(f'Exist:{category}')


