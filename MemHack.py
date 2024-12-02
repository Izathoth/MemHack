import psutil
import pymem
import json
from threading import Thread
from time import sleep


class ProcessManager:
    def find_process(self, process_name):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == process_name:
                return process
        raise ValueError(f"Processo '{process_name}' não encontrado")

    def list_all_processes(self):
        return [proc.info['name'] for proc in psutil.process_iter(attrs=['name'])]


class MemoryManager:
    def __init__(self, pid):
        self.process = pymem.Pymem(pid)

    def read_memory(self, address, data_type="int"):
        if data_type == "int":
            return self.process.read_int(address)
        elif data_type == "float":
            return self.process.read_float(address)
        elif data_type == "string":
            return self.process.read_string(address)
        raise ValueError(f"Tipo de dado '{data_type}' não suportado")

    def write_memory(self, address, value, data_type="int"):
        if data_type == "int":
            self.process.write_int(address, value)
        elif data_type == "float":
            self.process.write_float(address, value)
        elif data_type == "string":
            self.process.write_string(address, value)
        else:
            raise ValueError(f"Tipo de dado '{data_type}' não suportado")

    def scan_memory(self, value, data_type="int", region_limit=10):
        results = []
        for region in self.process.get_memory_regions()[:region_limit]:
            try:
                data = self.process.read_bytes(region.BaseAddress, region.RegionSize)
                if data_type == "int" and value.to_bytes(4, 'little') in data:
                    results.append(region.BaseAddress + data.index(value.to_bytes(4, 'little')))
            except Exception:
                continue
        return results


class FileManager:
    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def write_file(self, file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def write_json(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def append_to_file(self, file_path, content):
        with open(file_path, 'a') as file:
            file.write(content)

    def replace_in_file(self, file_path, old_value, new_value):
        with open(file_path, 'r+') as file:
            content = file.read()
            content = content.replace(old_value, new_value)
            file.seek(0)
            file.write(content)
            file.truncate()


class MemoryObserver:
    def __init__(self, memory_manager, address, callback, interval=0.1):
        self.memory_manager = memory_manager
        self.address = address
        self.callback = callback
        self.interval = interval
        self.last_value = None
        self.running = False

    def start(self):
        self.running = True
        Thread(target=self._observe, daemon=True).start()

    def stop(self):
        self.running = False

    def _observe(self):
        while self.running:
            value = self.memory_manager.read_memory(self.address)
            if value != self.last_value:
                self.callback(value)
                self.last_value = value
            sleep(self.interval)


class MemoryCheatEngine:
    def __init__(self, process_name):
        self.process_manager = ProcessManager()
        self.process = self.process_manager.find_process(process_name)
        self.memory_manager = MemoryManager(self.process.info['pid'])
        self.file_manager = FileManager()
        self.observers = []

    def observe_memory(self, address, callback, interval=0.1):
        observer = MemoryObserver(self.memory_manager, address, callback, interval)
        observer.start()
        self.observers.append(observer)

    def stop_all_observers(self):
        for observer in self.observers:
            observer.stop()
        self.observers.clear()
