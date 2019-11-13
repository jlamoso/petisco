import json

import pytest
from meiga import Success, isFailure

from petisco import controller, CorrelationId, ERROR, INFO
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_correlation_id_as_only_input_parameter():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller(correlation_id: CorrelationId):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    correlation_id = json.loads(first_logging_message[1])["correlation_id"]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", correlation_id=correlation_id, message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            correlation_id=correlation_id,
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_without_input_parameters():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller():
        return isFailure

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Unknown Error", "type": "HttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )

    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller", message="Result[status: failure | value: Error]"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_with_correlation_id_as_only_input_parameter():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller(correlation_id: CorrelationId):
        return isFailure

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Unknown Error", "type": "HttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    correlation_id = json.loads(first_logging_message[1])["correlation_id"]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", correlation_id=correlation_id, message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            correlation_id=correlation_id,
            message="Result[status: failure | value: Error]",
        ).to_json(),
    )