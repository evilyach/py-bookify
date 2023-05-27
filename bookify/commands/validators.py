from typer import BadParameter


def validate_urls(value: list[str]) -> list[str]:
    if len(value) == 0:
        raise BadParameter("You provided no URLs...")

    return value
