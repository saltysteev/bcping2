import datetime
import os
import threading
from time import sleep

from flask import Flask, redirect, render_template, request, url_for

from ping import check_servers, load_hosts, save_hosts

app = Flask(__name__)
HOSTS_FILE = os.path.join(os.path.dirname(__file__), "hosts.json")
CHECK_INTERVAL = 5


def ping_loop():
    while True:
        check_servers(CHECK_INTERVAL)
        sleep(CHECK_INTERVAL)


@app.route("/")
def index():
    results = load_hosts()
    for host in results:
        host.update({"timestamp": str(datetime.timedelta(seconds=host["duration"]))})
    return render_template("index.html", results=results)


@app.route("/manage", methods=["GET", "POST"])
def manage():
    hosts = load_hosts()

    if request.method == "POST":
        form_properties = ["name", "ip", "address", "phone"]
        action = request.form.get("action")

        if action == "add":
            hosts.append(
                {
                    "name": request.form["name"],
                    "ip": request.form["ip"],
                    "address": request.form["address"],
                    "phone": request.form["phone"],
                    "duration": 0,
                    "alive": False,
                    "attempt": 2,
                }
            )

        elif action == "delete":
            ip_to_delete = request.form["ip"]
            hosts = [h for h in hosts if h["ip"] != ip_to_delete]

        elif action == "update":
            original_ip = request.form["original_ip"]
            for host in hosts:
                if host["ip"] == original_ip:
                    for prop in form_properties:
                        host[prop] = request.form[prop]
                    break

        save_hosts(hosts)
        return redirect(url_for("manage"))

    return render_template("manage.html", hosts=hosts)


if __name__ == "__main__":
    # Ping thread
    periodic_thread = threading.Thread(target=ping_loop)
    periodic_thread.daemon = True
    periodic_thread.start()

    # Flask thread
    app.run(debug=True)
