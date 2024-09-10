import streamlit as st
import os
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="SUPER PEDIDOS")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
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
    st.markdown("<h1 style='color:red; font-weight:bold; text-align:center;'>SUPER PEDIDOS</h1>", unsafe_allow_html=True)

    st.markdown("<p>Teléfono: 3812588535</p>", unsafe_allow_html=True)
    st.markdown("<p><strong>Selecciona la Cantidad y productos que deseas y presiona el boton al final de la pagina para enviar</strong></p>", unsafe_allow_html=True)
    

# Función para mostrar productos en dos columnas
def mostrar_productos():
    st.markdown("<h1 style='color:black; font-weight:bold; text-align:center;'>Lista de Productos</h1>", unsafe_allow_html=True)
    #st.header("Lista de Productos")
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

# Función para generar el mensaje de WhatsApp
def generar_mensaje(productos):
    mensaje = "Hola, quisiera hacer el siguiente pedido:\n"
    for producto, cantidad in productos:
        mensaje += f"- {producto}: {cantidad} unidades\n"
    return mensaje

# Página principal

# Mostrar información del local
mostrar_info_local()

# Mostrar productos y permitir la selección
productos_seleccionados = mostrar_productos()

if productos_seleccionados:
    if st.button("Enviar pedido por WhatsApp"):
        mensaje = generar_mensaje(productos_seleccionados)
        url_whatsapp = f"https://wa.me/5493814644703?text={mensaje.replace(' ', '%20').replace('\n', '%0A')}"
        st.markdown(f"[Presionar para Enviar pedido por WhatsApp]({url_whatsapp})", unsafe_allow_html=True)
else:
    st.write("Selecciona al menos un producto para realizar el pedido.")