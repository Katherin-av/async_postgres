# async_postgres
Mi primer trabajo sobre base de datos.

## Configuración de despliegue

Esta aplicación requiere la variable de entorno `DATABASE_URL` para conectarse a PostgreSQL.

Ejemplo:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_base_datos
```

En Vercel, agrega `DATABASE_URL` en la sección de Environment Variables del proyecto.
