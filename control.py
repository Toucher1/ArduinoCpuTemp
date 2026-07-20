import sys
import time

import serial
import wmi

# настройки
ARDUINO_PORT = "COM5"      # свой порт сюда (COM3, COM4 ...)
BAUD_RATE = 9600           # так же, как в скетче
UPDATE_INTERVAL = 1.0      # раз в сколько секунд читаем температуру
RECONNECT_DELAY = 3.0      # сколько ждать перед новой попыткой подключиться


def connect_arduino(port, baud):
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(2)  # плата ресетится при открытии порта, даём ей очухаться
    return ser


def get_cpu_temperature(wmi_conn):
    # ищем сенсор температуры CPU, если нет - вернём None
    for sensor in wmi_conn.Sensor():
        if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
            return int(sensor.Value)
    return None


def main():
    # namespace через raw-строку, иначе \O ломается
    try:
        wmi_conn = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
    except wmi.x_wmi:
        print("Не удалось подключиться к Open Hardware Monitor.")
        print("Убедитесь, что программа запущена (openhardwaremonitor.org).")
        sys.exit(1)

    arduino = None
    try:
        while True:
            # ещё не подключены - пробуем
            if arduino is None:
                try:
                    arduino = connect_arduino(ARDUINO_PORT, BAUD_RATE)
                    print(f"Подключено к {ARDUINO_PORT} на {BAUD_RATE} бод.")
                except serial.SerialException as e:
                    print(f"Не удалось открыть {ARDUINO_PORT}: {e}")
                    print(f"Повтор через {RECONNECT_DELAY} с...")
                    time.sleep(RECONNECT_DELAY)
                    continue

            temp = get_cpu_temperature(wmi_conn)
            if temp is None:
                print("Сенсор температуры CPU не найден, пропускаю итерацию.")
                time.sleep(UPDATE_INTERVAL)
                continue

            print(f"CPU Temperature: {temp}°C")
            try:
                arduino.write(f"{temp}\n".encode())
            except serial.SerialException as e:
                # выдернули плату - роняем порт и идём на переподключение
                print(f"Потеряно соединение с Arduino: {e}")
                arduino.close()
                arduino = None
                continue

            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
    finally:
        if arduino is not None and arduino.is_open:
            arduino.close()


if __name__ == "__main__":
    main()
