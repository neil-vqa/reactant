class ReactionException(Exception):
    pass


class RenderFailed(ReactionException):
    def __init__(self, file_kind: str) -> None:
        message = f"Rendering {file_kind} failed."
        super().__init__(message)
