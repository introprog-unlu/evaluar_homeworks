# Script para obtener las calificaciones de los assignaments

clonar el repositorio y 
dirigirse a la raiz del proyecto

```bash

git clone https://github.com/introprog-unlu/evaluar_homeworks.git evaluador_hw

cd evaluador_hw

```

copiar el env de ejemplo y completar con los path requeridos, per defecto se encuenran los del año 2021

```bash

cp .enc.example .env

```

```bash

pip3 install -r requirements.txt

```


```bash

python3 runtest.py -i /path/origen/assignaments/ -o path/destino/resultados

```