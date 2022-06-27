from wagtail.models import Page

class HomePage(Page):
    @property
    def freezer_follow_urls(self):
        return [
            "/static/followed.txt"
        ]
