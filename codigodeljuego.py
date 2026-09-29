import os
import sys
import random

# Estado global del jugador y el juego
jugador = {
    "vida": 100,
    "vida_max": 100,
    "diamantes": 0,
    "tiene_linterna": False,
    "tiene_mochila": False,
    "tiene_escudo": False,
    "inventario": [],
    "limite_inventario": 3,
    "llave_encontrada": False
}

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_salida():
    """Menú de interfaz para cuando el jugador decide salir o está en pausa."""
    while True:
        limpiar_pantalla()
        print("========================================")
        print("         ¿DESEAS ABANDONAR LA ESCUELA?    ")
        print("========================================")
        print(" 1. Volver al juego actual")
        print(" 2. Volver al menú principal")
        print(" 3. Salir del juego (Cerrar)")
        print("----------------------------------------")
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            return
        elif opcion == "2":
            menu_principal()
            break
        elif opcion == "3":
            limpiar_pantalla()
            print("\nHas decidido quedarte en las sombras... Nadie sale de aquí fácilmente.")
            print("¡Hasta la próxima!\n")
            sys.exit()
        else:
            input("\nOpción inválida. Presiona Enter para intentar de nuevo...")

def tienda():
    """Tienda para comprar mejoras y skins usando diamantes."""
    while True:
        limpiar_pantalla()
        print("========================================")
        print("        TIENDA DE LA ESCUELA            ")
        print("========================================")
        print(f" Tienes 💎 {jugador['diamantes']} diamantes.")
        print("----------------------------------------")
        print(" 1. Comprar Botiquín (Restaura 50 HP) - 💎 5")
        print(" 2. Mejora de Escudo Protector - 💎 10")
        print(" 3. Linterna de Alta Potencia (Ilumina más) - 💎 8")
        print(" 4. Salir de la tienda")
        print("========================================")
        
        opcion = input("Elige una opción: ").strip()
        
        if opcion == "1":
            if jugador["diamantes"] >= 5:
                jugador["diamantes"] -= 5
                if len(jugador["inventario"]) < jugador["limite_inventario"]:
                    jugador["inventario"].append("Botiquín")
                    print("\n¡Has comprado un Botiquín y se guardó en tu inventario!")
                else:
                    print("\n¡Inventario lleno! El botiquín se usó de inmediato para curarte.")
                    jugador["vida"] = min(jugador["vida_max"], jugador["vida"] + 50)
            else:
                print("\n¡No tienes suficientes diamantes!")
            input("\nPresiona Enter para continuar...")
        elif opcion == "2":
            if jugador["diamantes"] >= 10:
                jugador["diamantes"] -= 10
                jugador["tiene_escudo"] = True
                print("\n¡Has mejorado/conseguido el Escudo! Ahora estás más protegido.")
            else:
                print("\n¡No tienes suficientes diamantes!")
            input("\nPresiona Enter para continuar...")
        elif opcion == "3":
            if jugador["diamantes"] >= 8:
                jugador["diamantes"] -= 8
                jugador["tiene_linterna"] = True
                print("\n¡Linterna mejorada! Ahora ves con claridad en los pasillos más oscuros.")
            else:
                print("\n¡No tienes suficientes diamantes!")
            input("\nPresiona Enter para continuar...")
        elif opcion == "4":
            break
        else:
            input("\nOpción inválida. Presiona Enter...")

def explorar_habitacion():
    """Lógica principal de exploración de la escuela."""
    eventos = ["objeto", "criatura", "vacio", "tienda"]
    evento = random.choice(eventos)
    
    limpiar_pantalla()
    print("========================================")
    print("         EXPLORANDO LA ESCUELA          ")
    print("========================================")
    
    if not jugador["tiene_linterna"]:
        print("⚠️ Estás a oscuras. Apenas puedes ver por dónde pisas...")
    else:
        print("🔦 Tu linterna alumbra los tenebrosos pasillos de la escuela.")
        
    print(f"❤️ Vida: {jugador['vida']}/{jugador['vida_max']} | 💎 Diamantes: {jugador['diamantes']} | 🎒 Inventario: {len(jugador['inventario'])}/{jugador['limite_inventario']}")
    print("----------------------------------------")
    
    input("\nPresiona Enter para abrir la puerta de la siguiente habitación...")

    if evento == "objeto":
        hallazgo = random.choice(["Linterna", "Botiquín", "Mochila", "Diamantes"])
        limpiar_pantalla()
        print("✨ ¡Has encontrado algo en un casillero viejo!")
        
        if hallazgo == "Linterna":
            jugador["tiene_linterna"] = True
            print("🔦 ¡Encontraste una Linterna! Ahora la oscuridad no te cegará.")
        elif hallazgo == "Mochila":
            jugador["tiene_mochila"] = True
            jugador["limite_inventario"] = 6
            print("🎒 ¡Encontraste una Mochila! Tu inventario se ha expandido a 6 espacios.")
        elif hallazgo == "Diamantes":
            cant = random.randint(3, 8)
            jugador["diamantes"] += cant
            print(f"💎 ¡Encontraste un escondite con {cant} diamantes!")
        elif hallazgo == "Botiquín":
            print("💊 Has encontrado un Botiquín.")
            if len(jugador["inventario"]) < jugador["limite_inventario"]:
                jugador["inventario"].append("Botiquín")
                print("Se ha guardado en tu inventario.")
            else:
                print("Tu inventario está lleno. Lo usas de inmediato.")
                jugador["vida"] = min(jugador["vida_max"], jugador["vida"] + 40)
        
        # Posibilidad de hallar la llave de salida
        if not jugador["llave_encontrada"] and random.random() < 0.3:
            jugador["llave_encontrada"] = True
            print("🔑 ¡Increíble! También encontraste la LLAVE PRINCIPAL para escapar de la escuela.")

    elif evento == "criatura":
        limpiar_pantalla()
        print("⚠️ ¡PELIGRO! ¡Una criatura de las sombras te ha amboscado!")
        print("Los susurros ensordecedores te paralizan por un momento...")
        
        daño = random.randint(25, 45)
        if jugador["tiene_escudo"]:
            print("🛡️ ¡Tu escudo absorbió parte del ataque de la criatura!")
            daño = max(5, daño // 2)
            
        jugador["vida"] -= daño
        print(f"La criatura te ha atacado. Has perdido {daño} puntos de vida.")
        
        if jugador["vida"] <= 0:
            print("\n💀 Las criaturas te han atrapado. La oscuridad te consume...")
            print("========================================")
            print("           FIN DEL JUEGO                ")
            print("========================================")
            input("\nPresiona Enter para volver al menú principal...")
            return "game_over"

    elif evento == "tienda":
        print("🏫 Has encontrado un aula extraña y segura con un altar misterioso (Tienda).")
        op = input("¿Deseas entrar a la tienda? (s/n): ").strip().lower()
        if op == 's':
            tienda()

    else:
        print("💨 Esta habitación está vacía, solo hay eco y polvo en el ambiente.")
        if not jugador["llave_encontrada"] and random.random() < 0.2:
            jugador["llave_encontrada"] = True
            print("🔑 ¡Bajo una carpeta vieja encuentras la LLAVE PRINCIPAL de la escuela!")

    input("\nPresiona Enter para continuar explorando...")
    return "continuar"

def gestionar_inventario():
    """Permite usar objetos del inventario como botiquines."""
    limpiar_pantalla()
    print("========================================")
    print("           INVENTARIO                   ")
    print("========================================")
    print(f"Espacios: {len(jugador['inventario'])}/{jugador['limite_inventario']}")
    print(f"Objetos: {jugador['inventario']}")
    print("----------------------------------------")
    if "Botiquín" in jugador["inventario"]:
        op = input("¿Deseas usar un Botiquín para curarte? (s/n): ").strip().lower()
        if op == 's':
            jugador["inventario"].remove("Botiquín")
            jugador["vida"] = min(jugador["vida_max"], jugador["vida"] + 50)
            print("❤️ Te has curado. Vida actual:", jugador["vida"])
    else:
        print("No tienes objetos utilizables en este momento.")
    input("\nPresiona Enter para volver...")

def iniciar_juego():
    """Inicia o reinicia las estadísticas del juego principal."""
    global jugador
    jugador = {
        "vida": 100,
        "vida_max": 100,
        "diamantes": 0,
        "tiene_linterna": False,
        "tiene_mochila": False,
        "tiene_escudo": False,
        "inventario": [],
        "limite_inventario": 3,
        "llave_encontrada": False
    }
    
    limpiar_pantalla()
    print("========================================")
    print("     CARGANDO: ESCAPE ESCOLAR...        ")
    print("========================================")
    print("\nDespiertas en un pasillo oscuro y frío. El suelo está cubierto de polvo")
    print("y papeles viejos. A lo lejos, escuchas pasos arrastrándose y susurros...")
    print("Debes encontrar la llave y escapar antes de que te encuentren.")
    input("\nPresiona Enter para comenzar tu escape...")

    while jugador["vida"] > 0:
        # Si ya tiene la llave, puede intentar escapar
        if jugador["llave_encontrada"]:
            limpiar_pantalla()
            print("========================================")
            print("     ¡TIENES LA LLAVE PRINCIPAL!        ")
            print("========================================")
            print(" 1. Seguir explorando (buscar más diamantes)")
            print(" 2. Ir hacia la puerta principal y ESCAPAR")
            print(" 3. Ver inventario / Pausa")
            opcion = input("Elige una acción (1-3): ").strip()
            
            if opcion == "2":
                limpiar_pantalla()
                print("🌟 ¡Corres hacia las grandes puertas de la escuela, abres con la llave y huyes hacia la libertad!")
                print("¡HAS GANADO EL JUEGO, SOBREVIVISTE A LA ESCUELA ABANDONADA! 🎉")
                input("\nPresiona Enter para volver al menú principal...")
                return
            elif opcion == "3":
                menu_salida()
                continue
        
        # Bucle de acciones normales
        limpiar_pantalla()
        print("========================================")
        print("          PASILLOS DE LA ESCUELA        ")
        print("========================================")
        print(f"❤️ Vida: {jugador['vida']} | 💎 Diamantes: {jugador['diamantes']} | 🔑 Llave: {'Sí' if jugador['llave_encontrada'] else 'No'}")
        print("----------------------------------------")
        print(" 1. Explorar la siguiente habitación")
        print(" 2. Revisar Inventario / Usar Botiquín")
        print(" 3. Pausa / Menú de Salida")
        print("========================================")
        
        opcion = input("Elige una opción (1-3): ").strip()
        
        if opcion == "1":
            resultado = explorar_habitacion()
            if resultado == "game_over":
                break
        elif opcion == "2":
            gestionar_inventario()
        elif opcion == "3":
            menu_salida()
        else:
            input("\nOpción inválida. Presiona Enter...")

def menu_principal():
    """Menú de bienvenida antes de iniciar el juego."""
    while True:
        limpiar_pantalla()
        print("========================================")
        print("           ESCUELA ABANDONADA           ")
        print("        El Despertar de las Sombras     ")
        print("========================================")
        print(" 1. Iniciar Juego")
        print(" 2. Controles / Instrucciones")
        print(" 3. Salir del Juego")
        print("----------------------------------------")
        
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            iniciar_juego()
        elif opcion == "2":
            limpiar_pantalla()
            print("========================================")
            print("               INSTRUCCIONES            ")
            print("========================================")
            print(" - Explora las aulas en busca de la llave y objetos.")
            print(" - Linterna: Te ayuda a guiarte en la oscuridad.")
            print(" - Botiquines: Restauran tu salud ante los ataques.")
            print(" - Mochila: Amplía tu inventario de 3 a 6 espacios.")
            print(" - Diamantes: Úsalos en la tienda para comprar mejoras.")
            print(" - Escudo: Te protege contra el daño de las criaturas.")
            print("========================================")
            input("\nPresiona Enter para regresar al menú...")
        elif opcion == "3": 
            limpiar_pantalla()
            print("\n¡Gracias por jugar! Hasta pronto.")
            sys.exit()
        else:
            input("\nOpción inválida. Presiona Enter para intentar de nuevo...")

if __name__ == "__main__":
    menu_principal()