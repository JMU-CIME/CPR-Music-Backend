from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import EnsembleType, Composer, Piece, Part, PartTransposition, PartType


@admin.register(EnsembleType)
class EnsembleTypeAdmin(VersionAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(PartType)
class PartTypeAdmin(VersionAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Composer)
class ComposerAdmin(VersionAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)


@admin.register(Piece)
class PieceAdmin(VersionAdmin):
    list_display = (
        "id",
        "name",
        "composer",
        "video",
        "audio",
        "date_composed",
        "ensemble_type",
    )
    list_filter = ("composer", "ensemble_type")
    search_fields = ("name",)


@admin.register(Part)
class PartAdmin(VersionAdmin):
    list_display = ("id", "name", "piece")
    list_filter = ("piece",)
    search_fields = ("name",)


@admin.register(PartTransposition)
class PartTranspositionAdmin(VersionAdmin):
    list_display = ("id", "part", "transposition", "notation")
    list_filter = ("part", "transposition")
