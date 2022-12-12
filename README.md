> API desarrollada en Python (FastAPI) para consultar colonia, municipio y estado sobre un código postal.

**Ejemplo del funcionamiento de la API**

https://codigos-postales-fastapi.onrender.com/code/45070

**Documentación de los endpoints**

https://codigos-postales-fastapi.onrender.com/docs



Esta API emplea información provista por el sitio oficial:

[https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx)

Esta información fue transformada a un archivo JSON mediante un script, el código para transformar y actualizar la base de datos se encuentra en: 
https://github.com/ivangarcia88/api_codigos_postales_mexico



Para una mejor experiencia, se sugiere instalar venv o Anaconda (https://www.anaconda.com/) y crear un entorno virtual.

**Anaconda**

```plaintext
conda create -n apipostalcode python=3.10
conda activate apipostalcode
```
Los requerimentos se encuentran en el archivo _requirements.txt_ el cual se puede ejecutar de la siguiente manera

```plaintext
pip install -r requirements.txt
```

Para iniciar el servicio, se recomienda emplear uvicorn

```plaintext
uvicorn main:app --reload
```
