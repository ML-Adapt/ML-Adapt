MICROSERVICES = ['adservice', 'cartservice', 'checkoutservice', 'currencyservice', 'emailservice', 'frontend',
                 'paymentservice', 'productcatalogservice', 'recommendationservice', 'shippingservice']

METRICS = {
    'usage_per_deployment2':
        '(avg(sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate{namespace="default"}*'
        'on(namespace,pod)group_left(workload,workload_type)mixin_pod_workload{namespace="default",workload="",'
        'workload_type="deployment"})by(pod))*1000)',
    'usage_per_deployment':
        '((sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate{namespace="default"}*on(namespace,pod)group_left(workload,workload_type)namespace_workload_pod:kube_pod_owner:relabel{namespace="default", workload_type="deployment", workload=""})/sum(kube_pod_container_resource_requests_cpu_cores{namespace="default"}* on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace="default", workload_type="deployment", workload=""}))*100)'
}

PROMETHEUS_URL = 'http://10.66.66.53:30002/api/v1/query?query='


def usage_of_microservices(range_vector):
    """Method for collecting CPU consumption from all microservices.

        Args:
            range_vector (str): Consultation Interval.

        Returns:
            Dictionary. Each key is the name of the microservice, while its
            value is a list or float. This list/float contains data of the
            CPU consumption of the microservice.

            The return decision between list or float varies according to the
            consultation interval. If the range is not sent, the value becomes
            a single float, for example:

            {'shippingservice': 7.61828548262844,
            'productcatalogservice': 11.54966891949777,
            'adservice': 33.58434362754921}

            If the range is sent, the value becomes a list, for example:

            {'shippingservice': [7.61828548262844, 7.56664421203091],
            'productcatalogservice': [11.54966891949777, 11.17846043335954],
            'adservice': [33.58434362754921, 33.91381984647154]}

            and so on...
    """

    consumption_of_microservices = {}

    for microservice in MICROSERVICES:
        consumption_of_microservices[microservice] = [usage_per_microservice(microservice, range_vector),
                                                      collect_number_of_microservice_replicas(microservice)]

    return consumption_of_microservices


def usage_per_microservice(microservice, range_vector):
    """Request the Prometheus API.

    This method builds a request for the Prometheus API.
    The CPU consumption of a given microservice is collected.

        Args:
            microservice (str): Name of microservice.
            range_vector (str): Consultation Interval.

        Returns:
            If the range sent is empty, then the instantaneous value
            of the requested metric (float) is returned. If the range
            is not empty, then a historical list of the metric based
            on the range is returned list (float).

            If range_vector == null:
                7.61828548262844
            Else:
                [7.61828548262844, 7.56664421203091]

    """
    url_request_prometheus_api = PROMETHEUS_URL + METRICS['usage_per_deployment'][
                                                  0:255] + microservice + METRICS['usage_per_deployment'][
                                                                          255:491] + microservice + METRICS['usage_per_deployment'][
                                                                          491:] + range_vector
    return request_prometheus_api(url_request_prometheus_api, range_vector)


def request_prometheus_api(url_request_prometheus_api, range_vector):
    """Request the Prometheus API.

        Args:
            url_request_prometheus_api (str): Query URL in API format.
            range_vector (str): Consultation Interval.

        Returns:
            If the range sent is empty, then the instantaneous value
            of the requested metric (float) is returned. If the range
            is not empty, then a historical list of the metric based
            on the range is returned list (float).

            If range_vector == null:
                 7.61828548262844
            Else:
                 [7.61828548262844, 7.56664421203091]
    """

    from json import loads
    from requests import get

    get_api_prometheus = loads(get(url_request_prometheus_api).text)

    if range_vector:
        collected_values = get_api_prometheus['data']['result'][0]['values']
        microservice_usage_list = []
        for value in collected_values:
            microservice_usage_list.append(float(value[1]))

        return microservice_usage_list
    else:
        collected_value = float(get_api_prometheus['data']['result'][0]['value'][1])
        return collected_value


def collect_number_of_microservice_replicas(microservice):
    """Request the Kubernetes API.
        Args:
            microservice (str): Microservice name.

        Returns:
            request_format: The request format refers to a
            JSON collected from the Kubernetes API that
            contains information related to the microservice.
    """
    url = 'https://10.66.66.53:6443/apis/apps/v1/namespaces/default/deployments/' + microservice + '/scale'
    from requests import get
    import urllib3
    from json import JSONDecoder
    from collections import OrderedDict
    urllib3.disable_warnings()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1ySEgtX3ZrRHhnWUM2VU91Y2JYenBwRDBVVEZSamQ4d3JoWDctWllRQWsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFkbWluLXVzZXItdG9rZW4tejRjcTciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4tdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImFlNDBhZTdjLThhMTYtNGI0My05ZmUxLTM1OTJmYjYwNzEyNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmFkbWluLXVzZXIifQ.FSnOXq88eQfnRrnuNnjfDOmJzDEfBXs0HqNlIDH2-veOmS6jnwNlRffHFObQPE4SZYToH7Szg0-cBq4JkCFu8bPZBsBpKOFzzp---FWKxqwqpNfDI0ll8P9CBX3Sad6y9EGEZgWOljXvcdB7WhNlcACxP2BT3IOtB9lLwLDkXLjRW-bGG2OIZZTMqf5gHd9z4M-hpZdb6Zw8apjWqgCV-Le1ejfEFSFgriuIspTJGOlTYDjYNC0U-GYdR2K9ddtjkDBdkePJXAHuWd2kVy0cAveoteIp_WJgWm8Fb-oRa9CYuxqrhp4FGM_49d4vPVGBmgky0C4OR_cQgQT1xYOzeQ',
        'Accept': 'application/json',
    }

    response = get(url, headers=headers, verify=False)
    custom_decoder = JSONDecoder(object_pairs_hook=OrderedDict)
    request_format = custom_decoder.decode(response.text)

    return request_format


class Monitor:
    pass
