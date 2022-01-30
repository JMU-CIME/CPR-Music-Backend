import pytest
from django.urls import resolve, reverse

from teleband.instruments.models import Instrument

pytestmark = pytest.mark.django_db


def test_user_detail(instrument: Instrument):
    assert (
        reverse("api:instrument-detail", kwargs={"id": instrument.id})
        == f"/api/instruments/{instrument.id}/"
    )
    assert resolve(f"/api/instruments/{instrument.id}/").view_name == "api:instrument-detail"


def test_instrument_list():
    assert reverse("api:instrument-list") == "/api/instruments/"
    assert resolve("/api/instruments/").view_name == "api:instrument-list"
