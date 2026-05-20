import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
### 🟢 INICIO DE PROPUESTA (Librerías adicionales necesarias)
from google.cloud import bigquery
import os
### 🔴 FIN DE PROPUESTA

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Registro SISMED - Sistema Completo", layout="wide")

# --- CONEXIÓN A GOOGLE SHEETS ---
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

### 🟢 INICIO DE PROPUESTA (Manejo dinámico de credenciales locales/producción)
CREDENTIALS_FILE = 'credentials.json'

if os.path.exists('projectbigquery-474916-3fbbedcb8e15.json'):
    CREDENTIALS_FILE = 'projectbigquery-474916-3fbbedcb8e15.json'
elif 'gcp' in st.secrets:
    import json
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(dict(st.secrets['gcp']), f)

creds = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=scope
)
### 🔴 FIN DE PROPUESTA

client = gspread.authorize(creds)
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1OefaGTNypH1nj5FcsEdAMz16iEFhFyrYLyOxv3gr_Mk"
).sheet1

### 🟢 INICIO DE PROPUESTA (Inicialización del cliente BigQuery)
client_bq = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)
### 🔴 FIN DE PROPUESTA

# 2. BASE DE DATOS MAESTRA CON DIAGNÓSTICOS
DATA_IPRESS = {
    "123": ["INCN", "INSTITUTO NACIONAL DE CIENCIAS NEUROLOGICAS", ["Diálisis Peritoneal", "Enfermedades raras y huérfanas"]],
    "124": ["DIRIS LIMA CENTRO", "INSTITUTO NACIONAL DE OFTALMOLOGIA", ["Enfermedades raras y huérfanas"]],
    "125": ["DIRIS LIMA SUR", "INSTITUTO NACIONAL DE REHABILITACION", ["Enfermedades raras y huérfanas"]],
    "126": ["INSN-BREÑA", "INSTITUTO NACIONAL DE SALUD DEL NIÑO", ["Diálisis Peritoneal", "Enfermedades raras y huérfanas", "Hemodiálisis", "Oncología","Terapia sin reemplazo renal" ,"Trasplante"]]
}

# --- LÓGICA DE ESTADO Y AUTOCOMPLETADO ---
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

# ✅ NUEVO: ESTADO PARA LIMPIAR GRILLA
if "grilla_vacia" not in st.session_state:
    st.session_state.grilla_vacia = pd.DataFrame(
        columns=[
            "CodSISMED", "DESCRIPCION", "PRESENTACION", "CONCENTRACION", "FORMA", "CPM", "STOCK"
        ]
    )

def actualizar_establecimiento():
    cod = st.session_state.cod_ip.strip()
    if cod in DATA_IPRESS:
        info = DATA_IPRESS[cod]
        st.session_state.reg_ip = info[0]
        st.session_state.nom_ip = info[1]
        st.session_state.opciones_diag = ["Seleccione un diagnóstico..."] + info[2]
    else:
        st.session_state.reg_ip = ""
        st.session_state.nom_ip = ""
        st.session_state.opciones_diag = ["Seleccione un diagnóstico..."]

# --- 3. SEGURIDAD (LLAVE DE ACCESO) ---
st.sidebar.title("Acceso al Sistema")
llave_usuario = st.sidebar.text_input(
    "Ingrese la LLAVE DE ACCESO:", type="password"
)

if llave_usuario != "sismed2026":
    st.title("💊 Registro de Medicamentos e Insumos por IPRESS")
    st.warning(
        "Ingrese la llave correcta en la barra lateral para continuar."
    )
    st.stop()

# --- INTERFAZ PRINCIPAL ---
st.title("💊 Registro SISMED por IPRESS")
with st.container(border=True):
    st.subheader("Datos del Establecimiento")
    c1, c2, c3, c4 = st.columns([0.8, 1.2, 2.8, 2.5])
    with c1:
        st.text_input(
            "Código IPRESS *", key="cod_ip", on_change=actualizar_establecimiento, placeholder="Ej: 126"
        )
    with c2:
        st.text_input(
            "Región / DIRIS", key="reg_ip", disabled=True
        )
    with c3:
        st.text_input(
            "Nombre IPRESS", key="nom_ip", disabled=True
        )
    with c4:
        if "opciones_diag" not in st.session_state:
            st.session_state.opciones_diag = [
                "Seleccione un diagnóstico..."
            ]
        diag_sel = st.selectbox(
            "Estrategia / Diagnóstico *", options=st.session_state.opciones_diag, key="diag_actual"
        )

    # --- NUEVA SECCIÓN: DATOS DEL PERSONAL ---
    st.subheader("Datos del Personal Responsable")
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        nombres_pers = st.text_input(
            "Nombres y Apellidos *", key="pers_nom"
        )
    with p2:
        celular_pers = st.text_input(
            "Celular *", key="pers_cel"
        )
    with p3:
        correo_pers = st.text_input(
            "Correo electrónico *", key="pers_mail"
        )
    with p4:
        cargo_pers = st.text_input(
            "Cargo *", key="pers_cargo"
        )
    with p5:
        oficina_pers = st.text_input(
            "Nombre de Oficina *", key="pers_ofi"
        )

st.divider()

# --- PESTAÑAS DE TRABAJO ---
tab_individual, tab_masiva = st.tabs(
    ["📝 Registro Individual", "📊 Carga Masiva"]
)
datos_finales = pd.DataFrame()

# --- A. REGISTRO INDIVIDUAL ---
with tab_individual:
    with st.form(key=f"form_ind_{st.session_state.form_key}"):
        m1, m2 = st.columns(2)
        with m1:
            cod_s = st.text_input("CodSISMED *")
            desc = st.text_input("DESCRIPCIÓN *")
            pres = st.text_input("PRESENTACIÓN")
        with m2:
            conc = st.text_input("CONCENTRACIÓN")
            form_farm = st.text_input("FORMA FARMACÉUTICA")
            cpm_i = st.number_input("CPM", min_value=0.0, step=1.0)
            stk_i = st.number_input("STOCK Actual", min_value=0.0, step=1.0)
            
        if st.form_submit_button("Guardar Registro ✅"):
            if (
                diag_sel == "Seleccione un diagnóstico..." or not cod_s or not st.session_state.nom_ip or not nombres_pers
            ):
                st.error(
                    "❌ Verifique la IPRESS, seleccione un diagnóstico y complete sus datos personales."
                )
            else:
                datos_finales = pd.DataFrame([{
                    "CodIPRESS": st.session_state.cod_ip,
                    "Región": st.session_state.reg_ip,
                    "NombreIPRESS": st.session_state.nom_ip,
                    "Diagnóstico": diag_sel,
                    "Responsable": nombres_pers,
                    "Celular": celular_pers,
                    "Correo": correo_pers,
                    "Cargo": cargo_pers,
                    "Oficina": oficina_pers,
                    "CodSISMED": cod_s,
                    "DESCRIPCION": desc,
                    "PRESENTACION": pres,
                    "CONCENTRACION": conc,
                    "FORMA": form_farm,
                    "CPM": cpm_i,
                    "STOCK": stk_i
                }])

# --- B. CARGA MASIVA ---
with tab_masiva:
    st.info(
        "💡 Copie los datos desde su Excel y péguelos en la tabla de abajo."
    )
    # ✅ USAR SESSION STATE
    df_plantilla = st.session_state.grilla_vacia
    conf_grid = {
        "CodSISMED": st.column_config.TextColumn(
            "CodSISMED", required=True
        ),
        "DESCRIPCION": st.column_config.TextColumn(
            "DESCRIPCIÓN", required=True
        ),
        "CPM": st.column_config.NumberColumn(
            "CPM", min_value=0
        ),
        "STOCK": st.column_config.NumberColumn(
            "STOCK", min_value=0
        ),
    }
    datos_grid = st.data_editor(
        st.session_state.grilla_vacia,
        num_rows="dynamic",
        column_config=conf_grid,
        use_container_width=True,
        key=f"grilla_masiva_{st.session_state.form_key}"
    )
    
    if st.button("Guardar todos los registros"):
        if (
            diag_sel == "Seleccione un diagnóstico..." or not st.session_state.nom_ip or not nombres_pers
        ):
            st.error(
                "❌ Asegúrese de completar los datos de IPRESS, Diagnóstico y Personal Responsable."
            )
        elif not datos_grid.dropna(subset=["CodSISMED"]).empty:
            df_temp = datos_grid.dropna(subset=["CodSISMED"]).copy()
            df_temp.insert(0, "CodIPRESS", st.session_state.cod_ip)
            df_temp.insert(1, "Región", st.session_state.reg_ip)
            df_temp.insert(2, "NombreIPRESS", st.session_state.nom_ip)
            df_temp.insert(3, "Diagnóstico", diag_sel)
            df_temp.insert(4, "Responsable", nombres_pers)
            df_temp.insert(5, "Celular", celular_pers)
            df_temp.insert(6, "Correo", correo_pers)
            df_temp.insert(7, "Cargo", cargo_pers)
            df_temp.insert(8, "Oficina", oficina_pers)
            datos_finales = df_temp

# --- 4. LÓGICA DE GUARDADO (UNIFICADA) ---
if not datos_finales.empty:
    try:
        with st.spinner("Guardando en Google Sheets..."):
            data_actual = sheet.get_all_records()
            df_existente = pd.DataFrame(data_actual)
            df_actualizado = pd.concat(
                [df_existente, datos_finales], ignore_index=True
            )
            sheet.clear()
            sheet.update(
                [df_actualizado.columns.values.tolist()] + df_actualizado.values.tolist()
            )
            st.success(
                f"✅ ¡{len(datos_finales)} registro(s) guardado(s) exitosamente!"
            )
            
            # ✅ LIMPIAR GRILLA
            # Limpiar SOLO la grilla masiva
            st.session_state.grilla_vacia = pd.DataFrame(
                columns=[
                    "CodSISMED", "DESCRIPCION", "PRESENTACION", "CONCENTRACION", "FORMA", "CPM", "STOCK"
                ]
            )
            # Reiniciar formulario individual
            st.session_state.form_key += 1
            # Recargar app
            st.rerun()
    except Exception as e:
        st.error(f"❌ Error al conectar con Google Sheets: {e}")

# --- PANEL ADMIN ---
st.sidebar.divider()
if st.sidebar.text_input("Clave Maestra:", type="password") == "admin123":
    st.sidebar.success("Modo Admin Activo")
    if st.sidebar.button("Ver Base de Datos Actual"):
        df_ver = pd.DataFrame(sheet.get_all_records())
        st.subheader("📊 Base de Datos SISMED")
        st.dataframe(df_ver, use_container_width=True)
