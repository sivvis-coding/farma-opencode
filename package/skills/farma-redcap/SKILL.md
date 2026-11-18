---
name: farma-redcap
description: REDCap API, data dictionaries and safe local export for R or Python; integración y limpieza de datos REDCap
---

# REDCap

Antes de consultar, aclara institución, proyecto, autorización, campos necesarios
y qué información puede transmitirse al proveedor. La capacidad de exportar no
autoriza enviar datos a IA. Los metadatos y agregados también pueden ser sensibles.
No solicites tokens en la conversación, archivos de proyecto o código; nunca los
imprimas. Prefiere ejecutar la herramienta local de este paquete por la usuaria,
con token introducido de forma oculta, o elaborar código para un entorno
autorizado. Solo lectura; no importar, modificar ni borrar registros o metadatos.
Explica que los permisos de exportación del usuario aplican y que quitar campos
identificativos no garantiza anonimización. No leas ni resumas la exportación
con el modelo sin autorización expresa e institucional. Si falta autorización,
trabaja con datos sintéticos y plantillas.

Cuando expliques el exportador incluido (`tools/redcap_export.py`), indica que
seleccionar campos limita columnas, no filas: exporta todos los registros
accesibles y no admite filtrar registros. No sugieras que ese script implementa
filtros o anonimización. Si se necesita restringir filas, no lo ejecutes tal
como está; consulta con la institución otra vía autorizada y verificada.
La ruta `tools/redcap_export.py` es relativa a la carpeta del repositorio o del
paquete descargado, no a la carpeta de esta skill. Pide su ubicación si hace falta.
