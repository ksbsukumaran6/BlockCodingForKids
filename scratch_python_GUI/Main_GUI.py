import asyncio
import websockets
import json
import time
import sys
import threading
import time
import base64


# library to use Bluetooth module for the project
from BluetoothCommunication import BluetoothCommunication

device_name = "HC-05"

port = 1  # Replace with the appropriate port

bluetooth_communication = BluetoothCommunication(device_name, port)


jsonrpc_version = ''

method = ''

params = ''

service_id = ''

characteristic_id = ''

rpc_message=''

encoding=''

request_id = ''

 

# # Save the original standard output

# original_stdout = sys.stdout

# # Open a log file in append mode

# log_file = open('your_log_file.log', 'a')

# # Redirect standard output to the log file

# sys.stdout = log_file

 

def handle_json_rpc(message):

    try:

        global method

        global params

        global request_id

        global rpc_message

        global service_id

        global characteristic_id

        global rpc_message

        # Assuming 'message' is a JSON-formatted string

        json_message = json.loads(message)

 

        # Extracting relevant fields

        jsonrpc_version = json_message['jsonrpc'] if 'jsonrpc' in json_message else ''

        method = json_message['method'] if 'method' in json_message else ''

        request_id = json_message['id'] if 'id' in json_message else ''

 

        # params

        if 'params' in json_message:

           params = json_message.get('params', {})

           rpc_message = params['message'] if 'message' in params else ''

           service_id = params['serviceId'] if 'serviceId' in params else ''

           characteristic_id = params['characteristicId'] if 'characteristicId' in params else ''

        else:

            params = ''

            service_id = ''

            characteristic_id = ''

            rpc_message=''

       

        # # print("Encoding:", encoding)

        # print("Request ID:", request_id)

        # print("JSON-RPC Version:", jsonrpc_version)

        # print("Method:", method)

        # print("Service ID:", service_id)

        # print("Characteristic ID:", characteristic_id)

 

    except json.JSONDecodeError:

        print("Invalid JSON format:", message)

        # Perform further processing based on the extracted values

        # ...

def decode_base64(encoded_string):

    try:

        # Decoding the Base64-encoded string

        decoded_bytes = base64.b64decode(encoded_string)

       

        # Converting the bytes to a string

        decoded_string = decoded_bytes.decode('utf-8')

       

        return decoded_string

    except Exception as e:

        # Handle decoding errors, if any

        print(f"Error decoding Base64: {e}")

        return None

 

        # this._registerSensorOrMotor(4,WeDo2Device.MOTOR);

        # this._registerSensorOrMotor(5,WeDo2Device.MOTOR);

        # this._registerSensorOrMotor(6,WeDo2Device.DISTANCE);

 

async def receive_data_from_client(websocket):

    ATTACHED_IO = '00001527-1212-efde-1523-785feabcd123'

    LOW_VOLTAGE_ALERT = '00001528-1212-efde-1523-785feabcd123'

    INPUT_VALUES= '00001560-1212-efde-1523-785feabcd123'

    INPUT_COMMAND= '00001563-1212-efde-1523-785feabcd123'

    OUTPUT_COMMAND= '00001565-1212-efde-1523-785feabcd123'

    MOTOR= 1

    PIEZO= 22

    LED= 23

    TILT= 34

    DISTANCE= 35

    sensorDataArray = [5,6,77]

        # Create a JSON message

    json_message_DiscoverResponse = {

  "jsonrpc": "2.0",                  

  "method": "didDiscoverPeripheral",

  "params": {

    "peripheralId": 0xf005,          

    "name": "EV3",                  

    "rssi": -70,

    "serviceId":"00001523-1212-efde-1523-785feabcd123","characteristicId":"00001528-1212-efde-1523-785feabcd123"                      

  }

}

    json_message_ConnectResponse = {

  "jsonrpc": "2.0" ,

  "id": 1,          

  "result": {}  

}

 

    json_message_registerController =   {

  "jsonrpc": "2.0",                            

  "id": 2,                                    

  "method": "characteristicDidChange",              

  "params": {

    "serviceId": "battery_service",            

    "characteristicId": "battery_level_state",

    "message":"123",

    "encoding": "base64"                      

  }

}

    json_message_sensor =   {

  "jsonrpc": "2.0",                            

  "id": 2,                                    

  "method": "characteristicDidChange",              

  "params": {

    "serviceId": "battery_service",            

    "characteristicId": "battery_level_state",

    "message":"123",

    "encoding": "base64"                      

  }

}

    # Convert the JSON message to a string

    count = 0

    while True:

       

        try:

            global method

            global params

            global request_id

            global rpc_message

            global service_id

            global characteristic_id

            global rpc_message

            global bluetooth_communication

            # Receive data from the WebSocket connection

            data = await websocket.recv()

 

            handle_json_rpc(data)

           

           

            # # _id = data.get("method")

            # _method = parse_json_method(data)

            # _message = parse_json_message(data)

            # _idToSendBack = parse_json_id(data)

 

            print(method)

 

            if method == 'discover':

               

                json_string = json.dumps(json_message_DiscoverResponse)

            elif method == 'connect':

                print(f"Received data from client: {data}")

                json_string = json.dumps(json_message_ConnectResponse)

            # elif _id == "2":

            #     # time.sleep(0.100)

            #     # print (f"count :{count}")

            #     if(count == 0):

            #         print(f"Received data from client: {data}")

            #         json_string = json.dumps(json_message_startNotification_2) # passed

            elif method == 'write':

                print(f"Received data from client: {data}")

                print(base64.b64decode(rpc_message))

                bytearray = base64.b64decode(rpc_message)


                print(bytearray)

                bluetooth_communication.send_data((bytearray))

 

                print(f"data send to client : {json_string} ")

                json_string = json.dumps(json_message_ConnectResponse)

               

            elif method == "read":

                print(f"Received data from client: {data}")

                print(base64.b64decode(rpc_message))
                json_message_sensor["params"]["message"] = base64.b64encode(bytes(sensorDataArray)).decode('utf-8')
                print(f"data send to client : {json_message_sensor} ")
                json_string = json.dumps(json_message_sensor)

            # _method = data.get("method")

            else:

                json_string = json.dumps(json_message_ConnectResponse)

                pass

            # send data to Scratch blocks

            await websocket.send((json_string))#.encode('utf-8')))

        except websockets.ConnectionClosed:

            print("Connection closed by the client.")

            break

# Function to send data to the WebSocket every 20ms

async def send_data_to_client(websocket):

    json_message_sensor =   {

    "jsonrpc": "2.0",                            

    "id": 2,                                    

    "method": "characteristicDidChange",              

    "params": {

    "serviceId": "battery_service",            

    "characteristicId": "battery_level_state",

    "message":"123",

    "encoding": "base64"                      

    }

    }

    sensorDataArray = [5,6,77]

    sensorDataArray[2] = 0

    while True:

       

        try:

            # Your data to send

            # sensorDataArray[2] = 0

            json_message_sensor["params"]["message"] = base64.b64encode(bytes(sensorDataArray)).decode('utf-8')

            json_string = json.dumps(json_message_sensor)

            await websocket.send(json_string)

            sensorDataArray[2] = sensorDataArray[2] +1

            print(f"Sensor data sending to scratch : {sensorDataArray[2]}")

            await asyncio.sleep(0.500)  # Sleep for 20ms

 

        except websockets.exceptions.ConnectionClosed:

            print("Connection closed.")

            break

        except Exception as e:

            print(f"Error sending data: {e}")

            break

 

# web socket URL

# WEBSOCKET_URI = "ws://localhost:8765"

 

# async def websocket_handler(websocket, path):

#     try:

#         while True:

#             message = await websocket.recv()

#             print(f"Received: {message}")

#     except websockets.exceptions.ConnectionClosed:

#         print("Connection closed.")

 

async def on_connect(websocket, path):

    print(f"Client connected: {path}")

   

    # Start a task to send data to the client every 20ms

    send_task = asyncio.create_task(send_data_to_client(websocket))

   

    # Start a task to receive data from the client

    receive_task = asyncio.create_task(receive_data_from_client(websocket))

     # Wait for both tasks to finish

    await asyncio.gather(send_task, receive_task)

 

async def main(bluetooth_communication):

 

    server = await websockets.serve(on_connect, "localhost", 8765)

    await server.wait_closed()

 

if __name__ == "__main__":

        # Replace "HC-05" with the name of your Bluetooth device

    print("Connecting: Please Wait\n")

    bluetooth_communication.connect()

    print("Connection Successful\n")

    asyncio.run(main(bluetooth_communication))

 

    #     # To restore the standard output to the original value

    # sys.stdout = original_stdout

 

    # # Close the log file

    # log_file.close()

 

 