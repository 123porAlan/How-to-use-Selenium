from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# --- CONFIGURACIÓN INICIAL ---
# Se define el servicio apuntando al ejecutable del driver (debe estar en la misma carpeta)
s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Maximizar ventana para ver todos los elementos correctamente
driver.maximize_window()

# --- 1. NAVEGACIÓN Y COOKIES ---
# Accedemos a Yahoo Finance España
driver.get("https://es.finance.yahoo.com")

# Localizar y clicar el botón de "Aceptar todo" (Cookies)
# El tutorial usa el atributo 'name' que es "agree"
try:
    boton_aceptar_cookies = driver.find_element(By.NAME, "agree")
    boton_aceptar_cookies.click()
except:
    print("No se encontró el botón de cookies o ya fue aceptado.")

# Espera breve para asegurar que la página cargue tras las cookies
sleep(2)

# --- 2. BÚSQUEDA DE ACCIONES (Ej: Apple) ---
# NOTA IMPORTANTE: En el video, el autor inspecciona la página (Click derecho -> Inspeccionar) 
# para copiar los IDs. Estos IDs suelen ser códigos como 'ybar-sbq'.
# Debes inspeccionar tu navegador y reemplazar 'TU_ID_AQUI' con el ID real.

try:
    # Localizar la barra de búsqueda por ID
    id_barra_busqueda = "TU_ID_DE_LA_BARRA_DE_BUSQUEDA" # Reemplazar con el ID copiado del navegador
    busqueda_acciones = driver.find_element(By.ID, id_barra_busqueda)
    
    # Escribir el símbolo de la acción (AAPL para Apple)
    busqueda_acciones.send_keys("AAPL")
    
    # Localizar y clicar el botón de búsqueda (la lupa)
    id_boton_buscar = "TU_ID_DEL_BOTON_BUSCAR" # Reemplazar con el ID copiado del navegador
    boton_busqueda_acciones = driver.find_element(By.ID, id_boton_buscar)
    boton_busqueda_acciones.click()
    
except Exception as e:
    print(f"Error en la búsqueda (revisa los IDs): {e}")

# --- 3. EXTRACCIÓN DE DATOS (SCRAPING) ---
# Esperamos explícitamente a que cargue el precio para evitar errores
# El tutorial usa WebDriverWait para elementos dinámicos

try:
    # Esperar hasta 10 segundos a que el elemento del precio sea visible
    # Se usa un selector CSS. En el video usa algo como 'fin-streamer[data-test="qsp-price"]'
    # Debes inspeccionar el precio y copiar el selector o el atributo data-test.
    selector_precio = 'fin-streamer[data-field="regularMarketPrice"]' # Ejemplo común en Yahoo Finance
    
    elemento_precio = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector_precio))
    )
    
    print(f"Precio actual de la acción: {elemento_precio.text}")

    # --- EXTRACCIÓN DE TABLA DE DATOS (Múltiples elementos) ---
    # El tutorial busca extraer los pares "Campo: Valor" (ej. Cierre anterior: 150.00)
    
    # 1. Encontrar todos los títulos/etiquetas (usando su clase común)
    # Debes copiar la clase del elemento 'span' o 'td' de la izquierda en la tabla
    clase_titulos = "CLASE_COPIADA_DEL_INSPECTOR" 
    campos_de_datos = driver.find_elements(By.CSS_SELECTOR, f"span.{clase_titulos}") # O By.CLASS_NAME
    
    # 2. Encontrar todos los valores (usando su clase común)
    # Debes copiar la clase del elemento de la derecha en la tabla
    clase_valores = "CLASE_COPIADA_DEL_INSPECTOR"
    campos_resultados = driver.find_elements(By.CLASS_NAME, clase_valores)
    
    # Bucle para imprimir los pares juntos
    print("\n--- Datos de la Acción ---")
    for indice, campo in enumerate(campos_de_datos):
        # Imprimimos el texto del título
        titulo = campo.text
        
        # Verificamos que exista un valor correspondiente para ese índice
        if indice < len(campos_resultados):
            valor = campos_resultados[indice].text
            print(f"{indice} - {titulo}: {valor}")

except Exception as e:
    print(f"Error en la extracción de datos: {e}")

# Pausa final antes de cerrar
sleep(10)
driver.quit()
