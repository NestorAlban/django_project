import datetime
import random
from secrets import choice
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


#lo más común a testear son modelos y clases

class QuestionModelTests(TestCase):

    def test_was_published_recently_future_questions(self):
        """was_published_recently returns False for questions whose published_date is in the future"""
        days_int = random.randint(1, 30)
        time = timezone.now() + datetime.timedelta(days = days_int)
        test_future_question = Question(
            question_text = "¿Quién es el mejor Course Director de Platzi?",
            published_date = time
        )
        # sirve self.assertEqual como el assertIs
        print("=========================")
        print(
            test_future_question.question_text, 
            test_future_question.published_date,
            test_future_question.was_published_recently()
        )
        print("=========================")
        self.assertIs(
            test_future_question.was_published_recently(), 
            False
        )

    def test_was_published_recently_past_questions(self):
        """was_published_recently returns False for questions whose published_date is, at least, 1 day in the past"""
        days_int = random.randint(1, 30)
        time = timezone.now() - datetime.timedelta(days = days_int)
        test_past_question = Question(
            question_text = "¿Quién es el mejor Course Director de Platzi?",
            published_date = time
        )
        print("=========================")
        print(
            test_past_question.question_text, 
            test_past_question.published_date,
            test_past_question.was_published_recently())
        print("=========================")
        self.assertIs(
            test_past_question.was_published_recently(), 
            False
        )

    def test_was_published_recently_actual_questions(self):
        """was_published_recently returns True for questions whose published_date is now"""
        time = timezone.now()
        test_actual_question = Question(
            question_text = "¿Quién es el mejor Course Director de Platzi?",
            published_date = time
        )
        print("=========================")
        print(
            test_actual_question.question_text, 
            test_actual_question.published_date,
            test_actual_question.was_published_recently())
        print("=========================")
        self.assertIs(
            test_actual_question.was_published_recently(), 
            True
        )

def create_question(question_text, days):
    """
    Create a question with a given "question_text", and published the given
    number of days offset to now (negative for questions published in the past,
    positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(
        question_text = question_text, 
        published_date = time
    )

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exist, a message will be displayed"""
        response = self.client.get(reverse("polls:index"))
        print(response)
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertContains(
            response, 
            "No polls are avaliable."
        )
        self.assertQuerysetEqual(
            response.context["lastest_question_list"], 
            []
        )

    def test_future_questions_self(self):
        """If future a question exist, it won't be displayed"""
        days_int = random.randint(1, 30)
        future_time = timezone.now() + datetime.timedelta(days = days_int)
        test_future_question = Question(
            question_text = "¿Quién es el mejor Course Director de Platzi?",
            published_date = future_time
        )
        test_future_question.save()
        actual_time = timezone.now()
        test_actual_question = Question(
            question_text = "¿Quién es el mejor CD de Platzi?",
            published_date = actual_time
        )
        test_actual_question.save()
        response = self.client.get(reverse("polls:index"))
        print(response)
        print(test_actual_question.question_text)
        self.assertEqual(
            response.status_code, 
            200
        )
        self.assertContains(
            response, 
            test_actual_question.question_text
        )
        self.assertNotContains(
            response, 
            test_future_question.question_text
        )
    
    def test_future_question(self):
        """
        Questions with a published_date in the future aren't displayed on the index page.
        """
        create_question(
            "Future question", 
            days = 30
        )
        response = self.client.get(reverse("polls:index"))
        self.assertContains(
            response, 
            "No polls are avaliable."
        )
        self.assertQuerysetEqual(
            response.context["lastest_question_list"], 
            []
        )

    def test_past_question(self):
        """
        Questions with a published_date in the future are displayed on the index page.
        """
        past_question = create_question(
            "Past question", 
            days = -10
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"], 
            [past_question]
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed.
        """
        past_question = create_question(
            "Past question", 
            days = -10
        ) 
        future_question = create_question(
            "Future question", 
            days = 30
        ) 
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """The questions index page may display multiple questions."""
        past_question1 = create_question(
            "Past question 1", 
            days = -10
        ) 
        past_question2 = create_question(
            "Past question 2", 
            days = -15
        ) 
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_question(self):
        """The questions index page may display multiple questions."""
        future_question1 = create_question(
            "Future question 1", 
            days = 10
        ) 
        future_question2 = create_question(
            "Future question 2", 
            days = 15
        ) 
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"],
            []
        )

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a published_date in the future
        returns a 404 error not found.
        """
        future_question = create_question(
            "Future question", 
            days = 30
        ) 
        url = reverse(
            "polls:detail", 
            args =(future_question.id,)
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 
            404
        )

    def test_past_question(self):
        """
        The detail view of a question with a published_date in the past
        displays the question's text.
        """
        past_question = create_question(
            "Past question", 
            days = -30
        ) 
        url = reverse(
            "polls:detail", 
            args =(past_question.id,)
        )
        response = self.client.get(url)
        self.assertContains(
            response, 
            past_question.question_text
        )


class QuestionResultsViewTests(TestCase):
    def test_question_not_exist(self):
        """If question id not exists shows error 404"""
        url = reverse(
            "polls:results",
            args = (1,)
        )
        response = self.client.get(url) 
        self.assertEqual(
            response.status_code,
            404
        )


# class QuestionModelTests(TestCase):

#     def test_no_create_question_without_choices(self):
#         """If there aren't choices, the question isn't going to be created."""
#         test_question = Question.objects.create(
#             question_text = "¿Quién es el mejor Course Director de Platzi?",
#             published_date = timezone.now(),
#             choices = 0 
#         )

# Create your tests here.
