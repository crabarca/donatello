# Scrapper
Esta pequeña librería hace scrapping de la pagina de diputados para obtener la información referente a las asignaciones
parlamentarias y su detalle. El objetivo final sería realizar una recopilación centralizada y ordenada de todos los datos de transparencia que están a disposición en la pagina de la camara de diputados. 

## Motivación
Actualmente la Transparencia realizada por la camara de diputados parece ser que es para decir: Somos transparentes porque tenemos los datos. Lo que no se menciona es que hacer analisis de estos datos resulta casi tan dificil como encontrar un parlamentario no corrupto. Por lo que

## Funcionamiento
Por el momento para obtener la información de las asignaciones se hace Scrapping utilizando Selenium. La razón de esto es que los cambios de inputs(fecha y año) hacen trigger de una tabla dinamica la cual no es sencilla de replicar utilizando HTTP requests y capturando el HTML de respuesta. Utilizando Selenium se simula el cambio de fecha y el HTML se parsea utilizando BeautifoulSoup

## Requerimientos
```
beautifulsoup4
selenium
requests
```

## To do
- Agregar la información de los viajes realizados por cada diputado
- Evaluar reemplazar algunas funcionalidades por la API de [datos abiertos](https://www.camara.cl/transparencia/datosAbiertos.aspx)