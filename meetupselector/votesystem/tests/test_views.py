from django.test import (
    Client,
    TestCase
)
from django.urls import reverse

from ..models import TopicProposal


class TopicProposalTestcase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_it_serves_topic_proposal_view(self):
        response = self.client.get(reverse('topic_proposal'))

        self.assertEqual(response.status_code, 200)

    def test_it_renders_form(self):
        url = reverse('topic_proposal')
        form_html = f'<form action="{url}" method="post"'
        topic_html = '<input type="text" name="topic"'
        description_html = '<textarea name="description"'
        level_html = '<select name="level"'

        response = self.client.get(reverse('topic_proposal'))

        self.assertContains(response=response, text=form_html)
        self.assertContains(response=response, text=topic_html)
        self.assertContains(response=response, text=description_html)
        self.assertContains(response=response, text=level_html)

    def test_it_validates_topic_form_fields(self):
        required_field_error = 'This field is required.'
        invalid_value_error = 'Select a valid choice. anything is not one of the available choices.'

        response = self.client.post(
            reverse('topic_proposal'),
            {'topic': '', 'description': '', 'level': 'anything'}
        )

        self.assertFormError(response=response, form='topic_form', field='topic', errors=required_field_error)
        self.assertFormError(response=response, form='topic_form', field='description', errors=required_field_error)
        self.assertFormError(response=response, form='topic_form', field='level', errors=invalid_value_error)

    def test_it_creates_a_topic_proposal(self):
        url = reverse('topic_proposal')
        form_data = {
            'topic': 'Anything',
            'description': 'Have fun and drink beers',
            'level': 'BASIC'
        }

        self.client.post(url, form_data)

        created_topic_proposals = TopicProposal.objects.filter(**form_data)
        self.assertEqual(created_topic_proposals.count(), 1)
