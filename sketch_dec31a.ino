#define LED1 3  // зелёный, всё ок
#define LED2 4  // жёлтый, греется
#define LED3 5  // красный, жарко

// пороги, °C. ниже WARN - зелёный, до HOT - жёлтый, дальше красный
#define TEMP_WARN 56
#define TEMP_HOT  70

int lastTemp = -1; // -1 пока ничего не пришло

void setLeds(bool green, bool yellow, bool red) {
  digitalWrite(LED1, green ? HIGH : LOW);
  digitalWrite(LED2, yellow ? HIGH : LOW);
  digitalWrite(LED3, red ? HIGH : LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  setLeds(false, false, false); // на старте гасим всё
}

void loop() {
  if (Serial.available() > 0) {
    int temp = Serial.parseInt();

    // parseInt на таймауте/мусоре даёт 0, такое пропускаем
    if (temp <= 0) {
      return;
    }

    // дёргаем светодиоды только если число реально поменялось
    if (temp != lastTemp) {
      lastTemp = temp;

      if (temp < TEMP_WARN) {
        setLeds(true, false, false);
      } else if (temp < TEMP_HOT) {
        setLeds(false, true, false);
      } else {
        setLeds(false, false, true);
      }
    }
  }
}