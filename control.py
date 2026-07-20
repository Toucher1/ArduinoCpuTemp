import sys
import time

import serial
import wmi

# --- Настройки ---
ARDUINO_PORT = "COM5"      # Замените на ваш порт (например, COM3)
BAUD_RATE = 9600           # Должен совпадать со скетчем Arduino
UPDATE_INTERVAL = 1.0      # Как часто опрашивать датчик, секунды
RECONNECT_DELAY = 3.0      # Пауза перед повторным подключением, секунды


def connect_arduino(port, baud):
    """Открывает последовательное соединение и ждёт инициализации платы."""
    ser = serial.Serial(port, baud, timeout=1)
    time.sleep(2)  # Ожидание для инициализации Arduino (авто-reset при открытии порта)
    return ser


def get_cpu_temperature(wmi_conn):
    """
    Возвращает температуру процессора из Open Hardware Monitor
    или None, если подходящий сенсор не найден.
    """
    for sensor in wmi_conn.Sensor():
        if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
            return int(sensor.Value)
    return None


def main():
    # Подключение к WMI (namespace задаём как raw-строку из-за обратного слэша)
    try:
        wmi_conn = wmi.WMI(namespace=r"root\OpenHardwareMonitor")
    except wmi.x_wmi:
        print("Не удалось подключиться к Open Hardware Monitor.")
        print("Убедитесь, что программа запущена (openhardwaremonitor.org).")
        sys.exit(1)

    arduino = None
    try:
        while True:
            # Подключаемся к Arduino, если ещё не подключены
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
                # Плату отключили — закрываем порт и пробуем переподключиться
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
