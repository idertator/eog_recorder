# saccrec
Registro de señales sacádicas mediante la utilización del OpenBCI

## Requerimientos

- [Python](https://www.python.org/downloads/) >= 3.7
- [PyQt5](https://pypi.org/project/PyQt5/) >= 5.12.1
- [openbci-interface](https://pypi.org/project/openbci-interface/) >= 0.8.0

## Instrucciones de instalación

Teniendo todos los requerimientos instalados debería ser tan simple como ejecutar:

```shell
$ python setup.py install
```

Luego se ejecuta:

```shell
$ ./SaccRec.py
```

## Instrucciones para desarrollar

Lo primero que hay es que crear el entorno con los requerimientos utilizando el siguiente comando estando en la carpeta raíz del proyecto:

```shell
$ pipenv install
```

Luego activamos el ambiente con:

```shell
$ pipenv shell
```

Si es la primera vez que preparamos el ambiente para desarrollo debemos ejecutar el siguiente comando:

```shell
$ python setup.py develop
```

Por último para ejecutar el programa:

```shell
$ ./SaccRec.py
```
