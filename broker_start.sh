sudo echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf
sudo echo "allow_anonymous true" >> /etc/mosquitto/mosquitto.conf
sudo systemctl start mosquitto.service
sudo systemctl enable mosquitto.service
sudo systemctl status mosquitto.service
pip install -r requirements.txt