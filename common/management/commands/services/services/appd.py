from abc import ABC, abstractmethod
import multiprocessing.process
from threading import Thread, Lock, Event
import socket
from threading import Thread
import json
import logging
from common.base.utils import AESCipherV2
import multiprocessing
from .base import BaseService
import inspect
import time
import pkgutil
import importlib

logger = logging.getLogger(__name__)


class AppdService(BaseService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appd_services = []
        self.appd_service_check_time = 30

    def find_service_cls(self, base_class, submodule_name="services"):
        subclasses = []
        appnames = [
            appstr.split(".")[0]
            for appstr in importlib.import_module("config").ULAB_APPS
        ]
        for appname in appnames:
            try:
                submodule = importlib.import_module(f"{appname}.{submodule_name}")
                for _, cls in inspect.getmembers(submodule, inspect.isclass):
                    if issubclass(cls, base_class) and cls is not base_class:
                        # Check if the class has a custom flag or uses the abstract method
                        if hasattr(cls, "__is_abstract") and not getattr(
                            cls, "__is_abstract"
                        ):
                            subclasses.append(cls)
                        elif not inspect.isabstract(cls):
                            subclasses.append(cls)
            except Exception as e:
                pass
        return subclasses

    def run(self):
        appd_service_cls = self.find_service_cls(AppServiceBase)
        self.appd_services = [subcls() for subcls in appd_service_cls]
        for service in self.appd_services:
            service.start()
        # while True:
        #     for service in self.appd_services:
        #         if service.alive():
        #             msg = f"Appd {service} is running."
        #         else:
        #             msg = f"Appd {service} is not running."
        #         print(msg)
        #     time.sleep(self.appd_service_check_time)

    def open_subprocess(self):
        self._process = multiprocessing.Process(target=self.run, daemon=True)
        self._process.start()

    def start(self):
        print("\n- Start Appd as App Service")
        return super().start()

    def stop(self, force=False):
        for service in self.appd_services:
            service.stop()
        self._process.terminate()
        self._process.close()
        return super().stop(force)


class AppServiceBase(ABC):
    def __init__(self) -> None:
        self._running_stop_event = Event()
        self._running_process = None
        self._running_lock = Lock()
        self._running = False

    @abstractmethod
    def run_main_loop(self) -> None:
        pass

    def run(self) -> None:
        self._running = True
        while not self._running_stop_event.is_set():
            self.run_main_loop()
        self._running = False

    def start(self) -> None:
        if self._running:
            return
        self._running_stop_event.clear()
        self._running_process = Thread(target=self.run)
        self._running_process.start()
        logger.info(f"{self.__class__.__name__} started")

    def stop(self):
        self._running_stop_event.set()

    def alive(self):
        return self._running


class SecureSocketAppService(AppServiceBase):
    def __init__(self):
        super().__init__()
        self.cipher = AESCipherV2(key=self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    @property
    @abstractmethod
    def host(self):
        return "localhost"

    @property
    @abstractmethod
    def port(self):
        return -1

    @property
    @abstractmethod
    def key(self):
        return ""

    @property
    @abstractmethod
    def username(self):
        return ""

    @property
    @abstractmethod
    def password(self):
        return ""

    @abstractmethod
    def handle_request(self, reqcmd, *args, **kwargs):
        return args, kwargs

    def _handle_client(self, conn, addr):
        logger.debug(f"Connected by {addr}")
        serial = 0
        try:
            self._valid_password(conn)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                index, timestamp, reqcmd, args, kwargs = self._decode_message(data)
                if index == serial:
                    if serial == 9999:
                        serial = 0
                    else:
                        serial += 1
                else:
                    break
                logger.debug(
                    f"Received{index}: {reqcmd}, Args: {args}, Kwargs: {kwargs}"
                )
                ret = self.handle_request(reqcmd, *args, **kwargs)
                if ret is not None:
                    if (
                        len(ret) == 2
                        and (type(ret[0]) == tuple or type(ret[0]) == list)
                        and type(ret[1]) == dict
                    ):
                        res_args, res_kwargs = ret
                    elif type(ret) == dict:
                        res_args, res_kwargs = [], ret
                    elif len(ret) > 0:
                        res_args, res_kwargs = ret, {}
                    else:
                        res_args, res_kwargs = [], {}
                else:
                    res_args, res_kwargs = [], {}
                self._send_response(conn, index, reqcmd, *res_args, **res_kwargs)
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            conn.close()

    def _encode_message(self, index, reqcmd, *args, **kwargs):
        return self.cipher.encrypt(
            json.dumps(
                {
                    "index": index,
                    "timestamp": int(time.time() * 1000),
                    "reqcmd": reqcmd,
                    "args": list(args),
                    "kwargs": kwargs,
                }
            ).encode("utf-8")
        )

    def _decode_message(self, message):
        data = json.loads(self.cipher.decrypt(message))
        return (
            data["index"],
            data["timestamp"],
            data["reqcmd"],
            data.get("args", []),
            data.get("kwargs", {}),
        )

    def _valid_password(self, conn):
        data = conn.recv(1024)
        if not data:
            return False
        index, timestamp, reqcmd, args, kwargs = self._decode_message(data)
        if index != -1:
            return False
        if (
            reqcmd != "password"
            and kwargs["username"] != self.username
            and kwargs["password"] != self.password
        ):
            return False
        self._send_response(conn, index, reqcmd, True)
        return True

    def _send_response(self, conn, index, reqcmd, *args, **kwargs):
        encrypted_response = self._encode_message(index, reqcmd, *args, **kwargs)
        conn.sendall(encrypted_response)

    def run_main_loop(self) -> None:
        conn, addr = self.socket.accept()
        client_thread = Thread(target=self._handle_client, args=(conn, addr))
        client_thread.start()

    def stop(self):
        super().stop()
        self.socket.close()


class SecureSocketAppClient:
    def __init__(self, host, port, username, password, key):
        self.host = host
        self.port = port
        self.key = key
        self.username = username
        self.password = password
        self.cipher = AESCipherV2(key=key)
        self.socket = None
        self.index = 0
        self.lock = Lock()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self._valid_password()

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def _encode_message(self, index, reqcmd, *args, **kwargs):
        return self.cipher.encrypt(
            json.dumps(
                {
                    "index": index,
                    "timestamp": int(time.time() * 1000),
                    "reqcmd": reqcmd,
                    "args": list(args),
                    "kwargs": kwargs,
                }
            ).encode("utf-8")
        )

    def _decode_message(self, message):
        data = json.loads(self.cipher.decrypt(message))
        return (
            data["index"],
            data["timestamp"],
            data["reqcmd"],
            data.get("args", []),
            data.get("kwargs", {}),
        )

    def _valid_password(self):
        index, reqcmd = -1, "password"
        self._send_message(
            index, reqcmd, username=self.username, password=self.password
        )
        response_data = self.socket.recv(1024)
        if not response_data:
            return False
        _index, timestamp, _reqcmd, args, kwargs = self._decode_message(response_data)
        if _index == index and _reqcmd == reqcmd and args[0]:
            return True
        return False

    def _send_message(self, index, reqcmd, *args, **kwargs):
        encrypted_response = self._encode_message(index, reqcmd, *args, **kwargs)
        self.socket.sendall(encrypted_response)

    def send_request(self, reqcmd, *args, **kwargs):
        with self.lock:
            try:
                if self.socket is None:
                    if not self.connect():
                        raise ConnectionError("Client is not connected.")
                self._send_message(self.index, reqcmd, *args, **kwargs)
                response_data = self.socket.recv(4096)
                if not response_data:
                    if not self.connect():
                        raise ConnectionResetError("Server closed connection.")
                index, timestamp, _reqcmd, args, kwargs = self._decode_message(
                    response_data
                )
                logger.debug(
                    f"{index}, {timestamp}, {reqcmd}, Args: {args}, Kwargs: {kwargs}"
                )
                if self.index != index:
                    return False, "Error in response index."
                if _reqcmd != reqcmd:
                    return False, "Error in response reqcmd."
                if self.index == 9999:
                    self.index = 0
                else:
                    self.index += 1
                return True, list(args), kwargs
            except Exception as e:
                logger.error(f"Error in send_message: {e}")
                return False, str(e)
