# Importamos módulos requeridos
import os
import random
import pygame
import sys

# Estados del juego
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"

# Rutas a la carpeta de imágenes (Ajustado a tu estructura: data/Pantallas)
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "Pantallas")

# Se específica el nombre del archivo para cada imagen de pantalla.
PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"
PANTALLA_FONDO_JUEGO = "fondo_juego.bmp"

# Para evitar que el jugador se mueva demasiado rápido
RETRASO = 200

# Códigos de cada elemento del tablero
VACIO = 0
OBSTACULO = 1
JUGADOR = 2
MANZANA = 3

# Tamaño del tablero
FILAS = 15
COLUMNAS = 15

# Variables globales para cargar nuestros sprites y fondos una sola vez
IMG_GATO = None
IMG_CHURU = None
IMG_FONDO_JUEGO = None
IMG_OBSTACULO = None # NUEVO: Variable global para el obstáculo


def aparecer_aleatorio(tablero, id_elem):
    """
    Coloca un elemento en una casilla vacía aleatoria del tablero.
    """
    vacios = []

    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            elem_pos = tablero[fila][columna]
            if elem_pos == VACIO:
                vacios.append((columna, fila))

    if len(vacios) == 0:
        return -1, -1

    columna, fila = random.choice(vacios)
    tablero[fila][columna] = id_elem

    return columna, fila


def poblar_tablero(tablero):
    """
    Coloca un obstáculo y la manzana en el tablero.
    """
    aparecer_aleatorio(tablero, OBSTACULO)
    aparecer_aleatorio(tablero, MANZANA)


def refrescar_tablero(screen, tablero):
    """
    Dibuja el estado actual del tablero en la pantalla, usando nuestras imágenes y fondo.
    """
    if IMG_FONDO_JUEGO:
        screen.blit(IMG_FONDO_JUEGO, (0, 0))
    else:
        screen.fill((200, 200, 200))

    alto_elem = screen.get_height() / FILAS
    ancho_elem = screen.get_width() / COLUMNAS

    pos_y = 0

    for i in range(FILAS):
        pos_x = 0
        for j in range(COLUMNAS):
            if tablero[i][j] == OBSTACULO:
                # NUEVO: Dibuja la imagen del obstáculo si existe, sino dibuja el cuadro negro
                if IMG_OBSTACULO:
                    screen.blit(IMG_OBSTACULO, (pos_x, pos_y))
                else:
                    pygame.draw.rect(
                        screen,
                        "black",
                        pygame.Rect((pos_x, pos_y), (ancho_elem, alto_elem)),
                    )
            elif tablero[i][j] == JUGADOR:
                if IMG_GATO:
                    screen.blit(IMG_GATO, (pos_x, pos_y))
            elif tablero[i][j] == MANZANA:
                if IMG_CHURU:
                    screen.blit(IMG_CHURU, (pos_x, pos_y))

            pos_x += ancho_elem
        pos_y += alto_elem

    pygame.display.flip()


def cambiar_direccion(keys, direccion_actual):
    """
    Cambia la dirección del jugador.
    """
    if keys[pygame.K_w]:
        return (0, -1)
    if keys[pygame.K_s]:
        return (0, 1)
    if keys[pygame.K_a]:
        return (-1, 0)
    if keys[pygame.K_d]:
        return (1, 0)

    return direccion_actual


def avanzar(tablero, pos_jugador, direccion):
    """
    Avanza el jugador un paso en la dirección dada.
    """
    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = pos_jugador

    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "derrota", pos_jugador

    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO:
        return "derrota", pos_jugador

    if pos_elem == MANZANA:
        return "victoria", (ind_nueva_col, ind_nueva_fila)

    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila)


def reiniciar():
    """
    Crea un nuevo tablero y estado para una nueva partida.
    """
    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    poblar_tablero(tablero)
    pos_jugador = aparecer_aleatorio(tablero, JUGADOR)

    return tablero, pos_jugador


def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.
    """
    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen = pygame.transform.scale(imagen, screen.get_size())
        screen.blit(imagen, (0, 0))
        pygame.display.flip()
    except Exception as e:
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}. Error: {e}")


def main():
    # NUEVO: Añadimos IMG_OBSTACULO a las globales
    global IMG_GATO, IMG_CHURU, IMG_FONDO_JUEGO, IMG_OBSTACULO
    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Juego Michi Salem")

    ancho_celda = screen.get_width() // COLUMNAS
    alto_celda = screen.get_height() // FILAS

    try:
        ruta_gato = os.path.join(DIR_PANTALLAS, "gato.png")
        img_g = pygame.image.load(ruta_gato).convert_alpha()
        IMG_GATO = pygame.transform.scale(img_g, (ancho_celda, alto_celda))
    except Exception as e:
        print(f"No se pudo cargar gato.png: {e}")

    try:
        ruta_churu = os.path.join(DIR_PANTALLAS, "churu.png")
        img_c = pygame.image.load(ruta_churu).convert_alpha()
        IMG_CHURU = pygame.transform.scale(img_c, (ancho_celda, alto_celda))
    except Exception as e:
        print(f"No se pudo cargar churu.png: {e}")

    # NUEVO: Cargar y escalar la imagen del obstáculo
    try:
        ruta_obstaculo = os.path.join(DIR_PANTALLAS, "obstaculo.bmp")
        img_o = pygame.image.load(ruta_obstaculo).convert_alpha()
        IMG_OBSTACULO = pygame.transform.scale(img_o, (ancho_celda, alto_celda))
    except Exception as e:
        print(f"No se pudo cargar obstaculo.bmp: {e}")

    try:
        ruta_fondo_juego = os.path.join(DIR_PANTALLAS, PANTALLA_FONDO_JUEGO)
        img_f_j = pygame.image.load(ruta_fondo_juego).convert()
        IMG_FONDO_JUEGO = pygame.transform.scale(img_f_j, screen.get_size())
    except Exception as e:
        print(f"Advertencia: No se pudo cargar {PANTALLA_FONDO_JUEGO}: {e}. Se usará fondo gris.")


    running = True

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    direccion = (0, 0)
    tiempo_ultimo_mov = 0

    mostrar_pantalla(screen, PANTALLA_INICIO)

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if estado == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        tablero, pos_jugador = reiniciar()
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        refrescar_tablero(screen, tablero)
                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    if evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):
                    if evento.key == pygame.K_r:
                        tablero, pos_jugador = reiniciar()
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        refrescar_tablero(screen, tablero)
                    elif evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado == ESTADO_JUGANDO:
                    direccion = cambiar_direccion(pygame.key.get_pressed(), direccion)

        if estado == ESTADO_JUGANDO:
            tiempo_actual = pygame.time.get_ticks()

            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO:
                resultado, pos_jugador = avanzar(tablero, pos_jugador, direccion)

                if resultado == "derrota":
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                elif resultado == "victoria":
                    estado = ESTADO_VICTORIA
                    mostrar_pantalla(screen, PANTALLA_VICTORIA)
                else:
                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()