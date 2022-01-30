import pytest

from teleband.musics.models import Piece

pytestmark = pytest.mark.django_db


def test_piece_name(piece: Piece):
    assert len(piece.name) > 0
