
# Prueba Destacame - Jorge Poveda



## Breve explicacion

se desarrollaron 3 tipos de roles:

- admin (permite crear los viajes,rutas,agregar seller o drivers, buses)
- seller (encargado de vender los puestos a cada pasajero)
- driver (solo ve sus rutas asignadas)
- pasajero - sin rol ( pagina inicial solo permite ver con la identificacion los tiquetes comprados)

/home pagina principal

/login acceso a cada uno de los roles
## Vesiones 

**Front:** Vue.js v2, node v16

**Backend:** python3.9, django v4.1

**DataBase:** Postgres:13


## Instalaccion

Instalacion manual usar python3.9

Backend 
- Lista de comandos
```bash
  cd api
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  python3 manager.py migrate
  python3 manager.py runserver 0.0.0.0:8000
```

Frontend
```bash
  cd app
  yarn install o npm install
  yarn dev o npm run dev
```
Ingresar a http://localhost:8080

Fontend
```bash
  python3 -m venv venv
  pip3 install -r requirements.txt
  python3 manager.py migrate
  python3 manager.py runserver 0.0.0.0:8000
  cd my-project
```


## Instalaccion Docker

Inicializacion con dockers en la raiz del proyecto ejecutar

```bash
  docker-compose up -d --build
```

Este comando deberia permitir ya el ingreso a toda la prueba

- Endpoint front: http://localhost:8080
- Endpoint backen: http://localhost:8000

pero para evitar algunos posibles errores ejecutar los siguientes comandos:

```bash
  docker-compose exec api python3 manage.py migrate
  docker-compose exec api python3 manage.py loaddata data.json
```

credenciales de admin: {
  email: "admin@destacame.com",
  password: "dddd"
}
- Conexion a bd http://localhost:5432
- docs swager para ver todos los endpoint de forma facil (falta esquemas), http://localhost:8000/docs/

## Tests



```bash
  docker-compose exec api python3 manage.py test
```

