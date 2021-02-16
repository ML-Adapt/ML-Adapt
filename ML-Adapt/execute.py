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
        'Authorization': 'Bearer ',
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
