class Emulator:
    def __init__(self, emulator_port, emulator_pid, emulator_model):
        self.port = emulator_port
        self.pid = emulator_pid
        self.model = emulator_model

    def __str__(self):
        return "Port: "+self.port +"\n" + "PID: " + self.pid + "\n" + "Model: "+self.model+"\n"
