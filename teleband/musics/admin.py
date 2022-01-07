from django.contrib import admin

from .models import EnsembleType, Composer, Piece, Part, PartTransposition


@admin.register(EnsembleType)
class EnsembleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Composer)
class ComposerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
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
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "piece")
    list_filter = ("piece",)
    search_fields = ("name",)


@admin.register(PartTransposition)
class PartTranspositionAdmin(admin.ModelAdmin):
    list_display = ("id", "part", "transposition", "notation")
    list_filter = ("part", "transposition")
