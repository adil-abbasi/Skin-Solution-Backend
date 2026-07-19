from sqlalchemy.orm import Session


def generate_code(
    db: Session,
    model,
    prefix: str,
    code_field: str
) -> str:
    """
    Generate sequential codes like:
    DOC-001
    PAT-000001
    """

    latest = (
        db.query(model)
        .order_by(model.id.desc())
        .first()
    )

    if latest is None:
        number = 1
    else:
        last_code = getattr(latest, code_field)

        try:
            number = int(last_code.split("-")[1]) + 1
        except (IndexError, ValueError):
            number = latest.id + 1

    if prefix == "DOC":
        return f"{prefix}-{number:03d}"

    return f"{prefix}-{number:06d}"