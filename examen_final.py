import xml.dom.minidom
import getpass
from ncclient import manager
from datetime import datetime

now=datetime.now()
date=now.strftime("%d/%m/%Y %H:%M:%S")
print('''
             **********************************************************
             *Ingrese la IP y las Credenciales de Usuario de su Router*
             **********************************************************
''')

ip_des=input("Ingrese la ip del Router: ")
usuario=input("Ingrese su usuario: ")
secret=input("Ingrese su contraseña: ")

m = manager.connect(
    host=ip_des,
    port=830,
    username=usuario,
    password=secret,
    hostkey_verify=False
)
def user_edit(name, priv, password):
    netconf_user=f"""
    <config>
        <native
            xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username>
                <name>{name}</name>
				<privilege>{priv}</privilege>
				<secret>
					<encryption>0</encryption>
					<secret>{password}</secret>
				</secret>
        </username>
        </native>
    </config>
    """
    netconf_reply=m.edit_config(target="running", config=netconf_user)

def host_name(name):
    netconf_name=f"""
    <config>
        <native
            xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{name}</hostname>
        </native>
    </config>
    """
    netconf_reply=m.edit_config(target="running", config=netconf_name)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

def interface_loopback(numero, ip, mask):
    netconf_loopback=f"""
    <config>
        <native
            xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>    
            <Loopback>
					<name>{numero}</name>
					<ip>
						<address>
							<primary>
								<address>{ip}</address>
								<mask>{mask}</mask>
							</primary>
						</address>
					</ip>
            </Loopback>
        </interface>
        </native>
    </config>
    """   
    netconf_reply=m.edit_config(target="running", config=netconf_loopback)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

def routin(ip, mask, inter, ip_hop):
    netconf_routing=f"""
    <config>
        <native
            xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
				<route>
					<ip-route-interface-forwarding-list>
						<prefix>{ip}</prefix>
						<mask>{mask}</mask>
						<fwd-list>
							<fwd>GigabitEthernet{inter}</fwd>
							<interface-next-hop>
								<ip-address>{ip_hop}</ip-address>
							</interface-next-hop>
						</fwd-list>
					</ip-route-interface-forwarding-list>
				</route>
        </ip>
        </native>
    </config>
    """
    netconf_reply=m.edit_config(target="running", config=netconf_routing)
    print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

def opcion_a():
    print(f''' 
             Bienvenido al asistente de configuración para Router Cisco
             **********************************************************
                         ________________________
                        |   {date}  |
                        |________________________|
                         by Cristian Colonia Rondinel
                         INTERCONEXION DE REDES

                        -VERSION: 16.9
                        -IP ADDRESS: {ip_des}
                        -DEFAULT GATEWAY: 192.168.1.1
                        -USERNAME: {usuario}
                        -INTERFACE-UP: GigabitEthernet 1
                
        ESCOJA UNA DE LAS OPCIONES DE CONFIGURACION:

        1. Configurar Usuario.
        2. Configurar nombre del Router.
        3. Configurar Interfaz Loopback.
        4. Configurar Enrutamiento Estatico.
        5. Salir.
                                         

    ''')

    opcion=input(" ---->  ")
    return(opcion)

def opcion_1():
    print('''
              CONFIGURAR USUARIO
              ******************
              ''')
    name=input("Ingrese el nombre de Usuario: ")
    priv=input("Privilegio del usuario: ")
    pasw=getpass.getpass("Introdusca la contraseña: ")
    user_edit(name, priv, pasw)
def opcion_2():
    print('''
              CONFIGURAR NOMBRE DEL ROUTER
              ****************************
              ''')
    name=input("Nombre del Router: ")
    host_name(name)
def opcion_3():
    print('''
              CONFIGURAR INTERFAZ LOOPBACK
              ****************************
              ''')
    numero=input("Numero de la loopback: ")
    ip=input("Ip de la Loopback: ")
    mask=input("Mascara de la Loopback: ")
    interface_loopback(numero, ip, mask)

def opcion_4():
    print('''
              CONFIGURAR ENRUTAMIENTO ESTATICO
              ********************************
              ''')
    ip=input("Introdusca la Red: ")
    mask=input("Introdusca la masca de la Red: ")
    inter=input("Introdusca el numero de la interfaz GigabitEthernet: ")
    ip_hop=input("Introdusca la Ip del siguiente salto: ")
    routin(ip, mask, inter, ip_hop)

def opcion_5():
    print(f'''
                  GRACIAS POR USAR EL ASISTENTE
                  *****************************
                  Sesion Terminada: {date}
                  Cerrando sesion del usuario: {usuario}


    ''')
    
while True:
    a=opcion_a()
    if a=="1":
        opcion_1()
        while True:
            cont=input("Desea Crear otro Usuario?(s/n) ")
            if cont=="s":
                opcion_1()
            else:
                break
        
    if a=="2":
        opcion_2()
        while True:
            cont=input("Desea Cambiar el Nombre del Router?(s/n) ")
            if cont=="s":
                opcion_2()
            else:
                break
            
                
    if a=="3":
        opcion_3()
        while True:
            cont=input("Desea Configurar otra Interfaz Loopback?(s/n) ")
            if cont=="s":
                opcion_3()
            else:
                break
    if a=="4":
        
        opcion_4()
        while True:
            cont=input("Desea Configurar otro Enrutamiento Estatico?(s/n) ")
            if cont=="s":
                opcion_4()
            else:
                break
    if a=="5":
        opcion_5()
        break
