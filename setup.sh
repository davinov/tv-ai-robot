curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

cp ./99-arduino.rules /etc/udev/rules.d/99-arduino.rules
chmod 644 /etc/udev/rules.d/99-arduino.rules

cp robot.service /etc/systemd/user/robot.service
chmod 644 /etc/systemd/user/robot.service

systemctl daemon-reload
systemctl restart systemd-udevd.service 

cp ./utils/hacktv /usr/local/bin/hacktv
chmod 755 /usr/local/bin/hacktv