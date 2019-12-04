"""Test a site with translated content."""

import io
import os
import shutil

import lxml.html
import pytest

import nikola.plugins.command.init
from nikola import __main__

from ..base import cd
from .test_empty_build import test_archive_exists  # NOQA
from .test_demo_build import (  # NOQA
    test_index_in_sitemap, test_avoid_double_slash_in_rss)


def test_translated_titles(build, output_dir, other_locale):
    """Check that translated title is picked up."""
    en_file = os.path.join(output_dir, "pages", "1", "index.html")
    pl_file = os.path.join(output_dir, other_locale, "pages", "1", "index.html")

    # Files should be created
    assert os.path.isfile(en_file)
    assert os.path.isfile(pl_file)

    # And now let's check the titles
    with io.open(en_file, 'r', encoding='utf8') as inf:
        doc = lxml.html.parse(inf)
        assert doc.find('//title').text == 'Foo | Demo Site'

    with io.open(pl_file, 'r', encoding='utf8') as inf:
        doc = lxml.html.parse(inf)
        assert doc.find('//title').text == 'Bar | Demo Site'


@pytest.fixture(scope="module")
def build(target_dir):
    """Build the site."""
    init_command = nikola.plugins.command.init.CommandInit()
    init_command.create_empty_site(target_dir)
    init_command.create_configuration(target_dir)

    src = os.path.join(os.path.dirname(__file__),
                       '..', 'data', 'translated_titles')
    for root, dirs, files in os.walk(src):
        for src_name in files:
            rel_dir = os.path.relpath(root, src)
            dst_file = os.path.join(target_dir, rel_dir, src_name)
            src_file = os.path.join(root, src_name)
            shutil.copy2(src_file, dst_file)

    with cd(target_dir):
        __main__.main(["build"])
