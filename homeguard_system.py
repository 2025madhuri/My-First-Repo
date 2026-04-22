"""
HomeGuard Security System Simulator
Author: Your Name
Description: A smart home monitoring system that processes sensor readings
             and triggers alerts for security, safety, and comfort issues.
"""

import random
import time
from datetime import datetime

# System configuration
HOME_MODES = ["HOME", "AWAY", "SLEEP"]
ALERT_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def create_sensor(sensor_id, location, sensor_type, threshold=None):
    """Creates a sensor dictionary."""
    return {
        "id": sensor_id,
        "location": location,
        "type": sensor_type,
        "threshold": threshold
    }


def create_alert(severity, message, sensor_id, timestamp):
    """Creates an alert dictionary."""
    return {
        "severity": severity,
        "message": message,
        "sensor_id": sensor_id,
        "timestamp": timestamp
    }


def is_abnormal_reading(sensor, reading_value):
    """Checks if a sensor reading is abnormal."""
    sensor_type = sensor["type"]

    if sensor_type == "temperature":
        return reading_value < 35 or reading_value > 95

    elif sensor_type == "motion":
        return reading_value is True

    elif sensor_type == "door":
        return reading_value == "OPEN"

    elif sensor_type == "smoke":
        return reading_value == "DETECTED"

    return False


def should_trigger_security_alert(sensor, reading_value, system_mode):
    """Checks if a security alert should be triggered."""
    sensor_type = sensor["type"]

    if system_mode == "AWAY":
        if sensor_type == "motion" and reading_value is True:
            return True
        if sensor_type == "door" and reading_value == "OPEN":
            return True

    return False


def generate_reading(sensor):
    """Generates a realistic reading for a sensor."""
    sensor_type = sensor["type"]

    if sensor_type == "temperature":
        return random.randint(30, 100)
    elif sensor_type == "motion":
        return random.choice([True, False])
    elif sensor_type == "door":
        return random.choice(["OPEN", "CLOSED"])
    elif sensor_type == "smoke":
        return random.choice(["CLEAR", "DETECTED"])

    return None


def process_reading(sensor, reading_value, system_mode):
    """Processes a sensor reading and returns a list of alerts."""
    alerts = []
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Security alerts
    if should_trigger_security_alert(sensor, reading_value, system_mode):
        if sensor["type"] == "motion":
            alerts.append(
                create_alert(
                    "HIGH",
                    f"SECURITY: Motion detected in {sensor['location']} while in {system_mode} mode!",
                    sensor["id"],
                    timestamp
                )
            )
        elif sensor["type"] == "door":
            alerts.append(
                create_alert(
                    "HIGH",
                    f"SECURITY: {sensor['location']} opened while in {system_mode} mode!",
                    sensor["id"],
                    timestamp
                )
            )

    # Safety alerts
    if sensor["type"] == "temperature":
        if reading_value < 35:
            alerts.append(
                create_alert(
                    "CRITICAL",
                    f"SAFETY: {sensor['location']} temperature is {reading_value}°F - frozen pipe risk!",
                    sensor["id"],
                    timestamp
                )
            )
        elif reading_value > 95:
            alerts.append(
                create_alert(
                    "CRITICAL",
                    f"SAFETY: {sensor['location']} temperature is {reading_value}°F - overheating risk!",
                    sensor["id"],
                    timestamp
                )
            )

    if sensor["type"] == "smoke" and reading_value == "DETECTED":
        alerts.append(
            create_alert(
                "CRITICAL",
                f"SAFETY: Smoke detected in {sensor['location']}!",
                sensor["id"],
                timestamp
            )
        )

    # Comfort notifications (only in HOME mode)
    if sensor["type"] == "temperature" and system_mode == "HOME":
        if reading_value < 65 or reading_value > 75:
            alerts.append(
                create_alert(
                    "LOW",
                    f"COMFORT: {sensor['location']} temperature is {reading_value}°F, outside comfort range.",
                    sensor["id"],
                    timestamp
                )
            )

    return alerts


def trigger_alert(alert):
    """Displays an alert."""
    severity_symbol = {
        "LOW": "ℹ️",
        "MEDIUM": "⚠️",
        "HIGH": "🚨",
        "CRITICAL": "🔥"
    }

    symbol = severity_symbol.get(alert["severity"], "⚠️")
    print(f"[ALERT!] {symbol} {alert['severity']}: {alert['message']}")


def log_event(message, timestamp=None):
    """Logs an event."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[LOG] [{timestamp}] {message}")


class Sensor:
    """Represents a sensor in the HomeGuard system."""

    def __init__(self, sensor_id, location, sensor_type, threshold=None):
        self.id = sensor_id
        self.location = location
        self.type = sensor_type
        self.threshold = threshold
        self.current_value = None

    def read(self):
        """Generates and stores a new reading."""
        sensor_dict = {
            "id": self.id,
            "location": self.location,
            "type": self.type,
            "threshold": self.threshold
        }
        self.current_value = generate_reading(sensor_dict)
        return self.current_value

    def isAbnormal(self):
        """Checks if current reading is abnormal."""
        sensor_dict = {
            "id": self.id,
            "location": self.location,
            "type": self.type,
            "threshold": self.threshold
        }
        return is_abnormal_reading(sensor_dict, self.current_value)

    def reset(self):
        """Resets the current reading."""
        self.current_value = None

    def __str__(self):
        status = "No reading" if self.current_value is None else str(self.current_value)
        return f"{self.id} ({self.location}): {status}"


def run_simulation(duration_minutes=3, system_mode="AWAY"):
    """Runs the HomeGuard simulation."""
    print("=" * 50)
    print("=== HomeGuard Security System ===")
    print("=" * 50)
    print(f"Mode: {system_mode}")

    sensors = [
        Sensor("MOTION_001", "Living Room", "motion"),
        Sensor("TEMP_001", "Kitchen", "temperature", threshold=35),
        Sensor("DOOR_001", "Front Door", "door"),
        Sensor("SMOKE_001", "Bedroom", "smoke")
    ]

    for minute in range(duration_minutes):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\nTime: {current_time}")

        for sensor in sensors:
            reading = sensor.read()

            if sensor.type == "temperature":
                status = "Normal" if 65 <= reading <= 75 else "Abnormal"
                print(f"[READING] {sensor.location} Temperature: {reading}°F ({status})")
            elif sensor.type == "motion":
                status = "DETECTED" if reading else "No activity"
                print(f"[READING] {sensor.location} Motion: {status}")
            elif sensor.type == "door":
                print(f"[READING] {sensor.location}: {reading}")
            elif sensor.type == "smoke":
                print(f"[READING] {sensor.location} Smoke: {reading}")

            sensor_dict = {
                "id": sensor.id,
                "location": sensor.location,
                "type": sensor.type,
                "threshold": sensor.threshold
            }

            alerts = process_reading(sensor_dict, reading, system_mode)

            for alert in alerts:
                trigger_alert(alert)
                if alert["severity"] in ["HIGH", "CRITICAL"]:
                    log_event("Sending notification to homeowner...")

        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("Simulation complete!")
    print("=" * 50)


if __name__ == "__main__":
    run_simulation(duration_minutes=3, system_mode="AWAY")