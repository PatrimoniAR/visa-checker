import requests
from bs4 import BeautifulSoup
import os

# URL oficial del estado de los países
URL = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"

# Leer desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS")

def enviar_telegram(mensaje):
    if not TELEGRAM_CHAT_IDS:
        print("⚠️ No hay chat_ids configurados.")
        return

    chat_ids = [chat_id.strip() for chat_id in TELEGRAM_CHAT_IDS.split(",")]
    
    for chat_id in chat_ids:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {"chat_id": chat_id, "text": mensaje}
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Mensaje enviado a {chat_id}")
            else:
                print(f"❌ Error al enviar a {chat_id}: {response.text}")
        except Exception as e:
            print(f"❌ Excepción para {chat_id}: {e}")

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
    print("🔎 Verificando estado de Spain...")
    estado = obtener_estado_spain()

    if estado:
        print(f"📌 Estado actual (raw): {repr(estado)}")
        estado_limpio = estado.encode('ascii', 'ignore').decode().strip().lower()
        if estado_limpio == "open":
            mensaje = "🇦🇺 ¡El estado de la visa Work and Holiday para España está OPEN!"
            enviar_telegram(mensaje)
        else:
            print(f"ℹ️ Estado detectado, pero no es 'OPEN': {estado_limpio}")
    else:
        print("⚠️ No se pudo obtener el estado.")



if __name__ == "__main__":
    main()
