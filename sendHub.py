#!/usr/bin/python
# -*- coding: utf8 -*-

# NOTE: jw: what is an 'appropriate IP Address' [sic] in a subnet? assume "x.y.z.1", since
# "/24" is netmask 255.255.255.0, we'll just assume .1 in subnet for the router

# TODO: jw: lookup up router for a given subnet dynamically (load balancing etc)
# TODO: jw: use ip address manipulation library for ip addys instead of string
# TODO: allow for various backend resource strategies


from collections import Iterable

# NOTE: throughput is given in msgs/request
# NOTE: cost is dollars/request
backend_resources = [
    { "category_name": "Small", "relay_ip": "10.0.1.1", "throughput": 1, "cost": 0.01},
    { "category_name": "Medium", "relay_ip": "10.0.2.1", "throughput": 5, "cost": 0.05},
    { "category_name": "Large", "relay_ip": "10.0.3.1", "throughput": 10, "cost": 0.10},
    { "category_name": "Super", "relay_ip": "10.0.4.1", "throughput": 25, "cost": 0.25}, 
    ]


def calculateRoutes(message, recipients, resources=backend_resources, sort_resources=False):
    """Calculate routes using smallest number of requests possible.

    Args:
        message: the message to send.
        recipients: a list of recipients
        resources: a list of dictionaries used to compute optimum routes. (default provided if ommitted)
        sort_resources: resources will be sorted in decsending order of throughput
    Raises:
        TypeError: if recipients is not a list
        ValueError: if recipients is empty
    """
    # TODO: jw: validate parameters and fail-fast
    # TODO: jw: if there is no throughput = 1 we need to ensure that there are
    #           enough throughput options to complete routing request
    # TODO: jw: check for valid and unique recipients
    # TODO: jw: add parameter to request cost


    # check that recipients is a non-empty list
    if not isinstance(recipients, Iterable):
        raise TypeError, "{} is not iterable".format(recipients)

    # sort the resource in reverse order of throughput, since requirement is to
    # utilize the smallest number of requests possible

    if sort_resources:
        resources.sort(key=lambda x: x['throughput'], reverse=True)
    else:
        # if there is more than one resource make sure the throughput of the
        # last is less than that of the second to last otherwise fail-fast
        print "{} {} {}".format(len(resources),resources[-1]['throughput'], resources[2]['throughput'])
        print "sort_resources = {}".format(sort_resources)
        assert len(resources)>1 and resources[-1]['throughput'] < resources[-2]['throughput']

    # initialize result dict with the message
    result = { "message": message, "routes":[] }

    processed = 0
    last_throughput = None
    for category in resources:

        recipients_remaining = len(recipients) - processed
        throughput = category['throughput']

        # confirm that subsequent throughputs reduce 
        assert last_throughput > throughput if last_throughput else True
        last_throughput = throughput

        # // operator emaphasizes integer division
        chunks = recipients_remaining // throughput

        if chunks > 0:
            # create a new route for each chunk: a route contains ip and recipient list
            for x in xrange(chunks):
                route = {}
                route['ip'] = category['relay_ip']
                route['recipients'] = recipients[processed:processed+throughput]
                result['routes'].append(route)
                processed += throughput

            # check if we are done
            if processed == len(recipients):
                break

    assert (processed == len(recipients)), "didn't process len(recipients)!!)"

    return result


if __name__ == "__main__":
    print( calculateRoutes("hi", ["1",], backend_resources) )
    print( calculateRoutes("hi", ["1","2","33","44"], backend_resources) )
    print( calculateRoutes("hi", ["1","2","33","44", "55"], backend_resources) )
    print( calculateRoutes("hi", range(11), backend_resources) )
    print( calculateRoutes("hi", range(30), backend_resources) )
    print( calculateRoutes(3232 ,range(2), backend_resources) )
    print( calculateRoutes("sdaf", 234, backend_resources) )
    print( calculateRoutes("sdaf", 'sdddsccxfddfsdfa', backend_resources) )
