"""
Import every model here so that `Base.metadata` (used by Alembic and by
create_all() in dev) is aware of all tables, even though nothing else in
the codebase directly imports this module.
"""
from app.models.user import User  # noqa: F401
from app.models.question import Question, QuestionConcept, InterviewType, Difficulty  # noqa: F401
from app.models.interview import Interview  # noqa: F401
from app.models.answer import Answer  # noqa: F401
from app.models.human_evaluation import HumanEvaluation  # noqa: F401
