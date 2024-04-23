from db_mongo import get_database_connection
import pandas as pd
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor



def process_document(document):
    cluster_method_theta = []
    cluster_method_phi = []
    db_theta = []
    db_phi = []
    cluster_list = []

    eas_event_id = document['_id']
    data_list = document['data_list']

    for data in data_list:
        cluster = data['cluster']
        stations = data['stations']
        direction = data['direction']

        cluster_dict = {}
        for station_name, station_data in stations.items():
            time = station_data.get('t_std', None)
            if time is not None:
                cluster_dict[station_name] = time

        if len(cluster_dict) - 2 > 0 and cluster == 9:
            arg1 = str(cluster)
            arg2 = json.dumps(cluster_dict)
            output = subprocess.run(["python", "cluster_method.py", arg1, arg2], capture_output=True)
            result = json.loads(output.stdout.decode()) if output.stdout else {"theta": None, "phi": None}
            cluster_method_theta.append(result["theta"])
            cluster_method_phi.append(result["phi"])

            db_theta.append(direction['theta'])
            db_phi.append(direction['phi'])
            cluster_list.append(cluster)

    dat = {
        'cluster': cluster_list,
        'cluster_method_theta': cluster_method_theta,
        'db_theta': db_theta,
        'cluster_method_phi': cluster_method_phi,
        'db_phi': db_phi
    }

    df = pd.DataFrame(dat)
    with open('reconstruction(cluster = 9).csv', 'a') as f:
        df.to_csv(f, index=False, header=False)

# Получение объекта базы данных
db = get_database_connection('nevod')
collection = db['eas_events_direction']


# Обход всех документов в коллекции
with ThreadPoolExecutor() as executor:
    for result in executor.map(process_document, collection.find()):
        pass  # Необходимо только для выполнения всех вызовов process_document
