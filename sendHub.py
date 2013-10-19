#!/usr/bin/env python
# -*- coding: utf8 -*-

# NOTE: jw: what is an 'appropriate IP Address' [sic] in a subnet? assume "x.y.z.1", since
# "/24" is netmask 255.255.255.0, we'll just assume .1 in subnet for the router

# TODO: jw: lookup up router for a given subnet dynamically (load balancing etc)
# TODO: jw: use ip address manipulation library for ip addys instead of string
# TODO: allow for various backend resource strategies

# NOTE: throughput is given in msgs/request
# NOTE: cost is dollars/request
backend_resources = [
    { "category_name": "Small", "relay_ip": "10.0.1.1", "throughput": 1, "cost": 0.01},
    { "category_name": "Medium", "relay_ip": "10.0.2.1", "throughput": 5, "cost": 0.05},
    { "category_name": "Large", "relay_ip": "10.0.3.1", "throughput": 10, "cost": 0.10},
    { "category_name": "Super", "relay_ip": "10.0.4.1", "throughput": 25, "cost": 0.25}, 
    ]


def router(message, recipients, resources):
    # TODO: jw: validate parameters and fail-fast
    # TODO: jw: if there is no throughput = 1 we need to ensure that there are
    #           enough throughput options to complete routing request
    # TODO: jw: check for valid and unique recipients
    # TODO: jw: add parameter to request cost

    # sort the resource in reverse order of throughput, since requirement is to
    # utilize the smallest number of requests possible

    # TODO: jw: sorting everytime could be redundant and unecessary if the list is presorted
    resources.sort(key=lambda x: x['throughput'], reverse=True)
    #print resources

    # initialize result dict with the message
    result = { "message": message, "routes":[] }

    recipients_processed = 0
    for category in resources:
        # integer division returns floor so x//y*y gives number of messages this
        # category can process. using // operator to emaphasize integer division
        recipients_remaining = len(recipients) - recipients_processed
        #print recipients_remaining
        eat = recipients_remaining // category['throughput'] * category['throughput']
        print eat

        if eat > 0:
            # create a new route: contains ip and recipient list
            route = {}
            route['ip'] = category['relay_ip']
            route['recipients'] = recipients[recipients_processed:recipients_processed+eat]
            result['routes'].append(route)
            recipients_processed += eat

            #print result

            # check if we are done
            if recipients_processed == len(recipients):
                break

    #print "recipients processed {}".format(recipients_processed)
    assert (recipients_processed == len(recipients)), "didn't process len(recipients)!!)"

    return result


if __name__ == "__main__":
    print( router("hi", ["1",], backend_resources) )
    print( router("hi", ["1","2","33","44"], backend_resources) )
    print( router("hi", ["1","2","33","44", "55"], backend_resources) )
    print( router("hi", range(11), backend_resources) )
    print( router("hi", range(30), backend_resources) )
