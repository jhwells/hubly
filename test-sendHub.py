from sendHub import calculateRoutes

from nose.tools import raises

@raises(TypeError)
def test_recipients_raises_type_error():
    result = calculateRoutes("message", 333)


def test_one_recipient():
    message = "message"
    result = calculateRoutes(message, ['+15551111111'])
    print result
    assert result['message'] == message
    assert len(result['routes']) == 1
    assert len(result['routes'][0]['recipients']) == 1

def test_six_recipients():
    message = "message"
    result = calculateRoutes(message, range(6))
    print result
    assert len(result['routes']) == 2

default_route_results = [
    (1,1), (5,1), (6,2), (10,1), (11,2), (12,3), (15,2), (16,3),
    (25,1), (26,2), (30,2), (31,3), (35,2), (40,3), (41,4),
    ]

def test_default_router_basic():
    for recipients, routes in default_route_results:
        yield expect_routes, recipients, routes

def expect_routes(recipients, routes):
    message = "message"
    result = calculateRoutes(message, range(recipients))
    print result
    assert result['message'] == message
    assert len(result['routes']) == routes
