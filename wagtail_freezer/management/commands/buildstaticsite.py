from pathlib import Path
from shutil import copyfile, rmtree

from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from wagtail.models import Site

class Command(BaseCommand):
    help = "Generate a static HTML version of this Wagtail site"

    def follow_url(self, url):
        if url.startswith(self.static_assets_url):
            self.static_assets.add(url[len(self.static_assets_url):])
        elif url.startswith(self.media_url):
            self.media.add(url[len(self.media_url):])

    def handle(self, *args, **options):
        try:
            static_root = Path(settings.FREEZER_BUILD_DIR)
        except AttributeError:
            raise ImproperlyConfigured("FREEZER_BUILD_DIR must be defined in settings")

        self.static_assets_url = getattr(settings, "STATIC_URL", "")
        self.copy_static_assets = self.static_assets_url.startswith("/")
        self.media_url = getattr(settings, "MEDIA_URL", "")
        self.copy_media = self.media_url.startswith("/")

        sites = Site.objects.all()

        for site in sites:
            self.static_assets = set()
            self.media = set()
            site_static_root = static_root / site.hostname
            rmtree(site_static_root, ignore_errors=True)

            pages = site.root_page.get_descendants(inclusive=True).live().order_by('path').specific()
            for page in pages:
                relative_path = page.url_path[len(site.root_page.url_path):]
                page_path = site_static_root / relative_path 

                dummy_meta = page._get_dummy_headers()
                request = WSGIRequest(dummy_meta)

                # Add a flag to let middleware know that this is a dummy request.
                request.is_dummy = True

                # Build a custom django.core.handlers.BaseHandler subclass that invokes serve() as
                # the eventual view function called at the end of the middleware chain, rather than going
                # through the URL resolver
                class Handler(BaseHandler):
                    def _get_response(self, request):
                        response = page.serve(request)
                        if hasattr(response, "render") and callable(response.render):
                            response = response.render()
                        return response

                # Invoke this custom handler.
                handler = Handler()
                handler.load_middleware()
                response = handler.get_response(request)

                page_path.mkdir(parents=True)
                with (page_path / "index.html").open(mode='wb') as f:
                    f.write(response.content)

                if self.copy_static_assets or self.copy_media:
                    soup = BeautifulSoup(response.content, "html.parser")
                    for elem in soup.find_all(lambda tag:('href' in tag.attrs or 'src' in tag.attrs)):
                        for attr in ('href', 'src'):
                            url = elem.get(attr, "")
                            if url:
                                self.follow_url(url)

                if hasattr(page, "freezer_follow_urls"):
                    for url in page.freezer_follow_urls:
                        self.follow_url(url)

            if self.static_assets:
                destination_base_path = site_static_root / self.static_assets_url[1:]
                for asset_path in self.static_assets:
                    source_file = finders.find(asset_path)
                    if source_file:
                        destination_path = destination_base_path / asset_path
                        destination_path.parent.mkdir(parents=True, exist_ok=True)
                        copyfile(source_file, destination_path)

            if self.media:
                destination_base_path = site_static_root / self.media_url[1:]
                media_root = Path(settings.MEDIA_ROOT)
                for media_path in self.media:
                    source_path = media_root / media_path
                    if source_path.is_file():
                        destination_path = destination_base_path / media_path
                        destination_path.parent.mkdir(parents=True, exist_ok=True)
                        copyfile(source_path, destination_path)
