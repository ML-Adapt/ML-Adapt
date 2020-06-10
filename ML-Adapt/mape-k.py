from time import sleep
from monitor import usage_of_microservices
from analyser import analysing_proactive_per_microservice
from planner import plan_adaptive_actions
from execute import execute_adaptation_plan


while True:
    microservices_information = usage_of_microservices('[20m:1m]')
    analysis_report = analysing_proactive_per_microservice(microservices_information)
    adaptation_plans = plan_adaptive_actions(analysis_report)
    execute_adaptation_plan(adaptation_plans)
    sleep(15)
