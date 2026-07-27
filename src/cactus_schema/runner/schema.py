from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, StrEnum, auto
from http import HTTPMethod, HTTPStatus

from dataclass_wizard import JSONWizard


class ClientInteractionType(StrEnum):
    RUNNER_START = "Runner Started"
    TEST_PROCEDURE_INIT = "Test Procedure Initialised"
    TEST_PROCEDURE_START = "Test Procedure Started"
    PROXIED_REQUEST = "Request Proxied"
    TEST_PROCEDURE_FINALIZED = "TEST_PROCEDURE_FINALIZED"


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
class WarningEntry(JSONWizard):
    type: str  # stable identifier, e.g. "set-max-w-varied", "over-polling"
    description: str  # short human line for lists/badges
    message: str  # full detail: values seen, timestamps, why it matters / production impact
    timestamp: datetime  # when first emitted (tz-aware UTC)


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
    upper_max_w: int | None = None  # Effective device max for export/discharge (watts)
    upper_max_label: str | None = None  # Field that upper_max_w was sourced from, e.g. "setMaxDischargeRateW"
    lower_max_w: int | None = None  # Effective device max for import/charge (watts)
    lower_max_label: str | None = None  # Field that lower_max_w was sourced from, e.g. "setMaxChargeRateW"


@dataclass
class DERCapabilityInfo(JSONWizard):
    """Snapshot of DERCapability for UI display"""

    der_type: str | None = None  # e.g. "PHOTOVOLTAIC_SYSTEM", "COMBINED_PV_AND_STORAGE"
    modes_supported: list[str] | None = None  # Active DERControlType flag names
    max_w: int | None = None
    max_va: int | None = None
    max_var: int | None = None
    max_var_neg: int | None = None
    max_a: int | None = None
    max_charge_rate_w: int | None = None
    max_discharge_rate_w: int | None = None
    max_wh: int | None = None
    doe_modes_supported: list[str] | None = None  # Active DOESupportedMode flag names


@dataclass
class DERSettingsInfo(JSONWizard):
    """Snapshot of DERSettings for UI display"""

    modes_enabled: list[str] | None = None  # Active DERControlType flag names
    max_w: int | None = None
    max_va: int | None = None
    max_var: int | None = None
    max_var_neg: int | None = None
    max_charge_rate_w: int | None = None
    max_discharge_rate_w: int | None = None
    grad_w: int | None = None  # Ramp rate (%setMaxW/second)
    doe_modes_enabled: list[str] | None = None  # Active DOESupportedMode flag names


@dataclass
class DERStatusInfo(JSONWizard):
    """Snapshot of current DER real-time status (from SiteDERStatus / sep2 DERStatus).
    Bitmaps/enums resolved to strings."""

    alarm_status: list[str] | None = None  # Active AlarmStatusType flag names
    inverter_status: str | None = None  # InverterStatusType enum name
    operational_mode_status: str | None = None  # OperationalModeStatusType enum name
    generator_connect_status: list[str] | None = None  # Active ConnectStatusType flag names
    storage_connect_status: list[str] | None = None  # Active ConnectStatusType flag names
    storage_mode_status: str | None = None  # StorageModeStatusType enum name
    state_of_charge_status: int | None = None  # Percent
    local_control_mode_status: str | None = None  # LocalControlModeStatusType enum name
    manufacturer_status: str | None = None  # Up to 6 chars


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
    der_capability: DERCapabilityInfo | None = None
    der_settings: DERSettingsInfo | None = None
    der_status: DERStatusInfo | None = None


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
    event_status: str | None = None  # Status update from the event listener for this step (eg - "Waiting 30 seconds")


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
    warnings: list[WarningEntry] = field(default_factory=list)
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
    test_procedure_id: str
    yaml_definition: str


@dataclass
class TestCertificates(JSONWizard):
    aggregator: str | None
    device: str | None


@dataclass
class RunGroup(JSONWizard):
    run_group_id: str
    name: str
    csip_aus_version: str
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
