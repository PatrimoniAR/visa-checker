import requests
import time
from bs4 import BeautifulSoup
import os

# URL oficial del estado de los países
URL = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"

# Leer desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Mensaje Telegram enviado")
        else:
            print("❌ Error en Telegram:", response.text)
    except Exception as e:
        print(f"❌ Error Telegram: {e}")

def obtener_estado_spain():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                pais = cols[0].get_text(strip=True).lower()
                estado = cols[1].get_text(strip=True).lower()
                if 'spain' in pais:
                    return estado
        return None
    except Exception as e:
        print(f"❌ Error al obtener el estado: {e}")
        return None

def main():
    estado_prev = None
    while True:
        print("🔎 Verificando estado de Spain...")
        estado = obtener_estado_spain()

        if estado:
            print(f"📌 Estado actual: {estado}")
            if estado == "open" and estado != estado_prev:
                mensaje = "🇦🇺 ¡El estado de la visa Work and Holiday para España ahora está OPEN!"
                enviar_telegram(mensaje)
                break  # Puedes quitar esto si quieres que siga ejecutándose siempre
            estado_prev = estado
        else:
            print("⚠️ No se pudo obtener el estado.")

        time.sleep(600)  # Espera 10 minutos

if __name__ == "__main__":
    main()