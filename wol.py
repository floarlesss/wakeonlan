from wakeonlan import send_magic_packet
from datetime import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

print("welcome to the wakeonlan script")
print("running...\n")


# Fetch the service account key JSON file contents
cred = credentials.Certificate('path/to/database/json/file.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://firebase_url.com'
})
# As an admin, the app has access to read and write all data, regradless of Security Rules


def check_db_status():
    pc_wake_cmd = db.reference('wakeonlan/pc_wakeup')
    pc_wake_cmd = str(pc_wake_cmd.get())

    if pc_wake_cmd == "0":
        pass
    if pc_wake_cmd == "1":
        pc_status_folder = db.reference('wakeonlan')
        pc_status_folder.update({
            'pc_wakeup': "0"
        })

        send_magic_packet('mac-address-in-format-00-00-00')

        #get time
        now = datetime.now()
        current_time = str(now.strftime("%I:%M"))

        print("magic packet sent successfully at "+ current_time +"")

        pc_status_folder = db.reference('wakeonlan')
        pc_status_folder.update({
            'pc_awake': '1'
        })

    time.sleep(1)
    check_db_status()



check_db_status()
