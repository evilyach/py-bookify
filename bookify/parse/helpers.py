def get_filename(count: int, name: str, title: str) -> str:
    formatted_name = name.lower().translate(str.maketrans({" ": "-"}))

    return f"{count}-{formatted_name}-{title}"
