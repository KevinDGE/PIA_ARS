# -*- coding: utf-8 -*-
"""Guion de la presentación ejecutiva. Es la fuente de las notas del orador del
PowerPoint y del PDF del guion, para que ambos digan lo mismo.

Cada diapositiva: n, titulo, quien (clave de ORADORES), accion (qué hacer o
señalar; solo aparece en el guion) y texto (párrafos que se dicen en voz alta)."""

ORADORES = {
    "david": "David Emiliano Rangel Tovar",
    "fernando": "Fernando Garza Chavez",
    "alejandro": "Alejandro Martinez Moya",
    "rene": "Rene Villareal Torres",
    "kevin": "Kevin Daniel Grimaldo Esquivel",
}

PARTES = [
    ("david", "Introducción: importancia del plan y cómo medimos los riesgos", [1, 2, 3]),
    ("fernando", "Implementación de ISO 31000: fases y responsables", [4, 5]),
    ("alejandro", "Problemas de la implementación e impacto en el negocio", [6, 7]),
    ("rene", "Mapa de calor y riesgos prioritarios", [8, 9]),
    ("kevin", "Resto de riesgos, seguimiento y conclusión", [10, 11, 12]),
]

PALABRAS_POR_MINUTO = 130

DIAPOSITIVAS = [
    dict(n=1, titulo="Portada", quien="david",
         accion="Saluda viendo al público, no a la pantalla.",
         texto=[
             "Buenos días. Somos el equipo del grupo 061 de Administración de Riesgos de TI: Fernando Garza, Alejandro Martinez, Rene Villareal, Kevin Grimaldo y yo, David Rangel. Hoy presentamos el plan de administración de riesgos para Casino Royale Enterprises, un casino ficticio que usamos como caso de estudio.",
             "En los próximos minutos vamos a explicar por qué un plan de riesgos importa para el negocio, cómo aplicamos el estándar ISO 31000 paso a paso y con qué problemas nos topamos, cómo los riesgos afectan los objetivos del casino y qué vamos a hacer con cada uno.",
             "La presentación está pensada para cualquier persona, sin conocimientos técnicos. Si algún término no queda claro, con gusto lo aclaramos al final.",
         ]),
    dict(n=2, titulo="¿Por qué el casino necesita un plan de riesgos?", quien="david",
         accion="Señala las tres tarjetas de izquierda a derecha y termina en el recuadro azul de abajo.",
         texto=[
             "Un casino es un negocio que depende por completo de la confianza y de la tecnología. Todo el día se mueve efectivo en la caja, en las mesas y en las máquinas tragamonedas, y casi todo pasa por un sistema.",
             "Tener un plan de riesgos importa por tres razones. Primero, protege el dinero: un fraude o una falla del sistema es pérdida directa. Segundo, nos ayuda a cumplir la ley: un casino necesita permiso para operar, debe prevenir el lavado de dinero y proteger los datos de sus clientes. Tercero, cuida la confianza: si un cliente duda de que el juego sea limpio o de que sus datos estén seguros, se va con la competencia.",
             "En pocas palabras, el plan contesta tres preguntas: qué puede salir mal, qué tan grave sería y qué hacemos antes de que pase. Así dejamos de reaccionar a los problemas y empezamos a prevenirlos.",
         ]),
    dict(n=3, titulo="¿Cómo medimos cada riesgo?", quien="david",
         accion="Recorre la fórmula Probabilidad + Impacto = Nivel y después los cuatro colores. Al terminar, cede la palabra a Fernando.",
         texto=[
             "Para comparar riesgos tan distintos como un fraude en una mesa y un ataque informático, usamos la misma regla para todos.",
             "Primero preguntamos qué tan seguido puede pasar: probabilidad alta, media o baja. Luego preguntamos cuánto daño haría si pasa: impacto alto, medio o bajo. Al combinar las dos respuestas sale el nivel de riesgo. Por ejemplo, algo muy probable y muy dañino es Crítico; algo poco probable pero muy dañino es Moderado.",
             "El nivel nos dice qué tan rápido actuar y cada cuándo revisarlo: los críticos cada semana, los altos cada quince días, los moderados cada mes y los bajos cada trimestre. Y para cada riesgo elegimos una de cuatro respuestas: evitarlo quitando la causa, mitigarlo con controles, transferirlo con un contrato o seguro, o aceptarlo y vigilarlo cuando controlarlo más cuesta más de lo que ahorra.",
             "Ahora Fernando les va a explicar cómo implementamos el estándar en el casino.",
         ]),
    dict(n=4, titulo="Implementamos ISO 31000 en 6 fases", quien="fernando",
         accion="Recorre la línea del tiempo de la fase 1 a la 6; al final señala la banda dorada y los tres datos de abajo.",
         texto=[
             "Gracias, David. Elegimos ISO 31000, la norma internacional de gestión de riesgos. Es una guía, no un certificado: su valor está en que todas las áreas usen el mismo método y el mismo lenguaje. La aplicamos en un caso simulado de 24 semanas, de mayo a octubre de 2026.",
             "Fase 1, mandato y compromiso: la dirección aprueba la política y nombra a un líder. Fase 2, diseño del marco: definimos roles, escalas y la plantilla de la matriz. Fase 3, contexto: hicimos el inventario de sistemas y procesos, un análisis FODA y revisamos las leyes que aplican. Fase 4, evaluación: con encuestas, entrevistas y lluvia de ideas identificamos y calificamos los 12 riesgos. Fase 5, tratamiento: decidimos qué hacer con cada riesgo y se aprobó presupuesto. Fase 6, seguimiento: arrancamos los indicadores y el primer informe.",
             "Algunas fases se traslapan, y durante todo el proyecto hubo comunicación y consulta con las áreas. El plan se revisa completo cada año, en noviembre.",
         ]),
    dict(n=5, titulo="Qué hicimos en cada fase y quién la encabezó", quien="fernando",
         accion="Señala cada tarjeta mientras dices quién la encabezó. Al terminar, cede la palabra a Alejandro.",
         texto=[
             "Aquí vemos con más detalle qué se hizo y quién estuvo a cargo de cada fase.",
             "La Dirección General arrancó el proyecto: sin su apoyo nadie le da prioridad. El Gerente de Riesgos y Cumplimiento fue el líder del plan y diseñó el marco: quién hace qué, cómo se mide y cada cuándo se revisa.",
             "El Director de TI y el Oficial de Cumplimiento hicieron el inventario de sistemas y revisaron las leyes. En la evaluación participaron los dueños de cada riesgo, es decir, las personas que mejor conocen cada área: caja, mesas, vigilancia, tecnología y cumplimiento. Después, cada dueño propuso cómo tratar su riesgo y el Comité aprobó el presupuesto. Finalmente, el Gerente de Riesgos puso en marcha el tablero de indicadores y entregó el primer informe.",
             "La idea clave es que el riesgo no es solo tema de TI: cada área es responsable del suyo. Alejandro les va a contar qué problemas tuvimos en el camino.",
         ]),
    dict(n=6, titulo="Problemas que encontramos y cómo los resolvimos", quien="alejandro",
         accion="Lee cada problema de la izquierda y luego su solución en el recuadro azul de la derecha.",
         texto=[
             "Gracias, Fernando. Ninguna implementación es perfecta. Estos fueron los principales problemas.",
             "Primero, la resistencia del personal: cajeros y crupieres pensaban que las entrevistas eran para buscar culpables. Lo resolvimos con encuestas anónimas y explicando que el objetivo era prevenir, no castigar. Segundo, el casino opera en horario extendido con turnos rotativos, así que no podíamos reunir a todos. Hicimos sesiones cortas de 30 minutos en cada turno.",
             "Tercero, no había un registro de incidentes; muchas cosas solo se recordaban de palabra. Reconstruimos la historia con los tickets de soporte y los reportes de vigilancia, y ahora existe una bitácora única. Cuarto, el presupuesto no alcanzaba para todo. El mapa de calor nos ayudó a priorizar.",
             "También hubo otros retos: cada área tenía su propia lista de riesgos, hay equipos antiguos que no se pueden actualizar fácilmente y la matriz anterior usaba una escala de 5 por 5 que convertimos a 3 por 3.",
         ]),
    dict(n=7, titulo="Cómo afectan los riesgos a los objetivos del negocio", quien="alejandro",
         accion="Señala las cuatro tarjetas y explica que el color de cada etiqueta es el nivel del riesgo. Al terminar, cede la palabra a Rene.",
         texto=[
             "Este es el punto más importante para el negocio: cada riesgo amenaza un objetivo concreto del casino. El color de cada etiqueta indica su nivel.",
             "Para operar sin interrupciones, lo que más nos preocupa es el ransomware, R7, que es un ataque que bloquea los sistemas y pide un rescate. Junto con la caída de pagos, la falla de respaldos y el uso de memorias USB, puede detener la caja y las máquinas.",
             "Para que el juego sea justo están la manipulación de cartas y dados, el acuerdo entre un cajero y un cliente, la alteración de tragamonedas y las fallas de cámaras. Para cumplir la ley están el uso del casino para lavar dinero y la fuga de datos de clientes. Y para que los clientes regresen, importa proteger sus datos, su saldo de puntos y que nadie use cuentas de administrador para alterar información.",
             "Rene les va a mostrar dónde quedó cada uno de estos riesgos.",
         ]),
    dict(n=8, titulo="Mapa de calor: dónde están nuestros 12 riesgos", quien="rene",
         accion="Señala primero los ejes, luego la celda roja (R7) y después la columna de impacto Alto.",
         texto=[
             "Gracias, Alejandro. Este es el mapa de calor. Hacia arriba crece la probabilidad y hacia la derecha crece el impacto. Rojo es crítico, naranja alto, amarillo moderado y verde bajo. Cada etiqueta es uno de nuestros 12 riesgos.",
             "Arriba a la derecha está el único riesgo crítico: el ransomware, R7. En naranja hay cinco riesgos altos: manipulación de elementos de juego, lavado de dinero, mal uso de cuentas de administrador, fuga de datos y falla de respaldos. En amarillo hay cinco moderados y en verde uno bajo, el ataque al sistema de clientes, que ya tiene buenos controles.",
             "Algo que se nota es que siete riesgos están en la columna de impacto alto: si pasan, duelen mucho. Por eso el plan apuesta por la prevención. Nuestra meta para el primer año es bajar de seis a tres los riesgos críticos o altos.",
         ]),
    dict(n=9, titulo="Riesgos prioritarios y cómo los vamos a tratar", quien="rene",
         accion="Recorre la tabla renglón por renglón; no leas la columna de responsables completa. Al terminar, cede la palabra a Kevin.",
         texto=[
             "Estos son los seis riesgos prioritarios: uno crítico y cinco altos. Para todos elegimos mitigar, es decir, reducirlos con controles concretos.",
             "Contra el ransomware, R7, pondremos doble factor de autenticación, que es pedir un segundo código además de la contraseña, un antivirus avanzado en todos los equipos y separaremos la red para que un ataque no se extienda. Lo encabeza el Jefe de Seguridad de la Información.",
             "Para la manipulación de elementos de juego, R1, habrá inspección en cada turno con registro digital. Para el lavado de dinero, R6, identificaremos a los clientes y tendremos alertas automáticas. Para las cuentas de administrador, R9, cada persona tendrá su propia cuenta y se vigilará su uso. Para la fuga de datos, R10, vamos a cifrar la información y bloquear su salida. Y para los respaldos, R11, habrá una copia fuera del casino y pruebas de recuperación cada mes.",
             "Cada acción tiene un responsable y un plazo, que aparecen completos en el documento y en la matriz de Excel. Kevin les va a presentar el resto de los riesgos y cómo vamos a dar seguimiento.",
         ]),
    dict(n=10, titulo="Riesgos moderados y bajos: control y vigilancia", quien="kevin",
         accion="Destaca las tres estrategias distintas a Mitigar: Transferir (R8), Evitar (R12) y Aceptar (R4).",
         texto=[
             "Gracias, Rene. Los otros seis riesgos son menos urgentes, pero también tienen plan.",
             "El acuerdo entre cajero y cliente, R2, lo reducimos rotando a los cajeros y con alertas de pagos raros. La alteración de tragamonedas, R3, con software actualizado, sensores en las máquinas y una red separada. Las fallas de cámaras, R5, con mantenimiento y alertas automáticas.",
             "En la caída del sistema de pagos, R8, elegimos transferir: firmaremos un contrato con penalizaciones con el proveedor y contrataremos un seguro, además de un enlace de respaldo. En el uso de memorias USB y programas no autorizados, R12, elegimos evitar: simplemente se bloquean.",
             "Y el ataque al sistema de clientes, R4, lo aceptamos: ya tiene buenos controles, así que solo lo vigilamos cada trimestre. Aceptar un riesgo es una decisión consciente, no un descuido.",
         ]),
    dict(n=11, titulo="¿Cómo sabremos si el plan funciona?", quien="kevin",
         accion="Señala la tarjeta KPI, luego la KRI y al final la fila de colores con la frecuencia.",
         texto=[
             "Un plan sin medición es solo un documento. Por eso cada riesgo tiene dos indicadores.",
             "El KPI responde: ¿el control se está aplicando? Por ejemplo, qué porcentaje de las computadoras tiene el antivirus activo y las actualizaciones al día; la meta es 98 por ciento o más. El KRI responde: ¿qué tan expuestos estamos? Por ejemplo, cuántos empleados caen en un correo falso de prueba. Si son más del 5 por ciento, encendemos la alerta.",
             "Leídos juntos nos dicen si el control realmente reduce el riesgo. Si el KPI baja y el KRI sube, actuamos de inmediato.",
             "La revisión depende del nivel: críticos cada semana, altos cada quince días, moderados cada mes y bajos cada trimestre. El Comité recibe un reporte mensual y la dirección un informe trimestral.",
         ]),
    dict(n=12, titulo="Conclusión y próximos pasos", quien="kevin",
         accion="Primero las dos ideas de la izquierda, luego los plazos de la derecha. Cierra viendo al público e invita a todo el equipo a responder preguntas.",
         texto=[
             "Para cerrar, dos ideas. La primera es la mejora continua. Los riesgos cambian todo el tiempo: aparecen nuevos ataques, cambiamos sistemas y proveedores y las leyes se reforman. Por eso el plan no termina hoy: revisamos la matriz cada trimestre y el plan completo cada año, y cada incidente debe dejarnos una lección.",
             "La segunda es la cultura. La tecnología ayuda, pero los riesgos se controlan con personas. El cajero que rota de ventanilla, el crupier que registra la revisión de la baraja o el empleado que reporta un correo sospechoso valen tanto como cualquier herramienta. La dirección debe dar el ejemplo y reconocer a quien reporta.",
             "Los próximos pasos ya tienen fecha: en 30 días los controles más urgentes; en 90 días la red segmentada, el cifrado y los expedientes de clientes; y en 120 días el control de cuentas de administrador, la prevención de fugas y los sensores en tragamonedas.",
             "Muchas gracias. Quedamos atentos a sus preguntas.",
         ]),
]

PREGUNTAS = [
    ("¿Por qué ISO 31000 y no otro estándar?", "fernando",
     "Porque sirve para cualquier tipo de riesgo, no solo de TI, y nos permitió tener en una sola matriz los riesgos de tecnología, de la operación de juego, de la caja y del cumplimiento legal."),
    ("¿Por qué R3 bajó de Alto a Moderado si en la matriz anterior era Alto?", "alejandro",
     "Porque la matriz anterior usaba una escala de 5 por 5. Al convertirla a la escala 3 por 3 del PIA, una probabilidad baja con impacto alto da Moderado según la regla."),
    ("¿Por qué el ransomware es el único riesgo crítico?", "rene",
     "Porque es probable, ya que hay intentos de correo engañoso frecuentes y equipos sin actualizar, y su impacto es alto: detendría la caja, las tragamonedas y el programa de lealtad."),
    ("¿Por qué aceptar un riesgo en lugar de controlarlo?", "kevin",
     "R4 ya tiene buenos controles y su nivel es bajo. Agregar más costaría más de lo que reduciría el riesgo, así que lo vigilamos cada trimestre y lo reevaluamos si cambia algo."),
    ("¿Cuál es la diferencia entre KPI y KRI?", "kevin",
     "El KPI mide si el control se está aplicando; el KRI mide qué tan expuesta está la empresa. Juntos dicen si el control realmente funciona."),
]


def minutos(palabras):
    return palabras / PALABRAS_POR_MINUTO


def palabras(d):
    return sum(len(p.split()) for p in d["texto"])


def nota(d):
    """Texto de las notas del orador de una diapositiva."""
    return f"[{ORADORES[d['quien']]}]\n\n" + "\n\n".join(d["texto"])


def validar():
    ns = [d["n"] for d in DIAPOSITIVAS]
    assert ns == list(range(1, 13)), ns
    asignadas = sorted(n for _, _, ss in PARTES for n in ss)
    assert asignadas == ns, asignadas
    for quien, _, ss in PARTES:
        for n in ss:
            assert DIAPOSITIVAS[n - 1]["quien"] == quien, (n, quien)
    assert PARTES[0][0] == "david" and PARTES[0][2][0] == 1


validar()
