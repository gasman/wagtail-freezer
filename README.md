# Wagtail Freezer

Generates static HTML sites from a Wagtail project


[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

[![PyPI version](https://badge.fury.io/py/wagtail-freezer.svg)](https://badge.fury.io/py/wagtail-freezer)
[![wagtail-freezer CI](https://github.com/gasman/wagtail-freezer/actions/workflows/test.yml/badge.svg)](https://github.com/gasman/wagtail-freezer/actions/workflows/test.yml)

## Links

- [Documentation](https://github.com/gasman/wagtail-freezer/blob/main/README.md)
- [Changelog](https://github.com/gasman/wagtail-freezer/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/gasman/wagtail-freezer/blob/main/CHANGELOG.md)
- [Discussions](https://github.com/gasman/wagtail-freezer/discussions)
- [Security](https://github.com/gasman/wagtail-freezer/security)

## Supported versions

- Python 3.7 - 3.10
- Django 3.x
- Wagtail 3.x

## Installation

- `pip install wagtail-freezer`
- Add `"wagtail_freezer"` to INSTALLED_APPS
- Add a `FREEZER_BUILD_DIR` setting indicating where the static files will be output. To write into a folder named `build` at the project root, use:

      FREEZER_BUILD_DIR = os.path.join(BASE_DIR, "build")

## Usage

Run `./manage.py buildstaticsite`. This will generate one folder per site within FREEZER_BUILD_DIR, with subfolders making up the page tree and the pages themselves saved as `index.html` at the appropriate point.

While building the static files, wagtail-freezer will scan the HTML for any `href` or `src` attributes that reference files under `STATIC_URL` or `MEDIA_URL`, and copy these files to corresponding folders under the site root. This step only takes place if `STATIC_URL` or `MEDIA_URL` are local URLs beginning with '/'.

If you have additional static / media files that can't be found by parsing HTML (for example, images referenced within CSS, JavaScript or JSON), you can provide a `freezer_follow_urls` method on the page model that returns a list of media / static URLs to be followed:

```python
class HomePage(Page):
    @property
    def freezer_follow_urls(self):
        urls = ['/static/images/background.jpg']
        for item in self.playlist.select_related('video'):
            urls.append(item.video.url)
        return urls
```

## Deploying

When you're happy with how the local static site works (test it by running `python -m http.server` from the root folder), you can deploy it to Amazon S3 by installing the AWS command line tool (`pip install awscli`), creating a bucket [configured for static website hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html), and running:

    aws s3 sync build/localhost s3://mysite.example.com/ --acl public-read


## Limitations

wagtail-freezer was created as a "minimum viable product" substitute for static site generators such as [django-bakery](https://django-bakery.readthedocs.io/), which at the time of writing are lagging behind in support for current Django (and Wagtail) versions. It has only been tested against very simple sites, and will probably not work with custom URL routes (RoutablePageMixin), pages with multiple preview modes (wagtail.contrib.forms, although that's not too usable on a static site anyhow), non-standard middlewares and no doubt lots of other things. Use at your own risk!
