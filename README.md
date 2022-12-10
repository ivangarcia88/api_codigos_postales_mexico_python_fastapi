API desarrollada en Python (FastAPI) para consultar colonia, municipio y estado sobre un código postal.

El archivo esta basada en la información provista por el sitio oficial:

[https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx](https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/CodigoPostal_Exportar.aspx)

Esta información fue transformada a un archivo JSON mediante un script, el código se encuentra en: 
https://github.com/ivangarcia88/api_codigos_postales_mexico

Para una mejor experiencia, se sugiere instalar venv o Anaconda (https://www.anaconda.com/) y crear un entorno virtual.

**Anaconda**

```plaintext
conda create -n mpostalcode python=3.10
conda activate mpostalcode
```
Los requerimentos se encuentran en el archivo _requirements.txt_ el cual se puede ejecutar de la siguiente manera

```plaintext
pip install -r requirements.txt
```
