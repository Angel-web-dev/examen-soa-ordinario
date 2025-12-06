# Examen SOA - Scaffold v2

Esta versión fue creada asegurando:
- No existe la dependencia obsoleta `mysql:mysql-connector-java` en ningún archivo.
- El POM usa `com.mysql:mysql-connector-j` y Spring Boot 3.5.8.
- Java 21 es la versión objetivo (puedes cambiar a 17 si tu entorno no soporta 21).
- Flyway, Docker Compose y servicios separados (REST, SOAP, frontend).

Pasos rápidos (con Docker):
1. docker-compose up --build
2. Espera a que flyway y db terminen sus migraciones.
3. API REST en http://localhost:8080, API SOAP en http://localhost:5000/soap

Si no usas Docker, sigue las instrucciones dentro de la carpeta api-rest y api-soap.
