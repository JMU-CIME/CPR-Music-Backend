from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Transposition, Instrument


@admin.register(Transposition)
class TranspositionAdmin(VersionAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Instrument)
class InstrumentAdmin(VersionAdmin):
    list_display = ("id", "name", "transposition")
    list_filter = ("transposition",)
    search_fields = ("name",)
