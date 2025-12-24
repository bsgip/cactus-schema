from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, StrEnum, auto
from http import HTTPMethod, HTTPStatus

from cactus_test_definitions import CSIPAusVersion
from cactus_test_definitions.client import TestProcedureId
from dataclass_wizard import JSONWizard


class ClientInteractionType(StrEnum):
    RUNNER_START = "Runner Started"
    TEST_PROCEDURE_INIT = "Test Procedure Initialised"
    TEST_PROCEDURE_START = "Test Procedure Started"
    PROXIED_REQUEST = "Request Proxied"


class StepStatus(Enum):
    PENDING = 0  # The step is not yet active
    ACTIVE = auto()  # The step is currently active but not complete
    RESOLVED = auto()  # The step has been full resolved


@dataclass
class RequestEntry(JSONWizard):
    url: str
    path: str
    method: HTTPMethod
    status: HTTPStatus
    timestamp: datetime
    step_name: str
    body_xml_errors: list[str]  # Any XML schema errors detected in the incoming body
    request_id: int  # Increments per test


@dataclass
class InitResponseBody(JSONWizard):
    status: str
    test_procedure: str
    timestamp: datetime
    is_started: bool = (
        False  # True if the run has progressed to the started state. False if it's still waiting for a call to start it
    )


@dataclass
class CriteriaEntry(JSONWizard):
    success: bool
    type: str
    details: str


@dataclass
class PreconditionCheckEntry(JSONWizard):
    success: bool
    type: str
    details: str


@dataclass
class DataStreamPoint(JSONWizard):
    watts: int | None  # The data point value (in watts)
    offset: str  # Label for identifying the relative start - usually something like "2m20s"


@dataclass
class TimelineDataStreamEntry(JSONWizard):
    label: str  # Descriptive label of this data stream
    data: list[DataStreamPoint]
    stepped: bool  # If True - this data should be presented as a stepped line chart
    dashed: bool  # If True - this data should be a dashed line


@dataclass
class TimelineStatus(JSONWizard):
    data_streams: list[TimelineDataStreamEntry]  # The set of data streams that should be rendered on the timeline
    set_max_w: int | None  # The currently set set_max_w (if any)
    now_offset: str  # The name of the DataStreamPoint.offset that corresponds with "now" (when this was calculated)


@dataclass
class EndDeviceMetadata(JSONWizard):  # All optional as a device may not always be registered
    edevid: int | None = None  # Should always be 1, but nice to check
    lfdi: str | None = None
    sfdi: int | None = None
    nmi: str | None = None
    aggregator_id: int | None = None
    set_max_w: int | None = None
    doe_modes_enabled: int | None = None
    device_category: int | None = None
    timezone_id: str | None = None


@dataclass
class StartResponseBody(JSONWizard):
    status: str
    test_procedure: str
    timestamp: datetime


@dataclass
class RequestData(JSONWizard):
    request_id: int
    request: str | None
    response: str | None


@dataclass
class ClientInteraction(JSONWizard):
    interaction_type: ClientInteractionType
    timestamp: datetime


@dataclass
class StepEventStatus:
    started_at: datetime | None  # When was this step event handler enabled
    completed_at: datetime | None  # When was this step event handler completed at
    event_status: str | None  # Status update from the event listener for this step (eg - "Waiting 30 seconds")


@dataclass
class RunnerStatus(JSONWizard):
    timestamp_status: datetime  # when was this status generated?
    timestamp_initialise: datetime | None  # When did the test initialise
    timestamp_start: datetime | None  # When did the test start
    status_summary: str
    last_client_interaction: ClientInteraction
    csip_aus_version: str  # The CSIPAus version that is registered in the active test procedure (can be empty)
    log_envoy: str  # Snapshot of the current envoy logs
    criteria: list[CriteriaEntry] = field(default_factory=list)
    precondition_checks: list[PreconditionCheckEntry] = field(default_factory=list)
    instructions: list[str] | None = field(default=None)
    test_procedure_name: str = field(default="-")  # '-' represents no active procedure
    step_status: dict[str, StepEventStatus] | None = field(default=None)
    request_history: list[RequestEntry] = field(default_factory=list)
    timeline: TimelineStatus | None = None  # Streaming timeline data snapshot
    end_device_metadata: EndDeviceMetadata | None = None  # Snapshot of current active end device (if any)


@dataclass
class RequestList(JSONWizard):
    request_ids: list[int]
    count: int


@dataclass
class TestDefinition(JSONWizard):
    test_procedure_id: TestProcedureId
    yaml_definition: str


@dataclass
class TestCertificates(JSONWizard):
    aggregator: str | None
    device: str | None


@dataclass
class RunGroup(JSONWizard):
    run_group_id: str
    name: str
    csip_aus_version: CSIPAusVersion
    test_certificates: TestCertificates


@dataclass
class TestConfig(JSONWizard):
    subscription_domain: str | None
    is_static_url: bool
    pen: int = field(default=0)


@dataclass
class TestUser(JSONWizard):
    user_id: str
    name: str


@dataclass
class RunRequest(JSONWizard):
    run_id: str
    test_definition: TestDefinition
    run_group: RunGroup
    test_config: TestConfig
    test_user: TestUser
