HOUSE_POINTS_ATTRIBUTES = {
    "house": {
        "type": "string",
        "size": 100,
        "required": True,
        "default": None,
        "array": False,
    },
    "points": {
        "type": "float",
        "required": True,
        "min": 0,
        "max": 100000000,
        "default": 0,
        "array": False,
    },
}
