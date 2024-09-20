import serial
import time

def connect_serial(port, baudrate=9600, timeout=1):
    try:
        # Establish connection to the specified serial port
        ser = serial.Serial(port, baudrate, timeout=timeout)
        
        # Wait for the connection to be established
        time.sleep(2)  # Optional, depends on device boot time
        
        # Check if the port is open
        if ser.is_open:
            print(f"Connected to {port} at baudrate {baudrate}")
        else:
            print(f"Failed to connect to {port}")
        return ser
    
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def close_serial(ser):
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")
    else:
        print("No active serial connection to close.")
        
def main():
    # Specify the COM port and baud rate
    port = 'COM10'  # Update this to match your port, e.g., 'COM3' for Windows or '/dev/ttyUSB0' for Linux
    baudrate = 9600
    
    # Establish connection
    ser = connect_serial(port, baudrate)
    
    if ser:
        try:
            # Sending the 'color' command to the device
            command = 'level\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            time.sleep(2)  # Increase the delay if necessary
            
            command = 'read\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            
            command = 'level 21000\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            
            command = 'level\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            time.sleep(2)  # Increase the delay if necessary
            
            command = 'version\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            time.sleep(2)  # Increase the delay if necessary
            
            command = 'sn\r\n'  # Ensure this is correct format for the device
            ser.write(command.encode())  # Send command as bytes
            print(f"Sent command: {command.strip()}")
            time.sleep(2)  # Increase the delay if necessary
            
            # Wait for a longer time to ensure the device has time to respond
            time.sleep(2)  # Increase the delay if necessary
            
            # Reading the response from the device, if available
            bytes_available = ser.in_waiting
            print(f"Bytes available to read: {bytes_available}")
            
            if bytes_available > 0:
                response = ser.read(bytes_available).decode('utf-8')
                print(f"Received from device: {response}")
            else:
                print("No response from device.")
            
        
        finally:
            # Close the serial port connection when done
            close_serial(ser)

if __name__ == "__main__":
    main()
