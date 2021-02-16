"""
# Random
THRESHOLDS = {'adservice': [21.330315144500727, 33.190543114182056, list(range(0,20))],
              'cartservice': [21.600752137490385, 47.91014131225127, list(range(0,20))],
              'checkoutservice': [23.35596774326705, 81.99500812710826, list(range(0,20))],
              'currencyservice': [60.472365710413364, 138.67661534363845, list(range(0,20))],
              'emailservice': [10.178589163039009, 14.440786052831525, list(range(0,20))],
              'frontend': [131.05261387056865, 286.74749073714514, list(range(0,20))],
              'paymentservice': [6.144160311223364, 9.837633295363775, list(range(0,20))],
              'productcatalogservice': [77.17238428718936, 189.69626000490936, list(range(0,20))],
              'recommendationservice': [34.14857304166025, 134.8238319271482, list(range(0,20))],
              'shippingservice': [13.925914493363182, 28.12162994036877, list(range(0,20))]}
"""

#Periodic
"""
THRESHOLDS = {  'adservice': [18.91198647628613, 37.1594772412996, list(range(0, 20))],
                'cartservice': [5.070724560898366, 48.11930195601824, list(range(0, 20))],
                'checkoutservice': [7.963402920950859, 71.03122653351164, list(range(0, 20))],
                'currencyservice': [7.185656891371886, 113.0409457153268, list(range(0, 20))],
                'emailservice': [9.44292069567324, 18.68448489320464, list(range(0, 20))],
                'frontend': [11.737333378845575, 292.61023250737037, list(range(0, 20))],
                'paymentservice': [6.410916116332014, 13.00031692721426, list(range(0, 20))],
                'productcatalogservice': [9.315127028436958, 220.31994956254317, list(range(0, 20))],
                'recommendationservice': [7.064953383281728, 136.63164723739953, list(range(0, 20))],
                'shippingservice': [8.827862519145063, 33.87737287281202, list(range(0, 20))]}
"""


# Increasing
THRESHOLDS = {  'adservice':[13.157102159427831, 21.51729223322332, list(range(0, 20))],
                'cartservice':[3.5346605530313595, 31.36969448760304, list(range(0, 20))],
                'checkoutservice':[5.180312567203745, 44.216863194990395, list(range(0, 20))],
                'currencyservice':[4.865958671964396, 71.55975525864423, list(range(0, 20))],
                'emailservice':[5.891658694385612, 10.158396620318687, list(range(0, 20))],
                'frontend':[5.487733048372887, 179.52792606780957, list(range(0, 20))],
                'paymentservice':[5.0789719644685976, 10.056211449131656, list(range(0, 20))],
                'productcatalogservice':[8.169855981027922, 185.12202197243042, list(range(0, 20))],
                'recommendationservice':[5.5862027558917005, 93.84017331595925, list(range(0, 20))],
                'shippingservice':[7.860780743049197, 26.30510733556273, list(range(0, 20))]}


"""
# Decreasing
THRESHOLDS = {  'adservice': [17.601500388890837, 30.982235946714386, list(range(0,20))],
                'cartservice': [6.959972207015859, 41.198293435245965, list(range(0,20))],
                'checkoutservice': [8.461451256564418, 57.03675377913471, list(range(0,20))],
                'currencyservice': [14.118118925684529, 102.69207838272757, list(range(0,20))],
                'emailservice': [7.499053553055749, 11.923622677050785, list(range(0,20))],
                'frontend': [41.606793441541726, 278.1430990579928, list(range(0,20))],
                'paymentservice': [4.277209892119755, 7.209264766463832, list(range(0,20))],
                'productcatalogservice': [22.6087913610919, 150.85705345288847, list(range(0,20))],
                'recommendationservice': [11.076709058342102, 108.19477549713724, list(range(0,20))],
                'shippingservice': [10.089733885591752, 23.506739915702962, list(range(0,20))]}
"""


"""
# Mix
THRESHOLDS = { 'adservice':[19.53834319784148, 32.98285856141357, list(range(0, 20))],
               'cartservice':[5.190002675599407, 46.974442676490256, list(range(0, 20))],
               'checkoutservice':[8.379738079077159, 78.69781887549976, list(range(0, 20))],
               'currencyservice':[7.506160499222751, 106.7734116566961, list(range(0, 20))],
               'emailservice':[9.58123895696524, 15.691597879991722, list(range(0, 20))],
               'frontend':[7.1716795655656425, 274.714291480314, list(range(0, 20))],
               'paymentservice':[5.549937081665704, 10.119875642537076, list(range(0, 20))],
               'productcatalogservice':[7.856316322286871, 172.47180560098224, list(range(0, 20))],
               'recommendationservice':[8.34545251287876, 140.59876386222928, list(range(0, 20))],
               'shippingservice':[8.981415609692911, 26.38296929477965, list(range(0, 20))]}
"""


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
