import speedtest
import socket
import datetime
import json

def get_speedtest_results():
	st = speedtest.Speedtest()
	st.get_best_server()
	st.download()
	st.upload()
	results = st.results.dict()
	return results

def get_system_info():
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	public_ip = socket.gethostbyname(socket.getfqdn())
	return hostname, local_ip, public_ip

def save_results_to_file(data, filename='speedtest_results.json'):
	with open(filename, 'a') as file:
		json.dump(data, file, indent=4)

def main():
	results = get_speedtest_results()
	hostname, local_ip, public_ip = get_system_info()
	current_time = datetime.datetime.now().isoformat()
	
	data = {
		"ISP": results.get('client').get('isp'),
		"IP": results.get('client').get('ip'),
		"LOCAL_IP": local_ip,
		"HOSTNAME": hostname,
		"TIME": current_time,
		"UPLOAD_SPEED": results.get('upload') / 1_000_000,
		"DOWNLOAD_SPEED": results.get('download') / 1_000_000,
		"LATENCY": results.get('ping')
	}
	
	save_results_to_file(data)

main()
