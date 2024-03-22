from pymongo import MongoClient
import pandas as pd
import subprocess
import json

client = MongoClient('localhost', 27017)
db = client.nevod
collection = db.events

calculate_theta, calculate_phi = [], []
exp_theta, exp_phi = [], []

for doc in collection.find():

    times_dict = {}

    for direction in doc.get('eas_event_direction', []):
        if direction.get('cluster') == 8:
            stations = direction.get('stations', {})
            if len(stations) == 4:
                exp_theta.append(direction['direction']['theta'])
                exp_phi.append(direction['direction']['phi'])
                for station_name in stations:
                    i = int(station_name.split('_')[1])
                    station_data = stations[station_name]
                    t_std = station_data.get('t_std')
                    if t_std is not None:
                        times_dict[i] = t_std

    if len(times_dict) > 3:
        times_str = json.dumps(times_dict)

        print(times_str)

        output = subprocess.check_output(['python', 'calculate angeles.py', times_str])
        result = json.loads(output.decode())
        calculate_theta.append(result["theta"])
        calculate_phi.append(result["phi"])

client.close()

dat = {
    'calculate_theta': calculate_theta,
    'exp_theta': exp_theta,
    'calculate_phi': calculate_phi,
    'exp_phi': exp_phi
}

df = pd.DataFrame(dat)
print(df)
df.to_csv('angeles_data.csv', index=False)