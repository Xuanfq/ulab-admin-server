from threading import Lock
import logging
from abc import ABC, abstractmethod
import subprocess
import signal

logger = logging.getLogger(__name__)


class SingletonType(type):
    _instance_lock = Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class PortForwardController(ABC):
    def __init__(
        self,
        src_ip: str,
        src_port: int,
        protocol: str,
        dst_ip: str,
        dst_port: int,
    ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.protocol = protocol
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    @abstractmethod
    def is_forwarding(self):
        pass

    @abstractmethod
    def start_forwarding(self):
        pass

    @abstractmethod
    def stop_forwarding(self):
        pass


class PortForwardManager:
    def __init__(self, controller_class: PortForwardController):
        self.controller_class = controller_class
        self.forwarding_controllers = {}
        self.lock = Lock()
        # signal.signal(signal.SIGINT, self._signal_handler)
        logger.debug(f"NetForwardManager Initialized")

    def __len__(self):
        with self.lock:
            return len(self.forwarding_controllers)

    def _signal_handler(self, signal, frame):
        logger.info("NetForwardManager Stopping...")
        with self.lock:
            for controller in self.forwarding_controllers.values():
                controller.stop_forwarding()
            self.forwarding_controllers = {}
        logger.info("NetForwardManager Stopped...")

    def add_forwarding_controller(self, id: any, controller: PortForwardController):
        with self.lock:
            # check if controller already exists
            if id in self.forwarding_controllers:
                # raise ValueError(f"Forwarding controller with id {id} already exists")
                logger.warning(f"Forwarding controller with id {id} already exists")
                return False
            self.forwarding_controllers[id] = controller
            return True

    def add_forwarding_controller(
        self,
        id: any,
        src_ip: str,
        src_port: int,
        protocol: str,
        dst_ip: str,
        dst_port: int,
    ):
        with self.lock:
            # check if controller already exists
            if id in self.forwarding_controllers:
                # raise ValueError(f"Forwarding controller with id {id} already exists")
                logger.warning(f"Forwarding controller with id {id} already exists")
                return False
            controller = self.controller_class(
                src_ip, src_port, protocol, dst_ip, dst_port
            )
            self.forwarding_controllers[id] = controller
            controller.start_forwarding()
            return True

    def remove_forwarding_controller(self, id: any):
        controller = None
        with self.lock:
            if id in self.forwarding_controllers:
                controller = self.forwarding_controllers[id]
                del self.forwarding_controllers[id]
        if controller:
            controller.stop_forwarding()

    def get_forwarding_controller(self, id: any):
        controller = None
        with self.lock:
            if id in self.forwarding_controllers:
                controller = self.forwarding_controllers[id]
        return controller

    def is_forwarding(self, id: any):
        controller = self.get_forwarding_controller(id)
        if controller:
            return controller.is_forwarding()
        return False

    def remove_all_forwarding_controllers(self):
        with self.lock:
            for id, controller in self.forwarding_controllers.items():
                controller.stop_forwarding()
            self.forwarding_controllers.clear()
    
class PortForwardManagerSingleton(PortForwardManager, metaclass=SingletonType):
    pass


class SocatPortForwardController(PortForwardController):
    def __init__(
        self,
        src_ip: str,
        src_port: int,
        protocol: str,
        dst_ip: str,
        dst_port: int,
    ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.protocol = protocol
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.run_cmd = f"socat TCP-LISTEN:{self.src_port},bind={self.src_ip},reuseaddr,fork TCP:{self.dst_ip}:{self.dst_port}"
        self.socat_process = None

    def is_forwarding(self):
        status_cmd = f"ps aux | grep '{self.run_cmd}' | grep -v 'grep'"
        status, std = subprocess.getstatusoutput(status_cmd)
        return status == 0

    def start_forwarding(self):
        try:
            if (
                self.socat_process
                and self.socat_process.poll() is None
                and self.is_forwarding()
            ):
                return True
            self.socat_process = subprocess.Popen(self.run_cmd.split(" "))
        except Exception as e:
            logger.error(f"Error starting socat: {e}")
        logger.info(
            f"Started forwarding from {self.src_ip}:{self.src_port} to {self.dst_ip}:{self.dst_port}"
        )
        return self.is_forwarding()

    def stop_forwarding(self):
        kill_cmd = f'ps aux | grep "{self.run_cmd}" | grep -v "grep" | '
        kill_cmd += "awk '{print $2}' | xargs kill -9"
        try:
            if self.socat_process and self.socat_process.poll() is None:
                self.socat_process.terminate()
                self.socat_process.wait()
                status, std = subprocess.getstatusoutput(kill_cmd)
                self.socat_process = None
            else:
                status, std = subprocess.getstatusoutput(kill_cmd)
                if status != 0:
                    logger.warning(
                        "No active forwarding or process has already terminated."
                    )
        except Exception as e:
            logger.error(f"Error stopping socat: {e}")
        logger.info(
            f"Stopped forwarding from {self.dst_ip}:{self.dst_port} to {self.src_ip}:{self.src_port}"
        )
        return not self.is_forwarding()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    pass
