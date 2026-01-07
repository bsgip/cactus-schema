from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto
from typing import Generic, TypeVar

from cactus_test_definitions.client import TestProcedureId
from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import LetterCase

HEADER_USER_NAME = "CACTUS-User-Name"
HEADER_TEST_ID = "CACTUS-Test-Id"
HEADER_RUN_ID = "CACTUS-Run-Id"
HEADER_GROUP_ID = "CACTUS-Group-Id"
HEADER_GROUP_NAME = "CACTUS-Group-Name"


class RunStatusResponse(StrEnum):
    initialised = auto()
    started = auto()
    finalised = auto()
    provisioning = auto()


PaginatedType = TypeVar("PaginatedType")


class FastAPICompatibleWizard(JSONWizard):
    """This is our way of generating JSON that FastAPI should happily interact with directly as a dataclass"""

    class Meta(JSONWizard.Meta):
        key_transform_with_dump = LetterCase.SNAKE
        key_transform_with_load = LetterCase.SNAKE
        encode_enum_as_value = True
        datetime_to = "iso"


@dataclass
class Pagination(Generic[PaginatedType]):
    total_pages: int
    total_items: int
    page_size: int
    current_page: int
    prev_page: int | None
    next_page: int | None

    items: list[PaginatedType]


@dataclass
class InitRunRequest(FastAPICompatibleWizard):
    test_procedure_id: TestProcedureId


@dataclass
class StartRunResponse(FastAPICompatibleWizard):
    test_url: str


@dataclass
class InitRunResponse(StartRunResponse):
    run_id: int


@dataclass
class RunResponse(FastAPICompatibleWizard):
    run_id: int
    test_procedure_id: str
    test_url: str
    status: RunStatusResponse
    all_criteria_met: bool | None  # Whether this run has been assessed as successful or not (None means unknown)
    created_at: datetime
    finalised_at: datetime | None
    is_device_cert: bool  # Whether this run was initialised with the device cert or aggregator cert
    has_artifacts: bool  # Whether this run has artifacts available (False if not finalized or there was an failure during finalization)


@dataclass
class RunGroupRequest(FastAPICompatibleWizard):
    csip_aus_version: str


@dataclass
class GenerateClientCertificateRequest(FastAPICompatibleWizard):
    is_device_cert: bool


@dataclass
class RunGroupUpdateRequest(FastAPICompatibleWizard):
    """NOTE - this is explicitly NOT allowing updates on csip-aus version - it has too many weird considerations and
    realistically, a user should just create a new group if they want to test against a new version (there is no
    practical need to allow migrating legacy version test runs to a newer version)"""

    name: str | None  # If non null - update the RunGroup receiving this request


@dataclass
class RunGroupResponse(FastAPICompatibleWizard):
    run_group_id: int
    name: str
    csip_aus_version: str
    created_at: datetime

    is_device_cert: bool | None
    certificate_id: int | None
    certificate_created_at: datetime | None

    total_runs: int  # How many runs live underneath this group


@dataclass
class UserWithRunGroupsResponse(FastAPICompatibleWizard):
    """Represents a user with all their associated run groups"""

    user_id: int
    subject_id: str
    name: str | None
    run_groups: list[RunGroupResponse]


@dataclass
class CSIPAusVersionResponse(FastAPICompatibleWizard):
    """Represents the various CSIP-Aus versions available for testing"""

    version: str  # Derived from the cactus_test_definitions.CSIPAusVersion enum


@dataclass
class TestProcedureResponse(FastAPICompatibleWizard):
    __test__ = False
    test_procedure_id: TestProcedureId
    description: str
    category: str
    classes: list[str]


@dataclass
class TestProcedureRunSummaryResponse(FastAPICompatibleWizard):
    __test__ = False
    test_procedure_id: TestProcedureId
    description: str
    category: str
    classes: list[str] | None
    run_count: int  # Count of runs for this test procedure
    latest_all_criteria_met: bool | None  # Value for all_criteria_met of the most recent Run
    latest_run_status: int | None  # RunStatus of the most recent Run
    latest_run_id: int | None  # run_id of the most recent Run
    latest_run_timestamp: datetime | None  # timestamp of the most recent Run


@dataclass
class UserConfigurationRequest(FastAPICompatibleWizard):
    subscription_domain: str | None  # What domain will outgoing notifications be scoped to? If None - no update
    is_static_uri: (
        bool | None
    )  # If true - all test instances will share the same URI (limit to 1 test at a time). If None - no update
    pen: int | None


@dataclass
class UserUpdateRequest(FastAPICompatibleWizard):
    user_name: str


@dataclass
class UserConfigurationResponse(FastAPICompatibleWizard):
    subscription_domain: str  # What domain will outgoing notifications be scoped to? Empty string = no value configured
    is_static_uri: bool  # If true - all test instances will share the same URI (limit to 1 test at a time).
    pen: int
    static_uri: str | None  # What the static URI will be for this user (readonly and only set if is_static_uri is True)
