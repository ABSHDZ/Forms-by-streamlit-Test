#Google docs
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
#QR code
import qrcode
import datetime
from datetime import date

#Read google sheet
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="DatosForms")

# Create QR code instance
def createQRcode(data = "Test", names = "QR code"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)
    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("Public/qrcode.png")
    # Print the picture in streamlit
    st.image("Public/qrcode.png", names)

MIEMBRO = [
    "Si",
    "No"
]

# Data to be encoded
with st.form(key="Registro", enter_to_submit=False):
    Nombre = st.text_input("Nombre Completo*")
    Fecha = st.date_input("Fecha de Nacimiento*", value=None, min_value=datetime.date(1920,1,2))
    Correo = st.text_input("Correo*")
    Iglesia = st.text_input("Iglesia")
    Miembro = st.radio("Miembro o Visitante", MIEMBRO, index=None)
    #Mark mandatory fields
    st.markdown("**Required*")
    submit_button = st.form_submit_button("Registrar")
    if submit_button:
        st.cache_data.clear()
        existing_data = conn.read(worksheet="DatosForms")
        if not Nombre or not Fecha or not Correo:
            st.warning("Mandatory fields")
            st.stop()
        elif Nombre in existing_data["NombreCompleto"].values:
            st.warning("AlreadyExist")
            st.stop()
        else:
            fecha_actual = date.today()
            new_row = pd.DataFrame(
                [
                    {
                        "FechaRegistro" : fecha_actual.strftime("%d-%m-%Y"),
                        "NombreCompleto" : Nombre,
                        "FechaNacimiento" : Fecha.strftime("%d-%m-%Y"),
                        "Coerreo" : Correo,
                        "Iglesia" : Iglesia,
                        "MiembroVisitante" : Miembro,
                    }
                ]
            )
            update_row = pd.concat([existing_data, new_row], ignore_index=False)
            conn.update(worksheet="DatosForms", data=update_row)
            st.success("Data updated successfully")
            cadena = f"{Nombre},{Fecha},{Correo}"
            referr = f"{Nombre}"
            createQRcode(cadena,referr)

