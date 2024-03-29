# Generated by Django 3.2.11 on 2023-09-20 14:15

from django.db import migrations

parts = {
    "Air for Band Melody": "sample_audio/Air_for_Band_Trumpet_Melody.mp3",
    "Air for Band Bassline": "sample_audio/Air_for_Band_Bass_Line.mp3",
    "Celebration for a New Day Melody": "sample_audio/Celebration_of_a_New_Day_Melody_Recording.mp3",
    "Celebration for a New Day Bassline": "sample_audio/Celebration_of_New_Day_Bass_Line_Recording.mp3",
    "America the Beautiful Melody": "sample_audio/America_the_Beautiful_Melody_Recording.mp3",
    "America the Beautiful Bassline": "sample_audio/America_the_Beautiful_Bass_Line_Recording.mp3",
    "The Favorite Melody": "sample_audio/The_Favorite_Melody_Recording.mp3",
    "The Favorite Bassline": "sample_audio/The_Favorite_Bass_Line.mp3",
    "Freedom 2040 (Band) Melody": "sample_audio/Freedom_2040_-_Melody.mp3",
    "Freedom 2040 (Band) Bassline": "sample_audio/Freedom_2040_-_Bassline.mp3",
    "Freedom 2040 (Orchestra) Melody": "sample_audio/Freedom_2040_-Orchestra-_-_Melody_-F-.mp3",
    "Freedom 2040 (Orchestra) Bassline": "sample_audio/Freedom_2040_-Orchestra-_-_Bass_Line__-F-.mp3",
    "Down by the Riverside Melody": "sample_audio/Down_by_the_Riverside_-_Melody.mp3",
    "Down by the Riverside Bassline": "sample_audio/Down_by_the_Riverside_-_Bassline.mp3",
    "Deep River Melody": "sample_audio/Deep_River_-_Melody.mp3",
    "Deep River Bassline": "sample_audio/Deep_River_-_Bassline.mp3",
    "I Want to be Ready Melody": "sample_audio/I_Want_to_be_Ready_-_Melody.mp3",
    "I Want to be Ready Bassline": "sample_audio/I_Want_to_be_Ready_-_Bassline.mp3",
    "Beginning Band - When the Saints Go Marching In Melody": "sample_audio/When_the_Saints_Bass-beg-band-sample.mp3",
    "Beginning Band - When the Saints Go Marching In Bassline": "sample_audio/When_the_Saints_-_Melody-beg-band-sample.mp3",
    "Beginning Band - Ode to Joy Melody": "sample_audio/ODE_TO_JOY_Melody_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Ode to Joy Bassline": "sample_audio/ODE_TO_JOY_Bass_Line_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - London Bridge Melody": "sample_audio/LONDON_BRIDGE_Melody_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - London Bridge Bassline": "sample_audio/LONDON_BRIDGE_Bass_Line_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Jolly Old St. Nick Melody": "sample_audio/JOLLY_OLD_ST._NICHOLAS_Melody_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Jolly Old St. Nick Bassline": "sample_audio/JOLLY_OLD_ST._NICHOLAS_Bass_Line_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Jingle Bells Melody": "sample_audio/JINGLE_BELLS_Melody_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Jingle Bells Bassline": "sample_audio/JINGLE_BELLS_Bass_Line_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Hot Cross Buns Melody": "sample_audio/HOT_CROSS_BUNS_Melody_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Hot Cross Buns Bassline": "sample_audio/HOT_CROSS_BUNS_Bass_Line_Concert_Pitch-beg-band-sample.mp3",
    "Beginning Band - Good King Wenceslas Melody": "sample_audio/Good_King_Wenceslas_-_Melody-beg-band-sample.mp3",
    "Beginning Band - Good King Wenceslas Bassline": "sample_audio/Good_King_Wenceslas_-_Bass-beg-band-sample.mp3",
    "Beginning Band - Go Tell Aunt Rhody Melody": "sample_audio/Go_Tell_Aunt_Rhody_Melody_-beg-band-sample.mp3",
    "Beginning Band - Go Tell Aunt Rhody Bassline": "sample_audio/Go_Tell_Aunt_Rhody_-_Bass-beg-band-sample.mp3",
    "Beginning Band - Aura Lee Melody": "sample_audio/Aura_Lee_-_Melody-beg-band-sample.mp3",
    "Beginning Band - Aura Lee Bassline": "sample_audio/Aura_Lee_-_Bass-beg-band-sample.mp3",
    "Beginning Band - Amazing Grace Melody": "sample_audio/Amazing_Grace_-_Melody-beg-band-sample.mp3",
    "Beginning Band - Amazing Grace Bassline": "sample_audio/Amazing_Grace_-_Bass-beg-band-sample.mp3",
    "Beginning Orchestra - Bile em Cabbage Down Melody": "sample_audio/Bile_em_Cabbage_Down_-_Melody-beg-orch-sample.mp3",
    "Beginning Orchestra - Bile em Cabbage Down Bassline": "sample_audio/Bile_em_Cabbage_Down_-_Bassline-beg-orch-sample.mp3",
    "Beginning Orchestra - Go Tell Aunt Rhody Melody": "sample_audio/Go_Tell_Aunt_Rhody_-_Melody-beg-orch-sample.mp3",
    "Beginning Orchestra - Go Tell Aunt Rhody Bassline": "sample_audio/Go_Tell_Aunt_Rhody_-Bassline-beg-orch-sample.mp3",
    "Beginning Orchestra - Good King Wenceslas Melody": "sample_audio/Good_King_Wenceslas_-_Melody-beg-orch-sample.mp3",
    "Beginning Orchestra - Good King Wenceslas Bassline": "sample_audio/Good_King_Wenceslas_-_Bassline-beg-orch-sample.mp3",
    "Beginning Orchestra - Hot Cross Buns Melody": "sample_audio/Hot_Cross_Buns_-_Melody-beg-orch-sample.mp3",
    "Beginning Orchestra - Hot Cross Buns Bassline": "sample_audio/Hot_Cross_Buns_-_Bassline-beg-orch-sample.mp3",
}


def update_site_forward(apps, schema_editor):
    Part = apps.get_model("musics", "Part")
    for part_name, part_sample in parts.items():
        part = Part.objects.get(name=part_name)
        part.sample_audio = part_sample
        part.save()


class Migration(migrations.Migration):
    dependencies = [
        ("musics", "0020_auto_20230918_1451_seed_beginning_orchestra"),
    ]

    operations = [migrations.RunPython(update_site_forward, migrations.RunPython.noop)]
