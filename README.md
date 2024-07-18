# MercadoLibreScrapping

Aplicación de consola que permite extraer N cantidad de URL de la búsqueda de productos en MercadoLibre, y posteriormente extraer los datos de cada uno de los productos, exportándolos en un archivo .csv.

## Características

- Especificar los XPath de las secciones que se quieren extraer.
- Extraer las tablas completas de la sección de "Ver más características".

## Requisitos

- Python 3.x
- BeautifulSoup
- lxml
- Requests
- Selenium
- Webdriver manager
## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/FrancoYudica/MercadoLibreScrapping.git
    cd MercadoLibreScrapping
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Asegúrate de tener el driver de Chrome para Selenium:
    - Descárgalo desde [ChromeDriver](https://sites.google.com/chromium.org/driver).
    - Colócalo en tu PATH o en la carpeta del proyecto.

## Uso

### Argumentos de la Línea de Comandos

- `--table`: Incluye esta bandera para extraer las tablas de características.
- `--show_browser`: Incluye esta bandera para mostrar la interfaz del navegador durante el scraping.
- `--xpaths_file`: Especifica la ruta al archivo JSON que contiene los XPath nombrados.
- `--images`: Especifica la cantidad de URL de imágenes extraidas de la página de producto.

### Ejecución

1. Ejecuta el script principal:

    ```bash
    python main.py --xpaths path/to/NamedXPaths.json
    ```

2. Ingresa el término de búsqueda y la cantidad de productos que deseas extraer:

    ```text
    Search in mercado libre: Volkswagen Amarok 3.0 V6
    How many products do you want to search?: 10
    ```
3. El resultado, archivo .csv, será almacenado en la carpeta `output`


## NamedXPaths
El archivo NamedXPaths.json debe contener los XPath que deseas extraer en un formato de diccionario JSON. Ejemplo:

```
{
    "Titulo": "//*[@id=\"ui-pdp-main-container\"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1",
    "Precio": "//*[@id=\"ui-pdp-main-container\"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[1]/span/span/span[2]"
}
```
## Notas

- Asegúrate de que el archivo `NamedXPaths.json` tenga los XPath correctos según la estructura de la página de MercadoLibre.
- Si la página carga <b>contenido dinámico</b>, puede que necesites ajustar los tiempos de espera en el script para asegurar que todos los elementos se hayan cargado correctamente antes de intentar extraer los datos.
- Existen componentes, como las tablas de `"ver más características"` que se pueden acceder luego de apretar botones. En estos casos hay que usar selenium, simulando la interacción con un usuario real. El contenido de las tablas se carga dinámicamente, y por este motivo no basta con agregar el XPath de estos componentes.