import inspect
from itertools import chain, product

import pytest
from assertical.fake.generator import generate_class_instance, register_value_generator
from assertical.fixtures.generator import generator_registry_snapshot
from dataclass_wizard import JSONWizard

import cactus_schema.notification as notification
import cactus_schema.orchestrator as orchestrator
import cactus_schema.runner as runner

ALL_MODELS = [
    t
    for (name, t) in chain(
        inspect.getmembers(runner, inspect.isclass),
        inspect.getmembers(notification, inspect.isclass),
        inspect.getmembers(orchestrator, inspect.isclass),
    )
    if issubclass(t, JSONWizard)
]


@pytest.fixture()
def assertical_overrides():
    with generator_registry_snapshot():
        register_value_generator(dict, lambda x: {})
        yield


@pytest.mark.parametrize("t,optional_is_none", product(ALL_MODELS, [True, False]))
def test_json_roundtrip(assertical_overrides, t: type[JSONWizard], optional_is_none: bool):
    """sanity check to ensure that all JSON models can roundtrip successfully via JSON"""
    for seed in [101, 202]:
        initial = generate_class_instance(t, seed=seed, optional_is_none=optional_is_none, generate_relationships=True)
        json = initial.to_json()
        result = t.from_json(json)
        assert initial == result
