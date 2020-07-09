# Scrapper
Esta pequeña librería hace scrapping de la pagina de diputados para obtener la información referente a las asignaciones
parlamentarias y su detalle. El objetivo final sería realizar una recopilación centralizada y ordenada de todos los datos de transparencia que están a disposición en la pagina de la camara de diputados. 

## Motivación
Actualmente la Transparencia realizada por la camara de diputados parece ser que es para decir: "Somos transparentes porque subimos una tablita con números todos los meses". Lo que no se menciona es que hacer analisis de estos datos resulta casi tan dificil como encontrar un parlamentario no tan corrupto. Por lo que con esta herramienta buscamos agilizar un poco ese proceso de recopilación de datos para el que este interesado en saber en que se gasta el dinero de los contribuyentes (aló periodistas? aló ciudadania? aló comisiones fiscalizadoras?)

## Funcionamiento
Por el momento para obtener la información de las asignaciones se hace Scrapping utilizando Selenium. La razón de esto es que los cambios de inputs(fecha y año) hacen trigger de una tabla dinamica la cual no es sencilla de replicar utilizando HTTP requests y capturando el HTML de respuesta. Utilizando Selenium se simula el cambio de fecha y el HTML se parsea utilizando BeautifulSoup. 

Por el momento Selenium abre secuencialmente (una por una) las paginas de las tablas de asignaciones por diputados, cambia la fecha y espera un momento para extraer el HTML de respuesta, se podrá imaginar que extraer las tablas de asignaciones mensuales de los años 2018, 2019 y 2020 de los 155 honorables toma un tiempo razonable (35 minutos aproximadamente....We can do a lot better than that!!)

### Posibles soluciones a esto:
- Abrir multiples tabs en el Browser que abre Selenium para extraer los datos de múltiples honorables al mismo tiempo
- Lanzar una lambda function en amazon parametrizada según el nombre del honorable a extraer y paralelizar esto 155 (o menos) veces (Entretenido pero potencialmente caro(?)) Como funcionaría Selenium en ese caso?
- Encontrar la forma de actualizar la tabla simulando algún request (se ve dificíl porque la tabla se actualiza dinamicamente con Javascript! dough!)

## Requerimientos
```
beautifulsoup4
selenium
requests
```

## To do
- Analizar si se puede quitar Selenium de entremedio para simplificar las cosas!! (Prioridad 10000)
- Agregar la información de los viajes realizados por cada diputado
- Idear algún mecanismo que permita ejecutar este scrapper una vez al mes para ir agregando más datos. Si bien esto no esta directamente relacionado con el funcionamiento del scrapper en si sería bueno operacionalizarlo.
- Evaluar el reemplazo de funcionalidades implementadas aca que extraen datos por queries a la API de [datos abiertos](https://www.camara.cl/transparencia/datosAbiertos.aspx). No estamos al tanto si esta API se actualiza o no, al parecer si....
