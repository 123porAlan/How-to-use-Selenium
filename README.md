# 📈 Yahoo Finance Scraper con Selenium

Este proyecto es un script de automatización en Python que utiliza **Selenium WebDriver** para navegar en Yahoo Finance, buscar una acción bursátil específica (por defecto "Apple") y extraer sus datos financieros en tiempo real.

## 📋 Tabla de Contenidos

* [Descripción General](https://www.google.com/search?q=%23descripci%C3%B3n-general)
* [Requisitos Previos](https://www.google.com/search?q=%23requisitos-previos)
* [Instalación](https://www.google.com/search?q=%23instalaci%C3%B3n)
* [Cómo Funciona (Explicación del Código)](https://www.google.com/search?q=%23c%C3%B3mo-funciona-explicaci%C3%B3n-del-c%C3%B3digo)
* [Notas Importantes](https://www.google.com/search?q=%23notas-importantes)

## 📝 Descripción General

El script emula a un usuario humano realizando las siguientes acciones:

1. Abre un navegador Chrome controlado por software.
2. Entra a `es.finance.yahoo.com`.
3. Acepta las cookies automáticamente.
4. Busca el símbolo bursátil (Ticker) de una empresa (ej. AAPL).
5. Espera dinámicamente a que carguen los resultados.
6. Extrae ("scrapea") el precio actual y la tabla de datos fundamentales (Cierre anterior, rango diario, etc.).

## 🛠️ Requisitos Previos

* **Python 3.x** instalado.
* **Google Chrome** actualizado.
* **ChromeDriver**: El ejecutable debe coincidir con tu versión de Chrome y estar en la misma carpeta que el script (o en el PATH del sistema).

## 🚀 Instalación

1. Clona este repositorio o descarga el archivo `.py`.
2. Instala la librería necesaria:
```bash
pip install selenium

```


3. Ejecuta el script:
```bash
python scraper_yahoo.py

```



## 🧠 Cómo Funciona (Explicación del Código)

El código se divide en 4 bloques lógicos principales:

### 1. Configuración del Driver (`webdriver`)

```python
s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

```

* **Qué hace:** Crea la instancia del navegador. Es el "robot" que controlaremos.
* **Detalle:** `Service` gestiona el ejecutable del driver. `maximize_window()` asegura que todos los elementos sean visibles (algunas webs ocultan menús si la ventana es pequeña).

### 2. Gestión de Navegación y Cookies

```python
driver.get("https://es.finance.yahoo.com")
driver.find_element(By.NAME, "agree").click()

```

* **Qué hace:** Carga la URL y gestiona el pop-up de consentimiento de privacidad.
* **Lógica:** Usa `By.NAME` para encontrar el botón de "Aceptar". Se envuelve en un `try/except` por si Yahoo decide no mostrar el pop-up esa vez, evitando que el script se rompa.

### 3. Interacción con el Buscador

```python
busqueda.send_keys("AAPL")
boton.click()

```

* **Qué hace:** Simula el teclado y el mouse.
* **Lógica:**
* `find_element(By.ID, ...)`: Localiza la barra de búsqueda (el ID es único y el método más seguro).
* `send_keys(...)`: Escribe texto en el input.
* `click()`: Presiona la lupa para buscar.



### 4. Esperas Explícitas y Scraping (`WebDriverWait`)

Esta es la parte más crítica para la estabilidad del bot.

```python
WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))

```

* **Por qué se usa:** Las páginas modernas (SPA) cargan datos con JavaScript asíncrono. Si el script busca el precio *inmediatamente* después de hacer click, fallará porque el dato aún no existe en el DOM.
* **Cómo funciona:** Le dice al driver: *"Espera hasta 10 segundos, pero si el elemento aparece antes, continúa inmediatamente"*.

### 5. Extracción de Listas (`find_elements`)

```python
campos = driver.find_elements(By.CLASS_NAME, "...")

```

* **Diferencia clave:** `find_element` devuelve un objeto (el primero que encuentra). `find_elements` (plural) devuelve una **lista** de todos los objetos que coinciden.
* **Uso:** Se usa para "barrer" toda la tabla de datos financieros. Luego, con un ciclo `for`, unimos la etiqueta (ej. "Apertura") con su valor (ej. "150.45").

## ⚠️ Notas Importantes

* **Selectores Dinámicos:** Los sitios web cambian sus `ID` y `Class` frecuentemente. Si el script falla, debes inspeccionar la web (F12) y actualizar las constantes en el código.
* **Anti-Scraping:** Yahoo Finance permite el scraping moderado, pero si realizas miles de peticiones rápidas, tu IP podría ser bloqueada.
