import json
import time
from utils.logger import iris_logger

class IrisState:
    IDLE = "IDLE"
    BUSY = "BUSY"
    ALERT = "ALERT"
    SLEEP = "SLEEP"

class StateMachine:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.current_state = IrisState.IDLE
        self.last_state_change_time = 0
        self.min_state_duration = 1.0 # 1 saniyeden kısa zıplamaları loglama

    def update(self, data, is_connected=True):
        if not is_connected:
            return self._change_state(IrisState.SLEEP, data)

        thresh = self.config["thresholds"]
        new_state = IrisState.IDLE

        if data['battery'] < thresh["battery_alert"]:
            new_state = IrisState.ALERT
        elif data['cpu_usage'] > thresh["cpu_busy"]:
            new_state = IrisState.BUSY
        
        return self._change_state(new_state, data)

    def _change_state(self, new_state, data):
        if new_state != self.current_state:
            now = time.time()
            if (now - self.last_state_change_time) > self.min_state_duration:
                iris_logger.info(f"STATE CHANGE: {self.current_state} -> {new_state} | CPU: %{data.get('cpu_usage')}")
                self.current_state = new_state
                self.last_state_change_time = now
        return self.current_state