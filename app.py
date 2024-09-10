import streamlit as st
import os
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="SUPER PEDIDOS")

# Crear carpeta para almacenar imágenes si no existe
if not os.path.exists("imagenes"):
    os.makedirs("imagenes")

# Cargar o crear DataFrame para los productos
if os.path.exists("productos.csv"):
    productos_df = pd.read_csv("productos.csv")
    productos_df["Precio_unidad"] = productos_df["Precio_unidad"].astype(float)
    productos_df["Precio_por_3"] = productos_df["Precio_por_3"].astype(float)
else:
    productos_df = pd.DataFrame(columns=["Nombre", "Precio_unidad", "Precio_por_3", "Imagen"])

# Función para mostrar el título y la información del local
def mostrar_info_local():
    st.markdown("<h1 style='color:red; font-weight:bold;'>SUPER PEDIDOS</h1>", unsafe_allow_html=True)
    st.markdown("<p>Teléfono: 3812588535</p>", unsafe_allow_html=True)

# Función para mostrar productos en dos columnas
def mostrar_productos():
    st.header("Lista de Productos")
    productos_seleccionados = []
    
    if not productos_df.empty:
        for i in range(0, len(productos_df), 2):
            cols = st.columns(2)

            # Primera columna
            with cols[0]:
                if i < len(productos_df):
                    row = productos_df.iloc[i]
                    st.subheader(row["Nombre"])
                    st.markdown(f"<p style='font-size:20px;'>Precio por unidad: ${row['Precio_unidad']:.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:20px;'>Precio por 3 unidades: ${row['Precio_por_3']:.2f}</p>", unsafe_allow_html=True)
                    image_path = os.path.join("imagenes", row["Imagen"])
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        st.image(image, caption=row["Nombre"], use_column_width=False, width=200)
                    
                    # Checkbox para seleccionar el producto
                    seleccionar = st.checkbox(f"Seleccionar {row['Nombre']}", key=f"checkbox_{i}")
                    if seleccionar:
                        cantidad = st.number_input(f"Cantidad de {row['Nombre']}", min_value=1, key=f"cantidad_{i}")
                        productos_seleccionados.append((row["Nombre"], cantidad))
                    st.markdown("---")

            # Segunda columna
            with cols[1]:
                if i + 1 < len(productos_df):
                    row = productos_df.iloc[i + 1]
                    st.subheader(row["Nombre"])
                    st.markdown(f"<p style='font-size:20px;'>Precio por unidad: ${row['Precio_unidad']:.2f}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:20px;'>Precio por 3 unidades: ${row['Precio_por_3']:.2f}</p>", unsafe_allow_html=True)
                    image_path = os.path.join("imagenes", row["Imagen"])
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        st.image(image, caption=row["Nombre"], use_column_width=False, width=200)

                    seleccionar = st.checkbox(f"Seleccionar {row['Nombre']}", key=f"checkbox_{i+1}")
                    if seleccionar:
                        cantidad = st.number_input(f"Cantidad de {row['Nombre']}", min_value=1, key=f"cantidad_{i+1}")
                        productos_seleccionados.append((row["Nombre"], cantidad))
                    st.markdown("---")
    else:
        st.write("No hay productos disponibles.")
    
    return productos_seleccionados

# Función para modificar productos existentes
def modificar_producto(producto_seleccionado):
    row = productos_df[productos_df['Nombre'] == producto_seleccionado].iloc[0]
    nuevo_nombre = st.text_input("Modificar nombre del producto", value=row["Nombre"])
    nuevo_precio_unidad = st.number_input("Modificar precio por unidad", min_value=0.0, format="%.2f", value=row["Precio_unidad"])
    nuevo_precio_por_3 = st.number_input("Modificar precio por tres unidades", min_value=0.0, format="%.2f", value=row["Precio_por_3"])
    nueva_imagen = st.file_uploader("Modificar imagen del producto (opcional)", type=["png", "jpg", "jpeg"])

    if st.button("Guardar cambios"):
        if nueva_imagen:
            imagen_path = os.path.join("imagenes", nueva_imagen.name)
            with open(imagen_path, "wb") as f:
                f.write(nueva_imagen.getbuffer())
            productos_df.loc[productos_df['Nombre'] == producto_seleccionado, 'Imagen'] = nueva_imagen.name
        productos_df.loc[productos_df['Nombre'] == producto_seleccionado, 'Nombre'] = nuevo_nombre
        productos_df.loc[productos_df['Nombre'] == producto_seleccionado, 'Precio_unidad'] = nuevo_precio_unidad
        productos_df.loc[productos_df['Nombre'] == producto_seleccionado, 'Precio_por_3'] = nuevo_precio_por_3

        productos_df.to_csv("productos.csv", index=False)
        st.success(f"Producto '{nuevo_nombre}' modificado correctamente.")

# Función para generar el mensaje de WhatsApp
def generar_mensaje(productos):
    mensaje = "Hola, quisiera hacer el siguiente pedido:\n"
    for producto, cantidad in productos:
        mensaje += f"- {producto}: {cantidad} unidades\n"
    return mensaje

# Tabs de la aplicación
tab1, tab2 = st.tabs(["Agregar/Modificar Productos", "Ver Productos"])

# Tab para agregar o modificar productos
with tab1:
    st.header("Agregar o modificar un producto")

    opciones = ["Agregar nuevo producto"] + list(productos_df["Nombre"].unique())
    producto_seleccionado = st.selectbox("Selecciona un producto para modificar o agrega uno nuevo", opciones)

    if producto_seleccionado == "Agregar nuevo producto":
        nombre = st.text_input("Nombre del producto")
        precio_unidad = st.number_input("Precio por unidad", min_value=0.0, format="%.2f")
        precio_por_3 = st.number_input("Precio por tres unidades", min_value=0.0, format="%.2f")
        imagen = st.file_uploader("Cargar imagen del producto", type=["png", "jpg", "jpeg"])

        if st.button("Agregar producto"):
            if nombre and precio_unidad > 0 and precio_por_3 > 0 and imagen is not None:
                imagen_path = os.path.join("imagenes", imagen.name)
                with open(imagen_path, "wb") as f:
                    f.write(imagen.getbuffer())

                nuevo_producto = pd.DataFrame({
                    "Nombre": [nombre],
                    "Precio_unidad": [precio_unidad],
                    "Precio_por_3": [precio_por_3],
                    "Imagen": [imagen.name]
                })

                productos_df = pd.concat([productos_df, nuevo_producto], ignore_index=True)
                productos_df.to_csv("productos.csv", index=False)

                st.success(f"Producto '{nombre}' agregado correctamente.")
            else:
                st.error("Por favor, complete todos los campos correctamente.")
    else:
        modificar_producto(producto_seleccionado)

# Tab para mostrar productos y hacer pedidos
with tab2:
    mostrar_info_local()  # Mostrar el título y la información del local
    productos_seleccionados = mostrar_productos()

    if productos_seleccionados:
        if st.button("Enviar pedido por WhatsApp"):
            mensaje = generar_mensaje(productos_seleccionados)
            url_whatsapp = f"https://wa.me/5493814644703?text={mensaje.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f"[Enviar pedido por WhatsApp]({url_whatsapp})", unsafe_allow_html=True)
    else:
        st.write("Selecciona al menos un producto para realizar el pedido.")