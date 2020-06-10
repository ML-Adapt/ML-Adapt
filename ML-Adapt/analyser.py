def analysing_proactive_per_microservice(microservices_information):
    """Predict the CPU of a microservice

        Args:
            microservices_information (dict): Information about the microservice as
            name and history of CPU consumption

        Returns:
            Microservices_information. This list contains the name of the microservice,
            the proportion and the number of replicas of microservice.
            The proportion informs the current situation of the microservice so that
            the planning takes the necessary actions. However, this action in this method
            is based on a value predicted by a Machine Learning model.

            For example: 'shippingservice' = [0.78, 1]
    """
    for microservice_name, microservice_values in microservices_information.items():
        microservices_information[microservice_name] = [resource_prediction(microservice_name, microservice_values[0]),
                                                        microservice_values[1]]
    return calculation_microservice_proportion(microservices_information)


def resource_prediction(microservice_name, microservice_consumption):
    """Predict the resource of a microservice

        Args:
            microservice_name (str): Microservice name.
            microservice_consumption (list): Microservice CPU usage history.

        Returns:
            The forecast for microservice CPU consumption in the near future.
    """
    from knowledge import load_model, normalize, denormalize

    model = load_model('models/' + microservice_name + '_mlp')
    normalize_value = normalize(microservice_name, microservice_consumption)

    # If the model is MLP, RF or SVR.
    value_predict = model.predict(normalize_value)

    # If the model is XGBoost
    # import xgboost
    # normalize_value = xgboost.DMatrix(normalize_value)
    # value_predict = model.predict(normalize_value, ntree_limit=model.best_ntree_limit)

    return denormalize(microservice_name, value_predict)


def calculation_microservice_proportion(microservices_information):
    """Seleciona a situação dos deployments com base no sue limiares.

        Args:
            microservices_information (dict): Information about the microservice as
            name and history of CPU consumption

        Returns:
            Microservices_information. This list contains the name of the microservice,
            the proportion and the number of replicas of microservice.
            The proportion informs the current situation of the microservice so that
            the planning takes the necessary actions. However, this action in this method
            is based on a value predicted by a Machine Learning model.

            For example: 'shippingservice' = [0.78, 1]
    """
    desired_value = 80

    for name_microservice, values_of_microservice in microservices_information.items():
        forecast_value = values_of_microservice[0]
        request_format = values_of_microservice[1]
        ratio = (forecast_value / desired_value)
        microservices_information[name_microservice] = [ratio, request_format]

    return microservices_information


class Analyzer:
    pass
