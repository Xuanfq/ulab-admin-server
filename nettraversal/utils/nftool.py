from threading import Lock
import logging
from abc import ABC, abstractmethod
import subprocess
import signal

logger = logging.getLogger(__name__)


class NetForwardController(ABC):
    def __init__(
        self,
        src_ip: str,
        src_port: int,
        src_protocal: str,
        dst_ip: str,
        dst_port: int,
    ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.src_protocal = src_protocal
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    @abstractmethod
    def start_forwarding(self):
        pass

    @abstractmethod
    def stop_forwarding(self):
        pass


class NetForwardManager:
    def __init__(self, controller_class: NetForwardController):
        self.controller_class = controller_class
        self.forwarding_controllers = {}
        self.lock = Lock()
        # signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signal, frame):
        logger.info("NetForwardManager Stopping...")
        with self.lock:
            for controller in self.forwarding_controllers.values():
                controller.stop_forwarding()
            self.forwarding_controllers = {}
        logger.info("NetForwardManager Stopped...")

    def add_forwarding_controller(self, id: any, controller: NetForwardController):
        with self.lock:
            # check if controller already exists
            if id in self.forwarding_controllers:
                raise ValueError(f"Forwarding controller with id {id} already exists")
            self.forwarding_controllers[id] = controller

    def add_forwarding_controller(
        self,
        id: any,
        src_ip: str,
        src_port: int,
        src_protocal: str,
        dst_ip: str,
        dst_port: int,
    ):
        with self.lock:
            # check if controller already exists
            if id in self.forwarding_controllers:
                raise ValueError(f"Forwarding controller with id {id} already exists")
            controller = self.controller_class(
                src_ip, src_port, src_protocal, dst_ip, dst_port
            )
            self.forwarding_controllers[id] = controller

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

    def start_forwarding(self, id: any):
        controller = self.get_forwarding_controller(id)
        if controller:
            controller.start_forwarding()

    def stop_forwarding(self, id: any):
        controller = self.get_forwarding_controller(id)
        if controller:
            controller.stop_forwarding()


class SocatNetForwardController(NetForwardController):
    def __init__(
        self,
        src_ip: str,
        src_port: int,
        src_protocal: str,
        dst_ip: str,
        dst_port: int,
    ):
        self.src_ip = src_ip
        self.src_port = src_port
        self.src_protocal = src_protocal
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.socat_process = None
        self.socat_process_lock = Lock()

    def start_forwarding(self):
        command = [
            "socat",
            f"TCP-LISTEN:{self.dst_port},fork",
            f"TCP:{self.src_ip}:{self.src_port}",
        ]
        try:
            with self.socat_process_lock:
                if self.socat_process and self.socat_process.poll() is None:
                    return True
                self.socat_process = subprocess.Popen(command)
                logger.info(
                    f"Started forwarding from {self.dst_ip}:{self.dst_port} to {self.src_ip}:{self.src_port}"
                )
                return True
        except Exception as e:
            logger.error(f"Error starting socat: {e}")
            return False

    def stop_forwarding(self):
        cmd = f'ps aux | grep "socat TCP-LISTEN:{self.dst_port},fork TCP:{self.src_ip}:{self.src_port}" | grep -v "grep" | '
        cmd += "awk '{print $2}' | xargs kill -9"
        logger.info(cmd)
        with self.socat_process_lock:
            if self.socat_process and self.socat_process.poll() is None:
                self.socat_process.terminate()
                self.socat_process.wait()
                status, std = subprocess.getstatusoutput(cmd)
                self.socat_process = None
                logger.info(
                    f"Stopped forwarding from {self.dst_ip}:{self.dst_port} to {self.src_ip}:{self.src_port}"
                )
                return False
            else:
                status, std = subprocess.getstatusoutput(cmd)
                if status != 0:
                    logger.error(
                        "No active forwarding or process has already terminated."
                    )
                    return False
                return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    nf = NetForwardManager(SocatNetForwardController)
    nf.add_forwarding_controller(1, "127.0.0.1", 5173, "tcp", "127.0.0.1", 5174)
    nf.start_forwarding(1)
    input("Enter to exit")
    nf.stop_forwarding(1)
