# Concepcion Transparente
> https://concepciontransparente.ar/

## Desarrollo local

```bash
# Setup
./dev-setup.sh

# Update the data
docker-compose run --rm scraper scrapy runspider contrataciones.py
docker-compose run --rm scraper python post_processing.py

# Up the frontend
docker-compose up
# You can see the site on http://localhost:3000
```

## TODO

- [ ] Esta mal comparar los importes del 2009 con los de ahora. Actualizar los pesos?
- [ ] Obtener los nombres de los socios de la IGJ -> cruzar cuil
