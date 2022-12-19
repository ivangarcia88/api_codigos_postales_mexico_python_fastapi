# Introducción

API desarrollada en Python (FastAPI) para consultar colonia, municipio y estado sobre un código postal.

**Ejemplo del funcionamiento de la API** 
> Sometimes it takes like 30 seconds to wake up the API.

[https://apicodigospostalesmexico-production.up.railway.app/code/45070]( https://codigos-postales-fastapi.onrender.com/code/45070)

**Documentación de los endpoints**

[https://codigos-postales-fastapi.onrender.com/docs](https://codigos-postales-fastapi.onrender.com/docs)

**Esta API emplea información provista por el sitio oficial:**

[https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx)

La información fue transformada a un archivo JSON mediante un script, el código para este proceso se encuentra en: 

[https://github.com/ivangarcia88/mexican_postal_code_reformat](https://github.com/ivangarcia88/mexican_postal_code_reformat)


# Instalación

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
