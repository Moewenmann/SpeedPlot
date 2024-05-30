import speedtest
import socket
import datetime
import json

def active_connection():
	try:
		socket.create_connection(("www.google.com", 80), 2)
		return True
	except OSError:
		return False

def run_test():
	st = speedtest.Speedtest()
	st.get_best_server()
	st.download()
	st.upload()
	results = st.results.dict()
	return results

def sys_info():
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	public_ip = socket.gethostbyname(socket.getfqdn())
	return hostname, local_ip, public_ip

def s_to_f(data, filename='data.json'):
	with open(filename, 'a') as file:
		json.dump(data, file, indent=4)

def main():
	if active_connection():
		results = run_test()
		hostname, local_ip, public_ip = sys_info()
		current_time = datetime.datetime.now().isoformat()
		data = {
			"TIME": current_time,
			"ISP": results.get('client').get('isp'),
			"IP": results.get('client').get('ip'),
			"LOCAL_IP": local_ip,
			"HOSTNAME": hostname,
			"UPLOAD_SPEED": round(results.get('upload') / 1_000_000, 4),
			"DOWNLOAD_SPEED": round(results.get('download') / 1_000_000, 4),
			"LATENCY": results.get('ping')
		}
		s_to_f(data)
	else:
		print(f"\033[91mInternet connection failed.\033[0m")

main()
