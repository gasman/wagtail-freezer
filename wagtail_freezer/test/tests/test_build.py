from pathlib import Path
import shutil

from django.conf import settings
from django.core import management
from django.test import TestCase
from wagtail.models import Page, Site

from wagtail_freezer.test.models import HomePage


class TestBuild(TestCase):
    def setUp(self):
        Page.objects.filter(depth__gt=1).delete()
        root = Page.objects.get(depth=1)
        homepage = HomePage(title="Homepage")
        root.add_child(instance=homepage)
        subpage = HomePage(title="Subpage")
        homepage.add_child(instance=subpage)
        Site.objects.create(
            root_page=homepage,
            hostname="testserver",
        )

    def tearDown(self):
        shutil.rmtree(settings.FREEZER_BUILD_DIR, ignore_errors=True)

    def test_build(self):
        management.call_command("buildstaticsite")

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "index.html").open() as f:
            file_content = f.read()
        self.assertIn("<title>Homepage</title>", file_content)

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "subpage", "index.html").open() as f:
            file_content = f.read()
        self.assertIn("<title>Subpage</title>", file_content)

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "static", "homepage.css").open() as f:
            file_content = f.read()
        self.assertIn("body { background-color: yellow; }", file_content)

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "static", "homepage.js").open() as f:
            file_content = f.read()
        self.assertIn("/* homepage.js */", file_content)

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "static", "followed.txt").open() as f:
            file_content = f.read()
        self.assertIn("hello from followed.txt", file_content)

        with Path(settings.FREEZER_BUILD_DIR, "testserver", "media", "media.txt").open() as f:
            file_content = f.read()
        self.assertIn("hello from media.txt", file_content)
