import json
import matplotlib.pyplot as plt
from datetime import datetime

def read_json(filename):
	with open(filename, 'r') as file:
		data = json.load(file)
	return data

def plot_stats(data):
	download_speeds = [entry['DOWNLOAD_SPEED'] for entry in data]
	upload_speeds = [entry['UPLOAD_SPEED'] for entry in data]
	latencies = [entry['LATENCY'] for entry in data]

	download_min = min(download_speeds)
	download_max = max(download_speeds)
	download_avg = sum(download_speeds) / len(download_speeds)

	upload_min = min(upload_speeds)
	upload_max = max(upload_speeds)
	upload_avg = sum(upload_speeds) / len(upload_speeds)

	latency_min = min(latencies)
	latency_max = max(latencies)
	latency_avg = sum(latencies) / len(latencies)

	return {
		'download_min': download_min,
		'download_max': download_max,
		'download_avg': download_avg,
		'upload_min': upload_min,
		'upload_max': upload_max,
		'upload_avg': upload_avg,
		'latency_min': latency_min,
		'latency_max': latency_max,
		'latency_avg': latency_avg
	}

def create_plot(data, stats, hostname, start_time, end_time):
	timestamps = [datetime.fromisoformat(entry['TIME']) for entry in data]
	download_speeds = [entry['DOWNLOAD_SPEED'] for entry in data]
	upload_speeds = [entry['UPLOAD_SPEED'] for entry in data]
	latencies = [entry['LATENCY'] for entry in data]

	plt.figure(figsize=(10, 6))

	plt.plot(timestamps, download_speeds, label='Download in Mbps', marker='o', markersize=3)
	plt.plot(timestamps, upload_speeds, label='Upload in Mbps', marker='o', markersize=3)
	plt.plot(timestamps, latencies, label='Latency in ms', marker='o', markersize=3)

	plt.title(f'Server: {hostname} - {start_time} to {end_time}')
	plt.xlabel('Time')
	plt.ylabel('Speed / Latency')
	plt.legend()
	plt.subplots_adjust(bottom=0.2)
	stats_text = (f"Download: Avg={stats['download_avg']:.2f} Mbps, "
				  f"Min={stats['download_min']:.2f} Mbps, Max={stats['download_max']:.2f} Mbps\n"
				  f"Upload: Avg={stats['upload_avg']:.2f} Mbps, "
				  f"Min={stats['upload_min']:.2f} Mbps, Max={stats['upload_max']:.2f} Mbps\n"
				  f"Latency: Avg={stats['latency_avg']:.2f} ms, "
				  f"Min={stats['latency_min']:.2f} ms, Max={stats['latency_max']:.2f} ms")
	plt.gcf().text(0.02, 0.02, stats_text, fontsize=10)

	plt.savefig('plot.png')
	plt.show()

def main():
	filename = 'data.json'
	data = read_json(filename)
	
	start_time = data[0]['TIME']
	end_time = data[-1]['TIME']
	hostname = data[0]['HOSTNAME']
	
	stats = plot_stats(data)
	
	create_plot(data, stats, hostname, start_time, end_time)

if __name__ == "__main__":
	main()
