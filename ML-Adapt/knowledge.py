THRESHOLDS = {'adservice': [39.1615157257852, 67.9075138735587, list(range(0, 3)) + list(range(8, 20))],
              'cartservice': [12.936050230404, 138.02346614235, list(range(0, 2)) + list(range(8, 20))],
              'checkoutservice': [8.14417272336871, 83.6900237349347,
                                  list(range(0, 2)) + list(range(4, 8)) + list(range(15, 20))],
              'currencyservice': [11.790119682381999, 103.779011379582,
                                  list(range(0, 1)) + list(range(5, 14)) + list(range(15, 20))],
              'emailservice': [11.346050300136302, 18.8393812000376, list(range(0, 3)) + list(range(13, 20))],
              'frontend': [14.899815811642098, 95.8938188421319,
                           list(range(0, 2)) + list(range(3, 9)) + list(range(12, 15)) + list(range(16, 20))],
              'paymentservice': [5.241473804395235, 9.973718434645614, list(range(0, 1)) + list(range(10, 20))],
              'productcatalogservice': [8.231885828363584, 109.2058831922828, list(range(2, 10)) + list(range(14, 20))],
              'recommendationservice': [11.458991609862617, 124.20570637501785,
                                        list(range(4, 9)) + list(range(13, 20))],
              'redis-cart': [2.680692593950254, 10.164167471745056, list(range(0, 4)) + list(range(5, 20))],
              'shippingservice': [7.060557553995557, 26.827381770905443, list(range(0, 2)) + list(range(9, 20))]}


def load_model(path_model):
    """  Carregar um modelo de Machine Learning

        Args:
            path_model (str): Informa o nome e caminho do modelo.

        Returns:
            1 Modelo.
    """
    from joblib import load
    path_model = path_model + '.joblib'
    path_model = load(path_model)

    return path_model


def normalize(name_deployment, values_deployment):
    """  Normalizar uma série de valores.

        Args:
            name_deployment (str): Nome do Deployment
            values_deployment (list): Série de valores

        Returns:
            Série normalizada
    """

    from numpy import asarray
    minimum = asarray([THRESHOLDS[name_deployment][0]])
    maximum = asarray([THRESHOLDS[name_deployment][1]])
    serie = asarray([values_deployment])[:, THRESHOLDS[name_deployment][2]]
    serie_normalize = (serie - minimum) / (maximum - minimum)
    return serie_normalize


def denormalize(name_deployment, values_deployment):
    """  Desnormalizar uma série de valores.

        Args:
            name_deployment (str): Nome do Deployment
            values_deployment (list): Valor normalizado

        Returns:
            Valor (float) não normalizado.
    """
    from numpy import asarray
    minimum = asarray(THRESHOLDS[name_deployment][0])
    maximum = asarray([THRESHOLDS[name_deployment][1]])
    serie = (values_deployment * (maximum - minimum)) + minimum

    return float(serie)

def get_data_time():
    """Função para obter o horário atual
        Essa função é utilizada para obtenção de resultados da proposta.

        Returns:
            A hora e o dia atual.
    """
    from datetime import datetime
    data_e_hora_atuais = datetime.now()
    data_and_time = data_e_hora_atuais.strftime('%Y-%m-%d %H:%M:%S ')
    return data_and_time


