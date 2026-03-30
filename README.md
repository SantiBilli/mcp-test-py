# 📂 MCP Server: Gestión de OneDrive para IA

Este proyecto es un servidor **MCP (Model Context Protocol)** que permite a asistentes de inteligencia artificial (como ChatGPT, Copilot o Claude) gestionar archivos en tu **OneDrive** de forma automática. 

Imagina que puedes decirle a la IA: *"Crea un archivo de configuración para mi nueva app en OneDrive"* y la IA lo hace por ti usando este servidor.

---

## 🌟 ¿Qué hace este servidor?

Este servidor actúa como un "traductor" entre la IA y la API de Microsoft. Expone herramientas específicas que la IA puede "ver" y "usar" para:
1.  **Crear** archivos JSON en una carpeta específica (`AutoClickFiles`).
2.  **Modificar** datos dentro de esos archivos.
3.  **Eliminar** archivos cuando ya no sean necesarios.

---

## 🛠️ Tecnologías Usadas

-   **[Python](https://www.python.org/)**: El motor del servidor.
-   **[Microsoft Graph API](https://developer.microsoft.com/en-us/graph)**: La interfaz oficial de Microsoft para interactuar con OneDrive.
-   **[Starlette](https://www.starlette.io/) & [Uvicorn](https://www.uvicorn.org/)**: Tecnologías para que el servidor sea rápido y pueda recibir peticiones por internet o localmente.
-   **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Para manejar de forma segura tus llaves de acceso (tokens).

---

## 🔐 Configuración (Lo que necesitas)

Para que el servidor funcione, necesita permiso para hablar con tu cuenta de Microsoft. Estos datos se guardan en un archivo secreto llamado `.env`:

1.  **MICROSOFT_CLIENT_ID**: El ID de tu aplicación registrada en Azure.
2.  **MICROSOFT_CLIENT_SECRET**: La contraseña secreta de esa aplicación.
3.  **MICROSOFT_REFRESH_TOKEN**: Una llave especial que permite al servidor generar accesos temporales sin que tengas que iniciar sesión cada vez.

---

## 🧰 Herramientas Disponibles (Tools)

Cuando conectas este servidor a una IA, ella tendrá estos "superpoderes":

### 1. `create_json_onedrive`
-   **Uso**: Crea un archivo `.json` nuevo.
-   **Qué pide**: El nombre del archivo y los datos iniciales (un objeto JSON).
-   **Ubicación**: Siempre los guarda en la carpeta `/AutoClickFiles/` de tu OneDrive.

### 2. `modify_json_onedrive`
-   **Uso**: Cambia un valor específico dentro de un archivo que ya existe.
-   **Qué pide**: Nombre del archivo, la "llave" (nombre del dato) y el nuevo "valor".

### 3. `delete_json_onedrive`
-   **Uso**: Borra un archivo permanentemente.
-   **Qué pide**: El nombre del archivo a eliminar.

---

## 🚀 Cómo ponerlo en marcha

### 1. Instalar dependencias
Asegúrate de tener las librerías necesarias:
```bash
pip install starlette uvicorn httpx python-dotenv
```

### 2. Arrancar el servidor
Ejecuta el servidor para que empiece a escuchar peticiones:
```bash
python server.py
```
*El servidor se iniciará usualmente en `http://localhost:8000`.*

---

## 🧪 Pruebas (test_client.py)

Para verificar que todo funciona bien sin usar una IA real todavía, puedes usar el cliente de prueba:
```bash
python test_client.py
```
Este script intentará conectarse al servidor, listar las herramientas disponibles y confirmar que la comunicación es exitosa.

---

## 💡 Notas para principiantes
-   **MCP** es un estándar: Significa que si este servidor sigue las reglas de MCP, cualquier IA que entienda MCP podrá usarlo.
-   **Tokens**: Si el servidor imprime "Error de Microsoft", probablemente el `REFRESH_TOKEN` haya expirado o sea incorrecto.
-   **Seguridad**: Nunca compartas tu archivo `.env` con nadie, ya que contiene las llaves de tu OneDrive.
