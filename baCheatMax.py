# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import os, random, json
import shutil
from datetime import datetime, timedelta
import bascenev1 as bs
import bauiv1 as bui
import babase as ba
import _babase
import time 
from bascenev1._activity import Activity
from bascenev1lib.actor.bomb import Bomb
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.mainmenu import MainMenuActivity
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spazfactory import SpazFactory
import bascenev1lib.actor.popuptext as ptext
import bascenev1lib.actor.text as text
import bascenev1lib.actor.image as image
import bascenev1lib.actor.spaz as spaz

if TYPE_CHECKING:
    from typing import Sequence, Any, Callable

def act():
    """الحصول على النشاط الحالي مع تحسينات"""
    try:
        # الطريقة الأساسية
        activity = bs.get_foreground_host_activity()
        if activity is not None:
            return activity
        
        # الطريقة البديلة 1
        try:
            from bascenev1._session import Session
            session = bs.getsession()
            if hasattr(session, 'activity'):
                activity = session.activity
                if activity is not None:
                    return activity
        except:
            pass
        
        # الطريقة البديلة 2
        try:
            import _babase
            activity = _babase.get_foreground_host_activity()
            if activity is not None:
                return activity
        except:
            pass
        
        # الطريقة البديلة 3 - البحث في المكدس
        try:
            import babase._app
            app = babase._app
            if hasattr(app, '_foreground_host_session'):
                session = app._foreground_host_session
                if session and hasattr(session, 'activity'):
                    return session.activity
        except:
            pass
        
    except Exception as e:
        print(f"⚠️ Error in act(): {e}")
    
    return None

class Lang:
    def __init__(self,
                 text: str,
                 subs: list[str] = 'none'):

        
        icons = [bui.charstr(bui.SpecialChar.CROWN),
                 bui.charstr(bui.SpecialChar.LOGO)]

 
        lang = bs.app.lang.language
        setphrases = {
            "Installing":
                {"Spanish": f"Instalando <{__name__}>",
                 "English": f"Installing <{__name__}>",
                 "Portuguese": f"Instalando <{__name__}>"},
            "Installed":
                {"Spanish": f"¡<{__name__}> Se instaló correctamente!",
                 "English": f"<{__name__}> Installed successfully!",
                 "Portuguese": f"<{__name__}> Instalado com sucesso!"},
            "Make Sys":
                {"Spanish": "Se creó la carpeta sys",
                 "English": "Sys folder created",
                 "Portuguese": "Pasta sys criada"},
            "Restart Msg":
                {"Spanish": "Reiniciando...",
                 "English": "Rebooting...",
                 "Portuguese": "Reinício..."},
            "EJ":
                {"Spanish": f"Datos incompletos \n Ejemplo: {subs}",
                 "English": f"Incomplete data \n Example: {subs}",
                 "Portuguese": f"Dados incompletos \n Exemplo: {subs}"},
            "EX":
                {"Spanish": f"Ejemplo: {subs}",
                 "English": f"Example: {subs}",
                 "Portuguese": f"Exemplo: {subs}"},
            "Error Entering Client ID":
                {"Spanish": f"'{subs[0]}' no es válido. \n Ingresa números \n Ejemplo: {subs[1]}",
                 "English": f"'{subs[0]}' is invalid. \n Enter numbers \n Example: {subs[1]}",
                 "Portuguese": f"'{subs[0]}' é inválido. \n Digite os números \n Exemplo: {subs[1]}"},
            "Error Entering Player ID":
                {"Spanish": f"'{subs}' no es válido. \n Ingresa el ID del jugador. consulta el comando '/list'",
                 "English": f"'{subs}' no es válido. \n Add the player ID. use the '/list' command for more information.",
                 "Portuguese": f"'{subs}' no es válido. \n Adicione o ID do jogador. use o comando '/list' para obter mais informações."},
            "Happy":
                {"Spanish": "¡Estás felíz!",
                 "English": "Are you happy!",
                 "Portuguese": "Você está feliz!"},
            "Add Admin Msg":
                {"Spanish": f"'{subs}' Se agregó a la lista de Admins",
                 "English": f"'{subs}' Added to Admins list",
                 "Portuguese": f"'{subs}' Adicionado à lista de administradores"},
            "Delete Admin Msg":
                {"Spanish": f"Se removió a '{subs}' de la lista de Admins",
                 "English": f"'{subs}' was removed from the Admins list",
                 "Portuguese": f"'{subs}' foi removido da lista de administradores"},
            "Players Data":
                {"Spanish": "Nombre | Jugador ID | Cliente ID",
                 "English": "Name | Player ID | Client ID",
                 "Portuguese": "Nome |  Jogador ID |  ID do Cliente"},
            "Party Info":
                {"Spanish": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descripción: {subs[1]}\n{icons[1]}|Versión: {_babase.app.env.engine_version}",
                 "English": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Description: {subs[1]}\n{icons[1]}|Version: {_babase.app.env.engine_version}",
                 "Portuguese": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descrição: {subs[1]}|\n{icons[1]}|Versão: {_babase.app.env.engine_version}"},
            "Same Player":
                  {"Spanish": "No puedes expulsarte a tí mismo",
                   "English": "You cannot expel yourself",
                   "Portuguese": "Você não pode se expulsar"},
            "Kick Msg":
                  {"Spanish": f"Sin rodeos, {subs[0]} ha expulsado a {subs[1]}",
                   "English": f"{subs[0]} kicked {subs[1]} Goodbye!",
                   "Portuguese": f"{subs[0]} expulsou {subs[1]}"},
            "User Invalid":
                {"Spanish": f"'{subs}' No le pertenece a ningún jugador.",
                 "English": f"'{subs}' Does not belong to any player.",
                 "Portuguese": f"'{subs}' Não pertence a nenhum jogador."},
            "Chat Live":
                {"Spanish": f"{icons[0]} CHAT EN VIVO {icons[0]}",
                 "English": f"{icons[0]} CHAT LIVE {icons[0]}",
                 "Portuguese": f"{icons[0]} BATE-PAPO AO VIVO {icons[0]}"},
            "Not Exists Node":
                {"Spanish": "No estás en el juego",
                 "English": "You're not in the game",
                 "Portuguese": "Você não está no jogo"},
            "Show Spaz Messages":
                {"Spanish": "Mostrar mensajes arriba de los jugadores.",
                 "English": "Show messages above players.",
                 "Portuguese": "Mostrar mensagens acima dos jogadores."},
            "Mute Message":
                {"Spanish": f"Se silenció a {subs}",
                 "English": f"{subs} was muted",
                 "Portuguese": f"{subs} foi silenciado"},
            "Unmute Message":
                {"Spanish": f"Se quitó el muteo a {subs}",
                 "English": f"{subs} can chat again",
                 "Portuguese": f"{subs} pode conversar novamente"},
            "Not In Admins":
                {"Spanish": f"No se puede silenciar a [{subs}] porque es administrador.",
                 "English": f"[{subs}] cannot be muted because he is an administrator.",
                 "Portuguese": f"[{subs}] não pode ser silenciado porque é um administrador."},
            "Module Not Found":
                {"Spanish": "No se encontraron los módulos. usa el comando '!dw' para descargarlos.",
                 "English": "Modules not found. use the '!dw' command to download them.",
                 "Portuguese": "Módulos não encontrados.  use o comando '!dw' para baixá-los."},
            "Clima Error Message":
                {"Spanish": "Selecciona un clima,\n Usa el comando '-climas' para más información.",
                 "English": "Select a weather,\n Use the command '-climas' for more information.",
                 "Portuguese": "Selecione um clima,\n Use o comando '-climas' para mais informações."},
            "Clima Message":
                {"Spanish": f"Se cambió el clima a '{subs}'",
                 "English": f"The weather is now '{subs}'",
                 "Portuguese": f"O tempo está agora '{subs}'"},
           "None Account":
                {"Spanish": "Información del jugador no válida.",
                 "English": "Informações do jogador inválidas.",
                 "Portuguese": "Informações do jogador inválidas."}, 
           "Error ID User":
                {"Spanish": f"Se produjo un error al ingresar el ID del jugador. \n '{subs}' no es válido.",
                 "English": f"An error occurred while entering the player ID. \n '{subs}' is not valid.",
                 "Portuguese": f"Ocorreu um erro ao inserir o ID do jogador.  \n '{subs}' não é válido."},
           "Effect Invalid":
                {"Spanish": f"'{subs}' es inválido. ingresa el comando '-effects' para más información.",
                 "English": f"'{subs}' is invalid. enter the command '-effects' for more information.",
                 "Portuguese": f"'{subs}' é inválido. digite o comando '-effects' para mais informações."},
           "Use /list Command":
                {"Spanish": "Le sugerimos usar el comando '/list'",
                 "English": "We suggest you use the '/list' command",
                 "Portuguese": "Sugerimos que você use o comando '/list'"},
           "Add Effect Message":
                {"Spanish": f"Se agregó el efecto '{subs[0]}' a {subs[1]}",
                 "English": f"Added '{subs[0]}' effect to {subs[1]}",
                 "Portuguese": f"Adicionado efeito '{subs[0]}' para {subs[1]}"},
           "You Are Amazing":
                {"Spanish": "¡¡Eres ASOMBROSO!!",
                 "English": "You Are Amazing!!",
                 "Portuguese": "Você é incrível!!"},
           "Owner Added":
                {"Spanish": "¡Se agregó al propietario!",
                 "English": "Owner added!",
                 "Portuguese": "Proprietário adicionado!"},
           "Is Owner":
                {"Spanish": "¡Eres el propietario!",
                 "English": "You are the owner!",
                 "Portuguese": "Você é o proprietário!"},
           "Exe":
                {"Spanish": "Comando Ejecutado",
                 "English": "Command Executed",
                 "Portuguese": "Comando Executado"
            },
                 
            # ES
            "Agrega un texto":
                {"Spanish": "Añade un texto",
                 "English": "Add text",
                 "Portuguese": "Adicione texto"},
            "Cambios Guardados":
                {"Spanish": "Información guardada correctamente",
                 "English": "Information saved successfully",
                 "Portuguese": "Informações salvas com sucesso"},
            "Info Color":
                {"Spanish": "Argumento no válido, \n te sugerimos usar el comando '-colors'",
                 "English": "Invalid argument, \n we suggest you use the '-colors' command",
                 "Portuguese": "Argumento inválido, \n sugerimos que você use o comando '-colors'"},
            "ID Cliente Msj":
                {"Spanish": "Agrega el ID del cliente. \n utilice el comando '/list' para más información.",
                 "English": "Add the client ID.  \n use the '/list' command for more information.",
                 "Portuguese": "Adicione o ID do cliente. \n use o comando '/list' para mais informações."},
            "Guardando Informacion":
                {"Spanish": "Estamos guardando sus datos...",
                 "English": "Saving user data...",
                 "Portuguese": "Estamos salvando seus dados..."},
            "Ban A Admin Mensaje":
                {"Spanish": f"No puedes expulsar a [{subs}] porque es administrador",
                 "English": f"You can't kick [{subs}] because he's an admin",
                 "Portuguese": f"Você não pode chutar [{subs}] porque ele é um administrador"},
            "No Info Activa":
                {"Spanish": "Necesitas tener activa la información.\n Usa el comando '-info' para activarle.",
                 "English": "You need to have info active.\n Use the '-info' command to activate it",
                 "Portuguese": "Você precisa ter as informações ativas.\n Use o comando '-info' para ativá-las"},
            "ServerClosed":
                {"Spanish": f"El servidor está cerrado por {subs[0]} horas para entrenamiento del tag '{subs[1]}'",
                 "English": f"Server closed for {subs[0]} hours for '{subs[1]}' tag training",
                 "Portuguese": f"Servidor fechado por {subs[0]} horas para treino da tag '{subs[1]}'"},
            "ServerClosedMessage":
                {"Spanish": f"Hay un partido de entrenamiento para {subs[0]}. Intenta unirte después de {subs[1]}",
                 "English": f"There's a training match for {subs[0]}. Please try to join again after {subs[1]}",
                 "Portuguese": f"Há uma partida de treino para {subs[0]}. Por favor, tente entrar novamente após {subs[1]}"},
            "ServerAlreadyClosed":
                {"Spanish": "El servidor ya está cerrado",
                 "English": "Server is already closed",
                 "Portuguese": "O servidor já está fechado"},
            "ServerClosedStopped":
                {"Spanish": "El cierre del servidor ha sido detenido",
                 "English": "Server closure has been stopped",
                 "Portuguese": "O fechamento do servidor foi interrompido"},
            "NoServerCloseActive":
                {"Spanish": "No hay cierre de servidor activo",
                 "English": "No server closure active",
                 "Portuguese": "Nenhum fechamento de servidor ativo"},
            "ServerCloseStarted":
                {"Spanish": f"✅ Servidor cerrado por {subs[0]} horas para el tag '{subs[1]}'",
                 "English": f"✅ Server closed for {subs[0]} hours for tag '{subs[1]}'",
                 "Portuguese": f"✅ Servidor fechado por {subs[0]} horas para a tag '{subs[1]}'"},
            "InvalidHours":
                {"Spanish": "Las horas deben ser un número positivo",
                 "English": "Hours must be a positive number",
                 "Portuguese": "As horas devem ser um número positivo"},
            "StopCloseServer":
                {"Spanish": "Usa: /stopcloseserver",
                 "English": "Use: /stopcloseserver",
                 "Portuguese": "Use: /stopcloseserver"},
            "CloseServerUsage":
                {"Spanish": "Usa: /closeserver <horas> <tag-name>",
                 "English": "Use: /closeserver <hours> <tag-name>",
                 "Portuguese": "Use: /closeserver <horas> <tag-name>"},
                     }
    
        language = ["Spanish", "English", "Portuguese"]
        if lang not in language:
            lang = "English"
            
        if text not in setphrases:
            self.text = text
        else:
            self.text = setphrases[text][lang]
    
    def get(self):
        return self.text


def getlanguage(*args, **kwargs) -> str:
    subs = kwargs.get('subs', 'none')
    
    if type(subs) is not list:
        subs = str(subs)
    else:
        subs = [str(s) for s in subs]
    try:
        text = Lang(*args, subs=subs).get()
    except (IndexError, Exception):
        text = Lang(*args).get()
        text = text.replace('none', str(subs))
    finally:
        return text


calls: dict[str, Any] = {}
Chats: list[str] = []
roster = bs.get_game_roster
mutelist = list()
cfg = dict()

class PopupText(ptext.PopupText):
    """New PopupText."""
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node.shadow = 10.0
        self.node.color = (1.5, 1.5, 1.5, 1.0)
        bs.animate(self._combine, 'input3', {0: 0, 0.1: 1.0})
        
    def handlemessage(self, msg: Any) -> Any:
        pass
    
class Commands:
    """Usa los distintos comandos dependiendo tu rango (All, Admins)."""
    fct: Any
    util: Any
    
    @property
    def get(self) -> str:
        return self.value
    
    def __init__(self,
                 msg: str,
                 client_id: int,
                 arguments: list[str] = []) -> None:
            
        self.message = msg
        self.msg = msg.strip()
        self.client_id = client_id
        self.arguments = arguments
        self.value = None

        self.util = Uts
        self.fct = CommandFunctions

        # معالجة الأوامر
        self.process_commands()
        
    def process_commands(self):
        """معالجة جميع الأوامر"""
        try:
            # معالجة أوامر عامة للجميع
            self.command_all()
            
            # معالجة أوامر الأدمنز
            if self.fct.user_is_admin(self.client_id):
                self.admin_commands()
                
            # معالجة أوامر المالك
            if self.fct.user_is_owner(self.client_id):
                self.owner_commands()
                
        except Exception as e:
            print(f"❌ Error in process_commands: {e}")
            self.value = None
        
    def send_chat_message(self, message):
        try:
            bs.chatmessage(str(message), clients=[self.client_id], sender_override="")
        except:
            self.clientmessage('ERROR', color=(1,0,0))
            
    def clientmessage(self, msg: str,
            color: Sequence[float] = None):
        """إرسال رسالة شاشة عابرة"""
        # حل بديل لمعالجة الخطأ
        try:
            if color is not None:
                # محاولة استخدام bs.screenmessage مع clients
                bs.screenmessage(msg, color=color, clients=[self.client_id])
            else:
                bs.screenmessage(msg, clients=[self.client_id])
        except TypeError:
            # إذا فشل، استخدم bs.broadcastmessage
            try:
                if color is not None:
                    bs.broadcastmessage(msg, color=color, clients=[self.client_id])
                else:
                    bs.broadcastmessage(msg, clients=[self.client_id])
            except:
                # إذا فشل كل شيء، استخدم bs.screenmessage بدون clients
                if color is not None:
                    bs.screenmessage(msg, color=color)
                else:
                    bs.screenmessage(msg)
        except:
            # Fallback في حالة وجود مشكلة
            if color is not None:
                bs.screenmessage(msg, color=color)
            else:
                bs.screenmessage(msg)
    
    def command_all(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cmd = self.fct.all_cmd()
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage
    
        if msg.lower() == cmd[0]: # -pan
            self.util.cm("¡Haz recibido pan de \ue061Sr.Palomo!")
            self.value = '@'
        
        elif msg.lower() == cmd[1]: # -ceb
            current_act = bs.get_foreground_host_activity()
            if current_act is not None and cls_node is not None:
                with current_act.context:
                    if cls_node.node and cls_node.node.exists():
                        cls_node.handlemessage(
                            bs.CelebrateMessage(duration=3.0))
                ClientMessage("Are you happy!", color=(1.0, 1.0, 0.0))
            self.value = '@'
            
        elif msg.lower() == cmd[2]: # -colors
            cols = str()
            cols_list = self.util.sort_list(list(self.util.colors().keys()))
            for c in cols_list:
                cols += (' | '.join(c) + '\n')
            ClientMessage(cols)
            self.value = '@'
            
        elif msg.lower() == cmd[3]: # -mp (max players)
            mp = bs.get_public_party_max_size()
            ClientMessage(f"Max Players: {mp}")
            self.value = '@'

        elif msg.lower() == cmd[4]: # -pb
            self.fct.get_my_pb(self.client_id)
            self.value = '@'
    
        elif msg.lower() == cmd[5]: # -effects
            cols = str()
            for e in self.fct.effects():
                cols += (' | ' + e)
            ClientMessage(cols)
            self.value = '@'
            
        elif msg.lower() == '/list':  # الأمر لعرض قائمة اللاعبين
            self.process_list_players()
            self.value = '@'
            
        elif msg.lower() in ['test', 'تست']:
            self.clientmessage("✅ CheatMax is working!", color=(0, 1, 0))
            self.value = '@'
            
        elif msg.lower() in ['help', 'مساعدة']:
            help_msg = "📋 Commands: /list, -colors, -effects, test"
            self.clientmessage(help_msg)
            self.value = '@'
    
    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]
    
        if ms[0] == cmd[0]: # /name 0 La Pulga
            try: 
                name = ms[2]
            except:
                color = self.util.colors()['orange']
                ClientMessage(f"Incomplete data \n Example: {ms[0]} 0 La Pulga | {ms[0]} all La Pulga", color=color)
                self.value = '@'
            else:
                self.fct.actor_command(ms=ms,
                    call=bs.CallStrict(self.fct.actor_name, ' '.join(ms[2:])),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
                self.value = '@'
    
        elif ms[0] == cmd[1]: # /imp
            self.fct.actor_command(ms=ms,
                call=self.fct.impulse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
            
        elif ms[0] == cmd[2]: # /box
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_box,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                       
        elif ms[0] == cmd[3] or ms[0] == cmd[4]: # /addAdmin
            if len(ms) == 1:
                ClientMessage("Add the client ID. \n use the '/list' command for more information.")
                self.value = '@'
            else:
                try:
                    c_id = int(ms[1])
                except ValueError:
                    ClientMessage(
                            f"'{ms[1]}' is invalid. \n Enter numbers \n Example: /addAdmin 113")
                    self.value = '@'
                else:
                    if c_id not in self.util.usernames:
                            ClientMessage(f"'{c_id}' Does not belong to any player.")
                            self.value = '@'
                    else:
                        if ms[0] == cmd[3]:
                            self.util.add_or_del_user(c_id, add=True)
                        else:
                            self.util.add_or_del_user(c_id, add=False)
                        self.value = '@'
                        
        elif ms[0] == cmd[5]: # /kill
            self.fct.actor_command(ms=ms,
                call=self.fct.kill_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                        
        elif ms[0] == cmd[6]: # -pause
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                self.fct.pause()
            self.value = '@'
                        
        elif ms[0] == cmd[7]: # /infoHost
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage("You need to have info active.\n Use the '-info' command to activate it")
                self.value = '@'
            else:
                if len(ms) == 1:
                    ClientMessage("Add text")
                    self.value = '@'
                else:
                    cfg['Commands']['HostName'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage("Information saved successfully", color=(0.0, 1.0, 0.0))
                    self.value = '@'
                
        elif ms[0] == cmd[8]: # /infoDes
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage("You need to have info active.\n Use the '-info' command to activate it")
                self.value = '@'
            else:
                if len(ms) == 1:
                    ClientMessage("Add text")
                    self.value = '@'
                else:
                    cfg['Commands']['Description'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage("Information saved successfully", color=(0.0, 1.0, 0.0))
                    self.value = '@'
    
        elif ms[0] == cmd[9]: # -info
            if cfg['Commands'].get('ShowInfo'):
                cfg['Commands']['ShowInfo'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowInfo'] = True
                color = self.util.colors()['green']
                
            self.util.save_settings()
            ClientMessage("Information saved successfully", color=color)
            self.value = '@'
    
        elif ms[0] == cmd[10]: # /infoColor
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage("You need to have info active.\n Use the '-info' command to activate it")
                self.value = '@'
            else:
                if len(ms) == 1:
                    ClientMessage("Invalid argument, \n we suggest you use the '-colors' command")
                    self.value = '@'
                else:
                    if ms[1] not in self.util.colors():
                        ClientMessage("Invalid argument, \n we suggest you use the '-colors' command", color=(1, 0.5, 0))
                        self.value = '@'
                    else:
                        cfg['Commands']['InfoColor'] = self.util.colors()[ms[1]]
                        self.util.save_settings()
                        ClientMessage("Information saved successfully", color=(1, 1, 0))
                        self.value = '@'
    
        elif ms[0] == cmd[11]: # -end
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                with current_act.context:
                    current_act.end_game()
            self.value = '@'
    
        elif ms[0] == cmd[12]: # /kick
            if len(ms) == 1:
                ClientMessage("Add the client ID. \n use the '/list' command for more information.")
                self.value = '@'
            else:
                try:
                    c_id = int(ms[1])
                except Exception as exc:
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(
                            f"'{ms[1]}' is invalid. \n Enter numbers \n Example: {ms[0]} 113")
                    else:
                        ClientMessage(f'{type(exc).__name__}: {exc}')
                    self.value = '@'
                else:
                    if self.client_id == c_id:
                        ClientMessage("You cannot expel yourself")
                        self.value = '@'
                    else:
                        if c_id not in self.util.usernames:
                            ClientMessage(f"'{c_id}' Does not belong to any player.")
                            self.value = '@'
                        else:
                            user1 = self.util.usernames[self.client_id]
                            user2 = self.util.usernames[c_id]
                            if self.fct.user_is_admin(c_id):
                                ClientMessage(f"You can't kick [{user2}] because he's an admin")
                                self.value = '@'
                            else:
                                self.util.cm(f"{user1} kicked {user2} Goodbye!")
                                bs.disconnect_client(c_id)
                                self.value = '@'
    
        elif ms[0] == cmd[13]: # -chatLive
            if cfg['Commands'].get('ChatLive'):
                cfg['Commands']['ChatLive'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ChatLive'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage("Information saved successfully", color=color)
            self.value = '@'
    
        elif ms[0] == cmd[14]: # /freeze
            self.fct.actor_command(ms=ms,
                call=self.fct.freeze_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
            
        elif ms[0] == cmd[15]: # /playerColor
            try: 
                color = ms[2]
            except IndexError:
                ClientMessage("Invalid argument, \n we suggest you use the '-colors' command")
                ClientMessage(f"Incomplete data \n Example: {ms[0]} 0 yellow | {ms[0]} all green")
                self.value = '@'
            else:
                self.fct.actor_command(ms=ms,
                    call=bs.CallStrict(self.fct.player_color, color),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
                self.value = '@'
    
        elif ms[0] == cmd[16]: # /maxPlayers
            try:
                val = int(ms[1])
            except:
                ClientMessage(f"Incomplete data \n Example: {ms[0]} 5")
                self.value = '@'
            else:
                bs.set_public_party_max_size(val)
                ClientMessage(f"Max Players: {val}")
                self.value = '@'
    
        elif ms[0] == cmd[17]: # -showMessages
            if cfg['Commands'].get('ShowMessages'):
                cfg['Commands']['ShowMessages'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowMessages'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage("Show messages above players.", color=color)
            self.value = '@'
    
        elif ms[0] == cmd[18]: # /sleep
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sleep,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
    
        elif ms[0] == cmd[19] or ms[0] == cmd[20]: # /mute /unmute
            if len(ms) == 1:
                ClientMessage("Add the client ID. \n use the '/list' command for more information.")
                self.value = '@'
            else:
                try:
                    c_id = int(ms[1])
                except Exception as e:
                    ClientMessage(
                        f"'{ms[1]}' is invalid. \n Enter numbers \n Example: {ms[0]} 113")
                    self.value = '@'
                else:
                    if c_id not in self.util.accounts:
                        ClientMessage(f"'{c_id}' Does not belong to any player.")
                        self.value = '@'
                    else:
                        user = self.util.usernames[c_id]
                        if ms[0] == cmd[19]:
                            if self.fct.user_is_admin(c_id):
                                self.util.cm(f"[{Uts.usernames[c_id]}] cannot be muted because he is an administrator.")
                                self.value = '@'
                                return
                            if not self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = True
                                self.util.cm(f"{user} was muted")
                        elif ms[0] == cmd[20]:
                            if self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = False
                                self.util.cm(f"{user} can chat again")
                        Uts.save_players_data()
                        self.value = '@'

        elif ms[0] == cmd[21]: # /gm
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gm,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
    
        elif ms[0] == cmd[22]: # -slow
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                self.fct.slow()
            self.value = '@'

        elif ms[0] == cmd[23]: # /speed
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_speed,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                      
        elif ms[0] == cmd[24]: # /effect
            try:
                c_id = int(ms[1])
                eff = ms[2]
            except ValueError:
                ClientMessage(f"An error occurred while entering the player ID. \n '{ms[1]}' is not valid.", color=(1, 0, 0))
                self.value = '@'
            except IndexError:
                ClientMessage("Add the client ID. \n use the '/list' command for more information.", color=(1, 0.5, 0))
                ClientMessage(f"Incomplete data \n Example: {ms[0]} 113 fire", color=(1, 0.5, 0))
                self.value = '@'
            else:
                if c_id not in self.util.accounts:
                    ClientMessage(f"'{c_id}' Does not belong to any player.", color=(1, 0.5, 0))
                    ClientMessage("We suggest you use the '/list' command", color=(1, 0.5, 0))
                    self.value = '@'
                else:
                    if eff not in self.fct.effects():
                        ClientMessage(f"'{eff}' is invalid. enter the command '-effects' for more information.", color=(1, 0.5, 0))
                        self.value = '@'
                    else:
                        self.util.accounts[c_id]['Effect'] = eff
                        self.util.save_players_data()
                        user = self.util.usernames[c_id]
                        ClientMessage(f"Added '{eff}' effect to {user}", color=(0, 0.5, 1))
                        self.value = '@'

        elif ms[0] == cmd[25]: # /punch
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_punch,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
        
        elif ms[0] == cmd[26]: # /mbox
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_mgb,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                       
        elif ms[0] == cmd[27]: # /drop
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_drop,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[28]: # /gift
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gift,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                       
        elif ms[0] == cmd[29]: # /curse
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_curse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
                       
        elif ms[0] == cmd[30]: # /superjump
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sjump,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'
        
        elif ms[0] == '/customtag':  # الأمر المتطور للتاجات المخصصة
            self.process_advanced_customtag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/animationtag':  # الأمر للتاجات المتحركة
            self.process_animationtag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/removetag':  # إزالة التاج
            self.process_removetag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/savetag':  # حفظ التاج كقالب
            self.process_savetag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/tagdata':  # تطبيق تاج من قالب
            self.process_tagdata(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/listtags':  # عرض قوالب التاجات
            self.process_listtags(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/sharedaccounts':  # عرض اللاعبين الذين يشاركون نفس الحساب
            self.process_shared_accounts(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/closeserver':  # إغلاق السيرفر للتدريب
            self.process_close_server(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/stopcloseserver':  # إيقاف إغلاق السيرفر
            self.process_stop_close_server(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/closestatus':  # حالة إغلاق السيرفر
            self.process_close_status(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/testclosure':  # اختبار إغلاق السيرفر
            self.test_closure_system()
            self.value = '@'
                       
    def owner_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage
        
        ms[0] = ms[0].lower()
        
        if ms[0] == "/owner":
            ClientMessage("You are the owner!", color=(1.0, 0.5, 0.0))
            self.value = '@'
            
        elif ms[0] == "/fullpower":
            # إعطاء قوة كاملة للاعب
            if cls_node is not None:
                current_act = bs.get_foreground_host_activity()
                if current_act is not None:
                    with current_act.context:
                        # إعطاء جميع الـ powerups
                        powerups = ['triple_bombs', 'punch', 'ice_bombs', 'impact_bombs', 
                                   'land_mines', 'sticky_bombs', 'shield', 'health', 'curse']
                        for powerup in powerups:
                            cls_node.handlemessage(bs.PowerupMessage(powerup))
                        ClientMessage("Full Power Activated!", color=(1.0, 0.0, 1.0))
            self.value = '@'
    
    def test_closure_system(self):
        """اختبار نظام إغلاق السيرفر"""
        self.clientmessage("🔍 **اختبار نظام إغلاق السيرفر**", color=(0, 1, 1))
        self.clientmessage(f"🔸 Active: {Uts.server_close_active}", color=(1, 1, 0))
        self.clientmessage(f"🔸 End Time: {Uts.server_close_end_time}", color=(1, 1, 0))
        self.clientmessage(f"🔸 Current Time: {time.time()}", color=(1, 1, 0))
        self.clientmessage(f"🔸 Tag: {Uts.server_close_tag_name}", color=(1, 1, 0))
        self.clientmessage(f"🔸 Original Players: {Uts.server_close_original_players}", color=(1, 1, 0))
        
        if Uts.server_close_active:
            remaining = Uts.server_close_end_time - time.time()
            if remaining > 0:
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                self.clientmessage(f"🔸 Time Remaining: {hours}:{minutes:02d}:{seconds:02d}", color=(0, 1, 0))
                
                # اختبار لمعرفة من سيطرد
                activity = bs.get_foreground_host_activity()
                if activity:
                    for player in activity.players:
                        try:
                            client_id_test = player.sessionplayer.inputdevice.client_id
                            allowed = Uts.is_player_allowed_during_closure(client_id_test, Uts.server_close_tag_name)
                            status = "✅ Allowed" if allowed else "❌ Will be kicked"
                            self.clientmessage(f"👤 {player.getname()} ({client_id_test}): {status}", 
                                             color=(0, 1, 0) if allowed else (1, 0, 0))
                        except:
                            pass
    
    def process_close_server(self, msg: str, client_id: int):
        """معالجة أمر إغلاق السيرفر للتدريب"""
        try:
            parts = msg.split()
            
            if len(parts) < 3:
                self.clientmessage("Use: /closeserver <hours> <tag-name>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /closeserver 1 GOF", color=(1, 1, 0))
                return
            
            try:
                hours = float(parts[1])
                if hours <= 0:
                    self.clientmessage("Hours must be a positive number", color=(1, 0, 0))
                    return
            except ValueError:
                self.clientmessage("Hours must be a positive number", color=(1, 0, 0))
                return
            
            tag_name = parts[2]
            
            # التحقق من أن السيرفر ليس مغلقًا بالفعل
            if Uts.server_close_active:
                self.clientmessage("Server is already closed", color=(1, 1, 0))
                return
            
            # بدء إغلاق السيرفر
            if Uts.start_server_closure(hours, tag_name, client_id):
                self.clientmessage(f"✅ Server closed for {hours} hours for tag '{tag_name}'", color=(0, 1, 0))
                
                # إرسال إشعار للجميع
                Uts.cm(f"Server closed for {hours} hours for '{tag_name}' tag training")
                
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))
    
    def process_stop_close_server(self, client_id: int):
        """معالجة أمر إيقاف إغلاق السيرفر"""
        try:
            if not Uts.server_close_active:
                self.clientmessage("No server closure active", color=(1, 1, 0))
                return
            
            # إيقاف إغلاق السيرفر
            Uts.stop_server_closure()
            
            self.clientmessage("Server closure has been stopped", color=(0, 1, 0))
            Uts.cm("✅ Server closure stopped. Everyone can join now.")
            
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))
    
    def process_close_status(self, client_id: int):
        """عرض حالة إغلاق السيرفر"""
        try:
            if not Uts.server_close_active:
                self.clientmessage("📊 Server Status: Open (No closure active)", color=(0, 1, 0))
                return
            
            remaining_time = Uts.server_close_end_time - time.time()
            if remaining_time <= 0:
                self.clientmessage("📊 Server Status: Open (Closure expired)", color=(0, 1, 0))
                return
            
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            seconds = int(remaining_time % 60)
            
            status_msg = f"📊 Server Status: Closed\n"
            status_msg += f"⏰ Remaining: {hours}:{minutes:02d}:{seconds:02d}\n"
            status_msg += f"🏷️ Allowed Tag: {Uts.server_close_tag_name}\n"
            status_msg += f"👑 Allowed: Admins, Owners, Players with tag"
            
            self.clientmessage(status_msg, color=(1, 1, 0))
            
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))
            
    def process_list_players(self):
        """معالجة أمر /list لعرض قائمة اللاعبين"""
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game found", color=(1,0,0))
                return
            
            # تحديث بيانات المستخدمين
            self.util.update_usernames()
            
            # جمع بيانات اللاعبين
            players_data = []
            
            # أولاً: اللاعبون في roster
            roster_data = roster()
            if roster_data:
                for r in roster_data:
                    try:
                        client_id = r.get('client_id')
                        if client_id is None:
                            continue
                            
                        account_id = r.get('account_id', 'Unknown')
                        account_name = r.get('display_string', 'Unknown')
                        player_name = account_name
                        
                        # إذا كان هناك لاعبون في القائمة
                        players_list = r.get('players', [])
                        if players_list:
                            player_name = players_list[0].get('name_full', player_name)
                        
                        # تحديد الدور
                        role = "Player"
                        if client_id == -1:
                            role = "Owner"
                        elif account_id in self.util.pdata:
                            if self.util.pdata[account_id].get('Admin', False):
                                role = "Admin"
                        
                        # التاج
                        tag_text = "None"
                        if account_id in self.util.pdata:
                            if 'Tag' in self.util.pdata[account_id]:
                                tag_data = self.util.pdata[account_id]['Tag']
                                tag_text = tag_data.get('text', 'None')
                        
                        players_data.append({
                            'pb_id': account_id,
                            'role': role,
                            'account_name': account_name,
                            'player_name': player_name,
                            'client_id': client_id,
                            'tag': tag_text
                        })
                    except:
                        continue
            
            if not players_data:
                self.clientmessage("❌ No players found", color=(1,0,0))  
                return
            
            # ترتيب حسب Client ID
            players_data.sort(key=lambda x: x['client_id'])
            
            # إرسال الجدول
            self.send_chat_message("=============================================[Players_list]==================================================")
            self.send_chat_message("||        PB-ID        ||    Role    ||  Account_name   ||        Name         || Client ID ||   Name Tag  ||")
            self.send_chat_message("=============================================================================================================")
            
            for data in players_data:
                # إعداد النصوص
                pb_id = str(data['pb_id'])
                if len(pb_id) > 20:
                    pb_id = pb_id[:18] + ".."
                pb_id = pb_id.ljust(20)
                
                role = data['role']
                if role == "Owner":
                    role = "👑 Owner"
                elif role == "Admin":
                    role = "⭐ Admin"
                else:
                    role = "👤 Player"
                role = role.ljust(12)
                
                account_name = str(data['account_name'])
                if len(account_name) > 15:
                    account_name = account_name[:13] + ".."
                account_name = account_name.ljust(15)
                
                player_name = str(data['player_name'])
                if len(player_name) > 18:
                    player_name = player_name[:16] + ".."
                player_name = player_name.ljust(18)
                
                client_id = str(data['client_id'])
                if data['client_id'] == -1:
                    client_id = "👑 Host"
                client_id = client_id.center(10)
                
                tag = str(data['tag'])
                if len(tag) > 10:
                    tag = tag[:8] + ".."
                tag = tag.ljust(10)
                
                # إنشاء السطر
                row = f"|| {pb_id} || {role} || {account_name} || {player_name} || {client_id} || {tag} ||"
                self.send_chat_message(row)
            
            self.send_chat_message("==========================[Players_list]=============================")
            self.send_chat_message(f"👥 Total Players: {len(players_data)}")
            self.send_chat_message("👑 = Owner/Host | ⭐ = Admin | 👤 = Player")
            
        except Exception as e:
            print(f"❌ Error in process_list_players: {e}")
            self.clientmessage("❌ Error showing players list", color=(1,0,0))
    
    def process_advanced_customtag(self, msg: str, client_id: int):
        """معالجة أمر التاج المخصص المتطور"""
        try:
            parts = msg[11:].strip().split()
            if len(parts) < 4:
                self.clientmessage("❌ Use: /customtag <text> <color> <scale> <client_id>", color=(1,0,0))
                self.clientmessage("📝 Example: /customtag VIP gold 0.03 -1", color=(1,1,0))
                return
            
            text = parts[0]
            color_str = parts[1]
            
            try:
                scale = float(parts[2])
                scale = max(0.01, min(0.1, scale))
            except:
                self.clientmessage("❌ Scale must be a number", color=(1,0,0))
                return
            
            target_str = parts[3]
            
            # تحويل اللون
            color = Uts.tag_system.parse_color(color_str)
            if color == 'rainbow':
                self.clientmessage("⚠️ 'rainbow' is for animated tags only. Using yellow instead.", color=(1,1,0))
                color = (1.0, 1.0, 0.0)
            
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game found", color=(1,0,0))
                return
            
            if target_str.lower() == 'all':
                self.clientmessage("⚠️ This will affect ALL players!", color=(1,1,0))
                
                success = 0
                for player in activity.players:
                    if player.is_alive():
                        try:
                            target_client_id = player.sessionplayer.inputdevice.client_id
                            account_id = None
                            
                            # البحث عن account_id الخاص باللاعب
                            for acc_id, acc_data in Uts.pdata.items():
                                if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                    account_id = acc_id
                                    break
                            
                            if account_id:
                                Uts.tag_system.remove_tag_visual(target_client_id)
                                Uts.tag_system.stop_char_animation(target_client_id)
                                Uts.tag_system.stop_animation(target_client_id)
                                
                                # حفظ البيانات في نفس بيانات اللاعب
                                Uts.pdata[account_id]['Tag'] = {
                                    'text': text,
                                    'color': list(color) if isinstance(color, tuple) else color,
                                    'scale': scale,
                                    'type': 'normal'
                                }
                                
                                if player.is_alive() and player.actor and player.actor.node:
                                    if Uts.tag_system.create_tag_with_char_animation(player, target_client_id, text, color, scale, activity):
                                        success += 1
                        except:
                            continue
                
                Uts.save_players_data()
                self.clientmessage(f"✅ Applied custom tag to {success} players", color=(0,0,1))
                return
            
            try:
                target_client_id = int(target_str)
                target_player = None
                account_id = None
                
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == target_client_id:
                        target_player = player
                        # البحث عن account_id الخاص باللاعب
                        for acc_id, acc_data in Uts.pdata.items():
                            if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                account_id = acc_id
                                break
                        break
                
                if target_player and account_id:
                    player_name = target_player.getname()
                    Uts.tag_system.remove_tag_visual(target_client_id)
                    Uts.tag_system.stop_char_animation(target_client_id)
                    Uts.tag_system.stop_animation(target_client_id)
                    
                    # حفظ البيانات في نفس بيانات اللاعب
                    Uts.pdata[account_id]['Tag'] = {
                        'text': text,
                        'color': list(color) if isinstance(color, tuple) else color,
                        'scale': scale,
                        'type': 'normal'
                    }
                    
                    if target_player.is_alive() and target_player.actor and target_player.actor.node:
                        if Uts.tag_system.create_tag_with_char_animation(target_player, target_client_id, text, color, scale, activity):
                            Uts.save_players_data()
                            self.clientmessage(f"✅ Created custom tag '{text}' for {player_name} (Client ID: {target_client_id})", color=(0,0,1))
                else:
                    self.clientmessage(f"❌ Player with Client ID {target_client_id} not found or no account data", color=(1,0,0))
                    
            except ValueError:
                self.clientmessage("❌ Client ID must be a number", color=(1,0,0))
                
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_animationtag(self, msg: str, client_id: int):
        """معالجة أمر التاج المتحرك"""
        try:
            parts = msg[14:].strip().split()
            
            if len(parts) < 6:
                self.clientmessage("❌ Use: /animationtag <text> <scale> <speed> <client_id> <color1> <color2> ...", color=(1,0,0))
                self.clientmessage("💡 Minimum: 2 colors, Example: /animationtag VIP 0.03 0.5 -1 red blue green", color=(1,1,0))
                return
            
            text = parts[0]
            
            try:
                scale = float(parts[1])
                scale = max(0.01, min(0.2, scale))
            except:
                self.clientmessage("❌ Scale must be a number", color=(1,0,0))
                return
            
            try:
                speed = float(parts[2])
                speed = max(0.5, min(5.0, speed))
            except:
                self.clientmessage("❌ Speed must be a number (0.5-5.0)", color=(1,0,0))
                return
            
            target_str = parts[3]
            
            color_parts = parts[4:]
            if len(color_parts) < 2:
                self.clientmessage("❌ Need at least 2 colors for animation", color=(1,0,0))
                return
            
            colors = []
            rainbow_mode = False
            
            if 'rainbow' in color_parts:
                rainbow_mode = True
                colors = Uts.tag_system.generate_rainbow_colors(8)
            else:
                for color_str in color_parts:
                    color = Uts.tag_system.parse_color(color_str)
                    if color == 'rainbow':
                        rainbow_mode = True
                        colors = Uts.tag_system.generate_rainbow_colors(8)
                        break
                    colors.append(color)
            
            activity = bs.get_foreground_host_activity()
            if not activity:
                return
            
            if target_str.lower() == 'all':
                self.clientmessage("⚠️ This will affect ALL players!", color=(1,1,0))
                
                success = 0
                for player in activity.players:
                    if player.is_alive():
                        try:
                            target_client_id = player.sessionplayer.inputdevice.client_id
                            account_id = None
                            
                            # البحث عن account_id الخاص باللاعب
                            for acc_id, acc_data in Uts.pdata.items():
                                if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                    account_id = acc_id
                                    break
                            
                            if account_id:
                                Uts.tag_system.remove_tag_visual(target_client_id)
                                Uts.tag_system.stop_char_animation(target_client_id)
                                Uts.tag_system.stop_animation(target_client_id)
                                
                                # حفظ البيانات في نفس بيانات اللاعب
                                Uts.pdata[account_id]['Tag'] = {
                                    'text': text,
                                    'scale': scale,
                                    'speed': speed,
                                    'colors': colors,
                                    'type': 'animated',
                                    'rainbow': rainbow_mode
                                }
                                
                                if player.is_alive() and player.actor and player.actor.node:
                                    if Uts.tag_system.create_animated_tag_gradual(player, target_client_id, Uts.pdata[account_id]['Tag'], activity):
                                        success += 1
                        except:
                            continue
                
                Uts.save_players_data()
                self.clientmessage(f"🌈 Applied animated '{text}' to {success} players", color=(0,0,1))
                return
            
            try:
                target_client_id = int(target_str)
                target_player = None
                account_id = None
                
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == target_client_id:
                        target_player = player
                        # البحث عن account_id الخاص باللاعب
                        for acc_id, acc_data in Uts.pdata.items():
                            if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                account_id = acc_id
                                break
                        break
                
                if target_player and account_id:
                    player_name = target_player.getname()
                    Uts.tag_system.remove_tag_visual(target_client_id)
                    Uts.tag_system.stop_char_animation(target_client_id)
                    Uts.tag_system.stop_animation(target_client_id)
                    
                    # حفظ البيانات في نفس بيانات اللاعب
                    Uts.pdata[account_id]['Tag'] = {
                        'text': text,
                        'scale': scale,
                        'speed': speed,
                        'colors': colors,
                        'type': 'animated',
                        'rainbow': rainbow_mode
                    }
                    
                    if target_player.is_alive() and target_player.actor and target_player.actor.node:
                        if Uts.tag_system.create_animated_tag_gradual(target_player, target_client_id, Uts.pdata[account_id]['Tag'], activity):
                            Uts.save_players_data()
                            self.clientmessage(f"🌈 Created animated '{text}' for {player_name} (Speed: {speed}s, Client ID: {target_client_id})", color=(0,0,1))
                else:
                    self.clientmessage(f"❌ Player with Client ID {target_client_id} not found or no account data", color=(1,0,0))
                    
            except ValueError:
                self.clientmessage("❌ Client ID must be a number", color=(1,0,0))
                
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_removetag(self, msg: str, client_id: int):
        """معالجة أمر إزالة التاج"""
        try:
            target_str = msg[11:].strip()
            
            if not target_str:
                self.clientmessage("❌ Use: /removetag <client_id> or all", color=(1,0,0))
                return
            
            activity = bs.get_foreground_host_activity()
            if not activity:
                return
            
            if target_str.lower() == 'all':
                self.clientmessage("⚠️ This will remove ALL tags!", color=(1,1,0))
                
                for player_id_str in list(Uts.tag_system.current_tags.keys()):
                    try:
                        player_id = int(player_id_str)
                        Uts.tag_system.remove_tag_visual(player_id)
                    except:
                        pass
                
                # إزالة التيجان من جميع بيانات اللاعبين
                for account_id, player_data in list(Uts.pdata.items()):
                    if 'Tag' in player_data:
                        del player_data['Tag']
                
                Uts.tag_system.current_tags.clear()
                Uts.tag_system.animated_tags.clear()
                Uts.tag_system.char_animations.clear()
                Uts.tag_system.animation_states.clear()
                Uts.save_players_data()
                
                self.clientmessage("🗑️ All tags cleared", color=(1,1,0))
                return
            
            try:
                target_client_id = int(target_str)
                target_player = None
                account_id = None
                
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == target_client_id:
                        target_player = player
                        # البحث عن account_id الخاص باللاعب
                        for acc_id, acc_data in Uts.pdata.items():
                            if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                account_id = acc_id
                                break
                        break
                
                if target_player and account_id:
                    if str(target_client_id) in Uts.tag_system.current_tags:
                        Uts.tag_system.remove_tag_visual(target_client_id)
                    
                    # إزالة التاج من بيانات اللاعب
                    if 'Tag' in Uts.pdata[account_id]:
                        del Uts.pdata[account_id]['Tag']
                        Uts.save_players_data()
                    
                    self.clientmessage(f"🗑️ Removed tag from {target_player.getname()} (Client ID: {target_client_id})", color=(1,1,0))
                else:
                    self.clientmessage(f"❌ Player with Client ID {target_client_id} not found or no account data", color=(1,0,0))
                    
            except ValueError:
                self.clientmessage("❌ Client ID must be a number", color=(1,0,0))
                
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_savetag(self, msg: str, client_id: int):
        """معالجة أمر حفظ تاج كقالب"""
        try:
            parts = msg[9:].strip().split()
            
            if len(parts) < 4:
                self.clientmessage("❌ Use: /savetag <tag_data_name> <text> <color> <scale>", color=(1,0,0))
                self.clientmessage("📝 Example: /savetag crown_tag 👑 gold 0.03", color=(1,1,0))
                return
            
            tag_name = parts[0]
            text = parts[1]
            color_str = parts[2]
            
            try:
                scale = float(parts[3])
                scale = max(0.01, min(0.1, scale))
            except:
                self.clientmessage("❌ Scale must be a number", color=(1, 0, 0))
                return
            
            color = Uts.tag_system.parse_color(color_str)
            if color == 'rainbow':
                self.clientmessage("⚠️ 'rainbow' is for animated tags only. Using yellow instead.", color=(1,1,0))
                color = (1.0, 1.0, 0.0)
            
            Uts.tag_system.saved_tag_templates[tag_name] = {
                'text': text,
                'color': list(color) if isinstance(color, tuple) else color,
                'scale': scale,
                'type': 'normal'
            }
            
            Uts.tag_system.save_templates()
            self.clientmessage(f"💾 Saved tag template '{tag_name}' with text '{text}'", color=(0,0,1))
            
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_tagdata(self, msg: str, client_id: int):
        """معالجة أمر تطبيق تاج محفوظ"""
        try:
            parts = msg[9:].strip().split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /tagdata <tag_data_name> <client_id>", color=(1,0,0))
                self.clientmessage("📝 Example: /tagdata crown_tag -1  (for host)", color=(1,1,0))
                return
            
            tag_name = parts[0]
            target_str = parts[1]
            
            if tag_name not in Uts.tag_system.saved_tag_templates:
                self.clientmessage(f"❌ Tag template '{tag_name}' not found", color=(1,0,0))
                self.clientmessage("💡 Use /listtags to see available templates", color=(1,1,0))
                return
            
            template = Uts.tag_system.saved_tag_templates[tag_name]
            text = template['text']
            color = tuple(template['color']) if isinstance(template['color'], list) else template['color']
            scale = template['scale']
            
            activity = bs.get_foreground_host_activity()
            if not activity:
                return
            
            try:
                target_client_id = int(target_str)
                target_player = None
                account_id = None
                
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == target_client_id:
                        target_player = player
                        # البحث عن account_id الخاص باللاعب
                        for acc_id, acc_data in Uts.pdata.items():
                            if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                account_id = acc_id
                                break
                        break
                
                if target_player and account_id:
                    if target_player.is_alive():
                        Uts.tag_system.remove_tag_visual(target_client_id)
                        Uts.tag_system.stop_char_animation(target_client_id)
                        Uts.tag_system.stop_animation(target_client_id)
                        
                        # حفظ البيانات في نفس بيانات اللاعب
                        Uts.pdata[account_id]['Tag'] = {
                            'text': text,
                            'color': list(color) if isinstance(color, tuple) else color,
                            'scale': scale,
                            'type': 'normal'
                        }
                        
                        if Uts.tag_system.create_tag_with_char_animation(target_player, target_client_id, text, color, scale, activity):
                            name = target_player.getname()
                            Uts.save_players_data()
                            self.clientmessage(f"✅ Applied '{tag_name}' template to {name} (Client ID: {target_client_id})", color=(0,0,1))
                    else:
                        self.clientmessage(f"❌ Player {target_player.getname()} is not alive", color=(1,0,0))
                else:
                    self.clientmessage(f"❌ Player with Client ID {target_client_id} not found or no account data", color=(1,0,0))
                    
            except ValueError:
                self.clientmessage("❌ Client ID must be a number", color=(1,0,0))
                
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))
    
    def process_listtags(self, client_id: int):
        """عرض قائمة قوالب التيجان المحفوظة"""
        try:
            if not Uts.tag_system.saved_tag_templates:
                self.clientmessage("📂 No saved tag templates found", color=(0,0,1))
                self.clientmessage("💡 Use /savetag to create templates", color=(0,0,1))
                return
            
            self.clientmessage("📋 **Saved Tag Templates:**", color=(0,0,1))
            
            for name, data in Uts.tag_system.saved_tag_templates.items():
                text = data.get('text', 'Unknown')
                scale = data.get('scale', 0.03)
                color_info = data.get('color', '(1,1,1)')
                
                if isinstance(color_info, list):
                    color_str = f"RGB({color_info[0]:.1f},{color_info[1]:.1f},{color_info[2]:.1f})"
                else:
                    color_str = str(color_info)
                
                info = f"📝 {name}: '{text}' | Scale: {scale} | Color: {color_str}"
                self.clientmessage(info)
            
        except Exception as e:
            self.clientmessage("❌ Error showing tag templates", color=(1,0,0))

    def process_shared_accounts(self, client_id: int):
        """معالجة اللاعبين الذين يشاركون نفس الحساب"""
        try:
            if client_id not in Uts.userpbs:
                self.clientmessage("❌ You are not in the userpbs list", color=(1,0,0))
                return
            
            account_id = Uts.userpbs[client_id]
            shared_players = []
            
            # البحث عن جميع اللاعبين بنفس الحساب
            for cid, acc_id in list(Uts.userpbs.items()):
                if acc_id == account_id and cid != client_id:
                    shared_players.append(cid)
            
            if shared_players:
                self.clientmessage(f"👥 You share account with {len(shared_players)} other player(s)", color=(0,0,1))
                
                # عرض أسماء اللاعبين الآخرين
                for cid in shared_players:
                    name = Uts.usernames.get(cid, f"Player {cid}")
                    self.clientmessage(f"   ↳ {name} (Client ID: {cid})", color=(0.5,0.5,1))
                
                # تطبيق نفس التاج على الجميع إذا كان موجود
                if account_id in Uts.pdata and 'Tag' in Uts.pdata[account_id]:
                    self.clientmessage("🎯 Applying same tag to all shared account players", color=(1,1,0))
            else:
                self.clientmessage("👤 You are the only player with this account", color=(0,0,1))
                
        except Exception as e:
            print(f"❌ Error processing shared accounts: {e}")
            self.clientmessage("❌ Error processing shared accounts", color=(1,0,0))

class CommandFunctions:
    @staticmethod
    def all_cmd() -> list[str]:
        return [
            '-pan', '-ceb', '-colors', '-mp', '-pb', '-effects', 
            '/list', 'test', 'help', 'party', 'stats'
            ]
            
    @staticmethod
    def admins_cmd() -> list[str]:
        return [
            '/name', '/imp', '/box', '/addAdmin',
            '/delAdmin', '/kill', '-pause', '/infoHost',
            '/infoDes', '-info', '/infoColor', '-end',
            '/kick', '-chatLive', '/freeze', '/playerColor',
            '/maxPlayers', '-showMessages', '/sleep',
            '/mute', '/unmute', '/gm', '-slow', '/speed',
            '/effect', '/punch', '/mbox', '/drop', '/gift',
            '/curse', '/superjump', '/list', '/customtag', '/animationtag',
            '/removetag', '/savetag', '/tagdata', '/listtags', '/sharedaccounts',
            '/closeserver', '/stopcloseserver', '/closestatus', '/testclosure'
        ]

    @staticmethod
    def effects() -> list[str]:
        return ['none', 'footprint', 'fire', 'darkmagic',
                'spark', 'stars', 'aure', 'chispitas', 'rainbow', 'metal',
                'rock', 'ice', 'slime', 'splinter', 'stickers_rock', 
                'stickers_slime', 'stickers_metal', 'stickers_spark', 
                'stickers_splinter', 'tendrils', 'tendrils_smoke', 
                'tendrils_ice', 'distortion', 'flag_stand', 
                'tendrils_splinter', 'stickers_sweat', 'stickers_ice']

    @staticmethod
    def get_my_pb(client_id: int) -> None:
        if Uts.userpbs.get(client_id):
            pb = Uts.userpbs[client_id]
            Uts.sm(pb, transient=True, clients=[client_id])
    
    @staticmethod
    def spaz_sjump(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node
        
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                if getattr(actor, 'cm_superjump', None):
                    actor.cm_superjump = False
                else:
                    actor.cm_superjump = True
    
    @staticmethod
    def spaz_curse(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.handlemessage(bs.PowerupMessage('curse', node))
    
    @staticmethod
    def spaz_gift(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                ExplosiveGift(owner=node)
    
    @staticmethod
    def spaz_mgb(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                MagicBox(pos=node.position).autoretain()
            
    @staticmethod
    def spaz_punch(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node
        
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                actor._punch_power_scale = 8.0
            
    @staticmethod
    def spaz_speed(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                if node.hockey:
                    node.hockey = False
                else:
                    node.hockey = True

    @staticmethod
    def slow() -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                gnode = current_act.globalsnode
                if gnode.slow_motion:
                    gnode.slow_motion = False
                else:
                    gnode.slow_motion = True
            
    @staticmethod
    def spaz_gm(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                if node.invincible:
                    node.invincible = False
                else:
                    node.invincible = True
            
    @staticmethod
    def spaz_sleep(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                for x in range(5):
                    bs.timer(x, bs.CallStrict(node.handlemessage, 'knockout', 5000.0))
            
    @staticmethod
    def player_color(color: str, node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.color = Uts.colors()[color]
            
    @staticmethod
    def freeze_spaz(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node
        
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                if actor.shield:
                    actor.shield.delete()
                    
                actor.handlemessage(bs.FreezeMessage())

    @staticmethod
    def pause() -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                globs = current_act.globalsnode
                if globs.paused:
                    globs.paused = False
                else:
                    globs.paused = True

    @staticmethod
    def kill_spaz(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.handlemessage(bs.DieMessage())

    @staticmethod
    def spaz_box(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.torso_mesh = bs.getmesh('tnt')
                node.head_mesh = None
                node.pelvis_mesh = None
                node.forearm_mesh = None
                node.color_texture = node.color_mask_texture = bs.gettexture('tnt')
                node.color = node.highlight = (1,1,1)
                node.style = 'cyborg'

    @staticmethod
    def impulse(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                msg = bs.HitMessage(pos=node.position,
                                    velocity=node.velocity,
                                    magnitude=500 * 4,
                                    hit_subtype='imp',
                                    radius=7840)
                              
                if isinstance(msg, bs.HitMessage):
                    for i in range(2):
                        with current_act.context:
                            node.handlemessage(
                                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                                msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                                msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                                msg.force_direction[1], msg.force_direction[2])

    @staticmethod
    def actor_name(name: str, node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.name = name

    @staticmethod
    def actor_command(
            ms: list[str],
            call: Callable,
            attrs: dict[str, Any]) -> None:
        ClientMessage = attrs['ClientMessage']
        
        current_act = bs.get_foreground_host_activity()
        if current_act is None:
            ClientMessage("No active game found", color=(1,0,0))
            return
                
        def new_call(node: bs.Node):
            ClientMessage("Command Executed", color=(0, 1, 0))
            with current_act.context:
                call(node)
                
        if len(ms) == 1:
            if attrs['Actor'] is None:
                ClientMessage("You're not in the game")
            else:
                actor = attrs['Actor']
                new_call(actor.node)
        else:
            if ms[1] == 'all':
                for p in current_act.players:
                    if p.actor and p.actor.node:
                        node = p.actor.node
                        new_call(node)
            else:
                try:
                    p_id = int(ms[1])
                    if p_id >= 0 and p_id < len(current_act.players):
                        node = current_act.players[p_id].actor.node
                        new_call(node)
                    else:
                        ClientMessage(f"Player ID {p_id} not found", color=(1,0,0))
                except Exception as exc:
                    color = Uts.colors()['orange']
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(f"'{ms[1]}' is invalid. \n Add the player ID. use the '/list' command for more information.", color=color)
                    elif type_error is IndexError:
                        ClientMessage(f"'{p_id}' Does not belong to any player.", color=color)
                    else:
                        ClientMessage(f'{type(exc).__name__}: {exc}')
                    ClientMessage(f"Example: {ms[0]} 0 | {ms[0]} all")

    @staticmethod
    def spaz_drop(node: bs.Node) -> None:
        self = node.source_player.actor
        del node

        current_act = bs.get_foreground_host_activity()
        if current_act is None:
            return

        def drop():
            pos = self.node.position
            psts = [
                (pos[0]-1,pos[1]+4,pos[2]+1),
                (pos[0]+1,pos[1]+4,pos[2]+1),
                (pos[0],pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]-1),
                (pos[0],pos[1]+4,pos[2]+2)]
                
            for p in psts:
                bomb = Bomb(
                    position=p,
                    bomb_scale=1.3,
                    bomb_type='sticky').autoretain()
                bomb.node.gravity_scale = 4.0
                bomb.node.color_texture = bs.gettexture('bombStickyColor')
                    
        for x in range(2):
            with current_act.context:
                bs.timer(x * 0.308, drop)

    @staticmethod
    def get_user_list(c_id: int) -> None:
        current_act = bs.get_foreground_host_activity()
        
        def delete_text(t_id: int):
            if current_act and hasattr(current_act, '_ids') and current_act._ids.node.exists():
                if t_id == id(current_act._ids.node):
                    current_act._ids.node.opacity = 0.0
            
        def gText(txt: str):
            if current_act is None:
                # Can't display in-game text without activity
                bs.screenmessage(txt, clients=[c_id], transient=True)
                return
                
            with current_act.context:
                current_act._ids = text.Text(txt, position=(-0.0, 270.0),
                    h_align=text.Text.HAlign.CENTER, scale=1.1,
                    transition=text.Text.Transition.FADE_IN).autoretain()
                current_act._ids.node.opacity = 0.5
                
                t_id = id(current_act._ids.node)
                bs.timer(8.0, bs.CallStrict(delete_text, t_id))
    
        txt = str()
        txts = ["Name | Player ID | Client ID",
                "______________________"]

        try:
            if current_act is not None:
                players = current_act.players
                for idx, p in enumerate(players):
                    if p.is_alive():
                        s = p.sessionplayer
                        txts.append(f"{s.getname(False)} | {idx} | {s.inputdevice.client_id}")
        except Exception:
            players = []
        
        txt = '\n'.join(txts)

        # Always send via screenmessage for reliability
        bs.screenmessage(txt, clients=[c_id], transient=True)
        
        # Try to display in-game if possible
        try:
            if current_act is not None:
                with current_act.context:
                    try:
                        if current_act._ids.node.exists():
                            current_act._ids.node.delete()
                            gText(txt)
                    except AttributeError:
                        gText(txt)
        except:
            pass
    
    @staticmethod
    def get_characters() -> list[str]:
        return bs.app.spaz_appearances
    
    @staticmethod
    def user_is_admin(c_id: int) -> bool:
        if c_id == -1:
            return True
    
        if c_id in Uts.accounts:
            return Uts.accounts[c_id]['Admin']
        else:
            return False
            
    @staticmethod
    def user_is_owner(c_id: int) -> bool:
        """تحقق إذا كان اللاعب هو المالك"""
        if c_id == -1:
            return True
    
        if c_id in Uts.accounts:
            # تحقق إذا كان اللاعب في قائمة المالكين
            account_id = None
            for acc_id, data in Uts.pdata.items():
                if data.get('Owner', False):
                    # تحقق إذا كان هذا الحساب مرتبطًا بـ client_id الحالي
                    if c_id in Uts.userpbs and Uts.userpbs[c_id] == acc_id:
                        return True
            return Uts.accounts[c_id].get('Owner', False)
        else:
            return False
    
    @staticmethod
    def get_actor(c_id: int) -> spaz.Spaz:
        current_act = bs.get_foreground_host_activity()
        if current_act is None:
            return None
        
        for player in current_act.players:
            try:
                if c_id == player.sessionplayer.inputdevice.client_id:
                    return player.actor
            except:
                continue
        return None
        
def ActorMessage(msg: str, actor: spaz.Spaz):
    current_act = bs.get_foreground_host_activity()
    if current_act is None:
        return
        
    def die(node: bs.Node):
        if node.exists():
            bs.animate(popup.node, 'opacity', {0: 1.0, 0.1: 0.0})
            bs.timer(0.1, popup.node.delete)
        
    with current_act.context:
        if getattr(actor, 'my_message', None):
            actor.my_message.node.delete()
        
        c = (1.0, 1.0, 1.0)
        position = (-0.0, 1.5, 0.0)  # تغيير الموضع ليكون أعلى

        m = bs.newnode('math', owner=actor.node, attrs={'input1':
            (position[0], position[1], position[2]), 'operation': 'add'})
        actor.node.connectattr('position_center', m, 'input2')
        
        actor.my_message = popup = PopupText(
             text=msg, color=c, scale=1.5).autoretain()
        m.connectattr('output', popup.node, 'position')
        bs.timer(5.0, bs.CallStrict(die, popup.node))

# Effects
def _fire(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
        scale=3,count=50*2,spread=0.3,
        chunk_type='sweat')
    
def _spark(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
        scale=0.7,count=50*2,spread=0.3,
        chunk_type='spark')
    
def footprint(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        loc = bs.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': self.node.color,
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
        bs.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
        bs.apptimer(2.0, loc.delete)
    
def aure(self) -> None:
    def anim(node: bs.Node) -> None:
        bs.animate_array(node, 'color', 3,
            {0: (1,1,0), 0.1: (0,1,0),
             0.2: (1,0,0), 0.3: (0,0.5,1),
             0.4: (1,0,1)}, loop=True)
        bs.animate_array(node, 'size', 1,
            {0: [1.0], 0.2: [1.5], 0.3: [1.0]}, loop=True)

    attrs = ['torso_position', 'position_center', 'position']
    for i, pos in enumerate(attrs):
        loc = bs.newnode('locator', owner=self.node,
              attrs={'shape': 'circleOutline',
                     'color': self.node.color,
                     'opacity': 1.0,
                     'draw_beauty': True,
                     'additive': False})
        self.node.connectattr(pos, loc, 'position')
        bs.apptimer(0.1 * i, lambda node=loc: anim(node))
        
def black_aure(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        loc = bs.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': (1,1,1),
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
        bs.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
        bs.apptimer(2.0, loc.delete)
        
    def anim(node: bs.Node) -> None:
        bs.animate_array(node, 'color', 3,
            {0: (1,1,1), 0.1: (0,0,0),
             0.2: (1,1,1), 0.3: (0,0,0),
             0.4: (1,1,1)}, loop=True)
        bs.animate_array(node, 'size', 1,
            {0: [0.5], 0.2: [1.0], 0.3: [0.5]}, loop=True)

    attrs = ['torso_position', 'position_center', 'position']
    for i, pos in enumerate(attrs):
        loc = bs.newnode('locator', owner=self.node,
              attrs={'shape': 'circleOutline',
                     'color': self.node.color,
                     'opacity': 1.0,
                     'draw_beauty': True,
                     'additive': False})
        self.node.connectattr(pos, loc, 'position')
        bs.apptimer(0.1 * i, lambda node=loc: anim(node))
        
def stars(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.apptimer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            texs = ['bombStickyColor', 'aliColor', 'aliColorMask', 'eggTex3']
            tex = bs.gettexture(random.choice(texs))
            mesh = bs.getmesh('flash')
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.1,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [1.5],
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.035})
            node.connectattr('position', light, 'position')
            bs.apptimer(0.25, lambda node=node: die(node))
            
def chispitas(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.apptimer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            tex = bs.gettexture('null')
            mesh = None
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('bomb',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.1,
                       'body_scale': 0.0,
                       'color_texture': tex,
                       'fuse_length': 0.1,
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.035})
            node.connectattr('position', light, 'position')
            bs.apptimer(0.25, lambda node=node: die(node))
            
def darkmagic(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.apptimer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), 30.0, random.uniform(-m, m))

            tex = bs.gettexture('impactBombColor')
            mesh = bs.getmesh('impactBomb')
            factory = SpazFactory.get()
            
            mat = bs.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = bs.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'mesh': mesh,
                       'mesh_scale': 0.4,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [0.0],
                       'materials': [mat]})
            
            light = bs.newnode('light',
                owner=node,
                attrs={'intensity': 1.0,
                       'volume_intensity_scale': 0.5,
                       'color': (0.5, 0.0, 1.0),
                       'radius': 0.035})
            node.connectattr('position', light, 'position')
            bs.apptimer(0.25, lambda node=node: die(node))
            
def _rainbow(self) -> None:
    keys = {
        0.0: (2.0, 0.0, 0.0),
        0.2: (2.0, 1.5, 0.5),
        0.4: (2.0, 2.0, 0.0),
        0.6: (0.0, 2.0, 0.0),
        0.8: (0.0, 2.0, 2.0),
        1.0: (0.0, 0.0, 2.0),
    }.items()

    def _changecolor(color: Sequence[float]) -> None:
        if self.node.exists():
            self.node.color = color

    for time, color in keys:
        bs.apptimer(time, lambda color=color: _changecolor(color))
        
def rock(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                    count=50,
                    spread=0.08,
                    scale=1.5,
                    chunk_type='rock')  

def ice(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=50,
                spread=0.08,
                scale=0.8,
                chunk_type='ice')

def slime(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=50,
                spread=0.08,
                scale=2,
                chunk_type='slime')
        bs.emitfx(position=self.node.position,
                count=50,
                spread=0.08,
                scale=2,
                chunk_type='slime')
        bs.emitfx(position=self.node.position,
                count=50,
                spread=0.08,
                scale=2,
                chunk_type='slime')
                
def metal(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal')
                
def splinter(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter')
                
def stickers_rock(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='rock',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='rock',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='rock',
                emit_type='stickers')
                
def stickers_slime(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='slime',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='slime',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='slime',
                emit_type='stickers')
                
def stickers_metal(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='metal',
                emit_type='stickers')

def stickers_spark(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='spark',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='spark',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=1,
                spread=0.08,
                scale=1.5,
                chunk_type='spark',
                emit_type='stickers')

def stickers_splinter(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='stickers')
    
def stickers_ice(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='ice',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='ice',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='ice',
                emit_type='stickers')

def tendrils(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils')

def tendrils_smoke(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='thin_smoke')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='thin_smoke')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='thin_smoke')

def tendrils_ice(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='ice')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='ice')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='tendrils',
                tendril_type='ice')

def distortion(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='distortion')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='distortion')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='distortion')

def flag_stand(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='flag_stand')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='flag_stand')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                emit_type='flag_stand')
                
def tendrils_splinter(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='tendrils')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='tendrils')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='splinter',
                emit_type='tendrils')

def stickers_sweat(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='sweat',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='sweat',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=2,
                spread=0.08,
                scale=1.5,
                chunk_type='sweat',
                emit_type='stickers')
                
def apply_effect(self, eff: str) -> None:
    if eff == 'fire':
        self._cm_effect_timer = bs.Timer(0.1, lambda: _fire(self), repeat=True)
    elif eff == 'spark':
        self._cm_effect_timer = bs.Timer(0.1, lambda: _spark(self), repeat=True)
    elif eff == 'footprint':
        self._cm_effect_timer = bs.Timer(0.15, lambda: footprint(self), repeat=True)
    elif eff == 'stars':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stars(self), repeat=True)
    elif eff == 'chispitas':
        self._cm_effect_timer = bs.Timer(0.1, lambda: chispitas(self), repeat=True)
    elif eff == 'darkmagic':
        self._cm_effect_timer = bs.Timer(0.1, lambda: darkmagic(self), repeat=True)
    elif eff == 'rainbow':
        self._cm_effect_timer = bs.Timer(1.2, lambda: _rainbow(self), repeat=True)
    elif eff == 'aure':
        aure(self)
    elif eff == 'black_aure':
        black_aure(self)
    elif eff == 'rock':
        self._cm_effect_timer = bs.Timer(0.1, lambda: rock(self), repeat=True)
    elif eff == 'ice':
        self._cm_effect_timer = bs.Timer(0.1, lambda: ice(self), repeat=True)
    elif eff == 'slime':
        self._cm_effect_timer = bs.Timer(0.1, lambda: slime(self), repeat=True)
    elif eff == 'metal':
        self._cm_effect_timer = bs.Timer(0.1, lambda: metal(self), repeat=True)
    elif eff == 'splinter':
        self._cm_effect_timer = bs.Timer(0.1, lambda: splinter(self), repeat=True)
    elif eff == 'stickers_rock':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_rock(self), repeat=True)
    elif eff == 'stickers_slime':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_slime(self), repeat=True)
    elif eff == 'stickers_metal':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_metal(self), repeat=True)
    elif eff == 'stickers_spark':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_spark(self), repeat=True)
    elif eff == 'stickers_splinter':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_splinter(self), repeat=True)
    elif eff == 'stickers_ice':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_ice(self), repeat=True)
    elif eff == 'tendrils':
        self._cm_effect_timer = bs.Timer(0.1, lambda: tendrils(self), repeat=True)
    elif eff == 'tendrils_smoke':
        self._cm_effect_timer = bs.Timer(0.1, lambda: tendrils_smoke(self), repeat=True)
    elif eff == 'tendrils_ice':
        self._cm_effect_timer = bs.Timer(0.1, lambda: tendrils_ice(self), repeat=True)
    elif eff == 'distortion':
        self._cm_effect_timer = bs.Timer(0.1, lambda: distortion(self), repeat=True)
    elif eff == 'flag_stand':
        self._cm_effect_timer = bs.Timer(0.1, lambda: flag_stand(self), repeat=True)
    elif eff == 'tendrils_splinter':
        self._cm_effect_timer = bs.Timer(0.1, lambda: tendrils_splinter(self), repeat=True)
    elif eff == 'stickers_sweat':
        self._cm_effect_timer = bs.Timer(0.1, lambda: stickers_sweat(self), repeat=True)

def filter_chat_message(msg: str, client_id: int) -> None:
    try:
        # Get current activity first
        activity = bs.get_foreground_host_activity()
        
        # If no activity and it's a chat command, we can't process it
        if activity is None and msg.strip() != '':
            # Check if it's a command that doesn't need activity
            if msg.strip() in ['-pan', '-pb', '-mp', '-colors', '-effects']:
                # Create a simple Commands object without activity
                try:
                    command = Commands(msg, client_id, msg.split(' '))
                    return command.get
                except:
                    return None
            return None
            
        # Normal processing with activity
        command = Commands(msg, client_id, msg.split(' '))
        return command.get
    except Exception as e:
        print(f"⚠️ Error in filter_chat_message: {e}")
        import traceback
        traceback.print_exc()
        return None
    
def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)

def new_on_player_join(self, player: bs.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    Uts.player_join(player)
    
    # التحقق من إغلاق السيرفر
    if Uts.server_close_active:
        Uts.check_player_allowed_on_join(player)
    
def new_playerspaz_init_(self, *args, **kwargs) -> None:
    calls['PlayerSpazInit'](self, *args, **kwargs)
    Uts.update_usernames()

    try:
        user = self._player.sessionplayer.get_v1_account_id()
    except (AttributeError, ba.SessionPlayerNotFoundError):
        user = None
        
    if not hasattr(Uts, 'pdata'): 
        Uts.create_players_data()
    
    if user and user in Uts.pdata:
        eff = Uts.pdata[user]['Effect']
        apply_effect(self, eff)
    
    # تطبيق التاج المخصص إذا كان موجودًا
    if user and user in Uts.tags:
        tag_data = Uts.tags[user]
        text = tag_data.get('text', '')
        color = tag_data.get('color', (1, 1, 1))
        scale = tag_data.get('scale', 0.02)
        
        # تأخير إنشاء التاج لضمان اكتمال تهيئة العقدة
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                bs.timer(0.5, lambda: create_custom_tag_for_spaz(self, text, color, scale))

def create_custom_tag_for_spaz(spaz, text, color, scale):
    """إنشاء تاج مخصص للسباز"""
    if not spaz.node or not spaz.node.exists():
        return
    
    # إزالة التاج القديم إذا كان موجودًا
    if hasattr(spaz.node, 'custom_tag') and spaz.node.custom_tag:
        if spaz.node.custom_tag.exists():
            spaz.node.custom_tag.delete()
    
    # إنشاء نص التاج
    tag = bs.newnode('text',
        attrs={
            'text': text,
            'in_world': True,
            'shadow': 1.0,
            'flatness': 1.0,
            'h_align': 'center',
            'v_align': 'bottom',
            'scale': scale,
            'color': color
        })
    
    # ربط التاج بالسباز
    spaz.node.connectattr('position_center', tag, 'position')
    
    # حفظ المرجع
    spaz.node.custom_tag = tag
            
def new_playerspaz_on_jump_press(self) -> None:    
    calls['OnJumpPress'](self)
    
    if not getattr(self, 'cm_superjump', False):
        return
        
    if (not self.node or not self.node.jump_pressed):
        return
    
    current_act = bs.get_foreground_host_activity()
    if current_act is None:
        return
    
    msg = bs.HitMessage(pos=self.node.position,
                        velocity=self.node.velocity,
                        magnitude=160*2,
                        hit_subtype='imp',
                        radius=460*2)
                      
    if isinstance(msg, bs.HitMessage):
        for i in range(2):
            with current_act.context:
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
            
class ExplosiveGift(bs.Actor):
    def __init__(self,
                 time: float = 3.0,
                 owner: bs.Node = None):
        super().__init__()
        
        self.time = time
        self.owner = owner
        self.scale = 0.8
        self.touch = False
        
        pos = list(owner.position)
        velocity = (0.0, 60, 0.0)
        position = (pos[0], pos[1]+1.47, pos[2])
                     
        tex = bs.gettexture('crossOutMask')
        mesh = bs.getmesh('tnt')
                     
        self.node = bs.newnode('bomb',
                               delegate=self,
                               attrs={'body': 'sphere',
                                      'position': position,
                                      'velocity': velocity,
                                      'mesh': mesh,
                                      'body_scale': self.scale,
                                      'shadow_size': 0.3,
                                      'color_texture': tex,
                                      'sticky': True,
                                      'owner': owner,
                                      'reflection': 'soft',
                                      'reflection_scale': [0.22]})
        bs.animate(self.node, 'mesh_scale',
           {0: 0,
            0.2: self.scale * 1.3,
            0.26: self.scale})
        bs.animate(self.node, 'fuse_length', {0.0: 1.0, time: 0.0})
        bs.timer(time, self._xplosion)
        
    def _xplosion(self):
        radius = 3.0
        shared = SharedObjects.get()
        
        mat = bs.Material()
        mat.add_actions(
            conditions=(
                ('they_have_material', shared.player_material), 'or',
                ('they_have_material', shared.object_material)
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self.call)
            ))
        
        rmats = [mat, shared.attack_material]

        region = bs.newnode('region',
            delegate=self,
            owner=self.node,
            attrs={'scale': tuple(radius*0.7 for s in range(3)),
                   'type': 'sphere',
                   'materials': rmats})
        self.node.connectattr('position', region, 'position')
        
        shield = bs.newnode('shield',
            owner=region,
                attrs={'color': (2.0, 1.0, 0.0),
                       'radius': radius})
        region.connectattr('position', shield, 'position')
        
        bs.getsound('explosion03').play(1, self.node.position)
        bs.timer(0.1, bs.CallStrict(
            self.handlemessage, bs.DieMessage()))
        
    def call(self) -> None:
        node = bs.getcollision().opposingnode
        
        def action():
            #if node != self.owner or node != self.node:
                msg = bs.HitMessage(
                    pos=self.node.position,
                    velocity=node.velocity,
                    magnitude=1200 * 5,
                    radius=800 * 5)

                node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])

        if not self.touch:
            self.touch = True
        else:
            action()
            self.touch = False
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)

class MagicBox(bs.Actor):
    def __init__(self, pos: Sequence[float] = (0.0, 1.0, 0.0)) -> None:
        super().__init__()
        
        shared = SharedObjects.get()
        tex = bs.gettexture('rgbStripes')
        mesh = bs.getmesh('powerup')
        position = (pos[0], pos[1] + 1.5, pos[2])
        
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={'body': 'box',
                   'position': position,
                   'mesh': mesh,
                   'shadow_size': 0.5,
                   'color_texture': tex,
                   'reflection': 'powerup',
                   'reflection_scale': [1.0],
                   'materials': [shared.object_material]})
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PickedUpMessage):
            self.node.gravity_scale = -1.0
        elif isinstance(msg, bs.DroppedMessage):
            self.node.gravity_scale = 1.0
        elif isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)

class Uts:
    directory_user: str = _babase.app.env.python_directory_user
    directory_sys: str = directory_user + '/sys/' + _babase.app.env.engine_version + '_' + str(_babase.app.env.engine_build_number)
    sm: Callable = bs.broadcastmessage
    cm: Callable = bs.chatmessage
    key: str = '#CheatMax'
    mod: Any
    accounts: dict[int, Any] = {}
    usernames: dict[int, str] = {}
    shortnames: dict[int, str] = {}
    useraccounts: dict[int, str] = {}
    userpbs: dict[int, str] = {}
    players: dict[int, bs.SessionPlayer] = {}
    tags: dict[str, dict] = {}  # تخزين بيانات التاجات
    tag_system = None  # نظام التيجان المتطور
    
    # متغيرات إغلاق السيرفر
    server_close_active = False
    server_close_end_time = 0.0
    server_close_tag_name = ""
    server_close_countdown_text = None
    server_close_original_players = []
    server_close_last_update = 0.0

    @staticmethod
    def start_server_closure(hours: float, tag_name: str, admin_client_id: int) -> bool:
        """بدء إغلاق السيرفر للتدريب"""
        try:
            current_time = time.time()
            
            # التحقق من أن السيرفر ليس مغلقًا بالفعل
            if Uts.server_close_active:
                return False
            
            # بدء إغلاق السيرفر
            Uts.server_close_active = True
            Uts.server_close_end_time = current_time + (hours * 3600)
            Uts.server_close_tag_name = tag_name
            Uts.server_close_original_players = []
            Uts.server_close_last_update = current_time
            
            print(f"✅ Server closure started at {current_time}. End time: {Uts.server_close_end_time} for tag: {tag_name}")
            
            # حفظ اللاعبين الأصليين (الذين سيبقون)
            activity = bs.get_foreground_host_activity()
            if activity:
                for player in activity.players:
                    try:
                        client_id = player.sessionplayer.inputdevice.client_id
                        Uts.server_close_original_players.append(client_id)
                    except:
                        continue
            
            # بدء عرض العد التنازلي
            Uts.start_close_server_countdown()
            
            # إرسال إشعار للجميع
            Uts.cm(f"Server closed for {hours} hours for '{tag_name}' tag training")
            
            return True
            
        except Exception as e:
            print(f"❌ Error starting server closure: {e}")
            return False
    
    @staticmethod
    def is_player_allowed_during_closure(client_id: int, tag_name: str) -> bool:
        """التحقق إذا كان اللاعب مسموحًا له أثناء إغلاق السيرفر"""
        try:
            # المالكين (-1) والادمنز مسموح لهم دائمًا
            if client_id == -1 or CommandFunctions.user_is_admin(client_id):
                return True
            
            # الحصول على اسم اللاعب للبحث عنه
            player_name = Uts.usernames.get(client_id, None)
            if not player_name:
                # إذا لم يكن الاسم موجودًا، محاولة البحث في roster
                for r in roster():
                    if r['client_id'] == client_id:
                        player_name = r['display_string']
                        break
            
            if not player_name:
                return False
            
            # البحث عن بيانات اللاعب في Uts.pdata
            account_id = None
            for acc_id, acc_data in Uts.pdata.items():
                # التحقق من اسم الحساب في القائمة
                if 'Accounts' in acc_data:
                    for acc_name in acc_data['Accounts']:
                        if player_name == acc_name:
                            account_id = acc_id
                            break
                if account_id:
                    break
            
            if account_id and account_id in Uts.pdata:
                player_data = Uts.pdata[account_id]
                if 'Tag' in player_data:
                    tag_data = player_data['Tag']
                    player_tag = tag_data.get('text', '').strip().lower()
                    required_tag = tag_name.strip().lower()
                    
                    # مقارنة التيجان (بدون حساسية لحالة الحروف)
                    if player_tag == required_tag:
                        return True
            
            # إذا لم يكن لديه التاج المطلوب، تحقق إذا كان من اللاعبين الأصليين
            if client_id in Uts.server_close_original_players:
                return True
                
            return False
            
        except Exception as e:
            print(f"❌ Error checking player allowance: {e}")
            return False
    
    @staticmethod
    def start_close_server_countdown():
        """بدء عرض العد التنازلي لإغلاق السيرفر"""
        try:
            def update_countdown():
                try:
                    if not Uts.server_close_active:
                        # إزالة النص إذا توقف الإغلاق
                        if Uts.server_close_countdown_text and Uts.server_close_countdown_text.exists():
                            Uts.server_close_countdown_text.delete()
                            Uts.server_close_countdown_text = None
                        return
                    
                    activity = bs.get_foreground_host_activity()
                    if not activity:
                        # إعادة المحاولة بعد ثانية
                        bs.apptimer(1.0, update_countdown)
                        return
                    
                    # حساب الوقت المتبقي باستخدام time.time()
                    current_time = time.time()
                    remaining_time = Uts.server_close_end_time - current_time
                    
                    if remaining_time <= 0:
                        # انتهى الوقت، إوقف الإغلاق
                        Uts.stop_server_closure()
                        Uts.cm("✅ Server closure ended. Everyone can join now.")
                        return
                    
                    # تحويل الوقت إلى تنسيق ساعات:دقائق:ثواني
                    hours = int(remaining_time // 3600)
                    minutes = int((remaining_time % 3600) // 60)
                    seconds = int(remaining_time % 60)
                    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    
                    # استخدام سياق النشاط لعرض النص
                    if hasattr(activity, 'context'):
                        with activity.context:
                            # إنشاء أو تحديث نص العد التنازلي
                            if Uts.server_close_countdown_text is None or not Uts.server_close_countdown_text.exists():
                                # إنشاء نص جديد
                                Uts.server_close_countdown_text = text.Text(
                                    f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}",
                                    position=(0, 250),
                                    scale=1.0,
                                    color=(1, 0, 0),
                                    h_align=text.Text.HAlign.CENTER,
                                    v_align=text.Text.VAlign.CENTER
                                )
                                Uts.server_close_countdown_text.node.opacity = 0.7
                            else:
                                # تحديث النص الحالي مباشرة
                                try:
                                    Uts.server_close_countdown_text.node.text = f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}"
                                except:
                                    # إعادة إنشاء النص إذا كان هناك خطأ
                                    Uts.server_close_countdown_text = text.Text(
                                        f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}",
                                        position=(0, 250),
                                        scale=1.0,
                                        color=(1, 0, 0),
                                        h_align=text.Text.HAlign.CENTER,
                                        v_align=text.Text.VAlign.CENTER
                                    )
                                    Uts.server_close_countdown_text.node.opacity = 0.7
                    
                    # جدولة التحديث التالي بعد ثانية واحدة
                    bs.apptimer(1.0, update_countdown)
                        
                except Exception as e:
                    print(f"❌ Error in countdown update: {e}")
                    # إعادة المحاولة بعد 2 ثانية في حالة الخطأ
                    bs.apptimer(2.0, update_countdown)
            # بدء العد التنازلي
            bs.apptimer(0.5, update_countdown)
            print(f"✅ Countdown started for server closure")
            
        except Exception as e:
            print(f"❌ Error starting countdown: {e}")
    
    @staticmethod
    def stop_server_closure():
        """إيقاف إغلاق السيرفر"""
        try:
            Uts.server_close_active = False
            Uts.server_close_end_time = 0.0
            Uts.server_close_tag_name = ""
            Uts.server_close_original_players = []
            
            # إزالة نص العد التنازلي
            if Uts.server_close_countdown_text and Uts.server_close_countdown_text.exists():
                Uts.server_close_countdown_text.delete()
                Uts.server_close_countdown_text = None
            
            print("✅ Server closure stopped.")
            
        except Exception as e:
            print(f"❌ Error stopping server closure: {e}")
    
    @staticmethod
    def check_player_allowed_on_join(player: bs.Player):
        """التحقق من اللاعب عند الانضمام أثناء إغلاق السيرفر"""
        try:
            if not Uts.server_close_active:
                return
            
            client_id = player.sessionplayer.inputdevice.client_id
            
            # التحقق إذا كان اللاعب مسموحًا له
            if not Uts.is_player_allowed_during_closure(client_id, Uts.server_close_tag_name):
                # حساب الوقت المتبقي
                current_time = time.time()
                remaining_time = Uts.server_close_end_time - current_time
                
                if remaining_time <= 0:
                    Uts.stop_server_closure()
                    return
                
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                seconds = int(remaining_time % 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # إرسال رسالة للاعب
                message = f"There's a training match for {Uts.server_close_tag_name}. Please try to join again after {time_str}"
                
                # استخدام سياق النشاط إن وجد
                activity = bs.get_foreground_host_activity()
                if activity and hasattr(activity, 'context'):
                    try:
                        with activity.context:
                            bs.screenmessage(message, color=(1, 0, 0), transient=True, clients=[client_id])
                            
                            # طرد اللاعب بعد ثانيتين
                            def kick_player():
                                try:
                                    bs.disconnect_client(client_id)
                                except:
                                    pass
                            
                            bs.apptimer(2.0, kick_player)
                    except:
                        # إذا فشل السياق، طرد مباشرة
                        try:
                            bs.disconnect_client(client_id)
                        except:
                            pass
                else:
                    # إذا لم يكن هناك سياق، طرد مباشرة
                    try:
                        bs.disconnect_client(client_id)
                    except:
                        pass
                    
        except Exception as e:
            print(f"❌ Error checking player on join: {e}")

    @staticmethod
    def get_user_name(c_id: int) -> str:
        try:
            for r in roster():
                if r['client_id'] == c_id:
                    if r['players'] == []:
                        return r['display_string']
                    else:
                        return r['players'][0]['name_full']
        except:
            pass
        return 'UNNAMED'

    @staticmethod
    def sort_list(vals: list, count: int = 3) -> list:
        vals_dict = dict(r=[])
        
        for n in range(len(vals)):
            vals_dict[n] = list()
            
            for c in vals:
                if len(vals_dict[n]) == count:
                    break
                else:
                    if c not in vals_dict['r']:
                        vals_dict['r'].append(c)
                        vals_dict[n].append(c)
        
            if len(vals_dict['r']) == len(vals):
                vals_dict.pop('r')
                break

        return list(vals_dict.values())

    @staticmethod
    def colors() -> dict[str, Sequence[float]]:
        return dict(
                yellow=(1.0, 1.0, 0.0),
                red=(1.0, 0.0, 0.0),
                green=(0.0, 1.0, 0.0),
                blue=(0.2, 1.0, 1.0),
                pink=(1, 0.3, 0.5),
                orange=(1.0, 0.5, 0.0),
                violet=(0.5, 0.25, 1.0),
                white=(1.0, 1.0, 1.0),
                black=(0.25, 0.25, 0.25))

    @staticmethod
    def get_admins() -> list[str]:
        admins = []
        if not hasattr(Uts, 'pdata'): 
            Uts.create_players_data()
        
        if len(Uts.pdata) > 0:
            for p, d in getattr(Uts, 'pdata', {}).items():
                if d['Admin']:
                    admins.append(p)
        return admins
        
    @staticmethod
    def get_owners() -> list[str]:
        """الحصول على قائمة المالكين"""
        owners = []
        if not hasattr(Uts, 'pdata'): 
            Uts.create_players_data()
        
        if len(Uts.pdata) > 0:
            for p, d in getattr(Uts, 'pdata', {}).items():
                if d.get('Owner', False):
                    owners.append(p)
        return owners

    @staticmethod
    def add_or_del_user(c_id: int, add: bool = True) -> None:
        if c_id == -1:
            return Uts.sm("You Are Amazing!!", color=(0.5, 0, 1), clients=[c_id], transient=True)
            
        if c_id not in Uts.userpbs:
            Uts.sm(f"'{c_id}' Does not belong to any player.", clients=[c_id], transient=True)
        else:
            user = Uts.userpbs[c_id]
            if add:
                if not hasattr(Uts, 'pdata'): 
                    Uts.create_players_data()
                
                if user in Uts.pdata:
                    if not Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(f"'{Uts.usernames[c_id]}' Added to Admins list")
            else:
                if not hasattr(Uts, 'pdata'): 
                    Uts.create_players_data()
                
                if user in Uts.pdata:
                    if Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(f"'{Uts.usernames[c_id]}' was removed from the Admins list")
            Uts.save_players_data()
            
    @staticmethod
    def add_owner(account_id: str) -> None:
        """إضافة مالك جديد"""
        if not hasattr(Uts, 'pdata'): 
            Uts.create_players_data()
        
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'none',
                'Admin': True,  # المالك يكون مشرفًا
                'Owner': True,  # هذا هو الحقل الجديد للمالك
                'Accounts': []
            }
        else:
            Uts.pdata[account_id]['Admin'] = True
            Uts.pdata[account_id]['Owner'] = True
            
        Uts.save_players_data()
        print(f"Added owner: {account_id}")

    @staticmethod
    def create_players_data() -> None:
        # Check if already created to avoid recursion
        if hasattr(Uts, 'pdata'):
            return
        
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxPlayersData.json'
                
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            Uts.pdata = json.loads(r)
            
    @staticmethod
    def create_tags_data() -> None:
        """إنشاء ملف تخزين التاجات"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxTagsData.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            Uts.tags = json.loads(r)

    @staticmethod
    def save_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxPlayersData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.pdata, indent=4)
            f.write(w)
            
    @staticmethod
    def save_tags_data() -> None:
        """حفظ بيانات التاجات"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxTagsData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.tags, indent=4)
            f.write(w)

    @staticmethod
    def player_join(player: bs.Player) -> None:
        if not hasattr(Uts, "pdata"):
            Uts.create_players_data()
        
        try:
            sessionplayer = player.sessionplayer
            account_id = sessionplayer.get_v1_account_id()
            client_id = sessionplayer.inputdevice.client_id
            account_name = sessionplayer.inputdevice.get_v1_account_name(True)
        except Exception as e:
            # Only log if it's a real error, not just missing account
            if "account" not in str(e).lower():
                bs.chatmessage(f"Error in player_join: {e}")
            account_id = None
        
        if account_id:
            if type(account_id) is str and account_id.startswith('pb'):
                if account_id not in Uts.pdata:
                    Uts.add_player_data(account_id)
                    Uts.sm("Saving user data...", color=(0.35, 0.7, 0.1), transient=True, clients=[client_id])
                
                accounts = Uts.pdata[account_id]['Accounts']
                if account_name not in accounts:
                    accounts.append(account_name)
                    Uts.save_players_data()
                    
                Uts.accounts[client_id] = Uts.pdata[account_id]
                
                # إذا كان المالك، أرسل رسالة ترحيب
                if Uts.pdata[account_id].get('Owner', False):
                    Uts.sm("You are the owner!", color=(1.0, 0.5, 0.0), transient=True, clients=[client_id])
            
            Uts.usernames[client_id] = account_name
            Uts.useraccounts[client_id] = account_name
            Uts.players[client_id] = sessionplayer
                
    @staticmethod
    def update_usernames() -> None:
        try:
            for r in roster():
                c_id = r['client_id']
                if c_id not in Uts.accounts:
                    if r['account_id'] in Uts.pdata:
                        Uts.accounts[c_id] = Uts.pdata[r['account_id']]
                if c_id not in Uts.usernames:
                    Uts.usernames[c_id] = r['display_string']
                    
                acc = r['display_string']
                for acc_id, dt in list(Uts.pdata.items()):
                    for ac in dt['Accounts']:
                        if ac == acc:
                            Uts.accounts[c_id] = Uts.pdata[acc_id]
                            Uts.userpbs[c_id] = acc_id
                            
        except Exception as e:
            print(f"⚠️ Error in update_usernames (roster): {e}")
                        
        for c_id, p in list(Uts.players.items()):
            try:
                if p.exists():
                    Uts.usernames[c_id] = p.getname(full=True)
                    Uts.shortnames[c_id] = p.getname(full=False)
                    
                    if p.get_v1_account_id() is not None:
                        Uts.userpbs[c_id] = p.get_v1_account_id()
            except:
                # Player might have disconnected
                if c_id in Uts.players:
                    del Uts.players[c_id]
            
    @staticmethod
    def add_player_data(account_id: str) -> None:
        if not hasattr(Uts, 'pdata'):
            Uts.create_players_data()
        
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'none',
                'Admin': False,
                'Owner': False,
                'Accounts': []}
            Uts.save_players_data()

    @staticmethod
    def save_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxSettings.json'
        
        with open(file, 'w') as f:
            w = json.dumps(cfg, indent=4)
            f.write(w)

    @staticmethod
    def create_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxSettings.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            cfg = json.loads(r)

    @staticmethod
    def create_user_system_scripts() -> None:
        """Set up a copy of Ballistica app scripts under user scripts dir.
    
        (for editing and experimenting)
        """
        import shutil
        
        app = _babase.app.env

        # Its possible these are unset in non-standard environments.
        if app.python_directory_user is None:
            raise RuntimeError('user python dir unset')
        if app.python_directory_app is None:
            raise RuntimeError('app python dir unset')
    
        path = app.python_directory_user + '/sys/' + app.engine_version + '_' + str(_babase.app.env.engine_build_number)
        
        # Check if directory already exists
        if os.path.exists(path):
            print(f"System scripts already exist at: '{path}'")
            return
        
        try:
            print(f'COPYING "{app.python_directory_app}" -> "{path}".')
            shutil.copytree(app.python_directory_app, path, 
                           ignore=shutil.ignore_patterns('__pycache__'))
            
            print(f"Created system scripts at: '{path}'")
            print(f"Restart {bui.appname()} to use them.")
            print("(use babase.quit() to exit the game)")
        except Exception as e:
            print(f"Error creating system scripts: {e}")

    @staticmethod
    def create_data_text(self) -> None:
        if isinstance(self, MainMenuActivity):
            return

        if getattr(self, '_text_data', None):
            self._text_data.node.delete()

        if cfg['Commands'].get('ShowInfo'):
            info = f"\ue043|Host: {cfg['Commands'].get('HostName', '???')}\n\ue01e|Description: {cfg['Commands'].get('Description', '???')}\n\ue01e|Version: {_babase.app.env.engine_version}"
            color = tuple(list(cfg['Commands'].get('InfoColor', Uts.colors()['white'])) + [1])
                
            self._text_data = text.Text(info,
                position=(-650.0, -200.0), color=color)

    @staticmethod
    def create_live_chat(self,
                         live: bool = True,
                         chat: list[int, str] = None,
                         admin: bool = False) -> None:
        if isinstance(self, MainMenuActivity):
            return
        
        if getattr(self, '_live_chat', None):
            self._live_chat.node.delete()
            
        if cfg['Commands'].get('ChatLive'):
            max_chats = 6
            chats = list()
            txt = str()
            icon = bui.charstr(bui.SpecialChar.STEAM_LOGO) if admin else ''
            
            if any(bs.get_chat_messages()):
                if len(Chats) == max_chats:
                    Chats.pop(0)
                    
                if live:
                    name = Uts.shortnames.get(chat[0], chat[0])
                    msg = chat[1]
                    Chats.append(f'{icon}{name}: {msg}')
                
                for msg in Chats:
                    if len(chats) != max_chats:
                        chats.append(msg)
                    else: break
                txt = '\n'.join(chats)
            
            livetext = "\ue043 CHAT LIVE \ue043"
            txt = (livetext + '\n' + ''.join(['=' for s 
                in range(len(livetext))]) + '\n') + txt

            self._live_chat = text.Text(txt, position=(650.0, 200.0),
                color=(1, 1, 1, 1), h_align=text.Text.HAlign.RIGHT)

    @staticmethod
    def funtion() -> str:
        return """    %s
    try:
        cm = babase.app.cheatmax_filter_chat(msg, client_id)
        if cm == '@':
            return None
    except Exception:
        pass
        """ % Uts.key

# ==================== نظام التيجان المتطور ====================
class TagSystem:
    """نظام التيجان المتطور للأدمنز"""
    def __init__(self):
        self.current_tags = {}
        self.animated_tags = {}
        self.char_animations = {}
        self.animation_states = {}
        self.saved_tag_templates = {}
        
        # قاموس الأيقونات واختصاراتها
        self.icons = {
            # الرموز الأساسية
            'left': '\ue001', 'right': '\ue002', 'up': '\ue003', 'down': '\ue004',
            'dleft': '\ue005', 'dup': '\ue006', 'dright': '\ue007', 'ddown': '\ue008',
            'back': '\ue009', 'joystick': '\ue010', 'circles': '\ue019',
            'android': '\ue020', 'rbyp': '\ue021',
            
            # النرد والرموز الرياضية
            'dice1': '\ue022', 'dice2': '\ue023', 'dice3': '\ue024', 'dice4': '\ue025',
            'volley': '\ue026', 'gather': '\ue027', 't': '\ue028', 'ticket': '\ue029',
            'pc': '\ue030', 'rbyp2': '\ue031',
            
            # أعلام الدول
            'us': '\ue032', 'italy': '\ue033', 'germany': '\ue034', 'brazil': '\ue035',
            'russia': '\ue036', 'china': '\ue037', 'uk': '\ue038', 'canada': '\ue039',
            'rwb': '\ue040', 'hat': '\ue041', 'fire': '\ue042', 'crown': '\ue043',
            'zen': '\ue044', 'eye': '\ue045', 'skull': '\ue046', 'heart': '\ue047',
            'dragon': '\ue048', 'helmet': '\ue049', 'rgwb': '\ue050', 'mw': '\ue051',
            'syria': '\ue052', 'bgwr': '\ue053', 'gwl': '\ue054', 'saudi': '\ue055',
            'malaysia': '\ue056', 'bwr': '\ue057', 'australia': '\ue058', 'rws': '\ue059',
            
            # التحكم
            'up2': '\ue00a', 'down2': '\ue00b', 'bslogo': '\ue00c', 'back2': '\ue00d',
            'pause': '\ue00e', 'forward': '\ue00f', 'u': '\ue01a', 'y': '\ue01b',
            'a': '\ue01c', 'usmall': '\ue01d', 'logo': '\ue01e', 'ticket2': '\ue01f',
            
            # الميداليات
            'bronze': '\ue02a', 'silver': '\ue02b', 'gold': '\ue02c', 'badge1': '\ue02d',
            'badge2': '\ue02e', 'trophy': '\ue02f',
            
            # أعلام إضافية
            'india': '\ue03a', 'japan': '\ue03b', 'france': '\ue03c', 'rw': '\ue03d',
            'gwr': '\ue03e', 'korea': '\ue03f',
            
            # الرموز
            'mushroom': '\ue04a', 'nstar': '\ue04b', 'bull': '\ue04c', 'moon': '\ue04d',
            'spider': '\ue04e', 'fireball': '\ue04f', 'rect': '\ue05a', 'steam': '\ue05b',
            'nvidia': '\ue05c',
            
            # اختصارات إضافية
            'ns': '\ue04b',  # ninja star
            'dr': '\ue048',  # dragon
            'fb': '\ue04f',  # fireball
            'cr': '\ue043',  # crown
            'sk': '\ue046',  # skull
            'ht': '\ue047',  # heart
            'hl': '\ue049',  # helmet
            'ms': '\ue04a',  # mushroom
            'bl': '\ue04c',  # bull
            'mn': '\ue04d',  # moon
            'sp': '\ue04e',  # spider
            'la': '\ue001',  # left arrow
            'ra': '\ue002',  # right arrow
            'ua': '\ue003',  # up arrow
            'da': '\ue004',  # down arrow
        }
        
        self.colors = {
            'red': (1.0, 0.0, 0.0),
            'green': (0.0, 1.0, 0.0),
            'blue': (0.0, 0.0, 1.0),
            'yellow': (1.0, 1.0, 0.0),
            'gold': (1.0, 0.84, 0.0),
            'pink': (1.0, 0.3, 0.5),
            'orange': (1.0, 0.5, 0.0),
            'purple': (0.5, 0.0, 0.5),
            'white': (1.0, 1.0, 1.0),
            'black': (0.1, 0.1, 0.1),
            'cyan': (0.0, 1.0, 1.0),
            'lime': (0.5, 1.0, 0.0),
            'rainbow': 'rainbow'
        }
        
        self.positions = {
            'top': (0, 2.0, 0),  # أعلى رأس اللاعب
            'down': (0, -2.0, 0),
            'right': (2.0, 1.0, 0),
            'left': (-2.0, 1.0, 0),
            'center': (0, 2.0, 0),  # أعلى الرأس
            'head': (0, 2.5, 0),  # أعلى الرأس
            'feet': (0, -1.0, 0)
        }
        
        print("🎮 TagMaster Advanced System Loading...")
        
        # تحميل القوالب المحفوظة
        self.templates_file = Uts.directory_user + '/Configs/tag_templates.json'
        self.load_templates()
        
        # بدء مراقبة اللعبة بعد تأخير
        bs.apptimer(3.0, lambda: self.start_game_monitoring())
    
    def start_game_monitoring(self):
        """بدء مراقبة اللعبة مع فحص الصلاحيات"""
        def game_monitor():
            try:
                # في وضع السيرفر، تقليل التكرار
                activity = bs.get_foreground_host_activity()
                if activity and hasattr(activity, 'players'):
                    try:
                        self.quick_apply_tags(activity)
                        self.cleanup_dead_players(activity)
                        self.check_player_respawns(activity)
                    except Exception as e:
                        print(f"⚠️ Tag monitor error: {e}")
                
                # إعادة الجدولة
                bs.apptimer(2.0, game_monitor)
                    
            except Exception as e:
                print(f"❌ Game monitor error: {e}")
                # إعادة المحاولة بعد 5 ثواني في حالة الخطأ
                bs.apptimer(5.0, game_monitor)
        
        # بدء المراقبة بعد تأخير
        bs.apptimer(1.0, game_monitor)
        print("🎮 Tag monitoring started (server optimized)")
    
    def quick_apply_tags(self, activity):
        """تطبيق سريع للتيجان"""
        try:
            if not activity or not hasattr(activity, 'players'):
                return
                
            for player in activity.players:
                try:
                    if not player.is_alive() or not player.actor or not player.actor.node:
                        continue
                        
                    client_id = player.sessionplayer.inputdevice.client_id
                    
                    # البحث عن account_id
                    account_id = None
                    if client_id in Uts.userpbs:
                        account_id = Uts.userpbs[client_id]
                    
                    if account_id and account_id in Uts.pdata:
                        player_data = Uts.pdata[account_id]
                        if 'Tag' in player_data:
                            tag_data = player_data['Tag']
                            
                            # تطبيق التاج فقط إذا لم يكن مطبقًا بالفعل
                            if str(client_id) not in self.current_tags:
                                if tag_data.get('type') == 'animated':
                                    self.create_animated_tag_gradual(player, client_id, tag_data, activity)
                                else:
                                    self.create_tag_with_char_animation(player, client_id, tag_data['text'], 
                                                                      tuple(tag_data.get('color', (1,1,1))), 
                                                                      tag_data.get('scale', 0.03), 
                                                                      activity)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"❌ Quick apply tags error: {e}")

    def apply_normal_tag(self, player, client_id, tag_data, activity):
        """تطبيق تاج عادي"""
        try:
            if str(client_id) in self.current_tags:
                self.remove_tag_visual(client_id)
                self.stop_char_animation(client_id)
            
            self.create_tag_with_char_animation(player, client_id, tag_data['text'], 
                                              tuple(tag_data.get('color', (1,1,1))), 
                                              tag_data.get('scale', 0.03), activity)
        except Exception as e:
            print(f"❌ Error applying normal tag: {e}")

    def create_animated_tag_gradual(self, player, client_id, tag_data, activity):
        """إنشاء تاج متحرك"""
        try:
            player_name = player.getname()
            if not player.actor or not player.actor.node:
                return False
            
            with activity.context:
                colors = tag_data.get('colors', [(1, 1, 1)])
                first_color = colors[0] if colors else (1, 1, 1)
                
                attrs = {
                    'text': tag_data['text'],
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,  # نفس PopupText
                    'h_align': 'center',
                    'v_align': 'center',
                    'scale': tag_data['scale'],
                    'color': first_color,
                    'opacity': 0.0
                }
                
                tag_node = bs.newnode('text', attrs=attrs)
                
                # ربط التاج باللاعب أعلى الرأس - نفس PopupText
                math_node = bs.newnode('math',
                    attrs={'input1': (0.0, 1.5, 0.0), 'operation': 'add'})
                
                player.actor.node.connectattr('position_center', math_node, 'input2')
                math_node.connectattr('output', tag_node, 'position')
                
                self.current_tags[str(client_id)] = {
                    'type': 'animated_gradual',
                    'tag_node': tag_node,
                    'math_node': math_node,
                    'text': tag_data['text'],
                    'colors': colors,
                    'scale': tag_data['scale'],
                    'speed': tag_data['speed']
                }
                
                animation_data = {
                    'tag_node': tag_node,
                    'text': tag_data['text'],
                    'current_char_index': 0,
                    'start_time': bs.time(),
                    'duration': 0.5,
                    'original_opacity': 1.0
                }
                
                self.char_animations[str(client_id)] = animation_data
                
                def animate_text_display():
                    try:
                        if str(client_id) not in self.char_animations:
                            return
                        
                        data = self.char_animations[str(client_id)]
                        current_idx = data['current_char_index']
                        
                        if current_idx > len(data['text']):
                            data['tag_node'].opacity = data['original_opacity']
                            self.start_gradual_animation(client_id)
                            return
                        
                        partial_text = data['text'][:current_idx]
                        data['tag_node'].text = partial_text
                        
                        progress = min(1.0, current_idx / len(data['text']))
                        opacity = progress
                        
                        if progress < 0.5:
                            opacity = progress * 2
                        else:
                            opacity = 1.0
                        
                        data['tag_node'].opacity = opacity
                        data['current_char_index'] += 1
                        
                        if current_idx <= len(data['text']):
                            bs.apptimer(0.08, animate_text_display)
                    except:
                        pass
                
                bs.apptimer(0.1, animate_text_display)
                print(f"🌈 Animated tag '{tag_data['text']}' created for {player_name}")
                return True
        except Exception as e:
            print(f"❌ Failed to create animated tag: {e}")
            return False

    def start_gradual_animation(self, client_id):
        """بدء الأنيميشن التدريجي"""
        try:
            if str(client_id) not in self.current_tags:
                return
            
            tag_data = self.current_tags[str(client_id)]
            colors = tag_data['colors']
            
            if len(colors) < 2:
                return
            
            self.animation_states[str(client_id)] = {
                'current_index': 0,
                'next_index': 1,
                'transition': 0.0
            }
            
            def animate_gradual():
                try:
                    if str(client_id) not in self.current_tags or str(client_id) not in self.animation_states:
                        return
                    
                    tag_data = self.current_tags[str(client_id)]
                    tag_node = tag_data['tag_node']
                    
                    if not tag_node.exists():
                        if str(client_id) in self.animation_states:
                            del self.animation_states[str(client_id)]
                        return
                    
                    state = self.animation_states[str(client_id)]
                    colors = tag_data['colors']
                    
                    color1 = colors[state['current_index']]
                    color2 = colors[state['next_index']]
                    
                    t = state['transition']
                    r = color1[0] + (color2[0] - color1[0]) * t
                    g = color1[1] + (color2[1] - color1[1]) * t
                    b = color1[2] + (color2[2] - color1[2]) * t
                    
                    tag_node.color = (r, g, b)
                    state['transition'] += 0.05 * tag_data['speed']
                    
                    if state['transition'] >= 1.0:
                        state['transition'] = 0.0
                        state['current_index'] = state['next_index']
                        state['next_index'] = (state['next_index'] + 1) % len(colors)
                    
                    bs.apptimer(0.05, animate_gradual)
                except:
                    if str(client_id) in self.animation_states:
                        del self.animation_states[str(client_id)]
            
            bs.apptimer(0.05, animate_gradual)
        except Exception as e:
            print(f"❌ Error starting gradual animation: {e}")

    def cleanup_dead_players(self, activity):
        """تنظيف التيجان للاعبين الموتى"""
        try:
            for client_id_str in list(self.current_tags.keys()):
                player_found = False
                player_alive = False
                
                for player in activity.players:
                    try:
                        if str(player.sessionplayer.inputdevice.client_id) == client_id_str:
                            player_found = True
                            if player.is_alive():
                                player_alive = True
                            break
                    except:
                        continue
                
                if not player_found or not player_alive:
                    try:
                        client_id = int(client_id_str)
                        self.remove_tag_visual(client_id)
                        self.stop_char_animation(client_id)
                    except:
                        pass
        except:
            pass

    def check_player_respawns(self, activity):
        """التحقق من إعادة ولادة اللاعبين"""
        try:
            for player in activity.players:
                try:
                    client_id = player.sessionplayer.inputdevice.client_id
                    account_id = None
                    
                    # البحث عن account_id الخاص باللاعب
                    for acc_id, acc_data in Uts.pdata.items():
                        if client_id in Uts.userpbs and Uts.userpbs[client_id] == acc_id:
                            account_id = acc_id
                            break
                    
                    if account_id and account_id in Uts.pdata:
                        player_data = Uts.pdata[account_id]
                        if 'Tag' in player_data:
                            tag_data = player_data['Tag']
                            if player.is_alive() and player.actor and player.actor.node:
                                if str(client_id) not in self.current_tags:
                                    if tag_data.get('type') == 'animated':
                                        self.create_animated_tag_gradual(player, client_id, tag_data, activity)
                                    else:
                                        self.create_tag_with_char_animation(player, client_id, tag_data['text'],
                                                                          tuple(tag_data['color']),
                                                                          tag_data['scale'], activity)
                except:
                    pass
        except:
            pass

    def create_tag_with_char_animation(self, player, client_id, text: str, color, scale: float, activity) -> bool:
        """إنشاء تاج مع أنيميشن للحروف - يظهر أعلى رأس اللاعب"""
        try:
            player_name = player.getname()
            if not player.actor or not player.actor.node:
                return False

            with activity.context:
                # إزالة التاج السابق إذا موجود
                self.remove_tag_visual(client_id)
                self.stop_char_animation(client_id)

                # إنشاء عقدة النص - نفس خصائص PopupText
                tag_node = bs.newnode('text',
                                      attrs={
                                          'text': '',
                                          'in_world': True,
                                          'shadow': 1.0,
                                          'flatness': 1.0,  # نفس PopupText
                                          'h_align': 'center',
                                          'v_align': 'center',
                                          'scale': scale,
                                          'color': color,
                                          'opacity': 0.0
                                      })

                # ربط التاج باللاعب أعلى الرأس - نفس طريقة PopupText
                math_node = bs.newnode('math',
                                       attrs={'input1': (0.0, 1.5, 0.0), 'operation': 'add'})
                player.actor.node.connectattr('position_center', math_node, 'input2')
                math_node.connectattr('output', tag_node, 'position')

                # حفظ البيانات
                self.current_tags[str(client_id)] = {
                    'type': 'normal',
                    'tag_node': tag_node,
                    'math_node': math_node,
                    'text': text,
                    'color': color,
                    'scale': scale
                }

                # أنيميشن ظهور الحروف واحدة تلو الأخرى
                def animate_text():
                    try:
                        if str(client_id) not in self.current_tags:
                            return

                        tag_node = self.current_tags[str(client_id)]['tag_node']
                        if not tag_node.exists():
                            return

                        # إذا كانت الرسالة فارغة، تخطي
                        if not text:
                            tag_node.text = ''
                            tag_node.opacity = 1.0
                            return

                        # عرض الحروف تدريجيًا
                        for i in range(len(text) + 1):
                            def update_text(idx):
                                return lambda: self._update_text_animation(client_id, text, idx, color)

                            bs.apptimer(i * 0.05, update_text(i))

                        # بعد اكتمال ظهور النص، زيادة الشفافية
                        def finalize():
                            if str(client_id) in self.current_tags:
                                tag_node = self.current_tags[str(client_id)]['tag_node']
                                if tag_node.exists():
                                    tag_node.opacity = 1.0

                        bs.apptimer(len(text) * 0.05 + 0.5, finalize)
                    except Exception as e:
                        print(f"Error in animate_text: {e}")

                # بدء الأنيميشن بعد تأخير قصير
                bs.apptimer(0.1, animate_text)

                print(f"Created tag '{text}' for {player_name}")
                return True
        except Exception as e:
            print(f"Error creating tag with char animation: {e}")
            return False

    def _update_text_animation(self, client_id, full_text, index, color):
        """تحديث النص أثناء الأنيميشن"""
        try:
            if str(client_id) not in self.current_tags:
                return

            tag_node = self.current_tags[str(client_id)]['tag_node']
            if not tag_node.exists():
                return

            # عرض النص حتى الحرف الحالي
            partial_text = full_text[:index]
            tag_node.text = partial_text

            # تحديث اللون
            tag_node.color = color

            # زيادة الشفافية تدريجيًا
            opacity = min(1.0, index / len(full_text))
            tag_node.opacity = opacity
        except Exception as e:
            print(f"Error in _update_text_animation: {e}")

    def remove_tag_visual(self, client_id):
        """إزالة التاج المرئي"""
        try:
            client_id_str = str(client_id)
            if client_id_str in self.current_tags:
                tag_data = self.current_tags[client_id_str]
                if 'tag_node' in tag_data and tag_data['tag_node'] and tag_data['tag_node'].exists():
                    tag_data['tag_node'].delete()
                if 'math_node' in tag_data and tag_data['math_node'] and tag_data['math_node'].exists():
                    tag_data['math_node'].delete()
                del self.current_tags[client_id_str]
        except Exception as e:
            print(f"Error removing tag visual: {e}")

    def stop_char_animation(self, client_id):
        """إيقاف أنيميشن الحروف"""
        try:
            client_id_str = str(client_id)
            if client_id_str in self.char_animations:
                del self.char_animations[client_id_str]
        except:
            pass

    def stop_animation(self, client_id):
        """إيقاف الأنيميشن"""
        try:
            client_id_str = str(client_id)
            if client_id_str in self.animation_states:
                del self.animation_states[client_id_str]
        except:
            pass

    def load_templates(self):
        """تحميل قوالب التاجات المحفوظة"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r') as f:
                    self.saved_tag_templates = json.load(f)
            else:
                self.saved_tag_templates = {}
        except:
            self.saved_tag_templates = {}

    def save_templates(self):
        """حفظ قوالب التاجات"""
        try:
            with open(self.templates_file, 'w') as f:
                json.dump(self.saved_tag_templates, f, indent=4)
        except:
            pass

    def send_client_message(self, client_id, message, color=(1,1,1)):
        """إرسال رسالة إلى العميل"""
        try:
            bs.screenmessage(message, color=color, clients=[client_id], transient=True)
        except:
            pass

    def parse_color(self, color_str: str):
        """تحويل نص اللون إلى قيم RGB"""
        color_str = color_str.lower()

        # إذا كان اللون معروفًا في القاموس
        if color_str in self.colors:
            return self.colors[color_str]

        # إذا كان بتنسيق rgb مثل 1.0,0.5,0.0
        if ',' in color_str:
            try:
                parts = color_str.split(',')
                if len(parts) == 3:
                    r = float(parts[0].strip())
                    g = float(parts[1].strip())
                    b = float(parts[2].strip())
                    return (max(0.0, min(1.0, r)), max(0.0, min(1.0, g)), max(0.0, min(1.0, b)))
            except:
                pass

        # إذا كان بتنسيق hex مثل #ff00ff
        if color_str.startswith('#') and len(color_str) == 7:
            try:
                r = int(color_str[1:3], 16) / 255.0
                g = int(color_str[3:5], 16) / 255.0
                b = int(color_str[5:7], 16) / 255.0
                return (r, g, b)
            except:
                pass

        # افتراضي
        return (1.0, 1.0, 1.0)

    def generate_rainbow_colors(self, count: int):
        """إنشاء قائمة بألوان قوس قزح"""
        colors = []
        for i in range(count):
            # توزيع ألوان قوس قزح
            hue = i / count
            # تحويل من HSV إلى RGB (تبسيط)
            if hue < 1/6:
                r, g, b = 1.0, hue * 6, 0.0
            elif hue < 2/6:
                r, g, b = (2/6 - hue) * 6, 1.0, 0.0
            elif hue < 3/6:
                r, g, b = 0.0, 1.0, (hue - 2/6) * 6
            elif hue < 4/6:
                r, g, b = 0.0, (4/6 - hue) * 6, 1.0
            elif hue < 5/6:
                r, g, b = (hue - 4/6) * 6, 0.0, 1.0
            else:
                r, g, b = 1.0, 0.0, (1 - hue) * 6

            colors.append((r, g, b))
        return colors

# إنشاء مثيل نظام التيجان
Uts.tag_system = TagSystem()

def _install() -> None:
    from bascenev1 import _hooks
    from babase import _app, modutils
    _file = Uts.directory_sys + "/bascenev1/_hooks.py"
    
    # تعيين دالة فلترة الشات
    bs.app.cheatmax_filter_chat = filter_chat_message
    
    def seq():
        """تسلسل التثبيت"""
        bs.screenmessage(f"Installing <{__name__}>")
        bs.apptimer(2.0, bs.CallStrict(Uts.sm, f"<{__name__}> Installed successfully!", (0.0, 1.0, 0.0)))
        bs.apptimer(4.0, bs.CallStrict(Uts.sm, "Rebooting..."))
        bs.apptimer(6.0, bui.quit)
    
    # إنشاء المجلدات إذا لم تكن موجودة
    if not os.path.exists(Uts.directory_sys):
        os.makedirs(os.path.dirname(_file), exist_ok=True)
        print(f"✅ Created system directory: {Uts.directory_sys}")
    
    try:
        if os.path.exists(_file):
            with open(_file, 'r', encoding='utf-8') as s:
                read = s.read()
                read_l = read.split("\n")
            
            if Uts.key not in read:
                f_list = Uts.funtion().split("\n")
                try:
                    # البحث عن دالة filter_chat_message
                    ix = None
                    for i, line in enumerate(read_l):
                        if "def filter_chat_message" in line:
                            ix = i
                            break
                    
                    if ix is not None:
                        # إدخال الكود في المكان المناسب
                        for i, lt in enumerate(f_list):
                            read_l.insert(i + (ix + 1), lt)
                        read = "\n".join(read_l)
                        
                        # إنشاء نسخة احتياطية
                        backup_file = _file + ".backup"
                        if os.path.exists(backup_file):
                            os.remove(backup_file)
                        os.rename(_file, backup_file)
                        
                        # كتابة الملف المعدل
                        with open(_file, "w", encoding='utf-8') as s:
                            s.write(read)
                        print("✅ Successfully injected code into _hooks.py")
                        seq()
                    else:
                        print("⚠️ Could not find filter_chat_message function in _hooks.py")
                        # المحاولة باستمرار بدون إعادة تشغيل
                except (ValueError, IndexError) as e:
                    print(f"⚠️ Error finding insertion point: {e}")
                except PermissionError:
                    print("❌ Permission denied to modify _hooks.py")
                    # الاستمرار بدون الحقن
                except Exception as e:
                    print(f"❌ Error during injection: {e}")
        else:
            print(f"⚠️ _hooks.py not found at {_file}")
            # إنشاء ملف _hooks.py بديل إذا كان ضرورياً
            try:
                with open(_file, 'w', encoding='utf-8') as f:
                    f.write("""
# كود أساسي للـ hooks إذا كان الملف غير موجود
""")
                print(f"✅ Created new _hooks.py at {_file}")
            except Exception as e:
                print(f"❌ Failed to create _hooks.py: {e}")
    except Exception as e:
        print(f"❌ Install error: {e}")
        # المتابعة على أي حال
    
    # تهيئة البيانات
    try:
        Uts.create_players_data()
        Uts.save_players_data()
        
        # إنشاء بيانات التاجات
        if not hasattr(Uts, 'tags'):
            Uts.create_tags_data()
        
        # إضافة المالك الافتراضي
        owner_account = 'pb-IF4yVRIDXA=='
        if owner_account not in Uts.pdata:
            Uts.add_owner(owner_account)
            print(f"✅ Added owner: {owner_account}")
        
        # إرسال رسالة تأكيد
        bs.apptimer(3.0, lambda: Uts.sm("Owner added!", color=(1.0, 0.5, 0.0)))
        
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
    
    # تهيئة نظام التيجان
    if not hasattr(Uts, 'tag_system'):
        Uts.tag_system = TagSystem()
        print("✅ Tag system initialized")

def settings():
    """تهيئة الإعدادات"""
    global cfg
    Uts.create_settings()
    
    if cfg.get('Commands') is None:
        cfg['Commands'] = dict()
        # إعدادات افتراضية
        cfg['Commands']['ShowInfo'] = True
        cfg['Commands']['ShowMessages'] = True
        cfg['Commands']['ChatLive'] = True
        cfg['Commands']['HostName'] = "CheatMax Server"
        cfg['Commands']['Description'] = "Powered by CheatMax System"
        cfg['Commands']['InfoColor'] = list(Uts.colors()['white'])
        Uts.save_settings()
        print("✅ Default settings created")
    
    print("✅ Settings loaded successfully")

def plugin():
    """توصيل الدوال المخصصة باللعبة"""
    try:
        # حفظ الدوال الأصلية
        calls['GA_OnTransitionIn'] = bs.GameActivity.on_transition_in
        calls['OnJumpPress'] = PlayerSpaz.on_jump_press
        calls['OnPlayerJoin'] = Activity.on_player_join
        calls['PlayerSpazInit'] = PlayerSpaz.__init__
        
        # استبدال بالدوال المخصصة
        bs.GameActivity.on_transition_in = new_ga_on_transition_in
        PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
        Activity.on_player_join = new_on_player_join
        PlayerSpaz.__init__ = new_playerspaz_init_
        
        # تفعيل أيقونة الحزب دائمًا
        try:
            bui.set_party_icon_always_visible(True)
        except:
            pass
        
        print("✅ Plugin functions connected successfully")
        
    except Exception as e:
        print(f"❌ Error connecting plugin functions: {e}")

def additional_features():
    """إضافة ميزات إضافية"""
    
    # 1. نظام الحماية من الإساءة
    class AbuseProtection:
        def __init__(self):
            self.warning_count = {}
            self.kick_threshold = 3
            self.mute_duration = 300  # 5 دقائق
            
        def warn_player(self, client_id, reason):
            if client_id not in self.warning_count:
                self.warning_count[client_id] = 0
            self.warning_count[client_id] += 1
            
            name = Uts.usernames.get(client_id, f"Player {client_id}")
            bs.screenmessage(f"⚠️ Warning to {name}: {reason}", color=(1, 1, 0))
            
            if self.warning_count[client_id] >= self.kick_threshold:
                bs.disconnect_client(client_id)
                bs.chatmessage(f"🚫 {name} was kicked for repeated warnings")
                del self.warning_count[client_id]
    
    Uts.abuse_protection = AbuseProtection()
    
    # 2. نظام الإحصائيات
    class Statistics:
        def __init__(self):
            self.player_stats = {}
            
        def record_kill(self, killer_id, victim_id):
            if killer_id not in self.player_stats:
                self.player_stats[killer_id] = {'kills': 0, 'deaths': 0}
            if victim_id not in self.player_stats:
                self.player_stats[victim_id] = {'kills': 0, 'deaths': 0}
                
            self.player_stats[killer_id]['kills'] += 1
            self.player_stats[victim_id]['deaths'] += 1
            
        def get_stats(self, client_id):
            return self.player_stats.get(client_id, {'kills': 0, 'deaths': 0})
    
    Uts.statistics = Statistics()
    
    # 3. نظام المكافآت اليومية
    class DailyRewards:
        def __init__(self):
            self.rewards_file = Uts.directory_user + '/Configs/daily_rewards.json'
            self.rewards_data = self.load_rewards()
            
        def load_rewards(self):
            try:
                if os.path.exists(self.rewards_file):
                    with open(self.rewards_file, 'r') as f:
                        return json.load(f)
                return {}
            except:
                return {}
                
        def save_rewards(self):
            try:
                with open(self.rewards_file, 'w') as f:
                    json.dump(self.rewards_data, f, indent=4)
            except:
                pass
                
        def give_reward(self, account_id):
            today = str(datetime.now().date())
            if account_id not in self.rewards_data:
                self.rewards_data[account_id] = {'last_reward': '', 'streak': 0}
            
            if self.rewards_data[account_id]['last_reward'] != today:
                self.rewards_data[account_id]['last_reward'] = today
                self.rewards_data[account_id]['streak'] += 1
                self.save_rewards()
                
                # مكافأة حسب عدد الأيام المتتالية
                streak = self.rewards_data[account_id]['streak']
                reward_msg = f"🎁 Daily Reward! Streak: {streak} days"
                bs.chatmessage(reward_msg)
                return True
            return False
    
    Uts.daily_rewards = DailyRewards()
    
    print("✅ Additional features initialized")

def setup_automatic_backup():
    """إعداد النسخ الاحتياطي التلقائي"""
    import shutil
    from datetime import datetime
    
    backup_dir = Uts.directory_user + '/Backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    def backup_data():
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # نسخ بيانات اللاعبين
            players_file = Uts.directory_user + '/Configs/CheatMaxPlayersData.json'
            if os.path.exists(players_file):
                backup_file = f"{backup_dir}/players_backup_{timestamp}.json"
                shutil.copy2(players_file, backup_file)
            
            # نسخ الإعدادات
            settings_file = Uts.directory_user + '/Configs/CheatMaxSettings.json'
            if os.path.exists(settings_file):
                backup_file = f"{backup_dir}/settings_backup_{timestamp}.json"
                shutil.copy2(settings_file, backup_file)
            
            # حذف النسخ القديمة (احتفظ بـ 10 فقط)
            backup_files = sorted([f for f in os.listdir(backup_dir) if f.endswith('.json')])
            for old_file in backup_files[:-10]:
                try:
                    os.remove(os.path.join(backup_dir, old_file))
                except:
                    pass
                
        except Exception as e:
            print(f"⚠️ Backup error: {e}")
    
    # دالة تكرارية للنسخ الاحتياطي
    def backup_loop():
        backup_data()
        # إعادة الجدولة بعد ساعة
        bs.apptimer(3600.0, backup_loop)
    
    # بدء النسخ الاحتياطي التلقائي
    bs.apptimer(3600.0, backup_loop)
    print("✅ Automatic backup system activated")

def setup_performance_monitor():
    """مراقبة الأداء"""
    import threading
    
    class PerformanceMonitor:
        def __init__(self):
            self.fps_history = []
            self.max_history = 100
            self.thread = threading.Thread(target=self.monitor, daemon=True)
            self.thread.start()
            
        def monitor(self):
            import time
            while True:
                try:
                    fps = bs.get_fps()
                    self.fps_history.append(fps)
                    if len(self.fps_history) > self.max_history:
                        self.fps_history.pop(0)
                    
                    # تحذير إذا كان الـ FPS منخفض
                    if len(self.fps_history) > 10:
                        avg_fps = sum(self.fps_history[-10:]) / 10
                        if avg_fps < 30:
                            print(f"⚠️ Low FPS: {avg_fps:.1f}")
                    
                    time.sleep(5)
                except:
                    time.sleep(10)
                    
        def get_performance_report(self):
            if not self.fps_history:
                return "No data"
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            min_fps = min(self.fps_history)
            max_fps = max(self.fps_history)
            return f"FPS: Avg {avg_fps:.1f}, Min {min_fps:.1f}, Max {max_fps:.1f}"
    
    Uts.performance_monitor = PerformanceMonitor()
    print("✅ Performance monitor started")

def add_special_commands():
    """إضافة أوامر خاصة إضافية"""
    
    # قائمة بالأوامر الخاصة
    special_commands = {
        # أوامر المرح
        'party': {
            'description': 'بدء حفلة!',
            'admin_only': False,
            'function': lambda client_id: start_party(client_id)
        },
        
        # أوامر المعلومات
        'stats': {
            'description': 'عرض إحصائياتك',
            'admin_only': False,
            'function': lambda client_id: show_stats(client_id)
        }
    }
    
    def start_party(client_id):
        activity = bs.get_foreground_host_activity()
        if activity:
            for _ in range(50):
                pos = (random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-5, 5))
                Bomb(position=pos, bomb_type='impact', bomb_scale=0.5).autoretain()
            bs.screenmessage("🎉 PARTY TIME! 🎉", clients=[client_id], color=(1,0,1))
    
    def show_stats(client_id):
        if client_id in Uts.statistics.player_stats:
            stats = Uts.statistics.player_stats[client_id]
            message = f"📊 Kills: {stats['kills']} | Deaths: {stats['deaths']}"
            bs.screenmessage(message, clients=[client_id])
        else:
            bs.screenmessage("📊 No stats yet", clients=[client_id])
    
    # إضافة الأوامر إلى نظام الأوامر
    for cmd, data in special_commands.items():
        CommandFunctions.all_cmd().append(cmd)
    
    print(f"✅ Added {len(special_commands)} special commands")

def final_setup():
    """الإعداد النهائي بعد التحميل"""
    
    # التحقق من وجود النظام
    if not hasattr(bs, 'app') or not hasattr(bs.app, 'cheatmax_filter_chat'):
        print("⚠️ CheatMax system not fully initialized")
        # المحاولة لإعادة التعيين
        try:
            bs.app.cheatmax_filter_chat = filter_chat_message
        except:
            pass
    
    # عرض رسالة ترحيب
    welcome_msg = f"""
╔══════════════════════════════════════════╗
║       🎮 CheatMax System v2.0 🎮        ║
║      Advanced Tag & Admin System         ║
╠══════════════════════════════════════════╣
║ • Tag System: ✓ Active                  ║
║ • Commands: ✓ Loaded                    ║
║ • Multi-Language: ✓ Supported           ║
║ • Protection: ✓ Enabled                 ║
╚══════════════════════════════════════════╝
    """
    
    for line in welcome_msg.split('\n'):
        print(line)
    
    # بدء النظام
    try:
        Uts.tag_system.start_game_monitoring()
    except:
        pass
    
    print("✅ CheatMax system ready!")

# ==================== الفئة الرئيسية للمود ====================

# ba_meta export babase.Plugin
class CheatMaxSystem(bs.Plugin):
    """نظام CheatMax المتقدم للتحكم والإدارة في BombSquad"""
    
    def __init__(self):
        self.initialized = False
        self.version = "2.0.0"
        self.author = "CheatMax Team"
        
    def on_app_running(self) -> None:
        """عند تشغيل التطبيق"""
        try:
            print(f"🚀 Loading CheatMax System v{self.version}...")
            
            # تأخير بسيط لضمان تحميل كل شيء
            bs.apptimer(0.5, self.initialize_system)
            
        except Exception as e:
            print(f"❌ Error in on_app_running: {e}")
    
    def initialize_system(self):
        """تهيئة النظام"""
        try:
            # 1. توصيل الدوال
            plugin()
            
            # 2. تحميل الإعدادات
            settings()
            
            # 3. تثبيت النظام
            bs.apptimer(1.0, _install)
            
            # 4. الميزات الإضافية
            bs.apptimer(2.0, additional_features)
            
            # 5. النسخ الاحتياطي التلقائي
            bs.apptimer(3.0, setup_automatic_backup)
            
            # 6. مراقبة الأداء
            bs.apptimer(4.0, setup_performance_monitor)
            
            # 7. الأوامر الخاصة
            bs.apptimer(5.0, add_special_commands)
            
            # 8. الإعداد النهائي
            bs.apptimer(6.0, final_setup)
            
            self.initialized = True
            print("✅ CheatMax System initialization sequence started")
            
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            # المحاولة للاستمرار بأقل الميزات
            try:
                plugin()
                settings()
                print("⚠️ System loaded with minimal features")
            except:
                print("❌ Failed to load minimal system")

# ==================== التعامل مع الأخطاء ====================

def error_handler(func):
    """معالج أخطاء للدوال المهمة"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ Error in {func.__name__}: {e}")
            # تسجيل الخطأ في ملف
            try:
                error_log = Uts.directory_user + '/Configs/cheatmax_errors.log'
                with open(error_log, 'a') as f:
                    f.write(f"{datetime.now()}: {func.__name__} - {e}\n")
            except:
                pass
            return None
    return wrapper

# تطبيق معالج الأخطاء على الدوال المهمة
filter_chat_message = error_handler(filter_chat_message)
new_ga_on_transition_in = error_handler(new_ga_on_transition_in)
new_on_player_join = error_handler(new_on_player_join)
new_playerspaz_init_ = error_handler(new_playerspaz_init_)
new_playerspaz_on_jump_press = error_handler(new_playerspaz_on_jump_press)

# ==================== اختبار النظام ====================

def system_test():
    """اختبار النظام للتأكد من عمله"""
    def run_tests():
        print("🧪 Running system tests...")
        
        tests_passed = 0
        tests_failed = 0
        
        # اختبار 1: وجود الملفات
        try:
            if os.path.exists(Uts.directory_user + '/Configs'):
                print("✅ Test 1: Config directory exists")
                tests_passed += 1
            else:
                print("❌ Test 1: Config directory missing")
                tests_failed += 1
        except:
            tests_failed += 1
        
        # اختبار 2: نظام التيجان
        try:
            if hasattr(Uts, 'tag_system'):
                print("✅ Test 2: Tag system initialized")
                tests_passed += 1
            else:
                print("❌ Test 2: Tag system not initialized")
                tests_failed += 1
        except:
            tests_failed += 1
        
        # اختبار 3: بيانات اللاعبين
        try:
            if hasattr(Uts, 'pdata'):
                print("✅ Test 3: Player data loaded")
                tests_passed += 1
            else:
                print("❌ Test 3: Player data not loaded")
                tests_failed += 1
        except:
            tests_failed += 1
        
        # اختبار 4: الإعدادات
        try:
            global cfg
            if cfg and 'Commands' in cfg:
                print("✅ Test 4: Settings loaded")
                tests_passed += 1
            else:
                print("❌ Test 4: Settings not loaded")
                tests_failed += 1
        except:
            tests_failed += 1
        
        print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
        
        if tests_failed == 0:
            print("🎉 All tests passed! System is ready.")
        else:
            print("⚠️ Some tests failed. System may have issues.")
    
    # تشغيل الاختبارات بعد 10 ثواني
    bs.apptimer(10.0, run_tests)

# تشغيل اختبار النظام
bs.apptimer(8.0, system_test)

print("=" * 50)
print("CheatMax System Code Loaded Successfully!")
print("=" * 50)
