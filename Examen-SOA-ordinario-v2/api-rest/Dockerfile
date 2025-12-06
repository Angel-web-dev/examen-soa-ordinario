FROM eclipse-temurin:21-jdk-jammy
WORKDIR /app
COPY . /app
RUN mvn -q -DskipTests package
EXPOSE 8080
CMD ["java","-jar","target/api-rest-1.0.0.jar"]
