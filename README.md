# ML-Adapt
 
ML-adapt is an adaptive solution that predicts the future CPU consumption of microservices and, based on this information, plans a set of corrective actions (e.g., scaling-in/out). In ML-Adapt, resource prediction is performed using Machine Learning Models trained at design time by algorithms, such as Multilayer perceptron, Random Forest, Support Vector Regression and XGBoost. It is a generic solution that allows the addition of any component in its architecture.

# Installing

You can install ML-Adapt using::

    $ pip3 install -r requirements.txt
    $ Configure the various variables such as: 
      1. Monitor: Microservices, Prometheus API URL, Kubernetes API URL, Kubernetes authorisation;
      2. Analyser: Desired value in the proportion calculation, Machine Learning algorithm to be used;
      3. Planner: Time of Successive Adaptations Containment and Quarantine;
      4. Executor: Kubernetes API URL, Kubernetes authorisation;
      5. Knowledge: Thresholds of algorithms; 
    $ python3 mape-k.py
    
# Dependencies

* This project uses version 3 of Python.
* This project needs Machine Learning Models trained at design time.
