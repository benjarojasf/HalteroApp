import flet as ft
import asyncio
import datetime
import csv
import os

# --- LISTA MAESTRA ---
EJERCICIOS_BASE = [
    ("Olímpico - Competencia", "Snatch (Arrancada)"),
    ("Olímpico - Competencia", "Clean & Jerk (Cargada y Envión)"),
    ("Variantes Snatch", "Power Snatch (Arrancada de Potencia)"),
    ("Variantes Snatch", "Hang Snatch (Arrancada Colgante)"),
    ("Variantes Snatch", "Block Snatch (Arrancada sobre Soportes)"),
    ("Variantes Snatch", "Muscle Snatch (Arrancada sin Deslizamiento)"),
    ("Variantes Snatch", "Snatch Balance (Balance de Arranque)"),
    ("Variantes Snatch", "Snatch Drop (Final de Arranque)"),
    ("Variantes Snatch", "Tall Snatch (Arrancada desde Cadera)"),
    ("Variantes Snatch", "Deficit Snatch (Arrancada con Déficit)"),
    ("Variantes Clean", "Clean (Cargada)"),
    ("Variantes Clean", "Power Clean (Cargada de Potencia)"),
    ("Variantes Clean", "Hang Clean (Cargada Colgante)"),
    ("Variantes Clean", "Block Clean (Cargada sobre Soportes)"),
    ("Variantes Clean", "Muscle Clean (Cargada sin Deslizamiento)"),
    ("Variantes Clean", "Tall Clean (Cargada desde Cadera)"),
    ("Variantes Clean", "Deficit Clean (Cargada con Déficit)"),
    ("Variantes Clean & Jerk", "Jerk (Envión)"),
    ("Variantes Clean & Jerk", "Power Jerk (Envión de Potencia)"),
    ("Variantes Clean & Jerk", "Split Jerk (Envión de Soporte)"),
    ("Variantes Clean & Jerk", "Push Jerk"),
    ("Variantes Clean & Jerk", "Rack Jerk (Envión desde Soportes)"),
    ("Variantes Clean & Jerk", "Behind the Neck Jerk (Tras Nuca)"),
    ("Variantes Clean & Jerk", "Jerk Dip (Dip de Envión)"),
    ("Variantes Clean & Jerk", "Jerk Drive (Impulso de Envión)"),
    ("Variantes Clean & Jerk", "Jerk Recovery (Recuperación de Envión)"),
    ("Fuerza - Pierna", "Back Squat (Sentadilla Trasera)"),
    ("Fuerza - Pierna", "Front Squat (Sentadilla Frontal)"),
    ("Fuerza - Pierna", "Overhead Squat (Sentadilla de Arranque)"),
    ("Fuerza - Pierna", "Pause Squat (Sentadilla con Pausa)"),
    ("Fuerza - Pierna", "Box Squat (Sentadilla al Cajón)"),
    ("Fuerza - Pierna", "Bulgarian Split Squat (Sentadilla Búlgara)"),
    ("Fuerza - Tirón", "Snatch Pull (Halón de Arranque)"),
    ("Fuerza - Tirón", "Clean Pull (Halón de Cargada)"),
    ("Fuerza - Tirón", "High Pull (Halón Alto)"),
    ("Fuerza - Tirón", "Pause Pull (Halón con Pausa)"),
    ("Fuerza - Tirón", "Panda Pull (Halón Panda)"),
    ("Fuerza - Tirón", "Snatch Deadlift (Peso Muerto de Arranque)"),
    ("Fuerza - Tirón", "Clean Deadlift (Peso Muerto de Cargada)"),
    ("Fuerza - Tirón", "RDL (Peso Muerto Rumano)"),
    ("Fuerza - Tirón", "Deficit Deadlift (Peso Muerto con Déficit)"),
    ("Accesorios - Empuje", "Strict Press (Press Militar)"),
    ("Accesorios - Empuje", "Push Press (Empuje de Fuerza)"),
    ("Accesorios - Empuje", "Sotts Press (Press Sots)"),
    ("Accesorios - Empuje", "Dips (Fondos)"),
    ("Accesorios - Empuje", "Z Press (Press Z / Sentado)"),
    ("Accesorios - Empuje", "Lu Raises (Vuelos Chinos)"),
    ("Accesorios - Posterior", "Good Mornings (Buenos Días)"),
    ("Accesorios - Posterior", "Back Extensions (Hiperextensiones de Espalda)"),
    ("Accesorios - Posterior", "Single Leg RDL (Peso Muerto Rumano Unilateral)"),
    ("Accesorios - Tracción", "Pendlay Row (Remo Pendlay)"),
    ("Accesorios - Tracción", "Pull Ups (Dominadas)"),
    ("Accesorios - Tracción", "Chin Ups (Dominadas Supinas)"),
    ("Accesorios - Tracción", "Barbell Row (Remo con Barra)"),
    ("Pliometría", "Box Jump (Salto al Cajón)"),
    ("Pliometría", "Depth Jump (Salto de Profundidad)"),
]

def inicializar_maestro_ejercicios():
    nombre_archivo = "maestro_ejercicios.csv"
    if not os.path.isfile(nombre_archivo):
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Categoria", "Nombre"])
            writer.writerows(EJERCICIOS_BASE)

def leer_ejercicios():
    ejercicios_dict = {}
    if os.path.isfile("maestro_ejercicios.csv"):
        with open("maestro_ejercicios.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    cat, nom = row[0], row[1]
                    if cat not in ejercicios_dict:
                        ejercicios_dict[cat] = []
                    ejercicios_dict[cat].append(nom)
    return ejercicios_dict

async def main(page: ft.Page):
    # ==========================================
    #   CONFIGURACIÓN DE TEMA (SKIN)
    # ==========================================
    page.title = "Haltero Tracker"
    page.padding = 0 
    page.scroll = None 
    
    # Elige tu tema aquí:
    # color_scheme_seed determina el color principal de toda la app
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE, # Prueba: RED, TEAL, ORANGE, INDIGO
        use_material3=True
    )
    # Modo Claro (LIGHT) o Oscuro (DARK)
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.bgcolor = ft.Colors.WHITE

    # ==========================================
    #   INICIALIZACIÓN DE DATOS
    # ==========================================
    inicializar_maestro_ejercicios()
    DB_EJERCICIOS = leer_ejercicios()
    lista_categorias = list(DB_EJERCICIOS.keys())

    # Variables Globales
    segundos = 0
    contando = False
    numero_serie_global = 1 
    fecha_hoy_txt = datetime.date.today().strftime("%d-%m-%Y")
    indice_fila_editando = -1 
    detalle_fecha_actual = ""
    detalle_ejercicio_actual = ""
    ejercicio_a_editar_original = "" 
    categoria_a_editar_original = ""

    # ==========================================
    #   DEFINICIÓN DE VISTAS (UI)
    # ==========================================

    # --- 1. VISTA INICIO (DEFINIDA PRIMERO PARA EVITAR ERRORES) ---
    vista_inicio = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.FITNESS_CENTER, size=120, color=ft.Colors.BLACK),
                ft.Text("Haltero Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )

    # --- 2. COMPONENTES DE ENTRENAMIENTO ---
    def cambiar_fecha(e):
        campo_fecha_texto.value = date_picker.value.strftime("%d-%m-%Y")
        page.update()

    date_picker = ft.DatePicker(
        on_change=cambiar_fecha,
        first_date=datetime.datetime(2023, 1, 1),
        last_date=datetime.datetime(2030, 12, 31),
    )
    
    btn_calendario = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH, 
        icon_color=ft.Colors.PRIMARY, # Usa el color del tema
        on_click=lambda _: page.open(date_picker)
    )

    campo_fecha_texto = ft.TextField(
        value=fecha_hoy_txt, width=120, read_only=True, 
        text_align=ft.TextAlign.CENTER, border=ft.InputBorder.NONE, 
        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)
    )

    texto_cronometro = ft.Text(value="00:00", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    contenedor_cronometro_ui = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.TIMER, color=ft.Colors.WHITE), texto_cronometro], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.Colors.BLUE_GREY_900, padding=10, border_radius=10, margin=ft.margin.only(bottom=10)
    )
    
    fila_cronometro = ft.Row(controls=[contenedor_cronometro_ui], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    def cambiar_estado_crono(e):
        nonlocal contando
        contando = switch_crono.value
        fila_cronometro.visible = switch_crono.value
        page.update()

    switch_crono = ft.Switch(label="Activar Cronómetro", value=False, on_change=cambiar_estado_crono)

    async def resetear_cronometro():
        nonlocal segundos
        if switch_crono.value:
            segundos = 0
            texto_cronometro.value = "00:00"
            texto_cronometro.color = ft.Colors.GREEN_400
            page.update()
            await asyncio.sleep(0.5)
            texto_cronometro.color = ft.Colors.WHITE
            page.update()

    lista_series = ft.ListView(expand=True, spacing=10, padding=20)
    campo_kilos = ft.TextField(label="Kilos", width=100, keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.PRIMARY)
    campo_reps = ft.TextField(label="Reps", width=100, keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.PRIMARY)
    
    dd_ejercicio = ft.Dropdown(label="Ejercicio", width=None, disabled=True, options=[])

    def cambio_categoria(e):
        cat_selec = dd_categoria.value
        if cat_selec in DB_EJERCICIOS:
            opciones = [ft.dropdown.Option(nombre) for nombre in DB_EJERCICIOS[cat_selec]]
            dd_ejercicio.options = opciones
            dd_ejercicio.value = opciones[0].key 
            dd_ejercicio.disabled = False
        page.update()

    dd_categoria = ft.Dropdown(
        label="Categoría", width=None, 
        options=[ft.dropdown.Option(c) for c in lista_categorias],
        on_change=cambio_categoria
    )
    
    columna_selectores = ft.Column(controls=[dd_categoria, dd_ejercicio], spacing=10)

    # --- Lógica de Botones y Guardado ---
    def finalizar_entrenamiento(e):
        if len(lista_series.controls) == 0:
            page.snack_bar = ft.SnackBar(ft.Text("No hay series para guardar"))
            page.snack_bar.open = True
            page.update()
            return

        nombre_archivo = "historial_entrenamientos.csv"
        archivo_existe = os.path.isfile(nombre_archivo)
        fecha_registrada = campo_fecha_texto.value

        with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not archivo_existe:
                writer.writerow(["Fecha", "N_Serie", "Ejercicio", "Kilos", "Reps", "Sensacion"])
            
            for tarjeta in reversed(lista_series.controls):
                datos = tarjeta.data
                writer.writerow([fecha_registrada, datos["numero"], datos["ejercicio"], datos["kilos"], datos["reps"], datos["sensacion"]])

        page.snack_bar = ft.SnackBar(ft.Text(f"¡Ejercicio guardado exitosamente!"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        
        lista_series.controls.clear()
        nonlocal numero_serie_global
        numero_serie_global = 1
        dd_categoria.disabled = False
        dd_ejercicio.disabled = False
        
        actualizar_historial(None)
        actualizar_tabla_records() 
        page.update()

    def agregar_serie(e):
        nonlocal numero_serie_global
        if not campo_kilos.value or not campo_reps.value or not dd_ejercicio.value: return 
        
        if not dd_ejercicio.disabled:
            dd_categoria.disabled = True
            dd_ejercicio.disabled = True
            page.update()

        for tarjeta in lista_series.controls:
            tarjeta.border = ft.border.all(1, ft.Colors.GREY_200)
            tarjeta.content.controls[0].controls[0].color = ft.Colors.GREY_400 
            tarjeta.content.controls[1].color = ft.Colors.GREY_400 
            fila_botones_responsive = tarjeta.content.controls[3] 
            for boton in fila_botones_responsive.controls: 
                boton.color = ft.Colors.GREY_500
                boton.icon_color = ft.Colors.GREY_500

        mi_numero_serie = numero_serie_global
        val_kilos = campo_kilos.value
        val_reps = campo_reps.value
        val_ejercicio = dd_ejercicio.value 
        
        txt_titulo = ft.Text(f"Serie #{mi_numero_serie}: {val_ejercicio}", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLACK)
        txt_datos = ft.Text(f"{val_kilos} kg  x  {val_reps} reps", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)

        async def click_sensacion(e):
            btn_bien.bgcolor = ft.Colors.GREEN_100
            btn_regular.bgcolor = ft.Colors.ORANGE_100
            btn_mal.bgcolor = ft.Colors.RED_100
            btn_nulo.bgcolor = ft.Colors.GREY_200 
            btn_nulo.color = ft.Colors.BLACK
            btn_nulo.icon_color = ft.Colors.RED
            
            sensacion = e.control.text
            if sensacion == "Bien": e.control.bgcolor = ft.Colors.GREEN_400
            elif sensacion == "Regular": e.control.bgcolor = ft.Colors.ORANGE_400
            elif sensacion == "Mal": e.control.bgcolor = ft.Colors.RED_400
            elif sensacion == "Nulo": 
                e.control.bgcolor = ft.Colors.GREY_800
                e.control.color = ft.Colors.WHITE
            
            nueva_tarjeta.data["sensacion"] = sensacion
            page.update()
            
            if mi_numero_serie == (numero_serie_global - 1):
                await resetear_cronometro()

        estilo_btn = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=5)

        btn_bien = ft.ElevatedButton("Bien", on_click=click_sensacion, bgcolor=ft.Colors.GREEN_100, color=ft.Colors.BLACK, style=estilo_btn, col={"xs": 6, "sm": 3})
        btn_regular = ft.ElevatedButton("Regular", on_click=click_sensacion, bgcolor=ft.Colors.ORANGE_100, color=ft.Colors.BLACK, style=estilo_btn, col={"xs": 6, "sm": 3})
        btn_mal = ft.ElevatedButton("Mal", on_click=click_sensacion, bgcolor=ft.Colors.RED_100, color=ft.Colors.BLACK, style=estilo_btn, col={"xs": 6, "sm": 3})
        btn_nulo = ft.ElevatedButton("Nulo", icon=ft.Icons.FLAG, icon_color=ft.Colors.RED, on_click=click_sensacion, bgcolor=ft.Colors.GREY_200, color=ft.Colors.BLACK, style=estilo_btn, col={"xs": 6, "sm": 3})

        def guardar_edicion(e):
            txt_datos.value = f"{edit_kilos.value} kg  x  {edit_reps.value} reps"
            nueva_tarjeta.data["kilos"] = edit_kilos.value
            nueva_tarjeta.data["reps"] = edit_reps.value
            page.close(dlg_edit)
            page.update()

        edit_kilos = ft.TextField(label="Kilos", value=val_kilos)
        edit_reps = ft.TextField(label="Reps", value=val_reps)
        dlg_edit = ft.AlertDialog(title=ft.Text("Editar"), content=ft.Column([edit_kilos, edit_reps], height=150), actions=[ft.TextButton("Guardar", on_click=guardar_edicion)])
        
        def borrar_tarjeta(e):
            lista_series.controls.remove(nueva_tarjeta)
            page.update()

        nueva_tarjeta = ft.Container(
            content=ft.Column([
                ft.Row([txt_titulo, ft.Row([ft.IconButton(ft.Icons.EDIT, ft.Colors.BLUE_GREY, on_click=lambda _: page.open(dlg_edit)), ft.IconButton(ft.Icons.DELETE_OUTLINE, ft.Colors.RED_400, on_click=borrar_tarjeta)], spacing=0)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                txt_datos,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(controls=[btn_bien, btn_regular, btn_mal, btn_nulo], run_spacing=5)
            ]),
            padding=15, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, bgcolor=ft.Colors.WHITE,
            data={"numero": mi_numero_serie, "ejercicio": val_ejercicio, "kilos": val_kilos, "reps": val_reps, "sensacion": "Sin calificar"}
        )

        lista_series.controls.insert(0, nueva_tarjeta)
        campo_kilos.value = ""
        campo_reps.value = ""
        numero_serie_global += 1
        campo_kilos.focus()
        page.update()

    btn_agregar = ft.ElevatedButton("Agregar", on_click=agregar_serie, bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE, height=50)

    btn_finalizar_block = ft.ElevatedButton(
        text="FINALIZAR EJERCICIO", bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE,
        on_click=finalizar_entrenamiento, width=1000, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)) 
    )

    seccion_footer = ft.Container(
        content=ft.Column(controls=[fila_cronometro, btn_finalizar_block], spacing=0),
        bgcolor=ft.Colors.WHITE, 
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_300))
    )

    header = ft.Container(
        padding=20,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(controls=[
            ft.Row([ft.Text("Fecha:", weight=ft.FontWeight.BOLD, size=16), btn_calendario, campo_fecha_texto], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            columna_selectores, 
            switch_crono,
            ft.Divider(),
            ft.Row([campo_kilos, campo_reps, btn_agregar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=1, thickness=1),
        ])
    )

    vista_entrenar = ft.Column(controls=[header, lista_series, seccion_footer], expand=True, spacing=0)

    # --- 3. PESTAÑA RÉCORDS ---
    def cambiar_fecha_rm(e):
        campo_fecha_rm.value = date_picker_rm.value.strftime("%d-%m-%Y")
        page.update()

    date_picker_rm = ft.DatePicker(
        on_change=cambiar_fecha_rm,
        first_date=datetime.datetime(2020, 1, 1), 
        last_date=datetime.datetime(2030, 12, 31),
    )
    
    campo_fecha_rm = ft.TextField(value=fecha_hoy_txt, width=120, read_only=True, label="Fecha RM", text_style=ft.TextStyle(size=14))
    btn_calendario_rm = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.PRIMARY, on_click=lambda _: page.open(date_picker_rm))
    
    rm_dd_ejercicio = ft.Dropdown(label="Ejercicio", width=None, disabled=True)
    
    def rm_cambio_categoria(e):
        cat_selec = rm_dd_categoria.value
        if cat_selec in DB_EJERCICIOS:
            opciones = [ft.dropdown.Option(nombre) for nombre in DB_EJERCICIOS[cat_selec]]
            rm_dd_ejercicio.options = opciones
            rm_dd_ejercicio.value = opciones[0].key 
            rm_dd_ejercicio.disabled = False
        page.update()

    rm_dd_categoria = ft.Dropdown(
        label="Categoría", width=None, 
        options=[ft.dropdown.Option(c) for c in lista_categorias],
        on_change=rm_cambio_categoria
    )

    rm_campo_kilos = ft.TextField(label="Max Kg", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    def guardar_rm_manual(e):
        if not rm_campo_kilos.value or not rm_dd_ejercicio.value: return
        nombre_archivo = "historial_entrenamientos.csv"
        archivo_existe = os.path.isfile(nombre_archivo)
        with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not archivo_existe: writer.writerow(["Fecha", "N_Serie", "Ejercicio", "Kilos", "Reps", "Sensacion"])
            writer.writerow([campo_fecha_rm.value, "RM", rm_dd_ejercicio.value, rm_campo_kilos.value, "1", "Bien"])
        page.close(dlg_nuevo_rm) 
        page.snack_bar = ft.SnackBar(ft.Text("¡RM Registrado!"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        rm_campo_kilos.value = ""
        actualizar_tabla_records()
        actualizar_historial(None) 
        page.update()

    dlg_nuevo_rm = ft.AlertDialog(
        title=ft.Text("Nuevo Récord Manual"),
        content=ft.Column([ft.Row([btn_calendario_rm, campo_fecha_rm]), rm_dd_categoria, rm_dd_ejercicio, rm_campo_kilos], height=280, width=300),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_nuevo_rm)), ft.ElevatedButton("Guardar RM", on_click=guardar_rm_manual, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)]
    )

    tabla_records = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Ejercicio", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Max (Kg)", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), numeric=True),
            ft.DataColumn(ft.Text("Antigüedad", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), numeric=True), 
        ],
        rows=[], width=float('inf'), heading_row_height=40, column_spacing=30
    )

    def actualizar_tabla_records():
        nombre_archivo = "historial_entrenamientos.csv"
        if not os.path.isfile(nombre_archivo): return
        records_dict = {} 
        try:
            with open(nombre_archivo, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 6:
                        ejercicio, kilos, sensacion, fecha_str = row[2], float(row[3]), row[5], row[0]
                        if sensacion == "Nulo": continue
                        if ejercicio not in records_dict or kilos > records_dict[ejercicio]["kg"]:
                            records_dict[ejercicio] = {"kg": kilos, "fecha": fecha_str}
            nuevas_filas = []
            hoy = datetime.date.today()
            for ej, data in records_dict.items():
                fecha_record_obj = datetime.datetime.strptime(data["fecha"], "%d-%m-%Y").date()
                semanas = int((hoy - fecha_record_obj).days / 7)
                txt_tiempo = f"{semanas} sem" if semanas > 0 else "Esta semana"
                nuevas_filas.append(ft.DataRow(cells=[ft.DataCell(ft.Text(ej, color=ft.Colors.BLACK)), ft.DataCell(ft.Text(str(int(data["kg"])), weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK)), ft.DataCell(ft.Text(txt_tiempo, color=ft.Colors.BLACK))]))
            tabla_records.rows = nuevas_filas
        except: pass

    actualizar_tabla_records()

    vista_records = ft.Container(
        content=ft.Column([
            ft.Text("Mis Récords Actuales", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Divider(),
            ft.ElevatedButton("Ingresar Nuevo RM", on_click=lambda e: page.open(dlg_nuevo_rm), bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE),
            ft.Divider(color=ft.Colors.TRANSPARENT, height=20),
            ft.Column([tabla_records], scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True), padding=20, expand=True
    )

    # --- 4. PESTAÑA HISTORIAL ---
    dropdown_filtro_historial = ft.Dropdown(label="Filtrar por ejercicio", options=[ft.dropdown.Option("Todos")], value="Todos", on_change=lambda e: actualizar_historial(e), content_padding=10)
    columna_historial = ft.ListView(expand=True, spacing=15, padding=20)

    hist_edit_kilos = ft.TextField(label="Kilos")
    hist_edit_reps = ft.TextField(label="Reps")
    hist_edit_sens = ft.Dropdown(label="Sensación", options=[ft.dropdown.Option("Bien"), ft.dropdown.Option("Regular"), ft.dropdown.Option("Mal"), ft.dropdown.Option("Nulo")])

    contenido_detalle = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    dlg_detalle_ejercicio = ft.AlertDialog(
        title=ft.Text("Detalle del Entrenamiento", color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD),
        content=ft.Container(content=contenido_detalle, height=300, width=350),
        bgcolor=ft.Colors.WHITE, 
        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_detalle_ejercicio))]
    )

    def recargar_detalle_popup():
        if not detalle_fecha_actual or not detalle_ejercicio_actual: return
        nombre_archivo = "historial_entrenamientos.csv"
        if not os.path.isfile(nombre_archivo): return
        filas_coincidentes = []
        with open(nombre_archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas_totales = list(reader)
            for i in range(1, len(filas_totales)):
                if filas_totales[i][0] == detalle_fecha_actual and filas_totales[i][2] == detalle_ejercicio_actual:
                    filas_coincidentes.append({'data': filas_totales[i], 'index_csv': i})
        
        contenido_detalle.controls.clear()
        contenido_detalle.controls.append(ft.Text(detalle_ejercicio_actual, weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK))
        contenido_detalle.controls.append(ft.Divider())
        filas_tabla_detalle = []
        for item in filas_coincidentes:
            row = item['data']
            sensacion_txt = row[5]
            color_sens = ft.Colors.GREEN_700 if sensacion_txt == "Bien" else ft.Colors.AMBER_700 if sensacion_txt == "Regular" else ft.Colors.RED_700
            filas_tabla_detalle.append(ft.DataRow(cells=[ft.DataCell(ft.Container(content=ft.Text(row[3], color=ft.Colors.BLACK), alignment=ft.alignment.center)), ft.DataCell(ft.Container(content=ft.Text(row[4], color=ft.Colors.BLACK), alignment=ft.alignment.center)), ft.DataCell(ft.Container(content=ft.Text(sensacion_txt, color=color_sens), alignment=ft.alignment.center))], on_select_changed=abrir_edicion_historial, data={'index_csv': item['index_csv'], 'kilos': row[3], 'reps': row[4], 'sens': sensacion_txt}))
        
        contenido_detalle.controls.append(ft.DataTable(columns=[ft.DataColumn(ft.Text("Kg", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)), ft.DataColumn(ft.Text("Reps", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)), ft.DataColumn(ft.Text("Sens.", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK))], rows=filas_tabla_detalle, column_spacing=20, width=float('inf'), show_checkbox_column=False))
        page.update()

    def guardar_cambios_historial(e):
        nombre_archivo = "historial_entrenamientos.csv"
        filas = []
        with open(nombre_archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas = list(reader)
        fila_antigua = filas[indice_fila_editando]
        filas[indice_fila_editando] = [fila_antigua[0], fila_antigua[1], fila_antigua[2], hist_edit_kilos.value, hist_edit_reps.value, hist_edit_sens.value]
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(filas)
        page.close(dlg_historial_opciones)
        page.snack_bar = ft.SnackBar(ft.Text("Registro actualizado"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        actualizar_historial(None) 
        actualizar_tabla_records()
        recargar_detalle_popup()

    def eliminar_registro_historial(e):
        nombre_archivo = "historial_entrenamientos.csv"
        filas = []
        with open(nombre_archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas = list(reader)
        del filas[indice_fila_editando]
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(filas)
        page.close(dlg_historial_opciones)
        page.close(dlg_detalle_ejercicio) 
        page.snack_bar = ft.SnackBar(ft.Text("Registro eliminado"), bgcolor=ft.Colors.RED)
        page.snack_bar.open = True
        actualizar_historial(None)
        actualizar_tabla_records()
        recargar_detalle_popup()

    dlg_historial_opciones = ft.AlertDialog(
        title=ft.Text("Editar Serie"),
        content=ft.Column([ft.Text("Modifica o elimina esta serie:", size=12, color=ft.Colors.GREY), hist_edit_kilos, hist_edit_reps, hist_edit_sens], height=250, width=300),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_historial_opciones)), ft.TextButton("Eliminar", on_click=eliminar_registro_historial, style=ft.ButtonStyle(color=ft.Colors.RED)), ft.ElevatedButton("Guardar", on_click=guardar_cambios_historial, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)]
    )

    def abrir_edicion_historial(e):
        nonlocal indice_fila_editando
        datos_fila = e.control.data 
        indice_fila_editando = datos_fila['index_csv']
        hist_edit_kilos.value = datos_fila['kilos']
        hist_edit_reps.value = datos_fila['reps']
        hist_edit_sens.value = datos_fila['sens']
        page.open(dlg_historial_opciones)

    def abrir_detalle_popup(e):
        nonlocal detalle_fecha_actual, detalle_ejercicio_actual
        lista_filas_csv = e.control.data 
        if not lista_filas_csv: return
        primera_fila = lista_filas_csv[0]['data']
        detalle_fecha_actual = primera_fila[0]
        detalle_ejercicio_actual = primera_fila[2]
        recargar_detalle_popup()
        page.open(dlg_detalle_ejercicio)

    def actualizar_historial(e):
        nombre_archivo = "historial_entrenamientos.csv"
        if not os.path.isfile(nombre_archivo): return 
        datos_agrupados = {}
        ejercicios_encontrados = set()
        try:
            with open(nombre_archivo, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                filas_totales = list(reader)
                if len(filas_totales) < 2: return 
                for i in range(1, len(filas_totales)):
                    row = filas_totales[i]
                    if len(row) >= 6:
                        if row[1] == "RM": continue
                        ejercicios_encontrados.add(row[2])
                seleccion_actual = dropdown_filtro_historial.value
                nuevas_opciones = [ft.dropdown.Option("Todos")]
                for ej in sorted(list(ejercicios_encontrados)):
                    nuevas_opciones.append(ft.dropdown.Option(ej))
                dropdown_filtro_historial.options = nuevas_opciones
                if seleccion_actual in [op.key for op in nuevas_opciones]: dropdown_filtro_historial.value = seleccion_actual
                else: dropdown_filtro_historial.value = "Todos"
                filtro = dropdown_filtro_historial.value
                for i in range(len(filas_totales)-1, 0, -1):
                    row = filas_totales[i]
                    if len(row) >= 6:
                        if row[1] == "RM": continue
                        nombre_ejercicio = row[2]
                        if filtro == "Todos" or filtro == nombre_ejercicio:
                            fecha = row[0]
                            if fecha not in datos_agrupados: datos_agrupados[fecha] = {} 
                            if nombre_ejercicio not in datos_agrupados[fecha]: datos_agrupados[fecha][nombre_ejercicio] = []
                            datos_agrupados[fecha][nombre_ejercicio].append({'data': row, 'index_csv': i})
            columna_historial.controls.clear()
            if not datos_agrupados: columna_historial.controls.append(ft.Text("No se encontraron registros.", color=ft.Colors.GREY))
            for fecha, ejercicios_dict in datos_agrupados.items():
                header_fecha = ft.Container(content=ft.Text(f"📅 {fecha}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87), bgcolor=ft.Colors.GREY_200, padding=10, border_radius=5, alignment=ft.alignment.center_left)
                filas_resumen = []
                for nombre_ej, lista_series in ejercicios_dict.items():
                    pesos = []
                    total_reps = 0
                    for serie in lista_series:
                        try:
                            p = float(serie['data'][3])
                            r = int(serie['data'][4])
                            pesos.append(p)
                            total_reps += r
                        except: pass
                    txt_peso = "0"
                    if pesos:
                        min_p = int(min(pesos))
                        max_p = int(max(pesos))
                        txt_peso = f"{min_p} kg" if min_p == max_p else f"{min_p}-{max_p} kg"
                    txt_reps = f"{total_reps} reps"
                    filas_resumen.append(ft.DataRow(cells=[ft.DataCell(ft.Text(nombre_ej, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)), ft.DataCell(ft.Container(content=ft.Text(txt_peso, color=ft.Colors.BLACK), alignment=ft.alignment.center)), ft.DataCell(ft.Container(content=ft.Text(txt_reps, color=ft.Colors.BLACK), alignment=ft.alignment.center))], on_select_changed=abrir_detalle_popup, data=lista_series))
                tabla_resumen = ft.DataTable(columns=[ft.DataColumn(ft.Text("", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)), ft.DataColumn(ft.Text("Carga", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD), numeric=True), ft.DataColumn(ft.Text("Volumen", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD), numeric=True)], rows=filas_resumen, column_spacing=20, heading_row_height=40, width=float('inf'), show_checkbox_column=False)
                columna_historial.controls.append(ft.Column([header_fecha, tabla_resumen], spacing=0))
            if page: page.update()
        except Exception as e: print(f"Error: {e}")

    actualizar_historial(None)

    vista_historial = ft.Container(content=ft.Column(controls=[ft.Text("Historial de Entrenamientos", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), ft.Text("Toca un ejercicio para ver el detalle de las series", size=12, color=ft.Colors.GREY), dropdown_filtro_historial, ft.Divider(), columna_historial], expand=True), padding=10, expand=True)

    # --- 5. PESTAÑA EJERCICIOS ---
    lista_gestion_ejercicios = ft.ListView(expand=True, spacing=10)
    nuevo_ej_nombre = ft.TextField(label="Nombre Ejercicio", expand=True)
    nuevo_ej_cat = ft.TextField(label="Categoría (Ej: Fuerza)", expand=True)

    def refrescar_lista_gestion():
        lista_gestion_ejercicios.controls.clear()
        data_actual = leer_ejercicios()
        for cat in data_actual.keys():
            lista_gestion_ejercicios.controls.append(ft.Container(content=ft.Text(cat, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), bgcolor=ft.Colors.PRIMARY, padding=5, border_radius=5))
            for ej_nombre in data_actual[cat]:
                lista_gestion_ejercicios.controls.append(ft.ListTile(title=ft.Text(ej_nombre, color=ft.Colors.BLACK), trailing=ft.PopupMenuButton(icon=ft.Icons.MORE_VERT, items=[ft.PopupMenuItem(text="Editar", on_click=abrir_editar_ejercicio, data={"cat": cat, "nom": ej_nombre}), ft.PopupMenuItem(text="Eliminar", on_click=eliminar_ejercicio_maestro, data={"cat": cat, "nom": ej_nombre})])))
        page.update()

    def guardar_nuevo_ejercicio(e):
        cat = nuevo_ej_cat.value
        nom = nuevo_ej_nombre.value
        if not cat or not nom: return
        with open("maestro_ejercicios.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([cat, nom])
        nuevo_ej_cat.value = ""
        nuevo_ej_nombre.value = ""
        page.close(dlg_nuevo_ejercicio)
        refrescar_lista_gestion()
        nonlocal DB_EJERCICIOS, lista_categorias
        DB_EJERCICIOS = leer_ejercicios()
        lista_categorias = list(DB_EJERCICIOS.keys())
        dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        rm_dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        page.snack_bar = ft.SnackBar(ft.Text("Ejercicio Creado"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()

    dlg_nuevo_ejercicio = ft.AlertDialog(title=ft.Text("Nuevo Ejercicio"), content=ft.Column([nuevo_ej_cat, nuevo_ej_nombre], height=150), actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_nuevo_ejercicio)), ft.ElevatedButton("Guardar", on_click=guardar_nuevo_ejercicio)])
    
    edit_ej_cat = ft.TextField(label="Categoría")
    edit_ej_nom = ft.TextField(label="Nombre")
    
    def guardar_edicion_maestro(e):
        filas = []
        with open("maestro_ejercicios.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas = list(reader)
        for i in range(len(filas)):
            if filas[i][0] == categoria_a_editar_original and filas[i][1] == ejercicio_a_editar_original:
                filas[i] = [edit_ej_cat.value, edit_ej_nom.value]
                break
        with open("maestro_ejercicios.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(filas)
        page.close(dlg_editar_ejercicio)
        refrescar_lista_gestion()
        nonlocal DB_EJERCICIOS, lista_categorias
        DB_EJERCICIOS = leer_ejercicios()
        lista_categorias = list(DB_EJERCICIOS.keys())
        dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        rm_dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        page.update()

    dlg_editar_ejercicio = ft.AlertDialog(title=ft.Text("Editar Ejercicio"), content=ft.Column([edit_ej_cat, edit_ej_nom], height=150), actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_editar_ejercicio)), ft.ElevatedButton("Guardar", on_click=guardar_edicion_maestro)])

    def abrir_editar_ejercicio(e):
        nonlocal ejercicio_a_editar_original, categoria_a_editar_original
        data = e.control.data
        categoria_a_editar_original = data["cat"]
        ejercicio_a_editar_original = data["nom"]
        edit_ej_cat.value = categoria_a_editar_original
        edit_ej_nom.value = ejercicio_a_editar_original
        page.open(dlg_editar_ejercicio)

    def eliminar_ejercicio_maestro(e):
        data = e.control.data
        filas = []
        with open("maestro_ejercicios.csv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas = list(reader)
        filas_nuevas = [row for row in filas if not (row[0] == data["cat"] and row[1] == data["nom"])]
        with open("maestro_ejercicios.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(filas_nuevas)
        refrescar_lista_gestion()
        nonlocal DB_EJERCICIOS, lista_categorias
        DB_EJERCICIOS = leer_ejercicios()
        lista_categorias = list(DB_EJERCICIOS.keys())
        dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        rm_dd_categoria.options = [ft.dropdown.Option(c) for c in lista_categorias]
        page.update()

    refrescar_lista_gestion()

    vista_ejercicios = ft.Container(content=ft.Column([ft.Text("Gestión de Ejercicios", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), ft.ElevatedButton("Nuevo Ejercicio", icon=ft.Icons.ADD, on_click=lambda e: page.open(dlg_nuevo_ejercicio), bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE), ft.Divider(), lista_gestion_ejercicios], expand=True), padding=20, expand=True)

    # --- MAIN TABS ---
    tab_inicio = ft.Tab(text="Inicio", icon=ft.Icons.HOME, content=vista_inicio)
    mis_tabs = ft.Tabs(selected_index=0, animation_duration=300, tab_alignment=ft.TabAlignment.CENTER, tabs=[tab_inicio, ft.Tab(text="Entrenar", icon=ft.Icons.FITNESS_CENTER, content=vista_entrenar), ft.Tab(text="Récords", icon=ft.Icons.EMOJI_EVENTS, content=vista_records), ft.Tab(text="Historial", icon=ft.Icons.HISTORY, content=vista_historial), ft.Tab(text="Ejercicios", icon=ft.Icons.LIST, content=vista_ejercicios)], expand=True)

    def iniciar_app(e):
        mis_tabs.tabs.pop(0) 
        mis_tabs.selected_index = 0 
        page.update()

    vista_inicio.content.controls.append(ft.ElevatedButton("Comenzar", on_click=iniciar_app, bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE))

    page.add(mis_tabs)

    while True:
        if switch_crono.value:
            mins, secs = divmod(segundos, 60)
            texto_cronometro.value = "{:02d}:{:02d}".format(mins, secs)
            page.update()
            await asyncio.sleep(1)
            segundos += 1
        else:
            await asyncio.sleep(0.1)

# --- AL FINAL DEL ARCHIVO ---

ft.app(target=main)