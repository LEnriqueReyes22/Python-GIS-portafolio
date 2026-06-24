# Comprobación de que ya se está trabajando en el entorno virtual.
import geopandas as gpd
print("Todo Funciona Correctamente")

# Ejercicio 1:  definir la ruta del shape file, definir GeoDataFrame y mostrar las primeras filas y columnas del shp (head()).
import geopandas as gpd
ruta = r"datos\loc_ags.shp"
gdf = gpd.read_file(ruta)
print(gdf.head())
print(gdf.columns)
# Ver sistema de coordenadas.
print(gdf.crs)

# Ejercicio 2: Primer análisis filtrado de datos.
# Filtrar por atributo.
# Ejemplo: filtrar por nombre (ajustar el campo real)
filtro = gdf[gdf["GM_10"] == "Alto"]
print(filtro)
print(f"Registros filtrados: {len(filtro)} de {len(gdf)}")
filtro.to_file(r"resultados\filtrado.shp")
# Para visualizar el filtro, realizamos lo siguiente:
# Primero instalamos matplotlib.
import matplotlib.pyplot as plt
# Crear la figura y el eje.
# # fig, ax = plt.subplots(figsize=(10, 10))
# Dibujar el GeoDataFrame filtrado
# # filtro.plot(ax=ax, color='red', edgecolor='black', linewidth=0.5)
# Opcional: añadir título y ajustar.
# # ax.set_title('Localidades con GM_10 =  "Alto"')
# Quitar los ejes de coordenadas para un mapa más limpio
# # ax.set_axis_off()
# Mostrar el mapa
# # plt.show()

# Si se quiere realizar la comparativa del total de localidades con el filtro, hacer lo siguiente:
# Para ver el mapa comparativo. (todo en color gris y filtro en rojo).
fig, ax = plt.subplots(figsize=(10, 10))
# Capa base: todas las localidades
gdf.plot(ax=ax, c='#D3D3D3', markersize=15)
# Capa filtrada: solo las localidades con índice de marginación 'Alto'
filtro.plot(ax=ax, c='red', edgecolors='black', linewidth=0.5, markersize=50)
ax.set_title('Localidades con índice de Marginación "Alto" en el Edo de Ags')
ax.set_axis_off()
plt.tight_layout()
plt.show()
# Si quieres guardar la imagen en lugar de mostrarla hay que reemplazar lo siguiente:
# # plt.savefig(r"resultados\mapa_comparativa.png", dpi=150, bbox_inches='tight')

# BUFFER
import geopandas as gpd
# Cargar datos
gdf = gpd.read_file(r"datos\loc_ags.shp")
# IMPORTANTE: verificar CRS
print(gdf.crs)
# DETALLE CRÍTICO(muy importante)
# El buffer usa unidades del sistema de coordenadas
# Si estás en EPSG:4326 (grados) está mal.
# Se debe convertir a pryectado (metros) está bien.
# Para reproyectar:
gdf = gdf.to_crs(epsg=32614) # UTM zona 14N (Aguascalientes aprox)
# Crear buffer:
buffer = gdf.buffer(2000) # 2000 metros
# Guardar Resultado:
buffer_gdf = gpd.GeoDataFrame(geometry=buffer, crs=gdf.crs)
buffer_gdf.to_file(r"resultados\buffer.shp")
# Visualizar buffer
import matplotlib.pyplot as plt
# Crear la figura
fig, ax = plt.subplots(figsize=(10,10))
# Graficamos el buffer (abajo) y los puntos originales (arriba) para contrastar
buffer_gdf.plot(ax=ax, color='lightblue', edgecolor='blue', alpha=0.5, label='Buffer 2000m')
gdf.plot(ax=ax, color='red', markersize=5, label='Puntos originales')
# Título
plt.title("Visualización del Buffer - Aguascalientes")
plt.legend()
plt.show() # Esto abrirá una ventana con tu mapa interactivo

# INTERSECCIÓN
capa1 = gpd.read_file(r"resultados\buffer.shp")
capa2 = gpd.read_file(r"datos\riesgos_inun_ags.shp")
# Asegurar mismo CRS (coordenadas)
capa1 = capa1.to_crs(epsg=32614)
capa2 = capa2.to_crs(epsg=32614)
# Intersección
inter = gpd.overlay(capa1, capa2, how="intersection")
# Guardar 
inter.to_file(r"resultados\intersection.shp")
# Visualización
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
gdf.plot(ax=ax, color="blue", alpha=0.5)
buffer_gdf.plot(ax=ax, color="red", alpha=0.3)
ax.set_title("Buffer de 2000 m")
ax.set_axis_off()
plt.savefig(r"resultados\buffer_mapa.png", dpi=300, bbox_inches="tight")
plt.show()
#  Limpiar geometrías inválidas
gdf = gdf[gdf.is_valid]
