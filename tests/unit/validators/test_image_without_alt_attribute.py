#!/usr/bin/python
# -*- coding: utf-8 -*-

import lxml.html
from mock import Mock, call
from preggy import expect

from holmes.config import Config
from tests.unit.base import ValidatorTestCase
from holmes.reviewer import Reviewer
from holmes.validators.image_without_alt_attribute import (
    ImageWithoutAltAttributeValidator
)
from tests.fixtures import PageFactory


class TestImageWithoutAltAttributeValidator(ValidatorTestCase):

    def test_can_validate_image_without_alt_attribute_on_globo_html(self):
        config = Config()

        page = PageFactory.create()

        reviewer = Reviewer(
            api_url='http://localhost:2368',
            page_uuid=page.uuid,
            page_url=page.url,
            config=config,
            validators=[]
        )

        content = self.get_file('globo.html')

        result = {
            'url': page.url,
            'status': 200,
            'content': content,
            'html': lxml.html.fromstring(content)
        }
        reviewer.responses[page.url] = result
        reviewer.get_response = Mock(return_value=result)

        validator = ImageWithoutAltAttributeValidator(reviewer)
        validator.add_violation = Mock()
        validator.review.data = {
            'page.all_images': [{
                'src': 'the-src'
            }]
        }
        validator.validate()

        expect(validator.add_violation.call_args_list).to_include(
            call(key='invalid.images.alt',
                 title='Image(s) without alt attribute',
                 description='Images without alt text are not good for Search Engines. Images without alt were found for: <a href="http://my-site.com/the-src" target="_blank">the-src</a>.',
                 points=20))