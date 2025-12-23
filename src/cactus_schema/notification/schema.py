from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import JSONWizard


@dataclass(frozen=True)
class CreateEndpointResponse(JSONWizard):
    """Used in response to a CreateEndpointRequest"""

    endpoint_id: str  # Unique ID for identifying and managing the endpoint
    fully_qualified_endpoint: str  # A fully qualified https:// endpoint that can be used for subscription webhook


@dataclass(frozen=True)
class CollectedHeader(JSONWizard):
    """Simple representation of a HTTP header"""

    name: str
    value: str


@dataclass(frozen=True)
class CollectedNotification(JSONWizard):
    """Simple representation of a HTTP notification submitted by the utility server to a notification endpoint"""

    method: str  # What HTTP method was used
    headers: list[CollectedHeader]  # The submitted HTTP headers
    body: str  # String encoded HTTP request body
    received_at: datetime  # tz aware datetime
    remote: str | None  # Who sent this request (typically an IP address)


@dataclass(frozen=True)
class CollectEndpointResponse(JSONWizard):
    """Used to respond to a CollectEndpointRequest"""

    notifications: list[CollectedNotification]


@dataclass(frozen=True)
class ConfigureEndpointRequest(JSONWizard):
    """Used for adjusting the configuration of an existing endpoint"""

    enabled: (
        bool  # if False - submitted requests to the endpoint will be served with a HTTP 500 and ignored. Defaults True
    )
