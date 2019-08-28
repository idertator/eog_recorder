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

### Instalación completa en Ubuntu 18.04

Lo primero es instalar todos los paquetes requeridos por el proceso de instalación. Para ello ejecutamos el siguiente comando:

```shell
$ sudo apt-get install git python3.7 python3-distutils qt5dxcb-plugin
```

Una vez instalados los requrimientos, necesitamos instalar algunos paquetes base de python:

```shell
$ wget https://files.pythonhosted.org/packages/d9/ca/7279974e489e8b65003fe618a1a741d6350227fa2bf48d16be76c7422423/setuptools-41.2.0.zip
$ unzip setuptools-41.2.0.zip
$ cd setuptools-41.2.0
$ python3.7 setup.py install --user
$ cd ..
$ wget https://files.pythonhosted.org/packages/00/9e/4c83a0950d8bdec0b4ca72afd2f9cea92d08eb7c1a768363f2ea458d08b4/pip-19.2.3.tar.gz
$ tar xvf pip-19.2.3.tar.gz
$ cd pip-19.2.3
$ python3.7 setup.py install --user
$ cd ..
$ rm -rf setuptools* pip*
```

Luego creamos las carpetas donde vamos a poner el instalador y clonamos el código fuente. En este paso hemos asumido que ya se
ha configurado la llave SSH en el GitHub.

```shell
$ mkdir ~/Development
$ cd ~/Development
$ git clone git@github.com:rdlfgrcwork/saccrec.git
```

Por último instalamos los requerimientos de ejecución del App:

```shell
$ export PATH=~/.local/bin:$PATH
$ pip3.7 install -r saccrec/requirements.txt --user
$ cd saccrec
$ python3.7 setup.py install --user
```

Para ejecutar la aplicación ya solo tendríamos que llamar el script principal:

```shell
$ SaccRec.py
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
