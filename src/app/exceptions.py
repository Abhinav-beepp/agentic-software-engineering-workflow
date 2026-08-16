class AppError(Exception):
    """Base application error."""


class NotFoundError(AppError):
    pass


class CollisionError(AppError):
    pass


class WorkflowError(AppError):
    pass


class ApprovalRequiredError(WorkflowError):
    pass
