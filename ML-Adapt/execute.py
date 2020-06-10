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
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ikh6X3dLYVhCSHN0aHBEU0tpWUVnTGc1ZWExdnlfbUpfeGhfMGEwQ19taD'
                         'AifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9u'
                         'YW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZ'
                         'G1pbi11c2VyLXRva2VuLWpiYjlzIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubm'
                         'FtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJ'
                         'jNGJjYTAwYS1jMmIxLTQ4YTMtODM0Mi1jYWQ5Y2RlMjczYWUiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3Vi'
                         'ZS1zeXN0ZW06YWRtaW4tdXNlciJ9.U46SgrzKg4ad7bexbRVm4H7D6IB0H4mLLVXt7FNwQIkrSpj43djTfc3LovabMwKL'
                         'j-atTDSk_gNwPRRc8F-lZkSc6zLsqjI3t7c_e6qBU9ElXuZB2rlz-nJRNPYwastOz7Teqb0lxWJ_pB9PcwkmD1wMjiy71'
                         'QNIejHWwVRBmqlryE-wSVGLM5xHDkKx6iHhRijS4VZlW8dnCgGa1AX-Hi9LRsjZ86vbXs71LRweaqo-QVp5Pg9WvogIt7'
                         '1bf9FcH2o7OJltphMt7w6N64Zi3E97-DhhhF9bByBx7cvvZcHfjCrM0fdWghO54v3byBYUY7MaLnx5A-dGbcmqTJlBOg',
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
            if request_format['spec']['replicas'] > 10:
                request_format['spec']['replicas'] = 10
                request_format['status']['replicas'] = 10

            scale_kubernetes_put(request_format, microservice)


def execute_adaptation_plan(adaptation_plans):
    """Execute uma ação planejada.
        Args:
            adaptation_plans (list): List containing actions to be performed on the executor
    """
    scale_microservice(adaptation_plans)


class Execute:
    pass
