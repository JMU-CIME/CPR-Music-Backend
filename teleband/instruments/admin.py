from django.contrib import admin

from .models import Transposition, Instrument


@admin.register(Transposition)
class TranspositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "transposition")
    list_filter = ("transposition",)
    search_fields = ("name",)
