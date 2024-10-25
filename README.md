# Cita Checker: Automated Appointment Availability Script 🚀

Cita Checker is a Python tool that automates the process of checking appointment availability on the [cita previa platform](https://icp.administracionelectronica.gob.es/icpplus/index.html) for various services in Spain, such as police services, asylum applications, or TIE card renewals.

## Features 🌟
- Uses SeleniumBase to interact with the web interface.
- Randomizes window size to avoid fingerprinting.
- Automatically sends an email notification if an appointment is found.
- Configurable via JSON (`values.json`) for ease of use and customization.
- Uses VNC for manual follow-up if needed.

## Setup 🛠️
This project uses Docker Compose to simplify running the application. A noVNC server is created, allowing you to check in either through a web browser or a VNC client.

### Step 1: Clone the Repository
```sh
$ git clone https://github.com/TiagoCortinhal/cita-checker.git
$ cd cita-checker
```

### Step 2: Run Docker Compose 🐳
To start the Docker container, simply run:
```sh
$ docker-compose up
```
This command will set up a noVNC server that you can access via your web browser or a VNC client to monitor the script in real-time.

### Step 3: Access the VNC
Once the container is running, you can view the interface using:
- Browser: `http://localhost:6080` to access noVNC.
- VNC Client: Connect to `localhost:5901`.

## Configuration 📄
Update the `values.json` file with your personal details:
```json
{
  "url": "https://icp.administracionelectronica.gob.es/icpplus/index.html",
  "idCitadoValue": "YOUR_ID_VALUE",
  "desCitadoValue": "YOUR_FULL_NAME",
  "TypeID": "PASAPORTE",
  "paisNacValue": "YOUR_COUNTRY",
  "tramiteOptionText": "POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.",
  "receiver_email": "your_receiver@example.com",
  "sender_email": "your_sender@example.com",
  "password": "your_email_password",
  "smtp_server": "mail.gmx.com",
  "smtp_port": 587,
  "keyboard_layout": "YOUR_KEYBOARD_LAYOUT",
  "region": "Madrid"
}
```

## Trámite Options 📝
Here are all the possible trámite options you can choose from (they come with a bit of spice 🫑):

- 🌍 **ASILO - PRIMERA CITA**: The start of your asylum journey in Madrid.
- 🏛️ **ASILO - OFICINA DE ASILO Y REFUGIO**: Pradillo 40 is where the magic happens for asylum and document renewals.
- ✈️ **AUTORIZACIÓN DE REGRESO**: Need to leave and come back? Get your authorization here.
- 🆔 **POLICIA - RECOGIDA DE TARJETA DE IDENTIDAD DE EXTRANJERO (TIE)**: Time to pick up that shiny new TIE card.
- 🔢 **POLICIA-ASIGNACIÓN DE N.I.E.**: Need an NIE? This is your stop.
- 📜 **POLICIA-CARTA DE INVITACIÓN**: Hosting someone? Invite them officially.
- 💚 **POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.**: For our beloved EU citizens.
- 🏠 **POLICIA-CERTIFICADOS (DE RESIDENCIA, DE NO RESIDENCIA Y DE CONCORDANCIA)**: Certificates galore – residence, non-residence, or concordance.
- 🖐️ **POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA)**: Fingerprinting and card issuance (including renewals and duplicates).
- 🎫 **POLICÍA - RECOGIDA DE LA T.I.E. CUYA AUTORIZACIÓN RESUELVE LA DIRECCIÓN GENERAL DE MIGRACIONES**: Picking up TIE cards resolved by Migration.
- 🇺🇦 **POLICÍA TARJETA CONFLICTO UCRANIA**: For those displaced due to the conflict in Ukraine.
- 🇬🇧 **POLICÍA-EXP.TARJETA ASOCIADA AL ACUERDO DE RETIRADA CIUDADANOS BRITÁNICOS (BREXIT)**: Brits and Brexit – get your cards sorted here.
- 🌐 **POLICÍA-EXPEDICIÓN DE TARJETAS CUYA AUTORIZACIÓN RESUELVE LA DIRECCIÓN GENERAL DE MIGRACIONES**: Issuing cards as per Migration resolutions.

## Using GMX for Easy SMTP Setup ✉️
You can use GMX as an SMTP server, which is easy to set up and works seamlessly for sending notification emails.
- **Server**: `mail.gmx.com`
- **Port**: `587`
- **TLS**: Enabled

Simply add your sender email, password, and SMTP configuration to `values.json`.

## Logging and Notifications 🔔
- Logs are saved in `/tmp/events.log`.
- When an appointment is available, an email is sent with a screenshot attachment.

## Contributing 💡
Contributions are welcome! This project was inspired by [https://github.com/tbalza/cita-checker](https://github.com/tbalza/cita-checker), but some bugs were present that have been improved in this version. Please create a pull request if you'd like to enhance the codebase or add new features.

## License 📜
This project is licensed under the MIT License.

