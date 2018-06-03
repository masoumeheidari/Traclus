
import postgresql
import json
import time

db = postgresql.open('pq://postgres:angel9014@localhost:5432/mytestdb')

query = db.prepare("select * from public.points;")

rows = []

for line in query:
	rows.append(str(line))

data = []

json_data = {}
json_data['epsilon'] = 0.00016
json_data['min_neighbors'] = 2
json_data['min_num_trajectories_in_cluster'] = 3
json_data['min_vertical_lines'] = 2
json_data['min_prev_dist'] = 0.0002
json_data['trajectories'] = []
x_data = {}
y_data = []

d = rows[0].strip().split(', ')
date_str = d[3]+d[4]+d[5]+d[6]+d[7]+d[8]

i = int()
i = 0

for row in rows:
	data = row.strip().split(', ')
	time_zone = data[3]+data[4]+data[5]+data[6]+data[7]+data[8]
	if time_zone != date_str:
		json_data['trajectories'].append(y_data)
		del y_data[:]
		date_str = time_zone
	x_data['x'] = float(data[10])
	x_data['y'] = float(data[11])
	y_data.append(x_data.copy())

json_data['trajectories'].append(y_data)

t0 = time.time()
with open('data.txt', 'w') as outfile:
	json.dump(json_data, outfile, indent=4)
d = time.time() - t0
print("duration: %.2f s" % d)
