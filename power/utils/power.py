#!/bin/python3

from telnetlib import Telnet
import time
import argparse
from threading import Thread, Timer, Lock
import re
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class PowerController(ABC):
    @abstractmethod
    def power_status(self, ctrlport, cache=True):
        pass

    @abstractmethod
    def power_on(self, ctrlport, delay=0):
        pass

    @abstractmethod
    def power_off(self, ctrlport, delay=0):
        pass

    @abstractmethod
    def power_reboot(self, ctrlport, delay=0, interval=5):
        pass


class PowerControllerManager(ABC):
    def __init__(self) -> None:
        self.controller_dict = {}

    @abstractmethod
    def add(self, controller_id, controller: PowerController):
        if controller_id in self.controller_dict:
            return
        self.controller_dict[controller_id] = controller

    @abstractmethod
    def get(self, controller_id) -> PowerController:
        if controller_id in self.controller_dict:
            return self.controller_dict[controller_id]
        return None

    @abstractmethod
    def has(self, controller_id) -> bool:
        return controller_id in self.controller_dict

    @abstractmethod
    def remove(self, controller_id) -> bool:
        if controller_id in self.controller_dict:
            controller = self.controller_dict[controller_id]
            del controller
            del self.controller_dict[controller_id]

    @abstractmethod
    def power_status(self, controller_id, ctrlport, cache=True):
        pass

    @abstractmethod
    def power_on(self, controller_id, ctrlport, delay=0):
        pass

    @abstractmethod
    def power_off(self, controller_id, ctrlport, delay=0):
        pass

    @abstractmethod
    def power_reboot(self, controller_id, ctrlport, delay=0, interval=5):
        pass


class RepeatingTimer(Timer):

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class ApcPduPowerController(PowerController):

    def __init__(
        self,
        ip,
        port=23,
        username="apc",
        password="apc",
        update_status_flag=True,
        update_status_time=10,
        keep_alive_time=30,
        cmd_exec_time=0.5,
    ) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.status_dict = {}  # outlet:status
        self.update_status_flag = update_status_flag
        self.update_status_time = update_status_time if update_status_time >= 3 else 3
        self.update_status_timer = RepeatingTimer(
            self.update_status_time, self._update_status
        )
        self.cmd_exec_time = cmd_exec_time if cmd_exec_time >= 0.3 else 0.3
        self.keep_alive_time = keep_alive_time if keep_alive_time >= 10 else 10
        self.keep_alive_timer = RepeatingTimer(self.keep_alive_time, self._keep_alive)
        self.daemon_setup = False
        self.keep_alive_cmd = "olStatus all"
        self.last_cmd_time = int(time.time())
        self.tn = None
        self.tn_lock = Lock()
        self.tn_error = False
        self._setup()

    def close(self):
        try:
            with self.tn_lock:
                self.update_status_timer.cancel()
                self.keep_alive_timer.cancel()
                self.tn.close()
                del self.update_status_timer
                del self.keep_alive_timer
                del self.tn
        except Exception as e:
            pass

    def _setup(self):
        try:
            with self.tn_lock:
                self.tn = Telnet(host=self.ip, port=self.port)
                self.tn.read_until(b"User Name :")
                self.tn.write("{}\r".format(self.username).encode())
                self.tn.read_until(b"Password  :")
                self.tn.write("{}\r".format(self.password).encode())
                self.last_cmd_time = int(time.time())
                time.sleep(0.5)
                self.tn.read_very_eager()
                self.tn_error = False
            self._update_status()
        except Exception as e:
            self.tn_error = True
            print(f"APCPDU {self.ip}: {str(e)}")
        if not self.daemon_setup:
            # start keep alive timer
            self.keep_alive_timer.start()
            # start update status timer
            if self.update_status_flag:
                self.update_status_timer.start()
            self.daemon_setup = True

    def _keep_alive(self):
        if int(time.time()) - self.last_cmd_time >= self.keep_alive_time:
            # print('keep alive')
            result = self.send_cmd(self.keep_alive_cmd)

    def _update_status(self):
        # print('update status')
        if self.tn_error:
            for k, v in self.status_dict.items():
                self.status_dict[k] = "Unknown[APC Error]"
            return
        try:
            result = self.send_cmd("olStatus all")
            #  1: Outlet 1: On
            pattern = re.compile(r"(\d+):\s+Outlet\s+(\d+):\s+(\w+)")
            matches = pattern.findall(result)
            for match in matches:
                outlet_index, outlet_number, status = match
                self.status_dict[str(outlet_number)] = status
        except:
            return

    def send_cmd(self, cmd, cmd_exec_time=0.5):
        try:
            with self.tn_lock:
                self.tn.write("{}\r".format(cmd).encode())
                self.last_cmd_time = int(time.time())
                time.sleep(cmd_exec_time)
                result = self.tn.read_very_eager().decode()
                return result
        except Exception as e:
            self.tn_error = True
            print(f"APCPDU {self.ip}: {str(e)}")
            self._setup()

    def power_status(self, outlet, cache=True):
        if self.tn_error:
            return False, "APC Error"
        if cache:
            outlet = str(outlet)
            if outlet in self.status_dict:
                return self.status_dict[outlet]
            return "Unknown"
        cmd_exec_cat_status = "olStatus {}".format(outlet)
        with self.tn_lock:
            self.last_cmd_time = int(time.time())
            self.tn.write("{}\r".format(cmd_exec_cat_status).encode())
            time.sleep(self.cmd_exec_time)
            status = self.tn.read_very_eager().decode()
        return True, ("On" if "On" in status else "Off")

    def power_on(self, outlet, delay=0):
        if self.tn_error:
            return False, "APC Error"
        cmd_set_delayon_wait_time = "olOnDelay {} {}".format(outlet, delay)
        cmd_exec_delayon = "olDlyOn {}".format(outlet)
        with self.tn_lock:
            if delay > 0:
                self.last_cmd_time = int(time.time())
                self.tn.write("{}\r".format(cmd_set_delayon_wait_time).encode())
                time.sleep(self.cmd_exec_time)
            self.last_cmd_time = int(time.time())
            self.tn.write("{}\r".format(cmd_exec_delayon).encode())
            time.sleep(self.cmd_exec_time)
            status = self.tn.read_very_eager().decode()
        return (True if "Success" in status else False), None

    def power_off(self, outlet, delay=0):
        if self.tn_error:
            return False, "APC Error"
        cmd_set_delayoff_wait_time = "olOffDelay {} {}".format(outlet, delay)
        cmd_exec_delayoff = "olDlyOff {}".format(outlet)
        with self.tn_lock:
            if delay > 0:
                self.last_cmd_time = int(time.time())
                self.tn.write("{}\r".format(cmd_set_delayoff_wait_time).encode())
                time.sleep(self.cmd_exec_time)
            self.last_cmd_time = int(time.time())
            self.tn.write("{}\r".format(cmd_exec_delayoff).encode())
            time.sleep(self.cmd_exec_time)
            status = self.tn.read_very_eager().decode()
        return (True if "Success" in status else False), None

    def power_reboot(self, outlet, delay=0, interval=60):
        if self.tn_error:
            return False, "APC Error"
        cmd_set_delayoff_wait_time = "olOffDelay {} {}".format(outlet, delay)
        cmd_set_reboot_wait_time = "olRbootTime {} {}".format(outlet, interval)
        cmd_exec_delay_reboot = "olReboot {}".format(outlet)
        with self.tn_lock:
            if delay > 0:
                self.tn.write("{}\r".format(cmd_set_delayoff_wait_time).encode())
                time.sleep(self.cmd_exec_time)
            self.tn.write("{}\r".format(cmd_set_reboot_wait_time).encode())
            time.sleep(self.cmd_exec_time)
            self.tn.write("{}\r".format(cmd_exec_delay_reboot).encode())
            time.sleep(self.cmd_exec_time)
            status = self.tn.read_very_eager().decode()
        return (True if "Success" in status else False), None

    def alive(self):
        return not self.tn_error


class ApcPduPowerControllerManager(PowerControllerManager):

    def __init__(self) -> None:
        self.controller_dict = {}
        pass

    def add(
        self,
        id,
        ip,
        port=23,
        username="apc",
        password="apc",
        update_status_flag=True,
        update_status_time=10,
        keep_alive_time=30,
    ):
        if id in self.controller_dict:
            return
        self.controller_dict[id] = ApcPduPowerController(
            ip=ip,
            port=port,
            username=username,
            password=password,
            update_status_flag=update_status_flag,
            update_status_time=update_status_time,
            keep_alive_time=keep_alive_time,
        )

    def get(self, id):
        if id in self.controller_dict:
            return self.controller_dict[id]
        return None

    def has(self, id):
        return id in self.controller_dict

    def remove(self, id):
        if id in self.controller_dict:
            controller = self.controller_dict[id]
            controller.close()
            del controller
            del self.controller_dict[id]

    def alive(self, id):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.alive()

    def send_cmd(self, id, cmd, cmd_exec_time=0.5):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.send_cmd(cmd, cmd_exec_time)

    def power_status(self, id, outlet, cache=True):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.power_status(outlet, cache)

    def power_on(self, id, outlet, delay=0):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.power_on(outlet, delay)

    def power_off(self, id, outlet, delay=0):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.power_off(outlet, delay)

    def power_reboot(self, id, outlet, delay=0, interval=60):
        if id not in self.controller_dict:
            return None
        controller = self.controller_dict[id]
        return controller.power_reboot(outlet, delay, interval)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pass
