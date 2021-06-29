
from django.test import TestCase
from django.urls import reverse
from polls.models import Question
from polls.tests.test_views import create_question


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        O detail view das questionc om um pub_date no futuro retorna um '404 not found'
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Os detail view da question com a pub_date o passa são mostados nos text da questão
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

