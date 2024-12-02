from MemHack import *

# Inicializar o engine para um processo específico
engine = MemoryCheatEngine("game.exe")

# Escrever um valor em um endereço de memória
memory_address = 0x12345678
engine.memory_manager.write_memory(memory_address, 999, "int")

# Monitorar mudanças em um endereço de memória
def on_memory_change(new_value):
    print(f"Novo valor detectado: {new_value}")

engine.observe_memory(memory_address, on_memory_change)

# Escanear a memória para encontrar um valor específico
scan_results = engine.memory_manager.scan_memory(999, "int")
print(f"Endereços encontrados: {scan_results}")

# Parar todos os observadores de memória
engine.stop_all_observers()

# Ler e substituir conteúdo em um arquivo de configuração
engine.file_manager.replace_in_file("config.txt", "old_value", "new_value")

# Ler e gravar arquivos JSON
config = engine.file_manager.read_json("config.json")
config["cheat_enabled"] = True
engine.file_manager.write_json("config.json", config)

# Listar todos os processos ativos
process_list = engine.process_manager.list_all_processes()
print(f"Processos ativos: {process_list}")
