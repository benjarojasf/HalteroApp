import flet as ft
import asyncio
import datetime
import csv
import os
import time
import math 

# --- LISTA MAESTRA (V33) ---
EJERCICIOS_BASE = [
    ("Olímpico - Competencia", "Snatch (Arrancada)"),
    ("Olímpico - Competencia", "Clean & Jerk (Envión)"),
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
    # --- CONFIGURACIÓN ---
    page.title = "Haltero Tracker"
    page.padding = 0 
    page.scroll = None 
    
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, use_material3=True)
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.bgcolor = ft.Colors.WHITE

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

    # Variables para filtros de gráfico
    filtro_peso_min = None
    filtro_peso_max = None

    # ==========================================
    #   CONFIGURACIÓN / BACKUP (POPUP)
    # ==========================================
    
    def abrir_dialogo_datos(e):
        contenido_actual = ""
        if os.path.isfile("historial_entrenamientos.csv"):
            with open("historial_entrenamientos.csv", "r", encoding="utf-8") as f:
                contenido_actual = f.read()
        txt_backup.value = contenido_actual
        page.open(dlg_backup)

    def copiar_al_portapapeles(e):
        page.set_clipboard(txt_backup.value)
        page.snack_bar = ft.SnackBar(ft.Text("¡Datos copiados al portapapeles!"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.update()

    def guardar_importacion(e):
        nuevos_datos = txt_backup.value
        if nuevos_datos.strip():
            with open("historial_entrenamientos.csv", "w", encoding="utf-8") as f:
                f.write(nuevos_datos)
            
            page.close(dlg_backup)
            page.snack_bar = ft.SnackBar(ft.Text("Datos importados correctamente"), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
            
            actualizar_historial(None)
            actualizar_tabla_records()
            actualizar_grafico(None)
            page.update()

    txt_backup = ft.TextField(
        multiline=True, 
        min_lines=10, 
        max_lines=10, 
        text_size=10, 
        label="Datos CSV"
    )

    btn_copiar_datos = ft.IconButton(
        icon=ft.Icons.COPY, 
        tooltip="Copiar todo al portapapeles",
        on_click=copiar_al_portapapeles
    )

    dlg_backup = ft.AlertDialog(
        title=ft.Row([ft.Text("Gestión de Datos"), btn_copiar_datos], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        content=ft.Column([
            ft.Text("Respalda tus datos copiando este texto, o pega un respaldo anterior para restaurar.", size=12, color=ft.Colors.GREY),
            txt_backup,
        ], height=300, width=300),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_backup)),
            ft.ElevatedButton("Importar", on_click=guardar_importacion, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
        ]
    )

    switch_tema = ft.Switch(label="Modo Oscuro", value=False, disabled=True, tooltip="Próximamente")
    
    dlg_configuraciones = ft.AlertDialog(
        title=ft.Text("Opciones"),
        content=ft.Column([
            ft.Text("Apariencia", weight=ft.FontWeight.BOLD),
            switch_tema,
            ft.Divider(),
            ft.Text("Datos", weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Respaldar / Importar Datos", icon=ft.Icons.SAVE_ALT, on_click=abrir_dialogo_datos, bgcolor=ft.Colors.BLUE_GREY_100, color=ft.Colors.BLACK)
        ], height=200, width=300),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_configuraciones))]
    )

    # ==========================================
    #   VISTA INICIO
    # ==========================================
    vista_inicio = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.FITNESS_CENTER, size=120, color=ft.Colors.BLACK),
                ft.Text("Haltero Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Text("v57.0", size=16, color=ft.Colors.GREY),
                ft.Container(height=20),
                ft.Container(height=30),
                ft.IconButton(icon=ft.Icons.SETTINGS, icon_size=30, tooltip="Configuración", on_click=lambda e: page.open(dlg_configuraciones))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )

    # ==========================================
    #   PESTAÑA 1: ENTRENAMIENTO
    # ==========================================

    def cambiar_fecha(e):
        campo_fecha_texto.value = date_picker.value.strftime("%d-%m-%Y")
        page.update()

    date_picker = ft.DatePicker(on_change=cambiar_fecha)
    btn_calendario = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.PRIMARY, on_click=lambda _: page.open(date_picker))
    campo_fecha_texto = ft.TextField(value=fecha_hoy_txt, width=120, read_only=True, text_align=ft.TextAlign.CENTER, border=ft.InputBorder.NONE, text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    texto_cronometro = ft.Text(value="00:00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
    
    contenedor_crono_display = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.TIMER, color=ft.Colors.BLACK, size=20), texto_cronometro], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
        padding=5,
        border_radius=5,
        bgcolor=ft.Colors.BLUE_50,
        visible=False 
    )

    def cambiar_estado_crono(e):
        nonlocal contando, segundos
        contando = switch_crono.value
        contenedor_crono_display.visible = switch_crono.value
        if not switch_crono.value:
            segundos = 0
            texto_cronometro.value = "00:00"
        page.update()

    switch_crono = ft.Switch(label="Crono", value=False, on_change=cambiar_estado_crono)

    async def resetear_cronometro():
        nonlocal segundos
        if switch_crono.value:
            segundos = 0
            texto_cronometro.value = "00:00"
            texto_cronometro.color = ft.Colors.GREEN
            page.update()
            await asyncio.sleep(0.5)
            texto_cronometro.color = ft.Colors.BLACK
            page.update()

    lista_series = ft.ListView(expand=True, spacing=10, padding=20)
    
    campo_kilos = ft.TextField(label="Kilos", width=80, keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.PRIMARY, text_align=ft.TextAlign.CENTER, content_padding=5)
    campo_reps = ft.TextField(label="Reps", width=80, keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.PRIMARY, text_align=ft.TextAlign.CENTER, content_padding=5)

    # --- CORRECCIÓN DEFINITIVA AQUI ---
    def ajustar_kilos(delta):
        try: valor_actual = float(campo_kilos.value) if campo_kilos.value else 0
        except ValueError: valor_actual = 0
        
        nuevo_val = max(0, valor_actual + delta)
        
        # AQUI ESTABA EL ERROR (new_val vs nuevo_val)
        if nuevo_val.is_integer():
            campo_kilos.value = str(int(nuevo_val))
        else:
            campo_kilos.value = str(nuevo_val)
        page.update()

    def ajustar_reps(delta):
        try: valor_actual = int(campo_reps.value) if campo_reps.value else 0
        except ValueError: valor_actual = 0
        
        nuevo_val = max(0, valor_actual + delta)
        campo_reps.value = str(nuevo_val)
        page.update()

    input_kilos_group = ft.Row(
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: ajustar_kilos(-1), icon_color=ft.Colors.RED, icon_size=24),
            campo_kilos,
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: ajustar_kilos(1), icon_color=ft.Colors.GREEN, icon_size=24),
        ], 
        spacing=0, alignment=ft.MainAxisAlignment.CENTER
    )

    input_reps_group = ft.Row(
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: ajustar_reps(-1), icon_color=ft.Colors.RED, icon_size=24),
            campo_reps,
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: ajustar_reps(1), icon_color=ft.Colors.GREEN, icon_size=24),
        ],
        spacing=0, alignment=ft.MainAxisAlignment.CENTER
    )
    
    dd_ejercicio = ft.Dropdown(label="Ejercicio", width=float('inf'), disabled=True, options=[])

    def cambio_categoria(e):
        cat_selec = dd_categoria.value
        if cat_selec in DB_EJERCICIOS:
            opciones = [ft.dropdown.Option(nombre) for nombre in DB_EJERCICIOS[cat_selec]]
            dd_ejercicio.options = opciones
            dd_ejercicio.value = opciones[0].key 
            dd_ejercicio.disabled = False
        page.update()

    dd_categoria = ft.Dropdown(label="Categoría", width=float('inf'), options=[ft.dropdown.Option(c) for c in lista_categorias], on_change=cambio_categoria)
    
    contenedor_setup_inicial = ft.Column(
        controls=[
            ft.Row([ft.Text("Fecha:", weight=ft.FontWeight.BOLD, size=16), btn_calendario, campo_fecha_texto], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            dd_categoria,
            dd_ejercicio
        ],
        spacing=10, visible=True
    )
    
    texto_resumen_activo = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800, no_wrap=True, overflow=ft.TextOverflow.ELLIPSIS)
    contenedor_resumen_activo = ft.Container(
        content=ft.Row([ft.Icon(ft.Icons.FITNESS_CENTER_OUTLINED, size=20), ft.Container(content=texto_resumen_activo, expand=True)], alignment=ft.MainAxisAlignment.CENTER),
        padding=10, bgcolor=ft.Colors.BLUE_50, border_radius=5, visible=False
    )

    def resetear_interfaz_entrenamiento():
        nonlocal numero_serie_global, segundos
        lista_series.controls.clear()
        numero_serie_global = 1
        segundos = 0
        texto_cronometro.value = "00:00"
        switch_crono.value = False
        contenedor_crono_display.visible = False
        campo_kilos.value = ""
        campo_reps.value = ""
        contenedor_setup_inicial.visible = True
        contenedor_resumen_activo.visible = False
        dd_categoria.value = None
        dd_categoria.disabled = False
        dd_ejercicio.value = None
        dd_ejercicio.disabled = True
        dd_ejercicio.options = []

    def finalizar_entrenamiento(e):
        if len(lista_series.controls) == 0:
            page.snack_bar = ft.SnackBar(ft.Text("No hay series para guardar"))
            page.snack_bar.open = True
            page.update()
            return
        nombre_archivo = "historial_entrenamientos.csv"
        archivo_existe = os.path.isfile(nombre_archivo)
        with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not archivo_existe: writer.writerow(["Fecha", "N_Serie", "Ejercicio", "Kilos", "Reps", "Sensacion"])
            for tarjeta in reversed(lista_series.controls):
                datos = tarjeta.data
                writer.writerow([campo_fecha_texto.value, datos["numero"], datos["ejercicio"], datos["kilos"], datos["reps"], datos["sensacion"]])
        page.snack_bar = ft.SnackBar(ft.Text(f"¡Entrenamiento Guardado!"), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        resetear_interfaz_entrenamiento()
        actualizar_historial(None)
        actualizar_tabla_records() 
        actualizar_grafico(None)
        page.update()

    def cancelar_entrenamiento(e):
        resetear_interfaz_entrenamiento()
        page.snack_bar = ft.SnackBar(ft.Text("Cancelado"), bgcolor=ft.Colors.RED)
        page.snack_bar.open = True
        page.update()

    def agregar_serie(e):
        nonlocal numero_serie_global
        if not campo_kilos.value or not campo_reps.value or not dd_ejercicio.value: return 
        
        if contenedor_setup_inicial.visible:
            contenedor_setup_inicial.visible = False
            contenedor_resumen_activo.visible = True
            texto_resumen_activo.value = f"{dd_ejercicio.value}"
            page.update()

        mi_numero_serie = numero_serie_global
        val_kilos = campo_kilos.value
        val_reps = campo_reps.value
        val_ejercicio = dd_ejercicio.value 

        edit_kilos = ft.TextField(label="Kilos", value=val_kilos)
        edit_reps = ft.TextField(label="Reps", value=val_reps)
        
        texto_info_serie = ft.Text(f"{val_kilos} kg x {val_reps} reps", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK, expand=True, text_align=ft.TextAlign.CENTER)

        def guardar_edicion(e):
            texto_info_serie.value = f"{edit_kilos.value} kg x {edit_reps.value} reps"
            nueva_tarjeta.data["kilos"] = edit_kilos.value
            nueva_tarjeta.data["reps"] = edit_reps.value
            page.close(dlg_edit)
            page.update()
        
        def borrar_tarjeta(e):
            lista_series.controls.remove(nueva_tarjeta)
            page.update()

        dlg_edit = ft.AlertDialog(title=ft.Text("Editar"), content=ft.Column([edit_kilos, edit_reps], height=150), actions=[ft.TextButton("Guardar", on_click=guardar_edicion)])

        for tarjeta in lista_series.controls:
            tarjeta.border = ft.border.all(1, ft.Colors.GREY_200)
            try:
                tarjeta.content.controls[0].controls[0].color = ft.Colors.GREY_500
                tarjeta.content.controls[0].controls[1].content.color = ft.Colors.GREY_500
            except: pass

        async def click_sensacion(e):
            for btn in [btn_bien, btn_regular, btn_mal, btn_nulo]:
                btn.bgcolor = ft.Colors.TRANSPARENT
                btn.color = ft.Colors.BLACK
            
            sensacion = e.control.text
            if sensacion == "Bien": e.control.bgcolor = ft.Colors.GREEN_400; e.control.color = ft.Colors.WHITE
            elif sensacion == "Regular": e.control.bgcolor = ft.Colors.ORANGE_400; e.control.color = ft.Colors.WHITE
            elif sensacion == "Mal": e.control.bgcolor = ft.Colors.RED_400; e.control.color = ft.Colors.WHITE
            elif sensacion == "Nulo": e.control.bgcolor = ft.Colors.GREY_800; e.control.color = ft.Colors.WHITE
            nueva_tarjeta.data["sensacion"] = sensacion
            page.update()
            if mi_numero_serie == (numero_serie_global - 1): await resetear_cronometro()

        estilo_btn = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=5)
        btn_bien = ft.ElevatedButton("Bien", on_click=click_sensacion, bgcolor=ft.Colors.GREEN_100, color=ft.Colors.BLACK, style=estilo_btn, expand=1)
        btn_regular = ft.ElevatedButton("Regular", on_click=click_sensacion, bgcolor=ft.Colors.ORANGE_100, color=ft.Colors.BLACK, style=estilo_btn, expand=1)
        btn_mal = ft.ElevatedButton("Mal", on_click=click_sensacion, bgcolor=ft.Colors.RED_100, color=ft.Colors.BLACK, style=estilo_btn, expand=1)
        btn_nulo = ft.ElevatedButton("Nulo", icon=ft.Icons.FLAG, icon_color=ft.Colors.RED, on_click=click_sensacion, bgcolor=ft.Colors.GREY_200, color=ft.Colors.BLACK, style=estilo_btn, expand=1)

        nueva_tarjeta = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Serie #{mi_numero_serie}", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Container(
                        content=texto_info_serie,
                        expand=True,
                        alignment=ft.alignment.center
                    ),
                    ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE_GREY, icon_size=20, on_click=lambda _: page.open(dlg_edit)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, icon_size=20, on_click=borrar_tarjeta)
                    ], spacing=0)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                ft.Row([btn_bien, btn_regular, btn_mal, btn_nulo], spacing=5)
            ]),
            padding=10, 
            border=ft.border.all(1, ft.Colors.BLACK), 
            border_radius=10, 
            bgcolor=ft.Colors.WHITE, 
            data={"numero": mi_numero_serie, "ejercicio": val_ejercicio, "kilos": val_kilos, "reps": val_reps, "sensacion": "Sin calificar"}
        )

        lista_series.controls.insert(0, nueva_tarjeta)
        
        numero_serie_global += 1
        campo_kilos.focus()
        page.update()

    btn_agregar = ft.ElevatedButton("Agregar", icon=ft.Icons.ADD, on_click=agregar_serie, bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE, height=45)
    
    fila_accion_entrenar = ft.Row(
        controls=[
            switch_crono,
            ft.Container(
                content=contenedor_crono_display, 
                alignment=ft.alignment.center, 
                expand=True
            ),
            btn_agregar
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    btn_finalizar_block = ft.ElevatedButton(text="FINALIZAR EJERCICIO", bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE, on_click=finalizar_entrenamiento, expand=True, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))
    btn_cancelar_icon = ft.IconButton(icon=ft.Icons.DELETE_FOREVER, icon_color=ft.Colors.RED, icon_size=30, tooltip="Cancelar Entrenamiento", on_click=cancelar_entrenamiento)
    fila_botones_footer = ft.Row(controls=[btn_cancelar_icon, btn_finalizar_block], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)
    seccion_footer = ft.Container(content=ft.Column(controls=[fila_botones_footer], spacing=10), bgcolor=ft.Colors.WHITE, padding=10, border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_300)))
    
    header = ft.Container(
        padding=15,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(controls=[
            contenedor_setup_inicial,
            contenedor_resumen_activo,
            ft.Divider(height=5, thickness=1),
            ft.Row([input_kilos_group, input_reps_group], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Container(height=10),
            fila_accion_entrenar,
            ft.Divider(height=1, thickness=1),
        ])
    )

    vista_entrenar = ft.Column(controls=[header, lista_series, seccion_footer], expand=True, spacing=0)

    # --- PESTAÑA RÉCORDS ---
    def cambiar_fecha_rm(e):
        campo_fecha_rm.value = date_picker_rm.value.strftime("%d-%m-%Y")
        page.update()
    date_picker_rm = ft.DatePicker(on_change=cambiar_fecha_rm, first_date=datetime.datetime(2020, 1, 1), last_date=datetime.datetime(2030, 12, 31))
    campo_fecha_rm = ft.TextField(value=fecha_hoy_txt, width=120, read_only=True, label="Fecha RM", text_style=ft.TextStyle(size=14))
    btn_calendario_rm = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.PRIMARY, on_click=lambda _: page.open(date_picker_rm))
    rm_dd_ejercicio = ft.Dropdown(label="Ejercicio", width=float('inf'), disabled=True)
    def rm_cambio_categoria(e):
        cat_selec = rm_dd_categoria.value
        if cat_selec in DB_EJERCICIOS:
            opciones = [ft.dropdown.Option(nombre) for nombre in DB_EJERCICIOS[cat_selec]]
            rm_dd_ejercicio.options = opciones
            rm_dd_ejercicio.value = opciones[0].key 
            rm_dd_ejercicio.disabled = False
        page.update()
    rm_dd_categoria = ft.Dropdown(label="Categoría", width=float('inf'), options=[ft.dropdown.Option(c) for c in lista_categorias], on_change=rm_cambio_categoria)
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
        actualizar_grafico(None)
        page.update()
    dlg_nuevo_rm = ft.AlertDialog(title=ft.Text("Nuevo Récord Manual"), content=ft.Column([ft.Row([btn_calendario_rm, campo_fecha_rm]), rm_dd_categoria, rm_dd_ejercicio, rm_campo_kilos], height=280, width=300), actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_nuevo_rm)), ft.ElevatedButton("Guardar RM", on_click=guardar_rm_manual, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)])
    tabla_records = ft.DataTable(columns=[ft.DataColumn(ft.Text("Ejercicio", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)), ft.DataColumn(ft.Text("Max (Kg)", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), numeric=True), ft.DataColumn(ft.Text("Antigüedad", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), numeric=True)], rows=[], width=float('inf'), heading_row_height=40, column_spacing=30)
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
                        if len(row) < 6: continue # Protección
                        ejercicio, kilos, sensacion, fecha_str = row[2], float(row[3]), row[5], row[0]
                        if sensacion.strip() == "Nulo": continue
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
    vista_records = ft.Container(content=ft.Column([ft.Text("Mis Récords Actuales", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), ft.Divider(), ft.ElevatedButton("Ingresar Nuevo RM", on_click=lambda e: page.open(dlg_nuevo_rm), bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE), ft.Divider(color=ft.Colors.TRANSPARENT, height=20), ft.Column([tabla_records], scroll=ft.ScrollMode.AUTO, expand=True)], expand=True), padding=20, expand=True)

    # --- PESTAÑA GRÁFICOS (SCATTER SECUENCIAL FINAL) ---
    dropdown_filtro_grafico = ft.Dropdown(label="Selecciona Ejercicio", width=float('inf'), options=[ft.dropdown.Option("Todos")], value="Todos", on_change=lambda e: actualizar_grafico(e))
    # Padding bottom para el grafico y labels
    chart_container = ft.Container(height=350, bgcolor=ft.Colors.WHITE, padding=ft.padding.only(top=10, left=10, right=20, bottom=60), border_radius=10, border=ft.border.all(1, ft.Colors.GREY_200))
    
    tabla_mapeo_fechas = ft.DataTable(columns=[ft.DataColumn(ft.Text("N°", weight=ft.FontWeight.BOLD)), ft.DataColumn(ft.Text("Fecha del Entrenamiento", weight=ft.FontWeight.BOLD))], rows=[], width=float('inf'), heading_row_height=30)
    contenedor_mapeo = ft.Container(content=ft.Column([ft.Text("Referencias de Fecha:", weight=ft.FontWeight.BOLD, size=12), tabla_mapeo_fechas], scroll=ft.ScrollMode.AUTO, height=150), padding=10, bgcolor=ft.Colors.GREY_50, border_radius=5, border=ft.border.all(1, ft.Colors.GREY_300))

    txt_peso_min = ft.TextField(label="Min Kg", width=80, keyboard_type=ft.KeyboardType.NUMBER, text_style=ft.TextStyle(size=12)); txt_peso_max = ft.TextField(label="Max Kg", width=80, keyboard_type=ft.KeyboardType.NUMBER, text_style=ft.TextStyle(size=12))
    
    def aplicar_filtros_grafico(e):
        nonlocal filtro_peso_min, filtro_peso_max
        try: filtro_peso_min = float(txt_peso_min.value) if txt_peso_min.value else None
        except: filtro_peso_min = None
        try: filtro_peso_max = float(txt_peso_max.value) if txt_peso_max.value else None
        except: filtro_peso_max = None
        actualizar_grafico(None)
    
    def limpiar_filtros_grafico(e):
        nonlocal filtro_peso_min, filtro_peso_max
        filtro_peso_min = None; filtro_peso_max = None
        txt_peso_min.value = ""; txt_peso_max.value = ""
        actualizar_grafico(None)

    controles_filtro = ft.ExpansionTile(
        title=ft.Text("Configuración de Ejes", size=14, weight=ft.FontWeight.BOLD),
        initially_expanded=False, 
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Kg:", size=12), txt_peso_min, txt_peso_max, 
                        ft.ElevatedButton("Aplicar", on_click=aplicar_filtros_grafico, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE, height=35, width=80, style=ft.ButtonStyle(padding=0)),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Limpiar Filtros", icon_color=ft.Colors.RED, on_click=limpiar_filtros_grafico)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], spacing=10),
                padding=10
            )
        ],
        bgcolor=ft.Colors.GREY_50
    )

    def actualizar_grafico(e):
        nombre_archivo = "historial_entrenamientos.csv"
        ejercicio_seleccionado = dropdown_filtro_grafico.value
        ejercicios_disp = set()
        if os.path.isfile(nombre_archivo):
            try:
                with open(nombre_archivo, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)
                    rows = list(reader)
                    for row in rows:
                        if len(row) >= 6: ejercicios_disp.add(row[2])
            except: pass
        nuevas_ops = []
        for ej in sorted(list(ejercicios_disp)): nuevas_ops.append(ft.dropdown.Option(ej))
        sel_actual = dropdown_filtro_grafico.value
        dropdown_filtro_grafico.options = nuevas_ops
        if sel_actual in [op.key for op in nuevas_ops]: dropdown_filtro_grafico.value = sel_actual
        elif nuevas_ops: dropdown_filtro_grafico.value = nuevas_ops[0].key; ejercicio_seleccionado = nuevas_ops[0].key
        if not ejercicio_seleccionado or not os.path.isfile(nombre_archivo):
            chart_container.content = ft.Text("Sin datos", color=ft.Colors.GREY)
            if page: page.update()
            return
        puntos_bien, puntos_regular, puntos_mal, puntos_nulo, puntos_sin_calif = [], [], [], [], []
        max_historico = 0
        conteo_por_fecha = {}
        todos_timestamps = []
        fechas_unicas = set()
        rows_filtradas = []

        try:
             with open(nombre_archivo, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)
                all_rows = list(reader)
                for row in all_rows:
                    if len(row) < 6: continue
                    if row[2] == ejercicio_seleccionado:
                        try:
                            peso = float(row[3])
                            sensacion = row[5].strip()
                            if row[1] != "RM" and sensacion != "Nulo":
                                if peso > max_historico: max_historico = peso
                        except: pass

                        if row[1] != "RM":
                            try:
                                peso = float(row[3])
                                if filtro_peso_min is not None and peso < filtro_peso_min: continue
                                if filtro_peso_max is not None and peso > filtro_peso_max: continue
                                rows_filtradas.append(row)
                                fechas_unicas.add(row[0])
                            except: pass
        except: pass

        if not rows_filtradas:
            chart_container.content = ft.Text("No hay datos", color=ft.Colors.GREY); page.update(); return

        fechas_objs = []
        for f in fechas_unicas:
            try: fechas_objs.append(datetime.datetime.strptime(f, "%d-%m-%Y"))
            except: pass
        fechas_objs.sort()
        mapa_fecha_indice = {}
        tabla_mapeo_rows = []
        for i, f_obj in enumerate(fechas_objs):
            idx = i + 1
            f_str = f_obj.strftime("%d-%m-%Y")
            mapa_fecha_indice[f_str] = idx
            tabla_mapeo_rows.insert(0, ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(f_str))]))
        tabla_mapeo_fechas.rows = tabla_mapeo_rows
        
        conteo_series_dia = {} 
        for row in rows_filtradas:
            fecha_str = row[0]
            idx_entrenamiento = mapa_fecha_indice.get(fecha_str)
            if idx_entrenamiento is None: continue
            count = conteo_series_dia.get(fecha_str, 0)
            conteo_series_dia[fecha_str] = count + 1
            x_final = float(idx_entrenamiento) + (count * 0.08) 
            try:
                peso = float(row[3])
                sensacion = row[5].strip()
                point = ft.LineChartDataPoint(x=x_final, y=peso, tooltip=f"#{idx_entrenamiento} ({fecha_str}): {int(peso)}kg")
                if sensacion == "Bien": puntos_bien.append(point)
                elif sensacion == "Regular": puntos_regular.append(point)
                elif sensacion == "Mal": puntos_mal.append(point)
                elif sensacion == "Nulo": puntos_nulo.append(point)
                else: puntos_sin_calif.append(point)
            except: pass

        min_x = 1
        max_x = len(fechas_unicas) + 1 
        series_chart = []

        # LINEAS DE REFERENCIA (Segmentadas)
        if max_historico > 0:
            series_chart.append(ft.LineChartData(data_points=[ft.LineChartDataPoint(x=min_x, y=max_historico), ft.LineChartDataPoint(x=max_x, y=max_historico, tooltip="100%")], color=ft.Colors.BLUE_900, stroke_width=3, dash_pattern=[5, 5], point=False))
            series_chart.append(ft.LineChartData(data_points=[ft.LineChartDataPoint(x=min_x, y=max_historico*0.85), ft.LineChartDataPoint(x=max_x, y=max_historico*0.85, tooltip="85%")], color=ft.Colors.BLUE_700, stroke_width=2, dash_pattern=[5, 5], point=False))
            series_chart.append(ft.LineChartData(data_points=[ft.LineChartDataPoint(x=min_x, y=max_historico*0.70), ft.LineChartDataPoint(x=max_x, y=max_historico*0.70, tooltip="70%")], color=ft.Colors.BLUE_400, stroke_width=2, dash_pattern=[5, 5], point=False))
            series_chart.append(ft.LineChartData(data_points=[ft.LineChartDataPoint(x=min_x, y=max_historico*0.50), ft.LineChartDataPoint(x=max_x, y=max_historico*0.50, tooltip="50%")], color=ft.Colors.BLUE_200, stroke_width=2, dash_pattern=[5, 5], point=False))

        # PUNTOS
        if puntos_bien: series_chart.append(ft.LineChartData(data_points=puntos_bien, color=ft.Colors.GREEN, stroke_width=0, point=True))
        if puntos_regular: series_chart.append(ft.LineChartData(data_points=puntos_regular, color=ft.Colors.AMBER, stroke_width=0, point=True))
        if puntos_mal: series_chart.append(ft.LineChartData(data_points=puntos_mal, color=ft.Colors.RED, stroke_width=0, point=True))
        if puntos_nulo: series_chart.append(ft.LineChartData(data_points=puntos_nulo, color=ft.Colors.RED, stroke_width=0, point=True))
        if puntos_sin_calif: series_chart.append(ft.LineChartData(data_points=puntos_sin_calif, color=ft.Colors.GREY, stroke_width=0, point=True))

        chart = ft.LineChart(
            data_series=series_chart,
            min_x=min_x, max_x=max_x,
            min_y=filtro_peso_min if filtro_peso_min is not None else 0,
            max_y=filtro_peso_max if filtro_peso_max is not None else None,
            border=ft.border.all(1, ft.Colors.TRANSPARENT),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Kg"), title_size=20),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("N° Entrenamiento"), title_size=20,
                labels_interval=1,
                labels_size=30
            ),
            tooltip_bgcolor=ft.Colors.BLACK,
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.BLACK12, width=1),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.BLACK12, width=1),
            expand=True
        )
        chart_container.content = chart
        if page: page.update()

    actualizar_grafico(None)

    vista_graficos = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("Progreso de Cargas", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                dropdown_filtro_grafico,
                ft.Divider(),
                chart_container,
                 ft.Row([
                    ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREEN, size=12), ft.Text("Bien", size=12),
                    ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.AMBER, size=12), ft.Text("Reg", size=12),
                    ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.RED, size=12), ft.Text("Mal/Nulo", size=12),
                ], alignment=ft.MainAxisAlignment.CENTER),
                 ft.Text("* Las líneas indican: Máximo Histórico, 85%, 70% y 50% del RM", size=11, color=ft.Colors.GREY_600, italic=True),
                 ft.Container(height=10),
                 ft.Text("Referencias de Fecha:", size=12, weight=ft.FontWeight.BOLD),
                 contenedor_mapeo
            ], expand=True, scroll=ft.ScrollMode.AUTO),
            padding=20, expand=True
        ),
        ft.Divider(thickness=5, color=ft.Colors.GREY_100),
        ft.Container(content=controles_filtro, padding=10, bgcolor=ft.Colors.GREY_50)
    ], expand=True, spacing=0)

    # --- 4. PESTAÑA HISTORIAL ---
    dropdown_filtro_historial = ft.Dropdown(label="Filtrar por ejercicio", width=float('inf'), options=[ft.dropdown.Option("Todos")], value="Todos", on_change=lambda e: actualizar_historial(e), content_padding=10)
    columna_historial = ft.ListView(expand=True, spacing=15, padding=20)
    hist_edit_kilos = ft.TextField(label="Kilos")
    hist_edit_reps = ft.TextField(label="Reps")
    hist_edit_sens = ft.Dropdown(label="Sensación", options=[ft.dropdown.Option("Bien"), ft.dropdown.Option("Regular"), ft.dropdown.Option("Mal"), ft.dropdown.Option("Nulo")])
    contenido_detalle = ft.Column(scroll=ft.ScrollMode.AUTO)
    dlg_detalle_ejercicio = ft.AlertDialog(title=ft.Text("Detalle del Entrenamiento", color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD), content=ft.Container(content=contenido_detalle, height=300, width=350), bgcolor=ft.Colors.WHITE, actions=[ft.TextButton("Cerrar", on_click=lambda e: page.close(dlg_detalle_ejercicio))])
    def recargar_detalle_popup():
        if not detalle_fecha_actual or not detalle_ejercicio_actual: return
        nombre_archivo = "historial_entrenamientos.csv"
        if not os.path.isfile(nombre_archivo): return
        filas_coincidentes = []
        with open(nombre_archivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            filas_totales = list(reader)
            for i in range(1, len(filas_totales)):
                if len(filas_totales[i]) < 6: continue # PROTECCION INDEX
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
        contenido_detalle.controls.append(ft.DataTable(columns=[ft.DataColumn(ft.Text("Kg", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)), ft.DataColumn(ft.Text("Reps", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)), ft.DataColumn(ft.Text("Sens.", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK))], rows=filas_tabla_detalle, column_spacing=20, width=float('inf'), show_checkbox_column=False, heading_row_color=ft.Colors.GREY_100))
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
        actualizar_grafico(None)
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
        page.snack_bar = ft.SnackBar(ft.Text("Registro eliminado"), bgcolor=ft.Colors.RED)
        page.snack_bar.open = True
        actualizar_historial(None)
        actualizar_tabla_records()
        actualizar_grafico(None)
        recargar_detalle_popup()
    dlg_historial_opciones = ft.AlertDialog(title=ft.Text("Editar Serie"), content=ft.Column([ft.Text("Modifica o elimina esta serie:", size=12, color=ft.Colors.GREY), hist_edit_kilos, hist_edit_reps, hist_edit_sens], height=250, width=300), actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_historial_opciones)), ft.TextButton("Eliminar", on_click=eliminar_registro_historial, style=ft.ButtonStyle(color=ft.Colors.RED)), ft.ElevatedButton("Guardar", on_click=guardar_cambios_historial, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)], actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
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

    # --- MAIN TABS + SAFEAREA ---
    # Definimos las pestañas aquí
    tab_inicio = ft.Tab(text="Inicio", icon=ft.Icons.HOME, content=vista_inicio)
    mis_tabs = ft.Tabs(selected_index=0, animation_duration=300, tab_alignment=ft.TabAlignment.CENTER, tabs=[tab_inicio, ft.Tab(text="Entrenar", icon=ft.Icons.FITNESS_CENTER, content=vista_entrenar), ft.Tab(text="Gráficos", icon=ft.Icons.SHOW_CHART, content=vista_graficos), ft.Tab(text="Récords", icon=ft.Icons.EMOJI_EVENTS, content=vista_records), ft.Tab(text="Historial", icon=ft.Icons.HISTORY, content=vista_historial), ft.Tab(text="Ejercicios", icon=ft.Icons.LIST, content=vista_ejercicios)], expand=True)
    
    # Inyectamos el botón con la referencia a mis_tabs (ya creada)
    def iniciar_app(e):
        # Cambio de pestaña al índice 1 (Entrenar)
        mis_tabs.selected_index = 1
        page.update()

    # Se agrega el botón de comenzar al contenedor de inicio
    vista_inicio.content.controls.insert(2, ft.ElevatedButton("Comenzar", on_click=iniciar_app, bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE))
    
    # AGREGAMOS LA UI FINAL Y EL UPDATE
    page.add(ft.SafeArea(mis_tabs, expand=True))
    page.update()

    while True:
        if switch_crono.value:
            mins, secs = divmod(segundos, 60)
            texto_cronometro.value = "{:02d}:{:02d}".format(mins, secs)
            page.update()
            await asyncio.sleep(1)
            segundos += 1
        else:
            await asyncio.sleep(0.1)

ft.app(target=main)