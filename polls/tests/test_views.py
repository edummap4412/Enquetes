import datetime


from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):

    """
    Cria question dando 'question_text' e publica dando o número de dias ( negativo para
    question antigas , positivos para que questions não publicadas)

    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Se a question existe , uma mensagem aparece no display
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions com um pub_date no passado são mostradas no página 'index'
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question], )

    def test_future_question(self):
        """
        Quetions com a pub_date no futuro não são mostradas na página index.
        """

        create_question(question_text="Fuete question",days=30)
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Mesmo se ambas  questions existirem , tanto no passado quanto no futuro,
        somente as que estão no passados serão mostradas
        """

        question = create_question(question_text ="Past question.", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question]
        )

    def test_two_past_question(self):
        """
         As questões que aparecem no página index podem mostrar multiplas questions.
        """
        question1 = create_question(question_text ="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],[question2, question1]
        )
