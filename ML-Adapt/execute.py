def scale_kubernetes_put(request_format, microservice):
    """ Perform a certain action on the microservice
        Args:
            request_format (dict): Container Application Manager Request Format;
            microservice (str): Microservice name.
    """
    url = 'https://10.66.66.53:6443/apis/apps/v1/namespaces/default/deployments/' + microservice + '/scale'
    from requests import put
    from json import dumps

    data_json = dumps(request_format, indent=4)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1ySEgtX3ZrRHhnWUM2VU91Y2JYenBwRDBVVEZSamQ4d3JoWDctWllRQWsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFkbWluLXVzZXItdG9rZW4tejRjcTciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4tdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImFlNDBhZTdjLThhMTYtNGI0My05ZmUxLTM1OTJmYjYwNzEyNiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmFkbWluLXVzZXIifQ.FSnOXq88eQfnRrnuNnjfDOmJzDEfBXs0HqNlIDH2-veOmS6jnwNlRffHFObQPE4SZYToH7Szg0-cBq4JkCFu8bPZBsBpKOFzzp---FWKxqwqpNfDI0ll8P9CBX3Sad6y9EGEZgWOljXvcdB7WhNlcACxP2BT3IOtB9lLwLDkXLjRW-bGG2OIZZTMqf5gHd9z4M-hpZdb6Zw8apjWqgCV-Le1ejfEFSFgriuIspTJGOlTYDjYNC0U-GYdR2K9ddtjkDBdkePJXAHuWd2kVy0cAveoteIp_WJgWm8Fb-oRa9CYuxqrhp4FGM_49d4vPVGBmgky0C4OR_cQgQT1xYOzeQ',
        'Accept': 'application/json',
    }

    put(url, headers=headers, data=data_json, verify=False)


def scale_microservice(adaptation_plans):
    """Function to manage actions in Kubernetes.
        This function allows scaling-in/out. In addition, some rules can be selected. 
        For example, the minimum number of pods per standard deployments is 1, while 
        the maximum number is 10. The entry contains a list of actions for each microservice 
        selected in the Monitoring phase.

        Args:
            adaptation_plans (list): List containing actions to be performed on the executor
    """

    for plan in adaptation_plans:
        microservice = plan[0]
        id_scale = plan[1]
        request_format = plan[2]
        request_format['spec']['replicas'] = request_format['spec']['replicas'] + id_scale
        request_format['status']['replicas'] = request_format['spec']['replicas'] + id_scale

        if id_scale <= -1:
            scale_kubernetes_put(request_format, microservice)

        elif id_scale >= 1:
            if request_format['spec']['replicas'] > 20:
                request_format['spec']['replicas'] = 20
                request_format['status']['replicas'] = 20

            scale_kubernetes_put(request_format, microservice)


def execute_adaptation_plan(adaptation_plans):
    """Execute uma ação planejada.
        Args:
            adaptation_plans (list): List containing actions to be performed on the executor
    """
    scale_microservice(adaptation_plans)


class Execute:
    pass
