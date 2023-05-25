import typer

from bookify.commands import convert_command

app = typer.Typer()
app.command()(convert_command)


if __name__ == "__main__":
    app()
