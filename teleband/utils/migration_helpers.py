def create_part_et_al(apps, part, piece):
    Part = apps.get_model("musics", "Part")
    PartType = apps.get_model("musics", "PartType")
    PartTransposition = apps.get_model("musics", "PartTransposition")
    Transposition = apps.get_model("instruments", "Transposition")
    name = part['name']
    part_type = PartType.objects.get(name=part['part_type'])
    # print('\n\n\n\n\n===========\npart, piece')
    # print(part, piece)
    new_part = Part.objects.create(name=name, piece=piece, part_type=part_type)
    for t in part['transpositions']:
        transposition = Transposition.objects.get(name=t['transposition'])
        part_trans = PartTransposition.objects.create(part=new_part,transposition=transposition, flatio=t["flatio"])
        new_part.transpositions.add(part_trans)
    new_part.save()
    piece.parts.add(new_part)

def create_piece_et_al(apps, data):
    Piece = apps.get_model("musics", "Piece")
    EnsembleType = apps.get_model("musics", "EnsembleType")
    # print('\n\n\n\n\n===========\ndata')
    # print(data)
    already_at_piece = Piece.objects.filter(name=data['name']).exists()
    piece = None
    if not already_at_piece:
        piece = Piece.objects.create(name=data['name'], ensemble_type=EnsembleType.objects.get(name=data['ensemble_type']))
    else:
        piece = Piece.objects.get(name="Air for Band")
    piece.accompaniment = data['accompaniment']
    piece.save()
    part_data = data['parts']
    for part in part_data:
        create_part_et_al(apps, part, piece)
        