import typer
from pydantic import ValidationError
from rich.console import Console
from rich.prompt import Confirm, Prompt

from app.crud import crud_user
from app.db.session import SessionLocal
from app.schemas import UserCreateCommand

command = typer.Typer()
console = Console(stderr=True)


def get_db():
    with SessionLocal() as db:
        return db

@command.command('create')
def create_user():
    user = UserCreateCommand()
    db = get_db()

    while True:
        username = Prompt.ask('*Username')

        try:
            user.username = username
            if crud_user.get_by_username(db=db, username=username) is not None:
                console.print(
                    f'[red]Username {username} already exists\n[/red]'
                )
                continue
            break
        except ValidationError as exc:
            console.print(exc)
            continue

    while True:
        email = Prompt.ask('Email', default=None)
        if email is None:
            break

        try:
            user.email = email
            if crud_user.get_by_email(db=db, email=email) is not None:
                console.print(f'[red]Email {email} already exists\n[/red]')
                continue
            break
        except ValidationError as exc:
            console.print(exc)
            continue

    while True:
        password = Prompt.ask('*Password', password=True)
        try:
            user.password = password

            confirm_password = Prompt.ask('*Confirm password', password=True)
            if confirm_password != password:
                console.print('[red]Passwords do not match\n[/red]')
                continue

            break
        except ValidationError as exc:
            console.print(exc)
            continue

    user.is_active = Confirm.ask('Is active?', default=True)
    user.is_superuser = Confirm.ask('Is superuser?', default=True)

    crud_user.create(db=db, obj_in=user)

    console.print('[green]\nUser created successfully[/green]')
    console.print_json(user.model_dump_json())
