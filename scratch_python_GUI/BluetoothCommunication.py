import bluetooth

 

class BluetoothCommunication:

    def __init__(self, device_name, port):

        self.device_name = device_name

        self.port = port

        self.socket = None

 

    def find_device_address(self):

        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, lookup_class=True)

        for addr, name, _ in nearby_devices:

            if name == self.device_name:

                return addr

        raise ValueError(f"Device with name '{self.device_name}' not found nearby")

 

    def connect(self):

        try:

            device_address = self.find_device_address()

            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

            self.socket.connect((device_address, self.port))

            print(f"Connected to {self.device_name} ({device_address}) on port {self.port}")

        except Exception as e:

            print("Error connecting:", e)

 

    def send_data(self, data):

        try:

            # hex_data = bytes.fromhex(data)

            self.socket.send(data)

            print("Sent data in hex:", data)

        except Exception as e:

            print("Error sending data:", e)

 

    def receive_data(self, buffer_size=1024):

        try:

            data = self.socket.recv(buffer_size)

            print("Received data:", data.hex())

            return data

        except Exception as e:

            print("Error receiving data:", e)

 

    def disconnect(self):

        try:

            self.socket.close()

            print("Disconnected")

        except Exception as e:

            print("Error disconnecting:", e)

 

# Example usage:

if __name__ == "__main__":

    # Replace "HC-05" with the name of your Bluetooth device

    device_name = "HC-05"

    port = 1  # Replace with the appropriate port

    print("Connecting: Please Wait\n")

    bluetooth_communication = BluetoothCommunication(device_name, port)

    bluetooth_communication.connect()

    print("Connection Successful\n")

    # Send and receive data as needed

    hex_data_to_send = "07000F000000"  # "Hello, Bluetooth" in hex

    bluetooth_communication.send_data(hex_data_to_send)

    received_data = bluetooth_communication.receive_data()

 

    # Disconnect when done

    bluetooth_communication.disconnect()

    exit