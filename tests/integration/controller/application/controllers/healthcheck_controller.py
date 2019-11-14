from meiga import Result, isSuccess

from petisco import controller


def success_handler(result: Result):
    return {"status": "OK", "value": result.value}, 200


@controller(success_handler=success_handler)
def get_healthcheck():  # noqa: E501
    return isSuccess
