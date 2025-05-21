# Clasificador de Gatos y Perros con Arduino

Este proyecto usa Flask y MobileNetV2 para identificar si una imagen contiene un gato o un perro, y envía la respuesta a un Arduino Uno vía puerto serial.

## ✅ Requisitos

- Python 3.8 o superior
- pip
- Arduino Uno
- Cable USB
- Servos (opcional)
- Puerto serial habilitado (Linux/macOS: `/dev/ttyUSB0`, Windows: `COMx`)

## 🔧 Instalación

1. Clona o descarga este repositorio.
2. Crea un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
