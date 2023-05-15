import subprocess
import threading
import signal
import os

class SingletonProcess:
    def __init__(self):
        self.process = None
        self.lock = threading.Lock()
    def __del__(self):
        print("Call destructor")
        self.stop()

    def start(self, command, *args):
        if self.process is not None:
            print("Process is already running")
            self.stop()
        with self.lock:
            self.return_code = None
            self.process = subprocess.Popen([command] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.monitor_thread = threading.Thread(target=self.monitor_process)
            self.monitor_thread.start()
    def stop(self):
        with self.lock:
            if self.process is None:
                print("No process is running")
                return
            try:
                self.process.terminate()
                self.monitor_thread.join()  # Wait for monitor_thread to finish
                
                print(self.return_code)
            except Exception as e:
                print('Oh :(')
                print(str(e))
            finally:
                self.process = None

    def monitor_process(self):
        stdout, stderr = self.process.communicate()
        print("STDOUT:\n", stdout.decode())
        print("STDERR:\n", stderr.decode())
        #print("Process finished with code %s" % return_code)
        self.return_code = self.process.returncode
        self.process = None
        #if return_code != 0:
        #    raise Exception('Process failed with code %s' % return_code)

if __name__ == "__main__":
    # Usage
    singleton = SingletonProcess()
    singleton.start('ping', 'www.google.com')
    from time import sleep
    sleep(3)
    singleton.stop()
    singleton.start('ping', '-c', '5', 'localhost')

