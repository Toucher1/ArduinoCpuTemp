import serial
import time
import wmi

# Настройка последовательного соединения с Arduino
arduino_port = "COM5"  # Замените на ваш порт
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Ожидание для инициализации Arduino

# Подключение к WMI
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def get_cpu_temperature():
    """
    Получает температуру процессора из Open Hardware Monitor.
    """
    sensors = w.Sensor()  # Получаем все сенсоры
    for sensor in sensors:
        if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
            return int(sensor.Value)  # Возвращаем температуру в виде целого числа
    return 50  # Если данные недоступны, возвращаем 50 как значение по умолчанию

try:
    while True:
        temp = get_cpu_temperature()
        print(f"CPU Temperature: {temp}°C")
        arduino.write(f"{temp}\n".encode())  # Отправляем температуру на Arduino
        time.sleep(30)  # Задержка 30 секунд перед следующей проверкой
except KeyboardInterrupt:
    print("Программа завершена.")
    arduino.close()