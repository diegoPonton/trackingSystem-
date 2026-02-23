
import os 
import json


#reading the actual route

route_actual_file = os.path.abspath(__file__)
route_actual_dir = os.path.dirname(route_actual_file)
base_route =  os.path.dirname(os.path.dirname(route_actual_dir))


config_parameter_file = os.path.join(base_route, 'config', 'parameters.json')

with open(config_parameter_file, "r", encoding="utf-8") as f:
    data = json.load(f)


def making_routes():
    tmp_route = os.path.join(base_route, data['routes']['temp_route'])
    tmp_fcalib_route = os.path.join(base_route, data['routes']['temp_fcalib_route'])
    print("### creating the directories ....")
    os.makedirs(tmp_fcalib_route, exist_ok=True)



def get_route_figcal():
    return os.path.join(base_route, data['routes']['temp_fcalib_route'])

def get_num_camera():
    return  data['config_calibration']['num_camera']

def get_route_aruco():
    return os.path.join(base_route, data['routes']['data_static_aruco']) 
