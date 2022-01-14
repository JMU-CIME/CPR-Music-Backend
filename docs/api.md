# To add a new Piece

Send a POST to /api/pieces with body like this:

```json
{
    "name": "Air for Band",
    "ensemble_type": "Band",
    "parts": [{
        "name": "Air for Band Melody",
        "part_type": "Melody",
        "transpositions": [{
            "transposition": "Bb",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch BC 8vb",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch BC",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch TC 8va",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch TC",
            "flatio": ""
        }, {
            "transposition": "Eb",
            "flatio": ""
        }, {
            "transposition": "F",
            "flatio": ""
        }]
    }, {
        "name": "Air for Band Bassline",
        "part_type": "Bassline",
        "transpositions": [{
            "transposition": "Bb",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch BC 8vb",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch BC",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch TC 8va",
            "flatio": ""
        }, {
            "transposition": "Concert Pitch TC",
            "flatio": ""
        }, {
            "transposition": "Eb",
            "flatio": ""
        }, {
            "transposition": "F",
            "flatio": ""
        }]
    }]
}
```
