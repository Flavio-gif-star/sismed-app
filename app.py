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
"123":["INCN","INSTITUTO NACIONAL DE CIENCIAS NEUROLOGICAS",["Enfermedades raras y huérfanas","Oncología"]],
"124":["INO","INSTITUTO NACIONAL DE OFTALMOLOGIA",["Enfermedades raras y huérfanas"]],
"125":["INR","INSTITUTO NACIONAL DE REHABILITACION",["Enfermedades raras y huérfanas"]],
"126":["INSN-BREÑA","INSTITUTO NACIONAL DE SALUD DEL NIÑO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Trasplante","Terapia sin reemplazo renal"]],
"127":["INMP","INSTITUTO NACIONAL MATERNO PERINATAL",["Enfermedades raras y huérfanas","Oncología"]],
"132":["DIRIS LIMA ESTE","HOSPITAL NACIONAL HIPOLITO UNANUE",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"136":["DIRIS LIMA NORTE","HOSPITAL SERGIO BERNALES",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"137":["DIRIS LIMA NORTE","HOSPITAL CAYETANO HEREDIA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Trasplante","Terapia sin reemplazo renal"]],
"141":["DIRIS LIMA SUR","HOSPITAL DE APOYO DEPARTAMENTAL MARIA AUXILIADORA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"143":["DIRIS LIMA CENTRO","HOSPITAL NACIONAL ARZOBISPO LOAYZA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Trasplante","Terapia sin reemplazo renal"]],
"144":["DIRIS LIMA CENTRO","HOSPITAL NACIONAL DOS DE MAYO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Trasplante"]],
"145":["DIRIS LIMA CENTRO","HOSPITAL DE APOYO SANTA ROSA",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"146":["DIRIS LIMA CENTRO","HOSPITAL DE EMERGENCIAS CASIMIRO ULLOA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"147":["DIRIS LIMA CENTRO","HOSPITAL DE EMERGENCIAS PEDIATRICAS",["Enfermedades raras y huérfanas","Oncología"]],
"149":["DIRIS LIMA CENTRO","HOSPITAL NACIONAL DOCENTE MADRE NIÑO - SAN BARTOLOME",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"522":["DIRIS LIMA NORTE","HOSPITAL CARLOS LANFRANCO LA HOZ",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"741":["ANCASH","REGION ANCASH-SALUD HUARAZ",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"742":["ANCASH","REGION ANCASH-SALUD ELEAZAR GUZMAN BARRON",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"743":["ANCASH","REGION ANCASH-SALUD LA CALETA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"766":["AREQUIPA","REGION AREQUIPA-HOSPITAL GOYENECHE",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"767":["AREQUIPA","REGION AREQUIPA-HOSPITAL REGIONAL HONORIO DELGADO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"768":["AREQUIPA","REGION AREQUIPA-SALUD CAMANA",["Enfermedades raras y huérfanas","Terapia sin reemplazo renal"]],
"769":["AREQUIPA","REGION AREQUIPA-SALUD APLAO",["Enfermedades raras y huérfanas","Oncología"]],
"811":["HUANUCO","REGION HUANUCO-SALUD TINGO MARIA",["Oncología"]],
"812":["HUANUCO","REGION HUANUCO-HOSPITAL DE HUANUCO HERMILIO VALDIZAN",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"824":["JUNIN","REGION JUNIN-SALUD DANIEL ALCIDES CARRION",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"825":["JUNIN","REGION JUNIN-SALUD EL CARMEN",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"827":["JUNIN","REGION JUNIN-SALUD TARMA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"829":["JUNIN","REGION JUNIN-SALUD SATIPO",["Enfermedades raras y huérfanas","Oncología"]],
"846":["LA LIBERTAD","REGION LA LIBERTAD-INSTITUTO REGIONAL DE OFTALMOLOGIA",["Enfermedades raras y huérfanas"]],
"847":["LA LIBERTAD","REGION LA LIBERTAD-SALUD NORTE ASCOPE",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"848":["LA LIBERTAD","REGION LA LIBERTAD-SALUD TRUJILLO SUR OESTE",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"872":["LORETO","REGION LORETO-SALUD HOSPITAL DE APOYO IQUITOS",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"874":["LORETO","REGION LORETO- HOSPITAL REGIONAL DE LORETO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"890":["PASCO","REGION PASCO-SALUD HOSPITAL DANIEL A.CARRION",["Enfermedades raras y huérfanas","Oncología"]],
"901":["PIURA","REGION PIURA-HOSPITAL DE APOYO III SULLANA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"916":["PUNO","REGION PUNO-SALUD AZANGARO",["Diálisis Peritoneal","Enfermedades raras y huérfanas"]],
"917":["PUNO","REGION PUNO-SALUD SAN ROMAN",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"930":["SAN MARTIN","REGION SAN MARTIN-SALUD",["Oncología"]],
"951":["UCAYALI","REGION UCAYALI-HOSPITAL REGIONAL DE PUCALLPA",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"952":["UCAYALI","REGION UCAYALI-HOSPITAL AMAZONICO",["Oncología","Terapia sin reemplazo renal"]],
"970":["TACNA","REGION TACNA-HOSPITAL DE APOYO HIPOLITO UNANUE",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"998":["AMAZONAS","REGION AMAZONAS-HOSPITAL DE APOYO CHACHAPOYAS",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"999":["CAJAMARCA","REGION CAJAMARCA-HOSPITAL CAJAMARCA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Oncología"]],
"1000":["HUANCAVELICA","GOB. REG. HUANCAVELICA-HOSPITAL DEPARTAMENTAL DE HUANCAVELICA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1001":["LAMBAYEQUE","REGION LAMBAYEQUE-HOSPITAL REGIONAL DOCENTE LAS MERCEDES- CHICLAYO",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1003":["MADRE DE DIOS","REGION MADRE DE DIOS-HOSPITAL SANTA ROSA DE PUERTO MALDONADO",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1014":["ICA","REGION ICA- HOSPITAL SAN JOSE DE CHINCHA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1024":["AYACUCHO","REGION AYACUCHO-HOSPITAL HUAMANGA",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1037":["APURIMAC","REGION APURIMAC-HOSPITAL GUILLERMO DIAZ DE LA VEGA-ABANCAY",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1038":["APURIMAC","REGION APURIMAC-HOSPITAL SUBREGIONAL DE ANDAHUAYLAS",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1047":["CAJAMARCA","REGION CAJAMARCA-HOSPITAL GENERAL DE JAEN",["Diálisis Peritoneal","Hemodiálisis","Oncología"]],
"1052":["ICA","REGION ICA-HOSPITAL REGIONAL DE ICA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1058":["SAN MARTIN","REGION SAN MARTIN-SALUD ALTO MAYO",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1130":["CUSCO","REGION CUSCO - HOSPITAL DE APOYO DEPARTAMENTAL CUSCO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1138":["DIRIS LIMA ESTE","HOSPITAL JOSE AGURTO TELLO DE CHOSICA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1169":["CUSCO","REGION CUSCO- HOSPITAL ANTONIO LORENA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1196":["ICA","REGION ICA-HOSPITAL DE APOYO SANTA MARIA DEL SOCORRO",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1216":["DIRIS LIMA CENTRO","HOSPITAL SAN JUAN DE LURIGANCHO",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1235":["INEN","INSTITUTO NACIONAL DE ENFERMEDADES NEOPLASICAS",["Enfermedades raras y huérfanas","Oncología","Trasplante","Terapia sin reemplazo renal"]],
"1282":["LA LIBERTAD","R.LA LIBERTAD- INST. REG.ENFERMEDADES NEOPLASICAS LUIS PINILLOS GANOZA - INREN-NORTE",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1286":["LIMA","REGION LIMA - HOSP. HUACHO-HUAURA-OYON Y SERV. BASICOS DE SALUD",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1288":["LIMA","REGION LIMA - HOSPITAL DE APOYO REZOLA",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1289":["LIMA","REGION LIMA - HOSP. BARRANCA-CAJATAMBO Y SERV. BASICOS DE SALUD",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1290":["LIMA","REGION LIMA - HOSP. CHANCAY Y SERVICIOS BASICOS DE SALUD",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1292":["LIMA","REGION LIMA - HOSPITAL HUARAL Y SERVICIOS BASICOS DE SALUD",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1306":["PIURA","REGION PIURA-HOSPITAL DE APOYO  I  SANTA ROSA",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal"]],
"1316":["CALLAO","REGION CALLAO - DIRECCION DE SALUD  I  CALLAO",["Oncología"]],
"1317":["CALLAO","REGION CALLAO - HOSPITAL DANIEL A. CARRION",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Oncología"]],
"1318":["CALLAO","REGION CALLAO - HOSPITAL DE APOYO SAN JOSE",["Enfermedades raras y huérfanas","Oncología"]],
"1320":["AREQUIPA","REG. AREQUIPA - INST. REG. DE ENFERMEDADES NEOPLASICAS DEL SUR (IREN SUR)",["Enfermedades raras y huérfanas","Oncología"]],
"1362":["AYACUCHO","GOB. REG. DE AYACUCHO- RED DE SALUD HUAMANGA",["Enfermedades raras y huérfanas"]],
"1394":["MOQUEGUA","GOB. REG. MOQUEGUA - HOSPITAL REGIONAL DE MOQUEGUA",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Oncología"]],
"1400":["SAN MARTIN","GOB. REG. SAN MARTIN - HOSPITAL II - 2 TARAPOTO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1407":["LORETO","GOB. REG. DE LORETO- HOSPITAL SANTA GEMA DE YURIMAGUAS",["Enfermedades raras y huérfanas","Oncología"]],
"1422":["LAMBAYEQUE","REGION LAMBAYEQUE- HOSPITAL REGIONAL LAMBAYEQUE",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1435":["PUNO","GOB.REG. PUNO - HOSPITAL REGIONAL MANUEL NUÑEZ BUTRON",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1436":["TUMBES","GOB.REG.TUMBES-HOSP.REGIONAL JOSE ALFREDO MENDOZA OLAVARRIA-JAMO II-2 TUMBES",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1452":["CALLAO","GOB. REG. DEL CALLAO - HOSPITAL DE VENTANILLA",["Enfermedades raras y huérfanas","Oncología"]],
"1489":["AYACUCHO","GOB. REG. DE AYACUCHO - RED DE SALUD SAN MIGUEL",["Enfermedades raras y huérfanas","Oncología"]],
"1512":["INSN-SAN BORJA","INSTITUTO NACIONAL DE SALUD DEL NIÑO - SAN BORJA",["Enfermedades raras y huérfanas","Hemodiálisis","Oncología","Terapia sin reemplazo renal""Trasplante de Hígado"]],
"1657":["AREQUIPA","REG. AREQUIPA - HOSPITAL CENTRAL DE MAJES ING. ANGEL GABRIEL CHURA GALLEGOS",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1667":["CALLAO","GOB. REG. DEL CALLAO - HOSPITAL DE REHABILITACION DEL CALLAO",["Enfermedades raras y huérfanas"]],
"1670":["DIRIS LIMA SUR","HOSPITAL DE EMERGENCIAS VILLA EL SALVADOR",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1731":["JUNIN","GOB. REG. DE JUNIN - HOSPITAL REGIONAL DOCENTE DE MEDICINA TROPICAL DOCTOR JULIO CESAR DEMARINI CARO",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología"]],
"1735":["JUNIN","GOB. REG. DE JUNIN - INSTITUTO REGIONAL DE ENFERMEDADES NEOPLÁSICAS DEL CENTRO - IREN CENTRO",["Enfermedades raras y huérfanas","Oncología","Terapia sin reemplazo renal"]],
"1743":["CAJAMARCA","GOB. REG. DPTO. CAJAMARCA - HOSPITAL SANTA MARIA DE CUTERVO",["Oncología"]],
"1746":["DIRIS LIMA ESTE","HOSPITAL DE LIMA ESTE - VITARTE",["Diálisis Peritoneal","Enfermedades raras y huérfanas","Hemodiálisis","Oncología""Terapia sin reemplazo renal"]],
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
