# Patrón Poderoso

#### Version de python sugerida v3.11
```bash
python --version
```


#### Instalar requerimientos
```bash
pip install -r requirements.txt
```

#### Ejecutar el proyecto

```bash
python index.py 4h
```
- donde 4h es el intervalo de tiempo, puede ser 5m, 4h, etc...

#### Importante
- Si al instalar TA-lib les da error fijarse si tienen las dependencias necesarias que indica https://pypi.org/project/TA-Lib/


#### Funcionamiento
- Al iniciar busca los pares con USDT
- y muestra en pantalla los posibles patrones poderosos 
- luego espera 1 minuto y vuelve a repetir el ciclo.
- para salir del programa presionar Ctrl + C