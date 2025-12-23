from assertical.fake.generator import generate_class_instance


def test_notification():
    """Any issues with importing the notification models?"""
    import cactus_schema.notification as notification

    assert notification.uri.URI_ENDPOINT
    assert generate_class_instance(notification.CollectedHeader)


def test_orchestrator():
    """Any issues with importing the notification models?"""
    import cactus_schema.orchestrator as orchestrator

    assert orchestrator.uri.AdminRun
    assert generate_class_instance(orchestrator.InitRunRequest)


def test_runner():
    """Any issues with importing the runner models?"""
    import cactus_schema.runner as runner

    assert runner.uri.Initialise
    assert generate_class_instance(runner.DataStreamPoint)
