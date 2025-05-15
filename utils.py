def format_name(name: str) -> str:
    name = name.lower().replace(" ", "-").replace(".png", "")
    return name if name.endswith(".pdf") else name + ".pdf"
