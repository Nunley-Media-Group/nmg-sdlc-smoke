def greet(name: str) -> str:
    """Return a greeting for a non-blank name."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must not be blank")
    return f"Hello, {name}"
