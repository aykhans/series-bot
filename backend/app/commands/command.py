import typer

if __name__ == "__main__":
    from pathlib import Path
    from sys import path
    path.append(str(Path(__file__).parent.parent.parent))

    from app.commands import user

    command = typer.Typer()
    command.add_typer(user.command, name='user')
    command()
