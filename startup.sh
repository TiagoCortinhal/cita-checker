#!/bin/bash

# Set VNC password if provided
if [ -n "$VNC_PASSWORD" ]; then
    mkdir -p /home/nonroot/.vnc
    echo -n "$VNC_PASSWORD" > /home/nonroot/.vnc/password1
    x11vnc -storepasswd $(cat /home/nonroot/.vnc/password1) /home/nonroot/.vnc/password2
    chmod 400 /home/nonroot/.vnc/password*
    sed -i 's/^command=x11vnc.*/& -rfbauth \/home\/nonroot\/.vnc\/password2/' /etc/supervisor/conf.d/supervisord.conf
    export VNC_PASSWORD=
    chown -R nonroot:nonroot /home/nonroot/.vnc
fi

# Set X11VNC arguments if provided
if [ -n "$X11VNC_ARGS" ]; then
    sed -i "s/^command=x11vnc.*/& ${X11VNC_ARGS}/" /etc/supervisor/conf.d/supervisord.conf
fi

# Set Openbox arguments if provided
if [ -n "$OPENBOX_ARGS" ]; then
    sed -i "s#^command=/usr/bin/openbox\$#& ${OPENBOX_ARGS}#" /etc/supervisor/conf.d/supervisord.conf
fi

# Set screen resolution if provided
if [ -n "$RESOLUTION" ]; then
    sed -i "s/1024x768/$RESOLUTION/" /usr/local/bin/xvfb.sh
fi

# Create nonroot user if it doesn't exist
if ! id "nonroot" &>/dev/null; then
    echo "* Creating user: nonroot"
    useradd --create-home --shell /bin/bash --user-group --groups adm,sudo nonroot
    if [ -z "$PASSWORD" ]; then
        echo "  Setting default password to \"root\""
        PASSWORD=root
    fi
    echo "nonroot:$PASSWORD" | chpasswd
    HOME=/home/nonroot
    if [ -d /root/.config ]; then
        cp -r /root/{.config,.gtkrc-2.0,.asoundrc} $HOME
    fi
    chown -R nonroot:nonroot $HOME
    [ -d "/dev/snd" ] && chgrp -R adm /dev/snd
fi

# Update supervisord.conf to reflect the correct user and home directory
sed -i -e "s|%USER%|nonroot|" -e "s|%HOME%|/home/nonroot|" /etc/supervisor/conf.d/supervisord.conf

# Ensure the home folder and required directories exist
if [ ! -x "/home/nonroot/.config/pcmanfm/LXDE/" ]; then
    mkdir -p /home/nonroot/.config/pcmanfm/LXDE/
    ln -sf /usr/local/share/doro-lxde-wallpapers/desktop-items-0.conf /home/nonroot/.config/pcmanfm/LXDE/
    chown -R nonroot:nonroot /home/nonroot
fi

# Create a Python virtual environment for nonroot user if it doesn't exist
if [ ! -d "/home/nonroot/venv" ]; then
    su - nonroot -c "python3 -m venv /home/nonroot/venv"
    su - nonroot -c "/home/nonroot/venv/bin/pip install seleniumbase webdriver-manager"
fi

# Ensure virtual environment is activated for Python scripts
echo "source /home/nonroot/venv/bin/activate" >> /home/nonroot/.bashrc

# Clear up sensitive environment variables
PASSWORD=
HTTP_PASSWORD=

# Start supervisord
exec /bin/tini -- supervisord -n -c /etc/supervisor/supervisord.conf
