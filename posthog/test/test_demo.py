import random

from posthog.models import Action, Dashboard, Event, Person, SessionRecordingEvent, Team
from posthog.test.base import BaseTest


class TestDemo(BaseTest):
    TESTS_API = True

    def test_create_demo_data(self):
        random.seed(900)

        self.client.get("/demo")
        demo_team = Team.objects.get(name__icontains="demo")
        self.assertEqual(Dashboard.objects.count(), 3)
        self.assertGreaterEqual(Event.objects.count(), 900)
        self.assertGreaterEqual(Person.objects.count(), 160)
        self.assertGreaterEqual(Action.objects.count(), 8)
        self.assertGreaterEqual(SessionRecordingEvent.objects.count(), 60)

        action_event_counts = [action.events.count() for action in Action.objects.all()]
        self.assertCountEqual(action_event_counts, [11, 122, 0, 0, 40, 100, 73, 91])

        self.assertIn("$pageview", demo_team.event_names)
