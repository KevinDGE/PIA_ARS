# -*- coding: utf-8 -*-
"""Fuente única de datos del PIA. Los tres entregables (PDF, Excel y PowerPoint)
se generan a partir de este archivo para que IDs, niveles, estrategias y
responsables coincidan siempre."""

EMPRESA = "Casino Royale Enterprises"
MATERIA = "Administración de Riesgos de TI"
GRUPO = "061"
UNIVERSIDAD = "Universidad Autónoma de Nuevo León"
FACULTAD = None  # PENDIENTE: no se proporcionó el nombre de la facultad
DOCENTE = "Melissa Jacqueline Mendieta Gonzalez"
FECHA = "04/11/2026"
TITULO = "Plan de Administración de Riesgos de TI"

PENDIENTE = "Pendiente"
INTEGRANTES = [
    ("David Emiliano Rangel Tovar", None),
    ("Fernando Garza Chavez", None),
    ("Kevin Daniel Grimaldo Esquivel", "1997415"),
    ("Alejandro Martinez Moya", None),
    ("Rene Villareal Torres", None),
]

# ---------------------------------------------------------------- escalas
PROBS = ["Alta", "Media", "Baja"]          # de arriba hacia abajo en el mapa
IMPS = ["Bajo", "Medio", "Alto"]           # de izquierda a derecha en el mapa
NIVELES = ["Crítico", "Alto", "Moderado", "Bajo"]

REGLA = {
    ("Alta", "Alto"): "Crítico",
    ("Alta", "Medio"): "Alto", ("Media", "Alto"): "Alto",
    ("Alta", "Bajo"): "Moderado", ("Media", "Medio"): "Moderado", ("Baja", "Alto"): "Moderado",
    ("Media", "Bajo"): "Bajo", ("Baja", "Medio"): "Bajo", ("Baja", "Bajo"): "Bajo",
}


def nivel(p, i):
    return REGLA[(p, i)]


# Colores por nivel (mismos en PDF, Excel y PowerPoint)
COLOR = {"Crítico": "B71C1C", "Alto": "E65100", "Moderado": "F9A825", "Bajo": "2E7D32"}
TEXTO_SOBRE = {"Crítico": "FFFFFF", "Alto": "FFFFFF", "Moderado": "1A1A1A", "Bajo": "FFFFFF"}
TINTE = {"Crítico": "FBE3E3", "Alto": "FDE9DA", "Moderado": "FEF5D6", "Bajo": "E3F1E4"}

ESCALA_PROB = [
    ("Alta", "Se espera que ocurra varias veces al año o la vulnerabilidad ya es conocida y fácil de aprovechar."),
    ("Media", "Puede ocurrir alrededor de una vez al año; hay antecedentes o condiciones que lo facilitan."),
    ("Baja", "Poco probable; requiere condiciones especiales o se espera menos de una vez cada dos o tres años."),
]
ESCALA_IMP = [
    ("Alto", "Detiene el juego o la caja por varias horas, causa pérdidas importantes, sanciones de la autoridad o daño a la reputación."),
    ("Medio", "Afecta un área o sistema por algunas horas, genera pérdidas moderadas o quejas de clientes."),
    ("Bajo", "Efecto local que se resuelve dentro del turno con recursos propios."),
]
# Conversión de la matriz 5x5 de la actividad anterior a la escala 3x3 del PIA
CONVERSION_PROB = [("Casi seguro / Muy probable", "Alta"), ("Posible", "Media"), ("Poco probable / Raro", "Baja")]
CONVERSION_IMP = [("Catastrófico / Mayor", "Alto"), ("Moderado", "Medio"), ("Menor / Insignificante", "Bajo")]

FRECUENCIA_MONITOREO = {
    "Crítico": "Semanal",
    "Alto": "Quincenal",
    "Moderado": "Mensual",
    "Bajo": "Trimestral",
}

# ---------------------------------------------------------------- riesgos
# Campos: id, nombre, corto (para diapositivas), activo, amenaza, vulnerabilidad,
# fuente, categoria, prob, imp, justificacion, estrategia, acciones (lista),
# responsable, recursos, tiempo, origen ("Matriz de riesgos 10/10/2026" o "Nuevo (TI)")
RIESGOS = [
    dict(
        id="R1", nombre="Manipulación de elementos de juego", corto="Manipulación de cartas, dados o ruleta",
        activo="Barajas, dados, fichas y ruletas de las mesas de juego.",
        amenaza="Jugadores o terceros que marcan cartas, introducen dados cargados o alteran la ruleta.",
        vulnerabilidad="Inspección manual sin registro y sin trazabilidad por lote de los elementos de juego.",
        fuente="Externa", categoria="Operativo", prob="Media", imp="Alto",
        justificacion="El control actual depende del criterio de cada crupier y no deja registro, por lo que una alteración puede pasar varios turnos sin detectarse (Media). Cada mesa manipulada genera pagos indebidos, disputas con clientes y observaciones de la autoridad (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Protocolo de inspección por turno con bitácora digital y firma del supervisor de mesa.",
            "Cambio de barajas en cada turno y de dados cada 8 horas, con destrucción documentada.",
            "Inventario de elementos de juego por lote con sello de seguridad.",
            "Revisión por video de manos ganadoras fuera de patrón.",
        ],
        responsable="Gerente de Operaciones de Juego",
        recursos="Supervisores de mesa, lámparas UV y calibradores de dados, bitácora digital, sellos de seguridad.",
        tiempo="Protocolo en 30 días; inventario por lote en 60 días; revisión mensual.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R2", nombre="Colusión empleado-cliente", corto="Acuerdo entre cajero y cliente",
        activo="Efectivo de caja, fichas y registros de pago de premios.",
        amenaza="Cajero que se pone de acuerdo con un cliente para pagos o cambios de fichas indebidos.",
        vulnerabilidad="El mismo cajero atiende por periodos largos a los mismos clientes y no hay alertas automáticas sobre patrones de pago.",
        fuente="Interna", categoria="Financiero", prob="Baja", imp="Alto",
        justificacion="Requiere el acuerdo de dos personas y hay arqueos diarios (Baja). Si ocurre, la pérdida puede repetirse durante semanas y daña la confianza en la caja (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Rotación obligatoria de cajeros entre ventanillas y turnos con calendario semanal.",
            "Reglas de alerta en el sistema de caja: pagos repetidos del mismo cajero al mismo cliente y cambios de fichas sin juego registrado.",
            "Arqueos sorpresa y doble firma en pagos mayores al límite que defina Tesorería.",
            "Línea de denuncia anónima para el personal.",
        ],
        responsable="Gerente de Caja y Tesorería",
        recursos="Calendario de rotación, módulo de reglas del sistema de caja, apoyo de Auditoría Interna.",
        tiempo="Rotación en 15 días; alertas en 60 días; arqueos sorpresa mensuales.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R3", nombre="Intervención en tragamonedas con dispositivos especializados", corto="Alteración de tragamonedas con aparatos",
        activo="Máquinas tragamonedas y su red de comunicación con el sistema de gestión de tragamonedas.",
        amenaza="Personas externas que usan dispositivos electrónicos para alterar sensores, provocar fallas o generar créditos y premios falsos.",
        vulnerabilidad="Modelos con firmware desactualizado, gabinetes sin sensor de apertura conectado a alarma y red de máquinas sin monitoreo de anomalías.",
        fuente="Externa", categoria="Tecnológico", prob="Baja", imp="Alto",
        justificacion="Requiere conocimiento y equipo especializado (Baja). Puede afectar varias máquinas a la vez, generar pérdidas y poner en duda la integridad del juego (Alto). En la matriz 5x5 era Alto; con la escala 3x3 queda en Moderado.",
        estrategia="Mitigar",
        acciones=[
            "Actualizar firmware según los boletines del fabricante.",
            "Sellos y sensores de apertura de gabinete conectados a las alarmas de vigilancia.",
            "Red de tragamonedas aislada y con alertas por créditos o pagos fuera de patrón.",
            "Inspección técnica mensual de las máquinas.",
        ],
        responsable="Jefe de Tecnología de Juego",
        recursos="Técnicos de tragamonedas, soporte del fabricante, sensores de apertura, reglas en el sistema de gestión.",
        tiempo="Firmware en 90 días; sensores en 120 días; inspección mensual.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R4", nombre="Ataque al sistema central de gestión de clientes", corto="Ataque al sistema de clientes y lealtad",
        activo="Sistema de gestión de clientes y lealtad (CRM) y su base de datos.",
        amenaza="Atacante externo que aprovecha fallas del portal web o contraseñas robadas para alterar puntos, saldos o datos.",
        vulnerabilidad="Portal de clientes expuesto a internet y parches que a veces se aplican con retraso.",
        fuente="Externa", categoria="Tecnológico", prob="Baja", imp="Medio",
        justificacion="El sistema ya tiene firewall de aplicaciones web y doble factor para administradores (Baja). Un ataque afectaría puntos y promociones, pero no detendría el juego ni la caja (Medio).",
        estrategia="Aceptar",
        acciones=[
            "Mantener los controles actuales: firewall de aplicaciones web, parches mensuales y escaneo trimestral de vulnerabilidades.",
            "Vigilar las alertas del sistema de monitoreo de seguridad (SIEM).",
            "Plan de contingencia: congelar canjes de puntos y restaurar desde respaldo si hay alteración.",
            "Reevaluar el riesgo cada trimestre o si cambia el sistema.",
        ],
        responsable="Jefe de Desarrollo y Aplicaciones",
        recursos="Herramientas actuales (firewall de aplicaciones, SIEM, escáner); sin inversión adicional.",
        tiempo="Revisión trimestral; contingencia activable en 1 hora.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R5", nombre="Punto ciego o falla temporal en la vigilancia de la sala principal", corto="Falla o punto ciego en cámaras",
        activo="Sistema de videovigilancia: cámaras, grabadores y software de gestión de video.",
        amenaza="Fallas de cámaras, pérdida de señal o mantenimiento que dejan zonas sin grabación.",
        vulnerabilidad="Cámaras con muchos años de uso, cobertura no revisada después de mover mesas y sin alertas automáticas de pérdida de señal.",
        fuente="Interna", categoria="Operativo", prob="Alta", imp="Bajo",
        justificacion="Las fallas breves y los huecos de cobertura se presentan con frecuencia (Alta). Una falla aislada tiene efecto limitado porque hay personal en piso y otras cámaras (Bajo), aunque facilita R1 y R2.",
        estrategia="Mitigar",
        acciones=[
            "Mantenimiento preventivo mensual y reemplazo programado de las cámaras más antiguas.",
            "Alertas automáticas de pérdida de señal en el software de video.",
            "Revisión de cobertura cada vez que cambie la distribución de la sala.",
            "Vigilancia física temporal mientras se repara una falla.",
        ],
        responsable="Jefe de Vigilancia (CCTV)",
        recursos="Técnico de CCTV, cámaras de reemplazo, licencia de alertas, guardias de piso.",
        tiempo="Alertas en 30 días; reemplazo escalonado en 6 meses; mantenimiento mensual.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R6", nombre="Uso del casino para operaciones con recursos ilícitos", corto="Lavado de dinero a través del casino",
        activo="Procesos de caja, compra y venta de fichas, pago de premios y expedientes de clientes.",
        amenaza="Clientes que ingresan efectivo de origen ilícito y lo retiran como premio para aparentar que es legal.",
        vulnerabilidad="Identificación incompleta de clientes en operaciones en efectivo y revisión manual de las operaciones que deben reportarse.",
        fuente="Externa", categoria="Legal", prob="Media", imp="Alto",
        justificacion="Los juegos con apuesta son actividad vulnerable según la LFPIORPI (art. 17, fracc. I) y el efectivo es el medio de pago principal (Media). Un incumplimiento puede traer multas, observaciones de la autoridad y daño a la reputación (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Expediente de identificación del cliente obligatorio a partir de los umbrales que marca la ley.",
            "Módulo de prevención de lavado (PLD) que acumule operaciones por cliente y genere alertas.",
            "Presentar los avisos ante la autoridad en tiempo y forma.",
            "Capacitación anual en PLD para cajeros y anfitriones; auditoría independiente anual.",
        ],
        responsable="Oficial de Cumplimiento PLD",
        recursos="Módulo PLD del sistema de caja, analista de cumplimiento, asesoría legal externa.",
        tiempo="Expedientes y alertas en 90 días; avisos según plazos legales; capacitación anual.",
        origen="Matriz de riesgos (10/10/2026)",
    ),
    dict(
        id="R7", nombre="Ataque de ransomware", corto="Secuestro de información (ransomware)",
        activo="Servidores, bases de datos y equipos de usuario (caja, sistema de gestión de casino y ERP).",
        amenaza="Grupos criminales que cifran la información y piden rescate; suelen entrar por correos engañosos (phishing) o accesos remotos.",
        vulnerabilidad="Equipos con sistema operativo sin soporte, acceso remoto sin doble factor, poca capacitación contra phishing y red poco segmentada.",
        fuente="Externa", categoria="Tecnológico", prob="Alta", imp="Alto",
        justificacion="En las entrevistas, TI reportó intentos de phishing frecuentes y equipos sin parches (Alta). Un cifrado detendría la caja, las tragamonedas en red y el programa de lealtad, con pérdidas por cada hora sin operar (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Antimalware avanzado (EDR) en todos los servidores y equipos.",
            "Doble factor de autenticación en VPN, correo y cuentas de administrador.",
            "Parches críticos en máximo 15 días y retiro de equipos sin soporte.",
            "Segmentar la red: juego, caja, CCTV y oficinas.",
            "Simulacros de phishing trimestrales y ejercicio semestral del plan de respuesta a incidentes.",
        ],
        responsable="Jefe de Seguridad de la Información (CISO)",
        recursos="Licencias EDR y de doble factor, equipo de TI, proveedor externo de respuesta a incidentes, presupuesto para renovar equipos.",
        tiempo="Doble factor y EDR en 30 días; segmentación en 90 días; simulacros trimestrales.",
        origen="Nuevo (TI)",
    ),
    dict(
        id="R8", nombre="Caída del sistema de pagos", corto="Caída del sistema de pagos",
        activo="Terminales punto de venta, sistema de caja y enlace con el procesador de pagos.",
        amenaza="Falla del procesador de pagos, del enlace de comunicaciones o del servidor de caja.",
        vulnerabilidad="Un solo enlace de internet para pagos y contrato con el procesador sin niveles de servicio ni penalizaciones.",
        fuente="Externa", categoria="Financiero", prob="Media", imp="Medio",
        justificacion="El enlace ha fallado algunas veces al año (Media). La operación sigue en efectivo, pero se pierden ventas con tarjeta y se retrasan pagos (Medio).",
        estrategia="Transferir",
        acciones=[
            "Renegociar el contrato con el procesador con nivel de servicio (SLA) y penalizaciones.",
            "Contratar una póliza de seguro por interrupción de negocio.",
            "Segundo enlace de comunicaciones con otro proveedor.",
            "Procedimiento manual de contingencia en caja con formatos y límites.",
        ],
        responsable="Director de TI",
        recursos="Área jurídica, compras, presupuesto para el segundo enlace y la póliza.",
        tiempo="Contrato y enlace en 60 días; póliza en 90 días; prueba de contingencia semestral.",
        origen="Nuevo (TI)",
    ),
    dict(
        id="R9", nombre="Acceso privilegiado indebido", corto="Mal uso de cuentas de administrador",
        activo="Cuentas de administrador de servidores, bases de datos y sistema de gestión de casino.",
        amenaza="Empleado, exempleado o proveedor con acceso remoto que usa privilegios para modificar saldos, datos o borrar registros.",
        vulnerabilidad="Cuentas de administrador compartidas, bajas de personal sin retirar accesos a tiempo y sin registro de sesiones privilegiadas.",
        fuente="Interna", categoria="Tecnológico", prob="Media", imp="Alto",
        justificacion="La revisión de accesos se hace una vez al año y existen cuentas genéricas (Media). Un abuso puede alterar saldos, borrar evidencia y facilitar fraudes (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Eliminar cuentas compartidas y asignar cuentas nominales.",
            "Herramienta de gestión de accesos privilegiados (PAM) con grabación de sesiones.",
            "Retiro de accesos el mismo día de la baja, ligado al aviso de Recursos Humanos.",
            "Revisión trimestral de accesos por cada dueño de sistema, con mínimo privilegio.",
        ],
        responsable="Jefe de Seguridad de la Información (CISO)",
        recursos="Licencia PAM, Recursos Humanos, dueños de sistema.",
        tiempo="Cuentas nominales en 30 días; PAM en 120 días; revisión trimestral.",
        origen="Nuevo (TI)",
    ),
    dict(
        id="R10", nombre="Fuga de datos de clientes", corto="Fuga de datos de clientes",
        activo="Base de datos de clientes: identificaciones, contacto, historial de juego y datos bancarios.",
        amenaza="Robo de información por un atacante externo que la vende o la usa para fraudes.",
        vulnerabilidad="Datos personales sin cifrar en reportes y respaldos, exportaciones a hojas de cálculo sin control y sin herramienta de prevención de fugas.",
        fuente="Externa", categoria="Reputacional", prob="Media", imp="Alto",
        justificacion="La base de clientes es valiosa para fraudes y circula en reportes internos (Media). Una fuga afecta la confianza de clientes frecuentes y VIP y puede derivar en sanciones conforme a la LFPDPPP (Alto).",
        estrategia="Mitigar",
        acciones=[
            "Clasificar y cifrar los datos personales en bases de datos y respaldos.",
            "Enmascarar datos en reportes y bloquear exportaciones masivas.",
            "Herramienta de prevención de fuga de datos (DLP) en correo y USB.",
            "Procedimiento de atención a vulneraciones y capacitación anual en protección de datos.",
        ],
        responsable="Oficial de Privacidad",
        recursos="Apoyo del CISO y del equipo de bases de datos, licencia DLP, asesoría legal.",
        tiempo="Cifrado en 90 días; DLP en 120 días; capacitación anual.",
        origen="Nuevo (TI)",
    ),
    dict(
        id="R11", nombre="Falla de respaldos", corto="Respaldos que no sirven al recuperar",
        activo="Respaldos de bases de datos, servidores y video.",
        amenaza="Respaldos incompletos, dañados o cifrados junto con los sistemas durante un ataque.",
        vulnerabilidad="No se prueban restauraciones, los respaldos están en la misma red que producción y no hay copia fuera de sitio inmutable.",
        fuente="Interna", categoria="Tecnológico", prob="Alta", imp="Medio",
        justificacion="Sin pruebas de restauración es muy probable que algún respaldo no funcione cuando se necesite (Alta). El daño directo es Medio porque los sistemas siguen operando, pero se agrava si coincide con R7.",
        estrategia="Mitigar",
        acciones=[
            "Regla 3-2-1: tres copias, en dos medios distintos, una fuera de sitio e inmutable.",
            "Prueba mensual de restauración de los sistemas críticos.",
            "Monitoreo diario de los trabajos de respaldo con alerta por falla.",
            "Definir tiempo objetivo de recuperación (RTO) y pérdida máxima de datos (RPO) por sistema.",
        ],
        responsable="Jefe de Infraestructura y Redes",
        recursos="Almacenamiento inmutable o en la nube, software de respaldo, operador de TI.",
        tiempo="RTO/RPO en 30 días; copia inmutable en 60 días; pruebas mensuales.",
        origen="Nuevo (TI)",
    ),
    dict(
        id="R12", nombre="Uso de software no autorizado y memorias USB", corto="Programas no autorizados y memorias USB",
        activo="Equipos de caja, estaciones de vigilancia y equipos administrativos.",
        amenaza="Instalación de programas no autorizados o conexión de memorias USB que introducen software malicioso.",
        vulnerabilidad="Usuarios con permisos de administrador en su equipo y puertos USB habilitados.",
        fuente="Interna", categoria="Tecnológico", prob="Media", imp="Medio",
        justificacion="El personal lo hace para pasar archivos o entretenerse en turnos largos (Media). Puede introducir software malicioso y abrir la puerta a R7 o R10 (Medio).",
        estrategia="Evitar",
        acciones=[
            "Bloquear puertos USB por política, con excepciones aprobadas.",
            "Retirar permisos de administrador local a los usuarios.",
            "Lista blanca de aplicaciones en equipos de caja y vigilancia.",
            "Política firmada por el personal y un medio aprobado para transferir archivos.",
        ],
        responsable="Jefe de Soporte Técnico",
        recursos="Directorio Activo, herramienta de control de aplicaciones, Recursos Humanos.",
        tiempo="Bloqueo de USB en 30 días; lista blanca en 60 días.",
        origen="Nuevo (TI)",
    ),
]
# Acción clave en pocas palabras (para la presentación ejecutiva)
CLAVE = {'R1': 'Inspección por turno con bitácora digital',
    'R2': 'Rotación de cajeros y alertas de pagos',
    'R3': 'Firmware al día, sensores y red aislada',
    'R4': 'Mantener controles actuales y vigilar',
    'R5': 'Mantenimiento y alertas de pérdida de señal',
    'R6': 'Identificar clientes y alertas antilavado',
    'R7': 'Doble factor, antimalware avanzado y red segmentada',
    'R8': 'Contrato con penalizaciones y seguro',
    'R9': 'Cuentas personales y control de accesos de administrador',
    'R10': 'Cifrar datos y bloquear su salida',
    'R11': 'Copia fuera de sitio y pruebas mensuales de restauración',
    'R12': 'Bloquear USB y programas no autorizados'}
for _r in RIESGOS:
    _r["clave"] = CLAVE[_r["id"]]
    _r["nivel"] = nivel(_r["prob"], _r["imp"])
    _r["frecuencia"] = FRECUENCIA_MONITOREO[_r["nivel"]]

RIESGO = {r["id"]: r for r in RIESGOS}

ESTRATEGIAS = [
    ("Evitar", "Eliminar la actividad o condición que origina el riesgo."),
    ("Mitigar", "Reducir la probabilidad, el impacto o ambos con controles."),
    ("Transferir", "Compartir el efecto económico con un tercero (contrato, seguro)."),
    ("Aceptar", "Asumir el riesgo de forma consciente y vigilarlo, porque un control extra cuesta más de lo que reduce."),
]

CATEGORIAS = [
    ("Financiero", "Pérdidas directas de dinero o de flujo de efectivo.", ["R2", "R8"]),
    ("Operativo", "Fallas en procesos, personas o equipos de la operación de juego.", ["R1", "R5"]),
    ("Tecnológico", "Fallas o ataques a sistemas, redes y datos.", ["R3", "R4", "R7", "R9", "R11", "R12"]),
    ("Legal", "Incumplimiento de leyes, permisos o regulaciones.", ["R6"]),
    ("Reputacional", "Pérdida de confianza de clientes, autoridades o la sociedad.", ["R10"]),
]

# ---------------------------------------------------------------- KPI y KRI
# Los tres primeros (R1, R2, R5) se retoman de la actividad del 18/10/2026 con las
# correcciones solicitadas.
KPI_KRI = {
    "R1": dict(
        control="Inspección periódica de barajas y dados.",
        kpi="% de cartas y dados inspeccionados según protocolo semanal", meta="≥ 98 %",
        kri="# de inconsistencias, alteraciones o cartas defectuosas detectadas", umbral="> 3 al mes",
        interpretacion="Si el KPI baja y el KRI sube, las inspecciones no se realizan correctamente y aumenta el riesgo de fraude.",
        accion="Auditar al personal, sancionar omisiones del protocolo y revisar los elementos de juego.",
        origen="Actividad KPI/KRI (18/10/2026), corregido",
    ),
    "R2": dict(
        control="Rotación obligatoria de cajeros. Monitoreo de patrones de pago.",
        kpi="% de cumplimiento en la rotación programada de cajeros", meta="100 %",
        kri="# de transacciones sospechosas o discrepancias reportadas", umbral="> 2 al mes",
        interpretacion="Si el KPI es alto y el KRI sube, el esquema de rotación no es suficiente o se están omitiendo las alertas.",
        accion="Iniciar investigaciones internas, auditar relaciones de personal y ajustar límites de pagos.",
        origen="Actividad KPI/KRI (18/10/2026), corregido",
    ),
    "R3": dict(
        control="Firmware actualizado, sensores de apertura y monitoreo de la red de tragamonedas.",
        kpi="% de máquinas con firmware vigente y sellos íntegros en la inspección mensual", meta="≥ 95 %",
        kri="# de eventos anómalos (aperturas no programadas, créditos o pagos fuera de patrón)", umbral="> 1 al mes",
        interpretacion="Si el KPI baja y el KRI sube, hay máquinas expuestas y posibles intentos de manipulación.",
        accion="Retirar de servicio las máquinas afectadas, revisar el video y escalar con el fabricante.",
        origen="Nuevo",
    ),
    "R4": dict(
        control="Firewall de aplicaciones web, parches mensuales y escaneo trimestral.",
        kpi="% de vulnerabilidades críticas del CRM corregidas en 30 días o menos", meta="≥ 95 %",
        kri="# de alertas de alta severidad sobre el CRM al mes", umbral="+50 % sobre el promedio",
        interpretacion="Si el KRI sube con el KPI estable, aumentó la presión de atacantes; si ambos empeoran, el riesgo aceptado ya no es bajo.",
        accion="Reevaluar la aceptación del riesgo y reforzar controles, por ejemplo con pruebas de penetración.",
        origen="Nuevo",
    ),
    "R5": dict(
        control="Mantenimiento preventivo y monitoreo en tiempo real del sistema de grabación.",
        kpi="% de disponibilidad operativa continua del sistema de cámaras", meta="≥ 99.5 %",
        kri="# de fallas técnicas, puntos ciegos o pérdidas de señal registradas", umbral="> 4 al mes",
        interpretacion="Si el KPI empeora y el KRI aumenta, existe alta probabilidad de quedar vulnerables ante robos o disputas.",
        accion="Revisar la infraestructura del sistema y colocar vigilancia física temporal.",
        origen="Actividad KPI/KRI (18/10/2026)",
    ),
    "R6": dict(
        control="Identificación de clientes y alertas del módulo PLD.",
        kpi="% de operaciones sujetas a identificación con expediente completo", meta="100 %",
        kri="# de avisos presentados fuera de plazo y de operaciones inusuales sin revisar", umbral="≥ 1",
        interpretacion="Si el KPI baja se atienden operaciones sin identificar; si hay avisos tardíos, la exposición a sanciones es directa.",
        accion="Bloquear operaciones sin expediente, reforzar la capacitación y revisar el módulo PLD.",
        origen="Nuevo",
    ),
    "R7": dict(
        control="EDR, doble factor, parches críticos y simulacros de phishing.",
        kpi="% de equipos con EDR activo y parches críticos al día", meta="≥ 98 %",
        kri="% de empleados que caen en el simulacro de phishing", umbral="> 5 %",
        interpretacion="Si el KPI baja y el KRI sube, crece la superficie de ataque y el personal es más vulnerable al engaño.",
        accion="Aislar equipos sin protección, dar capacitación focalizada y revisar el plan de respuesta a incidentes.",
        origen="Nuevo",
    ),
    "R8": dict(
        control="SLA con el procesador, póliza de interrupción y enlace alterno.",
        kpi="% de disponibilidad del servicio de pagos contra el SLA contratado", meta="≥ 99.9 %",
        kri="# de caídas del sistema de pagos y minutos sin servicio al mes", umbral="> 2 caídas o > 60 min",
        interpretacion="Si el KRI sube aunque se cumpla el SLA, el contrato no cubre la necesidad real del casino.",
        accion="Aplicar penalizaciones, activar el enlace alterno y renegociar o cambiar de proveedor.",
        origen="Nuevo",
    ),
    "R9": dict(
        control="Cuentas nominales, gestión de accesos privilegiados (PAM) y revisión trimestral.",
        kpi="% de accesos de personal dado de baja retirados el mismo día", meta="100 %",
        kri="# de cuentas privilegiadas genéricas o sin dueño", umbral="> 0",
        interpretacion="Si el KPI baja y el KRI sube, hay privilegios sin dueño que pueden usarse para fraudes.",
        accion="Deshabilitar las cuentas, revisar grabaciones de sesiones y escalar a Auditoría Interna.",
        origen="Nuevo",
    ),
    "R10": dict(
        control="Cifrado, enmascaramiento de datos y prevención de fugas (DLP).",
        kpi="% de bases de datos y respaldos con datos personales cifrados", meta="100 %",
        kri="# de envíos o copias de datos personales bloqueados por DLP al mes", umbral="> 5 al mes",
        interpretacion="Si el KRI sube, hay personal sacando datos fuera del flujo autorizado; si el KPI baja, una fuga causaría más daño.",
        accion="Investigar a los usuarios involucrados, reforzar la capacitación y ajustar las reglas DLP.",
        origen="Nuevo",
    ),
    "R11": dict(
        control="Regla 3-2-1 y pruebas mensuales de restauración.",
        kpi="% de pruebas de restauración exitosas en sistemas críticos", meta="100 %",
        kri="# de trabajos de respaldo fallidos o incompletos por semana", umbral="> 2 por semana",
        interpretacion="Si el KPI baja, no hay garantía de recuperar los sistemas ante un ataque como R7.",
        accion="Corregir los trabajos fallidos en 24 horas, repetir la prueba y escalar al Director de TI.",
        origen="Nuevo",
    ),
    "R12": dict(
        control="Bloqueo de USB, sin administrador local y lista blanca de aplicaciones.",
        kpi="% de equipos con USB bloqueado y sin administrador local", meta="100 %",
        kri="# de intentos bloqueados de instalar software o conectar USB al mes", umbral="Aumento 2 meses seguidos",
        interpretacion="Si el KRI sube, la práctica continúa y los usuarios están intentando saltar el control.",
        accion="Hablar con los jefes de área, reforzar la política y aplicar el reglamento interno.",
        origen="Nuevo",
    ),
}

# KPI y KRI del programa (introducción)
KPI_PROGRAMA = [
    ("% de planes de respuesta ejecutados en el tiempo comprometido", "≥ 90 %"),
    ("% de riesgos revisados en la frecuencia que marca su nivel", "100 %"),
    ("% de personal capacitado en riesgos y seguridad en el año", "≥ 95 %"),
]
KRI_PROGRAMA = [
    ("# de riesgos en nivel Crítico o Alto", "Bajar de 6 a 3 en 12 meses"),
    ("# de incidentes de seguridad relevantes por trimestre", "Tendencia a la baja"),
    ("# de observaciones de autoridades o auditoría", "0"),
]

# ---------------------------------------------------------------- implementación ISO 31000 (caso simulado)
# semanas 1-24 = mayo a octubre de 2026
FASES = [
    dict(n=1, nombre="Mandato y compromiso", ini=1, fin=2,
         que="La Dirección General aprueba la política de riesgos, nombra al líder del plan y crea el Comité de Riesgos.",
         quien="Dirección General", clausula="Liderazgo y compromiso (5.2)"),
    dict(n=2, nombre="Diseño del marco", ini=3, fin=6,
         que="Se definen roles, criterios de riesgo, escalas 3x3, plantilla de matriz y calendario de revisión.",
         quien="Gerente de Riesgos y Cumplimiento con el Director de TI", clausula="Marco de referencia (5.4)"),
    dict(n=3, nombre="Alcance, contexto y criterios", ini=5, fin=8,
         que="Inventario de activos de TI y procesos críticos, análisis FODA y requisitos legales.",
         quien="Director de TI y Oficial de Cumplimiento PLD", clausula="Proceso (6.3)"),
    dict(n=4, nombre="Evaluación del riesgo", ini=8, fin=14,
         que="Encuestas, entrevistas y lluvia de ideas para identificar, analizar y valorar los 12 riesgos; matriz y mapa de calor.",
         quien="Equipo de gestión de riesgos con los dueños de riesgo", clausula="Proceso (6.4)"),
    dict(n=5, nombre="Tratamiento del riesgo", ini=14, fin=20,
         que="Se elige estrategia por riesgo, se redactan planes de respuesta y el Comité aprueba presupuesto.",
         quien="Dueños de riesgo; aprobación del Comité de Riesgos", clausula="Proceso (6.5)"),
    dict(n=6, nombre="Seguimiento, registro e informe", ini=20, fin=24,
         que="Arranca el tablero de KPI y KRI, se entrega el primer informe al Comité y se programa la revisión.",
         quien="Gerente de Riesgos y Cumplimiento; Auditoría Interna", clausula="Proceso (6.6 y 6.7)"),
]
FASE_TRANSVERSAL = dict(nombre="Comunicación y consulta (toda la implementación)", ini=1, fin=24,
                        quien="Gerente de Riesgos y Cumplimiento", clausula="Proceso (6.2)")
MESES = ["May", "Jun", "Jul", "Ago", "Sep", "Oct"]
DURACION = "24 semanas (mayo a octubre de 2026)"

RETOS = [
    ("Resistencia del personal", "Cajeros y crupieres veían las entrevistas como una auditoría para buscar culpables.",
     "Se explicó que el fin es prevenir, se usaron encuestas anónimas y se compartieron los resultados."),
    ("Operación de horario extendido", "Los turnos rotativos impedían reunir a todos en talleres largos.",
     "Sesiones de 30 minutos en cada turno y encuesta en línea."),
    ("Datos incompletos", "No existía una bitácora de incidentes; muchos eventos solo se recordaban de palabra.",
     "Se reconstruyó la historia con tickets de soporte y reportes de vigilancia, y se creó un registro único de incidentes."),
    ("Áreas separadas", "TI, operaciones de juego y cumplimiento tenían listas de riesgos distintas.",
     "Un solo Comité de Riesgos y una sola matriz con dueño por riesgo."),
    ("Sistemas heredados", "Tragamonedas y cámaras antiguas no aceptan todas las actualizaciones.",
     "Controles compensatorios (red aislada, alertas) y plan de reemplazo por etapas."),
    ("Presupuesto limitado", "No era posible atender todos los riesgos al mismo tiempo.",
     "El mapa de calor se usó para priorizar: primero lo Crítico y Alto."),
    ("Escalas diferentes", "La matriz anterior usaba 5x5 y el PIA pide 3x3.",
     "Se definió una tabla de conversión y se documentaron los cambios de nivel."),
]

# ---------------------------------------------------------------- roles
ROLES = [
    ("Dirección General", "Patrocina el plan, aprueba la política de riesgos y el presupuesto."),
    ("Comité de Riesgos", "Director General, Director de TI, Director de Finanzas, Gerente de Operaciones de Juego, Gerente de Riesgos y Cumplimiento y Oficial de Cumplimiento PLD. Prioriza, aprueba tratamientos y da seguimiento mensual."),
    ("Gerente de Riesgos y Cumplimiento", "Líder del plan. Coordina al equipo de gestión de riesgos, mantiene la matriz y el tablero, y consolida reportes."),
    ("Director de TI", "Responsable de la infraestructura y los sistemas; integra los riesgos de TI al presupuesto."),
    ("Dueños de riesgo", "Ejecutan los planes de respuesta y reportan KPI y KRI de su riesgo (ver tabla de análisis)."),
    ("Auditoría Interna", "Revisa de forma independiente que los controles funcionen."),
    ("Todo el personal", "Reporta incidentes y situaciones de riesgo por los canales definidos."),
]

# ---------------------------------------------------------------- empresa (caso ficticio)
EMPRESA_INFO = dict(
    giro="Entretenimiento: centro de juegos con apuesta (casino) con mesas de juego, máquinas tragamonedas y servicios de hospitalidad. Para el caso se supone que opera con permiso de la Secretaría de Gobernación, conforme a la Ley Federal de Juegos y Sorteos y su Reglamento (Cámara de Diputados del H. Congreso de la Unión, 1947; Secretaría de Gobernación, 2004).",
    mision="Ofrecer una experiencia de entretenimiento segura, justa y responsable, con servicio de excelencia y apego a la ley.",
    vision="Ser en 2030 el casino de referencia del noreste de México por la confianza de sus clientes, la integridad de sus juegos y la seguridad de su operación.",
    mision_ti="Garantizar la disponibilidad, integridad y confidencialidad de la información y de los sistemas que sostienen el juego, la caja y la atención a clientes.",
    vision_ti="Ser un área de TI que habilite la operación continua del casino con sistemas resilientes, seguros y gestionados con base en riesgos.",
    productos=[
        "Mesas de juego: blackjack, ruleta, póker y dados.",
        "Máquinas tragamonedas electrónicas conectadas a un sistema central.",
        "Programa de lealtad con puntos, promociones y área VIP.",
        "Caja: venta y cambio de fichas y pago de premios.",
        "Restaurante-bar y eventos de entretenimiento.",
    ],
    clientes="Adultos mayores de 18 años de la zona metropolitana, turistas y viajeros de negocios, y jugadores frecuentes y VIP inscritos en el programa de lealtad.",
    ubicacion="Una sala principal en Monterrey, Nuevo León (supuesto del caso), con cobertura local y regional y operación los 365 días del año en horario extendido.",
    valores=[
        ("Integridad", "Juegos justos y transparentes."),
        ("Legalidad", "Cumplimiento de permisos y leyes aplicables."),
        ("Juego responsable", "Cuidado del cliente y de su bienestar."),
        ("Seguridad", "Protección de personas, dinero e información."),
        ("Servicio", "Atención cordial y eficiente."),
        ("Trabajo en equipo", "Colaboración entre áreas."),
    ],
    estructura_ti=[
        "Director de TI",
        "Jefe de Seguridad de la Información (CISO)",
        "Jefe de Infraestructura y Redes",
        "Jefe de Desarrollo y Aplicaciones",
        "Jefe de Soporte Técnico",
        "Jefe de Tecnología de Juego (tragamonedas)",
    ],
    tecnologias=[
        ("Servidores", "Clúster de servidores virtualizados en el centro de datos de la sala; servidor de video para CCTV; servicio en la nube para correo y respaldos."),
        ("Aplicaciones", "Sistema de gestión de casino y de tragamonedas; sistema de caja; gestión de clientes y lealtad (CRM); punto de venta; software de gestión de video; ERP de contabilidad y nómina; módulo de prevención de lavado (PLD)."),
        ("Bases de datos", "Bases de datos relacionales de clientes y lealtad, transacciones de caja, contabilidad del juego y bitácoras de seguridad."),
        ("Redes", "Red cableada con switches administrables y VLAN para juego, caja, CCTV y oficinas; Wi-Fi para clientes separado; firewall perimetral; VPN para soporte remoto; un enlace de internet principal."),
        ("Seguridad", "Directorio Activo, antivirus, firewall de aplicaciones web para el portal de clientes y monitoreo de eventos de seguridad (SIEM)."),
        ("Equipos de usuario", "Computadoras de caja y oficinas, estaciones de vigilancia, terminales punto de venta y tabletas para supervisores."),
    ],
)

FODA = dict(
    Fortalezas=[
        "Equipo de TI interno que conoce la operación.",
        "Sistemas centrales con soporte del fabricante.",
        "Vigilancia con personal dedicado en todos los turnos.",
        "Dirección comprometida con el plan.",
    ],
    Debilidades=[
        "Cámaras y equipos con muchos años de uso.",
        "Cuentas de administrador compartidas.",
        "Respaldos sin pruebas de restauración.",
        "Un solo enlace de internet para pagos.",
    ],
    Oportunidades=[
        "Servicios en la nube para respaldos y recuperación.",
        "Herramientas de seguridad accesibles (doble factor, EDR).",
        "Leyes de PLD y datos personales que impulsan buenas prácticas.",
        "Capacitación ofrecida por proveedores.",
    ],
    Amenazas=[
        "Ransomware y correos engañosos (phishing).",
        "Fraude organizado en mesas y tragamonedas.",
        "Uso del casino para lavado de dinero.",
        "Fallas de proveedores de pagos y comunicaciones.",
    ],
)

# ---------------------------------------------------------------- comunicación
COMUNICACION = [
    # (quién comunica, quién recibe, qué, canal, frecuencia)
    ("Dueños de riesgo", "Equipo de gestión de riesgos", "Avance de planes de respuesta y valores de KPI y KRI.", "Tablero compartido y correo", "Según el nivel: semanal, quincenal, mensual o trimestral"),
    ("Equipo de gestión de riesgos", "Comité de Riesgos", "Mapa de calor actualizado, riesgos nuevos o que cambiaron de nivel y recomendaciones.", "Reunión y reporte ejecutivo", "Mensual"),
    ("Comité de Riesgos", "Dirección General y accionistas", "Estado general de los riesgos, inversiones y decisiones requeridas.", "Informe ejecutivo", "Trimestral"),
    ("CISO", "Todo el personal", "Alertas de seguridad, intentos de phishing y buenas prácticas.", "Correo, chat corporativo y pantallas en comedor", "Cuando ocurra y boletín mensual"),
    ("Equipo de respuesta a incidentes", "Dirección General, Jurídico y Comunicación", "Incidentes graves y su avance.", "Llamada y grupo de crisis", "Inmediato (menos de 1 hora)"),
    ("Oficial de Cumplimiento PLD", "Autoridad competente", "Avisos de operaciones obligatorias.", "Portal oficial de la autoridad", "Según plazos legales"),
    ("Oficial de Privacidad y Comunicación Corporativa", "Clientes afectados", "Vulneraciones de datos personales y medidas tomadas.", "Correo y comunicado", "Cuando aplique"),
    ("Auditoría Interna", "Comité de Riesgos", "Resultados de auditorías de controles.", "Informe de auditoría", "Semestral"),
]

CANALES = [
    ("Chat corporativo (canal de riesgos)", "Avisos rápidos entre el equipo de riesgos y los dueños."),
    ("Correo electrónico", "Reportes formales y evidencias."),
    ("Reuniones del Comité", "Decisiones, priorización y aprobaciones."),
    ("Tablero de indicadores", "KPI, KRI y mapa de calor siempre actualizados."),
    ("Intranet y pantallas internas", "Campañas de concientización para todo el personal."),
    ("Pláticas de inicio de turno", "Mensajes clave para cajeros, crupieres y vigilancia."),
    ("Grupo de crisis", "Coordinación durante incidentes graves."),
]

# ---------------------------------------------------------------- referencias APA 7 (verificadas)
REFERENCIAS = [
    "Cámara de Diputados del H. Congreso de la Unión. (1947). <i>Ley Federal de Juegos y Sorteos</i>. Diario Oficial de la Federación, 31 de diciembre de 1947. https://www.diputados.gob.mx/LeyesBiblio/pdf/109.pdf",
    "Cámara de Diputados del H. Congreso de la Unión. (2025a). <i>Ley Federal de Protección de Datos Personales en Posesión de los Particulares</i>. Diario Oficial de la Federación, 20 de marzo de 2025. https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf",
    "Cámara de Diputados del H. Congreso de la Unión. (2025b). <i>Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita</i> (Publicada en el Diario Oficial de la Federación el 17 de octubre de 2012; última reforma del 16 de julio de 2025). https://www.diputados.gob.mx/LeyesBiblio/ref/lfpiorpi.htm",
    "International Electrotechnical Commission. (2019). <i>Risk management — Risk assessment techniques</i> (IEC 31010:2019).",
    "International Organization for Standardization. (2018). <i>Risk management — Guidelines</i> (ISO 31000:2018). https://www.iso.org/standard/65694.html",
    "Secretaría de Gobernación. (2004). <i>Reglamento de la Ley Federal de Juegos y Sorteos</i>. Diario Oficial de la Federación, 17 de septiembre de 2004 (última reforma del 16 de noviembre de 2023). https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo88470.html",
]
