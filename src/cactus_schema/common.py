from dataclasses import dataclass

from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import LetterCase


class FastAPICompatibleWizard(JSONWizard):
    """This is our way of generating JSON that FastAPI should happily interact with directly as a dataclass"""

    class Meta(JSONWizard.Meta):
        key_transform_with_dump = LetterCase.SNAKE
        key_transform_with_load = LetterCase.SNAKE
        encode_enum_as_value = True
        datetime_to = "iso"


@dataclass
class ProceedResponse(FastAPICompatibleWizard):
    """Shared between orchestrator and runner - lives here to avoid a circular import."""

    handled: bool  # If true, the proceed signal matched a listener and moved the test to the next step
