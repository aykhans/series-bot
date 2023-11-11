async def create_sub(
    uuid: str,
    is_active: bool = True,
    is_superuser: bool = False
) -> str:
    """
    Create a JWT subject string based on the provided UUID and user flags.

    Args:
        uuid (str): The UUID of the user.
        is_active (bool, optional): Whether the user is active.
        is_superuser (bool, optional): Whether the user is a superuser.

    Returns:
        str: The JWT subject string (pattern: uuid$is_active$is_superuser).
    """
    return f"{uuid}$"\
            f"{'true' if is_active is True else 'false'}$"\
                f"{'true' if is_superuser is True else 'false'}"
