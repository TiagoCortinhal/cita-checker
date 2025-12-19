import time
import random
from time import sleep

from seleniumbase import SB
from selenium.webdriver.common.by import By
import json
import smtplib
from email.message import EmailMessage
import os
import logging
import subprocess

# Utility function to find and kill all Brave browser processes
def find_and_kill():
    try:
        pids = subprocess.check_output("pgrep brave", shell=True).decode().strip().split()
        for pid in pids:
            subprocess.call(f"kill {pid}", shell=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("No Brave process is currently running.")

# Load configuration from values.json
with open('values.json') as config_file:
    config = json.load(config_file)

# Set keyboard layout
try:
    subprocess.run(["setxkbmap", "-layout", config['keyboard_layout']], check=True)
    print(f"Keyboard layout set to {config['keyboard_layout']}.")
except subprocess.CalledProcessError as e:
    print(f"Error setting keyboard layout: {e}")

# Send an email alert when an appointment is available
def send_email(subject, message, attach_screenshot=False):
    sender_email = config['sender_email']
    receiver_email = config['receiver_email']
    password = config['password']
    smtp_server = config['smtp_server']
    smtp_port = config['smtp_port']

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(message)

    # Attach screenshot if needed
    if attach_screenshot:
        screenshot_path = "/tmp/cita_disponible.png"
        if os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(screenshot_path)
                msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender_email, password)
            smtp.send_message(msg)
            logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Set a random window size for SB to avoid detection by anti-bot systems
def set_random_window_size(sb):
    width = random.randint(800, 1600)
    height = (width * 2) // 3
    sb.set_window_size(width, height)

# Setup logging for application
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("/tmp/events.log"),
            logging.StreamHandler()
        ]
    )

# Kill remaining browser processes during cleanup
def cleanup_browser_processes():
    try:
        os.system("pkill -f brave-browser")
        logging.info("Forcefully killed all remaining browser processes.")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

# Function to check for appointments
def check_for_appointments():
    with SB(
            browser="chrome",
            binary_location='/usr/bin/brave-browser',
            headed=True,
            use_auto_ext=True,
            slow=True,
            demo=True,
            incognito=True,
    ) as sb:
        try:
            set_random_window_size(sb)
            sleep(3)
            sb.open(config['url'])
            sleep(random.uniform(1, 6)) 
            sb.click("#form")
            sleep (4)
            sleep(random.uniform(5, 12)) 
            sb.select_option_by_text("#form", config['region'])
            sleep(5)
            sleep(random.uniform(5, 14))
            sb.click("#btnAceptar")
            sleep(7)
            sleep(random.uniform(3, 9)) 
            sb.select_option_by_text("#tramiteGrupo\\[1\\]", config['tramiteOptionText'])
            sleep (4)
            sleep(random.uniform(1, 8)) 
            sb.click("#btnAceptar") 
            sleep(3)
            sleep(random.uniform(3, 7))
            sb.click("#btnEntrar")
            sb.find_element(By.ID, "rdbTipoDocPas").click()
            sb.type("#txtIdCitado", config['idCitadoValue'])
            sleep(4)
            sb.type("#txtDesCitado", config['desCitadoValue'])
            sleep(4)
            sb.type("#txtAnnoCitado", config['AnnoCitadoValue'])
            sleep(4)
            sb.select_option_by_text("#txtPaisNac", config['paisNacValue'])
            sleep(4)
            sb.click("#btnEnviar")
            sleep(4)
            sb.click("#btnEnviar")
            sleep(4)
            if sb.is_text_visible("En este momento no hay citas disponibles"):
                logging.info("No available appointments. Trying again in 4 minutes.")
                find_and_kill()
                return "retry"
            else:
                sb.set_window_size(1280, 1024)
                sb.save_screenshot("/tmp/cita_disponible.png")
                send_email("Cita Disponible Alert", "localhost:6080 to complete", attach_screenshot=True)
                logging.info("Appointments might be available. Keeping the browser open for manual check.")
                time.sleep(600)
                return "manual_check_needed"
        except Exception as e:
            logging.error(f"Encountered an error during the steps: {e}. Trying again in 4 minutes.")
            find_and_kill()
            return "error"

# Main loop to retry appointment checks
def main():
    setup_logging()
    while True:
        result = check_for_appointments()
        if result in ("retry", "error"):
            time.sleep(600)
        elif result == "manual_check_needed":
            input("Press Enter to exit after your manual check...")
            break

if __name__ == "__main__":
    main()
