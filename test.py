text = """
    "Gathering Song": "Song",
    Greeting: "Text",
    Kyrie: "Text",
    "Prayer of the Day": "Text",
    "First Reading": "Text",
    Psalm: "Text",
    "Second Reading": "Text",
    "Gospel Acclamation": "Text",
    Gospel: "Text",
    Sermon: "Text",
    "Song of the Day": "Song",
    Creed: "Text",
    "Prayers of Intercession": "Text",
    Dialogue: "Text",
    Preface: "Text",
    "Holy, Holy, Holy": "Text",
    Thanksgiving: "Text",
    "Lord's Prayer": "Text",
    Communion: "Text",
    "Communion Song": "Text",
    "Communion Blessing": "Text",
    "Prayer after Communion": "Text",
    Blessing: "Text",
    "Sending Song": "Song",
    Dismissal: "Text",
"""

for line in text.strip().splitlines():
    print(
        "{name: "
        + line.strip().split(":")[0]
        + ", type: ServiceElementType."
        + line.strip().split(":")[1].split(",")[0].replace("\"", "").strip()
        + "},"
    )
