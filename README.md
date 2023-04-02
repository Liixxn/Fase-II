
<h1 align="center"><b><i>💧DROPLET💧</i></b></h1>

<p align="center"><b>Aplicación de gestión de centrales hidroeléctricas en PyQt5.</b></p>

Esta aplicación está diseñada para ayudar en la gestión de centrales hidroeléctricas mediante una interfaz gráfica de usuario construida con PyQt5.

El objetivo del proyecto es crear un sistema que, dado valores climatológicos, pueda predecir los niveles de agua en los embalses en diferentes días. 
Se busca facilitar y garantizar la gestión de los embalses mediante la utilización de esta información.

La aplicación, se encuentra diseñada bajo el concepto de “dashboard” o “panel de control”, herramienta de gestión de la información que monitoriza, analiza y muestra de manera visual métricas sobre las distintas presas. 
Cuenta con diferentes pestañas: una pestaña principal que da la bienvenida al usuario, y tres pestañas con el nombre correspondiente a su algoritmo.
El logo de Droplet es el siguiente:
<div align="center">
  <img src="faseII_BlackHats/Droplet_icon.png" width="100" height="100">
</div>

<hr>

<h2>Lenguajes y herramientas usadas</h2>

<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/></a>
<a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"><a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" width="40" height="40"/> </a>
<a href="https://numpy.org" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" alt="Numpy" width="40" height="40"/> </a>
<a href="https://riverbankcomputing.com/software/pyqt/intro" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Python_and_Qt.svg" alt="PyQt" width="40" height="40"/> </a>
<a href="https://jupyter.org" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" alt="Jupyter Notebook" width="40" height="40"/> </a>
<a href="https://www.jetbrains.com/es-es/pycharm/" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" alt="PyCharm" width="40" height="40"/> </a>
<a href="https://www.docker.com" target="_blank" rel="noreferrer"><img src="https://1000logos.net/wp-content/uploads/2021/11/Docker-Logo-2013.png" alt="Docker" width="40" height="40"/> </a>

<hr>

<h2>Instalación</h2>

<p>Droplet hace uso de difernetes librerías para su correcto funcionamiento, por lo que debe tener instalado 'pip' para descargar todos los componentes. Si no tiene pip
puede instalárselo con el siguiente comando en una terminal.</p>

```
pyhton get-pip.py
```

<p>A continuación, navegue desde la terminal hasta la ruta en la que se encuentre el proyecto. Uno de los ficheros que se encuentra denominado, 
<i>requirements.txt</i> contiene todas las librerías que Droplet necesita. Instálelas con el siguiente comando:</p>

```
pip install -r requirements.txt
```

<p>Tras la finalización de las diversas instalaciones, solo tiene que ejecutar el fichero principal <b>pyqt5.py</b> y ya podrá disfrutar de todas las 
funcionalidades que ofrece la aplicación.</p>

<hr>

<h2>Ficheros de interés</h2>
<p>Se van a explicar de una forma breve, los diferentes ficheros, carpetas etc. que conforman el proyecto, para un mayor entendimiento del funcionamiento y desarrollo
de Droplet.</p>

<h3 align="center">📑Ficheros📑</h3>

<ul>
  <li><b><i>pyqt5.py</i></b>: el fichero principal de la aplicación, dónde se inicializan todas las ventanas y gestiona las diferentes funcionalidades.</li>
  <li><b><i>[nombre].ui</i></b>: archivos que representan los diseños para la interfaz de Droplet, estos ficheros son generados por la aplicación de diseño QT Designer.</li>
  <li><b><i>resource.qrc</i></b>: fichero generado por la aplicación de diseño QT Designer, que guarda las imágenes o iconos utilizados en el diseño.</li>
  <li><b><i>index.qss</i></b>: archivo igual a una hoja de estilos, pero para elementos PYQT.</li>
  <li><b><i>data.py</i></b>: fichero que gestiona los datos necesitados para el correcto funcionamiento de la aplicación, además de realizar un preprocesamiento
  de éstos.</li>
  <li><b><i>aemet_predictions.py</i></b>: archivo que entrena cada modelo con las variables correspondientes y genera las predicciones para la presa elegida.</li>
</ul>

<h4 align="center">🗂Carpetas🗂</h4>

<ul>
  <li><b><i>data</i></b>: carpeta que guarda los diferentes archivos con la información que Droplet procesa.</li>
</ul>
