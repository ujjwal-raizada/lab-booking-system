import datetime
from datetime import timedelta

from django.test import TestCase

from ..factories import InstrumentFactory
from ..forms import BulkCreateSlotsForm
from ..models import Slot


class OverlappingSlotTestCase(TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        instr = InstrumentFactory()
        self.slot = Slot.objects.create(instrument=instr, status=Slot.STATUS_1, date=datetime.date.today(),
                                        start_time=self.now, end_time=self.now + timedelta(minutes=30))

    def test_when_new_completely_inside_old(self):
        slot = self.slot
        now = self.now
        manager = Slot.objects

        # completely equivalent or inside existing slot
        slot.start_time = now + timedelta(minutes=0)
        slot.end_time = now + timedelta(minutes=29)
        self.assertTrue(manager.is_slot_overlapping(slot))

        # begins before existing slot ends and ends after
        slot.start_time = now + timedelta(minutes=1)
        slot.end_time = now + timedelta(minutes=31)
        self.assertTrue(manager.is_slot_overlapping(slot))

        # begins before existing slot begins and ends after
        slot.start_time = now - timedelta(minutes=1)
        slot.end_time = now + timedelta(minutes=1)
        self.assertTrue(manager.is_slot_overlapping(slot))

        # subsumes or equivalent to existing slot
        slot.start_time = now - timedelta(minutes=0)
        slot.end_time = now + timedelta(minutes=31)
        self.assertTrue(manager.is_slot_overlapping(slot))

        # perfect slot
        slot.start_time = now + timedelta(minutes=30)
        slot.end_time = now + timedelta(minutes=31)
        self.assertFalse(manager.is_slot_overlapping(slot))

    def test_when_old_start_time_between_new_times(self):
        # new.start_time < old.start_time < new.end_time
        self.slot.start_time = self.now + timedelta(minutes=1)
        self.slot.end_time = self.now + timedelta(minutes=31)
        self.assertTrue(Slot.objects.is_slot_overlapping(self.slot))

    def test_when_old_end_time_within_new_times(self):
        # new.start_time < old.end_time < new.end_time
        self.slot.start_time = self.now - timedelta(minutes=1)
        self.slot.end_time = self.now + timedelta(minutes=1)
        self.assertTrue(Slot.objects.is_slot_overlapping(self.slot))

    def test_when_old_completley_inside_new(self):
        # new.start_time <= old.start_time < old.end_time <= new.end_time
        self.slot.start_time = self.now - timedelta(minutes=0)
        self.slot.end_time = self.now + timedelta(minutes=31)
        self.assertTrue(Slot.objects.is_slot_overlapping(self.slot))

    def test_when_same_time_for_old_and_new(self):
        # new.start_time == old.start_Time && old.end_time == new.end_time
        new = self.slot
        new.pk = None
        self.assertTrue(Slot.objects.is_slot_overlapping(self.slot))

    def test_valid_slot(self):
        self.slot.start_time = self.now + timedelta(minutes=30)
        self.slot.end_time = self.now + timedelta(minutes=31)
        self.assertFalse(Slot.objects.is_slot_overlapping(self.slot))


class BulkCreateSlotsFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instr = InstrumentFactory()

    def setUp(self):
        # We create a base valid form. Each test will modify and make it invalid.
        self.now = datetime.datetime.now()
        self.form = BulkCreateSlotsForm(data={
            'instrument': str(self.instr.pk),
            'start_date': str(datetime.date.today()),
            'start_time': str(self.now.time()),
            'end_time': str((self.now + timedelta(minutes=30)).time()),
            'slot_duration': "30",
            'for_the_next': "7",
        })

    def test_invalid_duration(self):
        form = self.form
        form.data['slot_duration'] = "0"
        self.assertEqual(
            form.errors['slot_duration'], ["The duration in minutes must be a positive integer."]
        )

    def test_start_time_after_end_time(self):
        form = self.form
        form.data['start_time'] = str((self.now + timedelta(minutes=31)).time())
        self.assertEqual(
            form.errors['start_time'], ["Start time cannot be after end time."]
        )

    def test_start_date_before_today(self):
        form = self.form
        form.data['start_date'] = str((self.now - timedelta(days=1)).date())
        self.assertEqual(
            form.errors['start_date'], ["Start date cannot be before today."]
        )

    def test_duration_gives_whole_number_of_slots(self):
        form = self.form
        form.data['slot_duration'] = "31"
        self.assertIn(
            "Cannot create whole number of slots between specified start and "
            "end time with the given duration.",
            form.non_field_errors(),
        )

    def test_valid_form(self):
        self.assertTrue(self.form.is_valid())
