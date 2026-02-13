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
        activity = bs.get_foreground_host_activity()
        if activity is not None:
            return activity
        try:
            from bascenev1._session import Session
            session = bs.getsession()
            if hasattr(session, 'activity'):
                activity = session.activity
                if activity is not None:
                    return activity
        except:
            pass
        try:
            import _babase
            activity = _babase.get_foreground_host_activity()
            if activity is not None:
                return activity
        except:
            pass
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
                 "English": f"'{subs}' is invalid. \n Add the player ID. use the '/list' command for more information.",
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
                 "English": "Invalid player information.",
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
                {"Spanish": "Agrega el ID del cliente.  \n utilice el comando '/list' para más información.",
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
            # New phrases for ban/report system
            "BanUsage":
                {"Spanish": "Usa: /ban <pb-ID أو client-ID أو الاسم> <السبب>",
                 "English": "Use: /ban <pb-ID or client-ID or Name> <reason>",
                 "Portuguese": "Use: /ban <pb-ID ou client-ID ou Nome> <motivo>"},
            "UnbanUsage":
                {"Spanish": "Usa: /unban <pb-ID أو client-ID أو الاسم>",
                 "English": "Use: /unban <pb-ID or client-ID or Name>",
                 "Portuguese": "Use: /unban <pb-ID ou client-ID ou Nome>"},
            "ReportUsage":
                {"Spanish": "Usa: /report <pb-ID أو client-ID أو الاسم> <السبب>",
                 "English": "Use: /report <pb-ID or client-ID or Name> <reason>",
                 "Portuguese": "Use: /report <pb-ID ou client-ID ou Nome> <motivo>"},
            "TargetNotFound":
                {"Spanish": f"اللاعب '{subs}' غير موجود",
                 "English": f"Target '{subs}' not found",
                 "Portuguese": f"Alvo '{subs}' não encontrado"},
            "AlreadyBanned":
                {"Spanish": f"⚠️ {subs} محظور بالفعل",
                 "English": f"⚠️ {subs} is already banned",
                 "Portuguese": f"⚠️ {subs} já está banido"},
            "CannotBanAdmin":
                {"Spanish": f"❌ لا يمكن حظر الأدمن/المالك {subs}",
                 "English": f"❌ Cannot ban admin/owner {subs}",
                 "Portuguese": f"❌ Não pode banir admin/proprietário {subs}"},
            "BanSuccess":
                {"Spanish": f"✅ {subs[0]} تم حظره بواسطة {subs[1]}",
                 "English": f"✅ {subs[0]} has been banned by {subs[1]}",
                 "Portuguese": f"✅ {subs[0]} foi banido por {subs[1]}"},
            "UnbanSuccess":
                {"Spanish": f"✅ {subs[0]} تم إلغاء حظره بواسطة {subs[1]}",
                 "English": f"✅ {subs[0]} has been unbanned by {subs[1]}",
                 "Portuguese": f"✅ {subs[0]} foi desbanido por {subs[1]}"},
            "NotBanned":
                {"Spanish": f"❌ {subs} غير محظور",
                 "English": f"❌ {subs} is not banned",
                 "Portuguese": f"❌ {subs} não está banido"},
            "ReportSubmitted":
                {"Spanish": f"✅ تم الإبلاغ عن {subs}",
                 "English": f"✅ Report submitted against {subs}",
                 "Portuguese": f"✅ Relatório enviado contra {subs}"},
            "NewReportAlert":
                {"Spanish": f"⚠️ تقرير جديد: {subs[0]} تم الإبلاغ عنه بواسطة {subs[1]}",
                 "English": f"⚠️ New report: {subs[0]} reported by {subs[1]}",
                 "Portuguese": f"⚠️ Novo relatório: {subs[0]} relatado por {subs[1]}"},
            "NoReports":
                {"Spanish": "📋 لا توجد تقارير",
                 "English": "📋 No reports found",
                 "Portuguese": "📋 Nenhum relatório encontrado"},
            "NoBans":
                {"Spanish": "📋 قائمة الحظر فارغة",
                 "English": "📋 Ban list is empty",
                 "Portuguese": "📋 Lista de banimentos está vazia"},
            "AdminOnly":
                {"Spanish": "❌ يجب أن تكون أدمن لاستخدام هذا الأمر",
                 "English": "❌ You must be an admin to use this command",
                 "Portuguese": "❌ Você deve ser um administrador para usar este comando"},
            "BannedMessage":
                {"Spanish": f"أنت محظور من هذا السيرفر.\nالسبب: {subs[0]}\nتم الحظر بواسطة: {subs[1]}",
                 "English": f"You are banned from this server.\nReason: {subs[0]}\nBanned by: {subs[1]}",
                 "Portuguese": f"Você está banido deste servidor.\nMotivo: {subs[0]}\nBanido por: {subs[1]}"},
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

# ==================== كرة قابلة للضرب من CheatMax ====================
class CMBall(bs.Actor):
    """كرة قدم بسيطة قابلة للضرب والحركة"""
    def __init__(self, position=(0, 1, 0)):
        super().__init__()
        shared = SharedObjects.get()
        self.node = bs.newnode('prop',
            delegate=self,
            attrs={
                'position': position,
                'mesh': bs.getmesh('shield'),
                'color_texture': bs.gettexture('ouyaUButton'),
                'body': 'sphere',
                'body_scale': 0.8,
                'mesh_scale': 0.2,
                'reflection': 'soft',
                'reflection_scale': [0.3],
                'shadow_size': 2.0,
                'materials': [shared.object_material, shared.footing_material, shared.player_material],
                'gravity_scale': 0.8
            })
        # إضافة ضوء خفيف لتظهر بشكل أفضل
        self.light = bs.newnode('light',
            owner=self.node,
            attrs={
                'position': position,
                'color': (1, 1, 1),
                'radius': 0.3,
                'intensity': 0.5,
                'height_attenuated': False
            })
        self.node.connectattr('position', self.light, 'position')

    def handlemessage(self, msg):
        if isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
            if self.light:
                self.light.delete()
        elif isinstance(msg, bs.HitMessage):
            # تطبيق دفعة على الكرة عند ضربها
            if self.node:
                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2],
                    1.0 * msg.magnitude,
                    1.0 * msg.velocity_magnitude, msg.radius, 0,
                    msg.force_direction[0], msg.force_direction[1], msg.force_direction[2]
                )
        else:
            super().handlemessage(msg)

# ==================== مسار ملف إعدادات A-Soccer ====================
ASOCCER_CONFIG_DIR = os.path.join(_babase.app.env.python_directory_user, 'Configs')
ASOCCER_CONFIG_FILE = os.path.join(ASOCCER_CONFIG_DIR, 'A-SoccerConfig.json')
# ==================== نظام الطقس العالمي (معدل بالكامل – بدون أخطاء) ====================
class WeatherEffect:
    """يدير تأثيرات الطقس العالمية (emitfx على الخريطة كلها)"""
    def __init__(self):
        self.timer = None
        self.active_type = 'none'
        self.valid_weather = [
            'none', 'snow', 'rock', 'metal', 'ice', 'spark',
            'slime', 'fire', 'splinter', 'smoke', 'rainbow'
        ]

    def start(self, weather_type: str):
        """بدء تأثير الطقس المحدد (يوقف السابق)"""
        if weather_type not in self.valid_weather:
            weather_type = 'none'
        self.stop()
        self.active_type = weather_type
        if weather_type != 'none':
            self.timer = bs.Timer(0.25, self._emit, repeat=True)  # كل 0.25 ثانية

    def stop(self):
        """إيقاف جميع تأثيرات الطقس"""
        if self.timer:
            self.timer = None
        self.active_type = 'none'

    def _emit(self):
        """تنفيذ الانبعاثات لعشرات المواقع العشوائية"""
        activity = bs.get_foreground_host_activity()
        if not activity:
            return
        with activity.context:
            for _ in range(12):
                x = random.uniform(-18, 18)
                y = random.uniform(5, 22)
                z = random.uniform(-18, 18)
                pos = (x, y, z)
                self._emit_at(pos, self.active_type)

    def _emit_at(self, pos, weather_type):
        """تحديد معاملات emitfx حسب نوع الطقس – آمن 100% (لا يمرر None)"""
        params = {
            'snow':     {'chunk_type': 'ice',      'scale': 0.5,  'count': 25, 'spread': 0.6},
            'rock':     {'chunk_type': 'rock',     'scale': 0.8,  'count': 15, 'spread': 0.5},
            'metal':    {'chunk_type': 'metal',    'scale': 0.8,  'count': 15, 'spread': 0.5},
            'ice':      {'chunk_type': 'ice',      'scale': 0.6,  'count': 20, 'spread': 0.6},
            'spark':    {'chunk_type': 'spark',    'scale': 0.5,  'count': 30, 'spread': 0.7},
            'slime':    {'chunk_type': 'slime',    'scale': 1.0,  'count': 12, 'spread': 0.5},
            'fire':     {'chunk_type': 'sweat',    'scale': 0.8,  'count': 20, 'spread': 0.5},
            'splinter': {'chunk_type': 'splinter', 'scale': 0.8,  'count': 15, 'spread': 0.5},
            'smoke':    {'chunk_type': 'spark',    'scale': 0.8,  'count': 20, 'spread': 0.5},
            
        }
        if weather_type not in params:
            return

        p = params[weather_type]
        kwargs = {
            'position': pos,
            'count': p['count'],
            'spread': p['spread'],
            'scale': p['scale'],
            'chunk_type': p['chunk_type']
        }
        if 'emit_type' in p:
            kwargs['emit_type'] = p['emit_type']
        if 'tendril_type' in p:
            kwargs['tendril_type'] = p['tendril_type']
        

        bs.emitfx(**kwargs)
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

        self.process_commands()
        
    def process_commands(self):
        try:
            self.command_all()
            if self.fct.user_is_admin(self.client_id):
                self.admin_commands()
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
                
        self.util.sm(msg, color=color,
            transient=True,
            clients=[self.client_id])
    
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
            
        elif msg.lower() == cmd[3]: # -mp
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
            
        elif msg.lower() == '/list':
            self.process_list_players()
            self.value = '@'
            
        elif msg.lower() in ['test', 'تست']:
            self.clientmessage("✅ CheatMax is working!", color=(0, 1, 0))
            self.value = '@'
            
        elif msg.lower() in ['help', 'مساعدة']:
            self.process_help_command(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/report':
            self.process_report_command(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] in ['/help']:
            self.process_help_command(msg, self.client_id)
            self.value = '@'
    
    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]

        # ========== أوامر الطقس ==========
        if ms[0] == '/weather':
            self.process_weather_command(msg, self.client_id)
            self.value = '@'
    
        elif ms[0] == cmd[0]: # /name
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
                       
        elif ms[0] == cmd[3] or ms[0] == cmd[4]: # /addAdmin /delAdmin
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
        
        elif ms[0] == '/customtag':
            self.process_advanced_customtag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/animationtag':
            self.process_animationtag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/removetag':
            self.process_removetag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/savetag':
            self.process_savetag(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/tagdata':
            self.process_tagdata(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/listtags':
            self.process_listtags(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/sharedaccounts':
            self.process_shared_accounts(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/closeserver':
            self.process_close_server(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/stopcloseserver':
            self.process_stop_close_server(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/closestatus':
            self.process_close_status(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/testclosure':
            self.test_closure_system()
            self.value = '@'
            
        # ========== أوامر الحظر والإبلاغ ==========
        elif ms[0] == '/ban':
            self.process_ban_command(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/unban':
            self.process_unban_command(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/reports':
            self.process_reports_command(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/banlist':
            self.process_banlist_command(self.client_id)
            self.value = '@'
            
        elif ms[0] == '/reportdone':
            self.process_report_done_command(msg, self.client_id)
            self.value = '@'

        # ========== الأوامر الجديدة (Teleport / Fly) ==========
        elif ms[0] == '/teleport':
            self.process_teleport_command(msg, self.client_id)
            self.value = '@'
            
        elif ms[0] == '/fly':
            self.process_fly_command_fixed(msg, self.client_id)
            self.value = '@'

        # ========== نظام التحذيرات ==========
        elif ms[0] == '/warn':
            self.process_warn_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/warns':
            self.process_warns_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/clearwarns':
            self.process_clearwarns_command(msg, self.client_id)
            self.value = '@'

        # ========== أمر الاختفاء ==========
        elif ms[0] == '/invisible':
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_visible,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            self.value = '@'

        # ========== أوامر تلوين الإضاءة والأنسجة ==========
        elif ms[0] == '/tint':
            self.process_tint_command(msg, self.client_id)
            self.value = '@'
        elif ms[0] == '/upwall':
            self.process_upwall_command(msg, self.client_id)
            self.value = '@'
        elif ms[0] == '/downwall':
            self.process_downwall_command(msg, self.client_id)
            self.value = '@'
        elif ms[0] == '/floor':
            self.process_floor_command(msg, self.client_id)
            self.value = '@'

        # ========== أمر الكرة ==========
        elif ms[0] == '/spawnball':
            self.process_spawnball_command(msg, self.client_id)
            self.value = '@'

        # ========== أمر الانفجار الكبير ==========
        elif ms[0] == '/explosion':
            self.process_explosion_command(msg, self.client_id)
            self.value = '@'

        # ========== أمر اللوكيتور ==========
        elif ms[0] == '/locator':
            self.process_locator_command(msg, self.client_id)
            self.value = '@'

        # ========== أمر البينغ ==========
        elif ms[0] == '/ping':
            self.process_ping_command(self.client_id)
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
            if cls_node is not None:
                current_act = bs.get_foreground_host_activity()
                if current_act is not None:
                    with current_act.context:
                        powerups = ['triple_bombs', 'punch', 'ice_bombs', 'impact_bombs', 
                                   'land_mines', 'sticky_bombs', 'shield', 'health', 'curse']
                        for powerup in powerups:
                            cls_node.handlemessage(bs.PowerupMessage(powerup))
                        ClientMessage("Full Power Activated!", color=(1.0, 0.0, 1.0))
            self.value = '@'
    
    # -----------------------------------------------------------------
    # أوامر تلوين الإضاءة والأنسجة – بدون حدود (أي قيمة مسموحة)
    # -----------------------------------------------------------------
    def process_tint_command(self, msg: str, client_id: int):
        """تغيير لون الإضاءة العامة (tint) – بدون حدود"""
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage("❌ Use: /tint <r> <g> <b>", color=(1,0,0))
                self.clientmessage("📝 Example: /tint 1 0.5 0.2", color=(1,1,0))
                return
            r = float(parts[1])
            g = float(parts[2])
            b = float(parts[3])
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1,0,0))
                return
            with activity.context:
                gnode = activity.globalsnode
                gnode.tint = (r, g, b)
                self.clientmessage(f"✅ Tint set to ({r}, {g}, {b})", color=(0,1,0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_upwall_command(self, msg: str, client_id: int):
        """تغيير لون الجدران العلوية – بدون حدود"""
        self._apply_color_to_soccer(msg, client_id, 'wall_up_color', 'upper', 
                                   ['hockeyStadiumStands', 'stands'], "Upper Wall")

    def process_downwall_command(self, msg: str, client_id: int):
        """تغيير لون الجدران السفلية – بدون حدود"""
        self._apply_color_to_soccer(msg, client_id, 'wall_down_color', 'lower',
                                   ['hockeyStadiumOuter', 'outer'], "Lower Wall")

    def process_floor_command(self, msg: str, client_id: int):
        """تغيير لون الأرضية – بدون حدود"""
        self._apply_color_to_soccer(msg, client_id, 'floor_color', 'floor',
                                   ['hockeyStadiumInner', 'inner', 'ground'], "Floor")

    def _apply_color_to_soccer(self, msg: str, client_id: int, config_key: str, 
                              wall_type: str, mesh_keywords: list, target_name: str):
        """تطبيق اللون على نشاط SoccerGame – بدون حدود على القيم"""
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage(f"❌ Use: {parts[0]} <r> <g> <b>", color=(1,0,0))
                return
            r = float(parts[1])
            g = float(parts[2])
            b = float(parts[3])

            # تحديث ملف إعدادات A-Soccer
            self._update_asoccer_config(config_key, r, g, b)
            self.clientmessage(f"✅ {target_name} color saved to A-Soccer config ({r},{g},{b})", color=(0,1,0))

            # محاولة تطبيق اللون مباشرة على النشاط الحالي (إذا كان SoccerGame)
            activity = bs.get_foreground_host_activity()
            if activity and activity.__class__.__name__ == 'SoccerGame':
                with activity.context:
                    if hasattr(activity, config_key):
                        setattr(activity, config_key, [r, g, b])
                    
                    applied = False
                    if wall_type == 'upper' and hasattr(activity, '_apply_wall_up_texture'):
                        activity._apply_wall_up_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_wall_up_texture()", color=(0,1,0))
                        applied = True
                    elif wall_type == 'lower' and hasattr(activity, '_apply_wall_down_texture'):
                        activity._apply_wall_down_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_wall_down_texture()", color=(0,1,0))
                        applied = True
                    elif wall_type == 'floor' and hasattr(activity, '_apply_ground_texture'):
                        activity._apply_ground_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_ground_texture()", color=(0,1,0))
                        applied = True
                    
                    if not applied:
                        self._set_node_color_by_mesh_fixed(msg, client_id, mesh_keywords, target_name, r, g, b)
            else:
                self._set_node_color_by_mesh_fixed(msg, client_id, mesh_keywords, target_name, r, g, b)

        except Exception as e:
            self.clientmessage(f"❌ Error in color command: {str(e)[:50]}", color=(1,0,0))

    def _set_node_color_by_mesh_fixed(self, msg: str, client_id: int, mesh_keywords: list, 
                                      target_name: str, r: float, g: float, b: float):
        """الطريقة العامة لتغيير لون العقد – بدون حدود على القيم"""
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1,0,0))
                return

            found_mesh = 0
            found_colored = 0
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'mesh') and node.mesh:
                        mesh_str = str(node.mesh).lower()
                        for kw in mesh_keywords:
                            if kw.lower() in mesh_str:
                                found_mesh += 1
                                if hasattr(node, 'color'):
                                    node.color = (r, g, b)
                                    found_colored += 1
                                break
                except:
                    continue

            if found_colored > 0:
                self.clientmessage(f"✅ {target_name} color set via node.color - {found_colored} nodes (out of {found_mesh} matching)", color=(0,1,0))
            elif found_mesh > 0:
                self.clientmessage(f"⚠️ Found {found_mesh} matching meshes but none have 'color' attribute. Colors may not appear.", color=(1,1,0))
            else:
                self.clientmessage(f"⚠️ No {target_name} nodes found. Make sure you are on Soccer Stadium map.", color=(1,1,0))
        except Exception as e:
            self.clientmessage(f"❌ Error in node color: {str(e)[:50]}", color=(1,0,0))

    def _parse_rgb(self, msg: str, client_id: int):
        """تحليل قيم RGB – بدون حدود (محتفظ به للتوافق)"""
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage(f"❌ Use: {parts[0]} <r> <g> <b>", color=(1,0,0))
                return None
            r = float(parts[1])
            g = float(parts[2])
            b = float(parts[3])
            return (r, g, b)
        except:
            self.clientmessage("❌ Invalid RGB values. Must be numbers.", color=(1,0,0))
            return None

    def _update_asoccer_config(self, key: str, r: float, g: float, b: float):
        """تحديث ملف إعدادات A-Soccer بقيمة لون معينة"""
        try:
            if not os.path.exists(ASOCCER_CONFIG_DIR):
                os.makedirs(ASOCCER_CONFIG_DIR)
            
            config = {}
            if os.path.exists(ASOCCER_CONFIG_FILE):
                with open(ASOCCER_CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            
            config[key] = [r, g, b]
            
            with open(ASOCCER_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"✅ A-Soccer config updated: {key} = ({r},{g},{b})")
        except Exception as e:
            print(f"❌ Failed to update A-Soccer config: {e}")

    def process_weather_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /weather <type>", color=(1,0,0))
                self.clientmessage(f"🌦️ Types: {', '.join(Uts.weather_effect.valid_weather)}", color=(0.5,0.8,1))
                self.clientmessage("📝 Example: /weather snow  |  /weather none", color=(1,1,0))
                return

            wtype = parts[1].lower()
            if wtype not in Uts.weather_effect.valid_weather:
                self.clientmessage(f"❌ Invalid weather type. Use: {', '.join(Uts.weather_effect.valid_weather)}", color=(1,0,0))
                return

            # حفظ الإعداد دائمًا
            cfg['Commands']['Weather'] = wtype
            Uts.save_settings()

            activity = bs.get_foreground_host_activity()
            if activity is not None:
                # ✅ مهم جداً: تنفيذ start داخل سياق النشاط
                with activity.context:
                    Uts.weather_effect.start(wtype)
                self.clientmessage(f"✅ Weather changed to '{wtype}'", color=(0,1,0))
                if wtype != 'none':
                    Uts.cm(f"🌍 Server weather is now: {wtype}")
                else:
                    Uts.cm("🌍 Server weather disabled")
            else:
                self.clientmessage(f"✅ Weather saved as '{wtype}'. It will start when a game begins.", color=(0,1,0))

        except Exception as e:
            self.clientmessage(f"❌ Weather error: {str(e)[:50]}", color=(1,0,0))
    # ========== باقي الدوال (موجودة في الملف الأصلي – كاملة) ==========
    def process_advanced_customtag(self, msg: str, client_id: int):
        """إنشاء تاج مخصص مع كتابة حرف حرف"""
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
                            for acc_id, acc_data in Uts.pdata.items():
                                if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                    account_id = acc_id
                                    break
                            if account_id:
                                Uts.tag_system.remove_tag_visual(target_client_id)
                                Uts.tag_system.stop_char_animation(target_client_id)
                                Uts.tag_system.stop_animation(target_client_id)
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
        """إنشاء تاج متحرك بألوان متعددة"""
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
                            for acc_id, acc_data in Uts.pdata.items():
                                if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                    account_id = acc_id
                                    break
                            if account_id:
                                Uts.tag_system.remove_tag_visual(target_client_id)
                                Uts.tag_system.stop_char_animation(target_client_id)
                                Uts.tag_system.stop_animation(target_client_id)
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
        """إزالة التاج من لاعب"""
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
                        for acc_id, acc_data in Uts.pdata.items():
                            if target_client_id in Uts.userpbs and Uts.userpbs[target_client_id] == acc_id:
                                account_id = acc_id
                                break
                        break
                if target_player and account_id:
                    if str(target_client_id) in Uts.tag_system.current_tags:
                        Uts.tag_system.remove_tag_visual(target_client_id)
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
        """حفظ تاج كقالب"""
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
        """تطبيق قالب تاج على لاعب"""
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
        """عرض قوالب التاج المحفوظة"""
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
        """عرض الحسابات المشتركة"""
        try:
            if client_id not in Uts.userpbs:
                self.clientmessage("❌ You are not in the userpbs list", color=(1,0,0))
                return
            account_id = Uts.userpbs[client_id]
            shared_players = []
            for cid, acc_id in list(Uts.userpbs.items()):
                if acc_id == account_id and cid != client_id:
                    shared_players.append(cid)
            if shared_players:
                self.clientmessage(f"👥 You share account with {len(shared_players)} other player(s)", color=(0,0,1))
                for cid in shared_players:
                    name = Uts.usernames.get(cid, f"Player {cid}")
                    self.clientmessage(f"   ↳ {name} (Client ID: {cid})", color=(0.5,0.5,1))
                if account_id in Uts.pdata and 'Tag' in Uts.pdata[account_id]:
                    self.clientmessage("🎯 Applying same tag to all shared account players", color=(1,1,0))
            else:
                self.clientmessage("👤 You are the only player with this account", color=(0,0,1))
        except Exception as e:
            print(f"❌ Error processing shared accounts: {e}")
            self.clientmessage("❌ Error processing shared accounts", color=(1,0,0))

    def process_close_server(self, msg: str, client_id: int):
        """إغلاق السيرفر للتدريب"""
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
            if Uts.server_close_active:
                self.clientmessage("Server is already closed", color=(1, 1, 0))
                return
            if Uts.start_server_closure(hours, tag_name, client_id):
                self.clientmessage(f"✅ Server closed for {hours} hours for tag '{tag_name}'", color=(0, 1, 0))
                Uts.cm(f"Server closed for {hours} hours for '{tag_name}' tag training")
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_stop_close_server(self, client_id: int):
        """إيقاف إغلاق السيرفر"""
        try:
            if not Uts.server_close_active:
                self.clientmessage("No server closure active", color=(1, 1, 0))
                return
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
            status_msg = f"📊 Server Status: Closed\n⏰ Remaining: {hours}:{minutes:02d}:{seconds:02d}\n🏷️ Allowed Tag: {Uts.server_close_tag_name}\n👑 Allowed: Admins, Owners, Players with tag"
            self.clientmessage(status_msg, color=(1, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

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

    def process_teleport_command(self, msg: str, client_id: int):
        """نقل لاعب إلى إحداثيات"""
        try:
            parts = msg.split()
            if len(parts) < 5:
                self.clientmessage("❌ Use: /teleport <x> <y> <z> <client-id>", color=(1,0,0))
                self.clientmessage("📝 Example: /teleport 0 5 0 -1", color=(1,1,0))
                return
            try:
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                target_id = int(parts[4])
            except ValueError:
                self.clientmessage("❌ Coordinates must be numbers, client ID must be integer", color=(1,0,0))
                return
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1,0,0))
                return
            target_actor = None
            target_player_name = None
            for player in activity.players:
                try:
                    if player.sessionplayer.inputdevice.client_id == target_id:
                        target_actor = player.actor
                        target_player_name = player.getname()
                        break
                except:
                    continue
            if not target_actor:
                self.clientmessage(f"❌ Player with client ID {target_id} not found", color=(1,0,0))
                return
            if not target_actor.node or not target_actor.node.exists():
                self.clientmessage(f"❌ Player {target_player_name or target_id} is not active", color=(1,0,0))
                return
            with activity.context:
                try:
                    target_actor.node.handlemessage(bs.StandMessage(position=(x, y, z)))
                    self.clientmessage(f"✅ Teleported {target_player_name} to ({x}, {y}, {z})", color=(0,1,0))
                except Exception as e:
                    self.clientmessage(f"❌ Teleport failed: {str(e)[:50]}", color=(1,0,0))
                    print(f"❌ Teleport error details: {e}")
        except Exception as e:
            self.clientmessage(f"❌ Teleport error: {str(e)[:50]}", color=(1,0,0))

    def process_fly_command_fixed(self, msg: str, client_id: int):
        """تفعيل/تعطيل الطيران"""
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /fly <client-id>", color=(1,0,0))
                self.clientmessage("📝 Example: /fly -1", color=(1,1,0))
                return
            try:
                target_id = int(parts[1])
            except ValueError:
                self.clientmessage("❌ Client ID must be an integer", color=(1,0,0))
                return
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1,0,0))
                return
            target_player = None
            target_actor = None
            for player in activity.players:
                try:
                    if player.sessionplayer.inputdevice.client_id == target_id:
                        target_player = player
                        target_actor = player.actor
                        break
                except:
                    continue
            if not target_actor or not target_actor.node or not target_actor.node.exists():
                self.clientmessage(f"❌ Player with client ID {target_id} not found or not alive", color=(1,0,0))
                return
            with activity.context:
                if getattr(target_actor, 'cm_fly', False):
                    target_actor.cm_fly = False
                    status = "disabled"
                else:
                    target_actor.cm_fly = True
                    status = "enabled"
                name = target_player.getname() if target_player else f"Player {target_id}"
                self.clientmessage(f"✈️ Fly mode {status} for {name}", color=(0,1,0))
        except Exception as e:
            self.clientmessage(f"❌ Fly command error: {str(e)[:50]}", color=(1,0,0))

    def process_warn_command(self, msg: str, client_id: int):
        """تحذير لاعب"""
        try:
            self.util.update_usernames()
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage("❌ Use: /warn <client-id> <reason>", color=(1,0,0))
                self.clientmessage("📝 Example: /warn 113 Spamming", color=(1,1,0))
                return
            target_str = parts[1]
            reason = " ".join(parts[2:])
            target_data = self.find_target_data(target_str)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target_str]), color=(1,0,0))
                return
            target_account_id = target_data.get('account_id')
            target_name = target_data.get('name', target_str)
            target_client_id = target_data.get('client_id')
            if not target_account_id:
                self.clientmessage("❌ Cannot warn player without PB-ID", color=(1,0,0))
                return
            if target_account_id in self.util.pdata:
                if self.util.pdata[target_account_id].get('Admin', False) or self.util.pdata[target_account_id].get('Owner', False):
                    self.clientmessage(f"❌ Cannot warn admin/owner {target_name}", color=(1,0,0))
                    return
            warner_name = self.util.usernames.get(client_id, "Unknown")
            warner_account = self.util.userpbs.get(client_id, "Unknown")
            warn_count = self.util.add_warning(target_account_id, warner_name, warner_account, reason)
            self.clientmessage(f"⚠️ Warned {target_name} (total warnings: {warn_count})", color=(0,1,0))
            self.util.cm(f"⚠️ {target_name} was warned by {warner_name} for: {reason}")
            if target_client_id and target_client_id != -1:
                try:
                    self.util.sm(f"⚠️ You received a warning from {warner_name}\nReason: {reason}", 
                                 color=(1,1,0), clients=[target_client_id])
                except:
                    pass
        except Exception as e:
            self.clientmessage(f"❌ Warn error: {str(e)[:50]}", color=(1,0,0))

    def process_warns_command(self, msg: str, client_id: int):
        """عرض التحذيرات"""
        try:
            self.util.update_usernames()
            parts = msg.split()
            target_account_id = None
            target_name = None
            is_admin = self.fct.user_is_admin(client_id)
            if len(parts) == 1:
                target_account_id = self.util.userpbs.get(client_id)
                target_name = self.util.usernames.get(client_id, f"Player {client_id}")
                if not target_account_id:
                    self.clientmessage("❌ You don't have a PB-ID linked", color=(1,0,0))
                    return
            else:
                if not is_admin:
                    self.clientmessage(getlanguage("AdminOnly"), color=(1,0,0))
                    return
                target_str = parts[1]
                target_data = self.find_target_data(target_str)
                if not target_data:
                    self.clientmessage(getlanguage("TargetNotFound", subs=[target_str]), color=(1,0,0))
                    return
                target_account_id = target_data.get('account_id')
                target_name = target_data.get('name', target_str)
                if not target_account_id:
                    self.clientmessage("❌ Player has no PB-ID", color=(1,0,0))
                    return
            warnings = self.util.get_warnings(target_account_id)
            if not warnings:
                self.clientmessage(f"📋 No warnings for {target_name}", color=(0.5,0.5,1))
                return
            self.send_chat_message(f"==========[ WARNINGS for {target_name} ]==========")
            for i, w in enumerate(warnings, 1):
                self.send_chat_message(f"{i}. Date: {w.get('date', 'Unknown')}")
                self.send_chat_message(f"   Warner: {w.get('warner_name', 'Unknown')}")
                self.send_chat_message(f"   Reason: {w.get('reason', 'No reason')}")
            self.send_chat_message(f"Total: {len(warnings)} warnings")
        except Exception as e:
            self.clientmessage(f"❌ Warns error: {str(e)[:50]}", color=(1,0,0))

    def process_clearwarns_command(self, msg: str, client_id: int):
        """مسح التحذيرات"""
        try:
            if not self.fct.user_is_admin(client_id):
                self.clientmessage(getlanguage("AdminOnly"), color=(1,0,0))
                return
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /clearwarns <client-id>", color=(1,0,0))
                return
            target_str = parts[1]
            target_data = self.find_target_data(target_str)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target_str]), color=(1,0,0))
                return
            target_account_id = target_data.get('account_id')
            target_name = target_data.get('name', target_str)
            if not target_account_id:
                self.clientmessage("❌ Player has no PB-ID", color=(1,0,0))
                return
            if self.util.clear_warnings(target_account_id):
                self.clientmessage(f"✅ Cleared all warnings for {target_name}", color=(0,1,0))
                self.util.cm(f"🧹 Admin {self.util.usernames.get(client_id, 'Admin')} cleared warnings for {target_name}")
            else:
                self.clientmessage(f"📋 No warnings found for {target_name}", color=(0.5,0.5,1))
        except Exception as e:
            self.clientmessage(f"❌ Clearwarns error: {str(e)[:50]}", color=(1,0,0))

    def process_ban_command(self, msg: str, client_id: int):
        """حظر لاعب"""
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage(getlanguage("BanUsage"), color=(1,0,0))
                self.clientmessage("📝 أمثلة:", color=(1,1,0))
                self.clientmessage("   /ban 113 السبب  (حظر باستخدام client ID)", color=(1,1,0))
                self.clientmessage("   /ban pb-XXX السبب  (حظر باستخدام PB-ID)", color=(1,1,0))
                self.clientmessage("   /ban الاسم السبب  (حظر باستخدام الاسم)", color=(1,1,0))
                return
            target = parts[1]
            reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
            admin_name = Uts.usernames.get(client_id, "Admin")
            admin_account = Uts.userpbs.get(client_id, "Unknown")
            print(f"🔨 Ban command by {admin_name} ({client_id}) on target: {target}, reason: {reason}")
            ban_data = self.find_target_data(target)
            if not ban_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1,0,0))
                print(f"❌ Target not found: {target}")
                return
            target_account_id = ban_data.get('account_id')
            target_name = ban_data.get('name', target)
            target_client_id = ban_data.get('client_id')
            target_type = ban_data.get('type', 'unknown')
            print(f"✅ Target found: {target_name} (Client ID: {target_client_id}, PB-ID: {target_account_id}, Type: {target_type})")
            if not target_account_id:
                self.clientmessage("❌ Cannot ban without a valid PB-ID (account ID).", color=(1,0,0))
                self.clientmessage("💡 Use /list to see player PB-IDs.", color=(1,1,0))
                return
            if target_type == 'all':
                self.clientmessage("⚠️ لا يمكنك حظر جميع اللاعبين! استخدم /kick all", color=(1,0,0))
                return
            if target_client_id == client_id:
                self.clientmessage("❌ لا يمكنك حظر نفسك!", color=(1,0,0))
                return
            already_banned = False
            ban_key = None
            if target_account_id:
                for key in Uts.bans_data:
                    ban_info = Uts.bans_data[key]
                    if ban_info.get('account_id') == target_account_id:
                        already_banned = True
                        ban_key = key
                        break
            if already_banned:
                self.clientmessage(getlanguage("AlreadyBanned", subs=[target_name]), color=(1,1,0))
                print(f"⚠️ Player already banned: {target_name}")
                return
            is_admin_or_owner = False
            if target_account_id and target_account_id in Uts.pdata:
                player_data = Uts.pdata[target_account_id]
                if player_data.get('Admin', False) or player_data.get('Owner', False):
                    is_admin_or_owner = True
            elif target_client_id in Uts.accounts:
                if Uts.accounts[target_client_id].get('Admin', False) or Uts.accounts[target_client_id].get('Owner', False):
                    is_admin_or_owner = True
            if is_admin_or_owner:
                self.clientmessage(getlanguage("CannotBanAdmin", subs=[target_name]), color=(1,0,0))
                print(f"❌ Cannot ban admin/owner: {target_name}")
                return
            ban_info = {
                'name': target_name,
                'account_id': target_account_id,
                'client_id': target_client_id,
                'reason': reason,
                'banned_by': admin_name,
                'banned_by_account': admin_account,
                'banned_by_client_id': client_id,
                'banned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'banned_timestamp': time.time(),
                'target_type': target_type
            }
            if target_account_id:
                ban_key = f"pb_{target_account_id}"
            elif target_client_id:
                ban_key = f"client_{target_client_id}"
            else:
                ban_key = f"name_{target_name.replace(' ', '_')}"
            Uts.bans_data[ban_key] = ban_info
            Uts.save_bans_data()
            print(f"✅ Ban saved for {target_name} | Key: {ban_key}")
            print(f"   Account: {target_account_id} | Client: {target_client_id}")
            print(f"   Reason: {reason}")
            print(f"   By: {admin_name}")
            if target_client_id and target_client_id != -1 and target_client_id != -999:
                try:
                    message = getlanguage("BannedMessage", subs=[reason, admin_name])
                    Uts.sm(message, color=(1,0,0), clients=[target_client_id], transient=True)
                    def kick_player():
                        try:
                            bs.disconnect_client(target_client_id)
                            print(f"✅ Kicked banned player: {target_name} (Client ID: {target_client_id})")
                        except Exception as e:
                            print(f"❌ Error kicking player: {e}")
                    bs.apptimer(2.0, kick_player)
                    ban_msg = getlanguage("BanSuccess", subs=[target_name, admin_name])
                    Uts.cm(ban_msg)
                except Exception as e:
                    print(f"❌ Error in kick process: {e}")
            self.clientmessage(f"✅ تم حظر {target_name} بنجاح", color=(0,1,0))
            self.clientmessage(f"📝 السبب: {reason}", color=(0.5,0.5,1))
        except Exception as e:
            print(f"❌ Error in process_ban_command: {e}")
            self.clientmessage(f"❌ خطأ: {str(e)[:50]}", color=(1,0,0))

    def process_unban_command(self, msg: str, client_id: int):
        """إلغاء حظر لاعب"""
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage(getlanguage("UnbanUsage"), color=(1,0,0))
                self.clientmessage("📝 أمثلة:", color=(1,1,0))
                self.clientmessage("   /unban 113  (إلغاء حظر باستخدام client ID)", color=(1,1,0))
                self.clientmessage("   /unban pb-XXX  (إلغاء حظر باستخدام PB-ID)", color=(1,1,0))
                self.clientmessage("   /unban الاسم  (إلغاء حظر باستخدام الاسم)", color=(1,1,0))
                return
            target = parts[1]
            print(f"🔓 Unban command on target: {target}")
            found_ban_keys = []
            for ban_key, ban_info in list(Uts.bans_data.items()):
                if ban_info.get('account_id') == target:
                    found_ban_keys.append(ban_key)
                elif str(ban_info.get('client_id')) == target:
                    found_ban_keys.append(ban_key)
                elif ban_info.get('name', '').lower() == target.lower():
                    found_ban_keys.append(ban_key)
                elif ban_key == target or ban_key.endswith(f"_{target}"):
                    found_ban_keys.append(ban_key)
            if not found_ban_keys:
                self.clientmessage(getlanguage("NotBanned", subs=[target]), color=(1,0,0))
                print(f"❌ No ban found for: {target}")
                return
            unbanned_names = []
            for ban_key in found_ban_keys:
                if ban_key in Uts.bans_data:
                    ban_info = Uts.bans_data[ban_key]
                    unbanned_names.append(ban_info.get('name', 'Unknown'))
                    del Uts.bans_data[ban_key]
                    print(f"✅ Removed ban: {ban_key}")
            if unbanned_names:
                Uts.save_bans_data()
                admin_name = Uts.usernames.get(client_id, "Admin")
                names_str = ", ".join(unbanned_names)
                self.clientmessage(f"✅ تم إلغاء حظر: {names_str}", color=(0,1,0))
                self.util.cm(getlanguage("UnbanSuccess", subs=[names_str, admin_name]))
                print(f"✅ Unbanned: {names_str}")
            else:
                self.clientmessage(getlanguage("NotBanned", subs=[target]), color=(1,0,0))
        except Exception as e:
            print(f"❌ Error in process_unban_command: {e}")
            self.clientmessage(f"❌ خطأ: {str(e)[:50]}", color=(1,0,0))

    def process_report_command(self, msg: str, client_id: int):
        """الإبلاغ عن لاعب"""
        try:
            self.util.update_usernames()
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage(getlanguage("ReportUsage"), color=(1,0,0))
                self.clientmessage("📝 Example: /report 113 Hacking", color=(1,1,0))
                return
            target = parts[1]
            reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
            reporter_name = Uts.usernames.get(client_id, "Unknown")
            reporter_account = Uts.userpbs.get(client_id, None)
            if reporter_account is None:
                try:
                    activity = bs.get_foreground_host_activity()
                    if activity:
                        for player in activity.players:
                            if player.sessionplayer.inputdevice.client_id == client_id:
                                reporter_account = player.sessionplayer.get_v1_account_id()
                                break
                except:
                    pass
            if reporter_account is None:
                reporter_account = "Unknown"
            server_name = cfg.get('Commands', {}).get('HostName', 'Unknown Server')
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1,0,0))
                return
            target_account_id = target_data.get('account_id')
            target_name = target_data.get('name', target)
            target_client_id = target_data.get('client_id')
            report = {
                'id': len(Uts.reports_data.get('reports', [])) + 1,
                'reporter_name': reporter_name,
                'reporter_account': reporter_account,
                'reported_name': target_name,
                'reported_account': target_account_id,
                'reported_client_id': target_client_id,
                'reason': reason,
                'status': 'Pending',
                'date': datetime.now().isoformat(),
                'time': datetime.now().strftime('%H:%M:%S'),
                'server_name': server_name
            }
            if 'reports' not in Uts.reports_data:
                Uts.reports_data['reports'] = []
            Uts.reports_data['reports'].append(report)
            Uts.save_reports_data()
            self.clientmessage(getlanguage("ReportSubmitted", subs=[target_name]), color=(0,1,0))
            self.clientmessage(f"📋 Reason: {reason}", color=(0.5,0.5,1))
            for admin_id in Uts.get_admins():
                try:
                    Uts.sm(getlanguage("NewReportAlert", subs=[target_name, reporter_name]),
                                   clients=[admin_id], color=(1,1,0))
                except:
                    pass
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_reports_command(self, client_id: int):
        """عرض التقارير"""
        try:
            if not self.fct.user_is_admin(client_id):
                self.clientmessage(getlanguage("AdminOnly"), color=(1, 0, 0))
                return
            reports = Uts.reports_data.get('reports', [])
            if not reports:
                self.clientmessage(getlanguage("NoReports"), color=(0.5, 0.5, 1))
                return
            self.send_chat_message("=" * 120)
            self.send_chat_message("|| #  ||     Reporter (PB-ID)      ||  Time  ||         Server         ||   Reported (PB-ID + Name)   ||             Reason             ||")
            self.send_chat_message("=" * 120)
            for i, report in enumerate(reports[-10:], 1):
                reporter_id = str(report.get('reporter_account', 'Unknown'))[:25].ljust(25)
                report_time = report.get('time', '--:--:--')
                server = str(report.get('server_name', 'Unknown'))[:20].ljust(20)
                reported_id = str(report.get('reported_account', 'Unknown'))[:20]
                reported_name = report.get('reported_name', 'Unknown')[:20]
                reported = f"{reported_id} ({reported_name})"[:35].ljust(35)
                reason = report.get('reason', 'No reason')[:30].ljust(30)
                row = f"|| {i:<2} || {reporter_id} || {report_time} || {server} || {reported} || {reason} ||"
                self.send_chat_message(row)
            self.send_chat_message("=" * 120)
            self.send_chat_message(f"📊 إجمالي التقارير: {len(reports)} | عرض آخر 10 | استخدم /reportdone <رقم> لحذف تقرير")
        except Exception as e:
            print(f"❌ Error in process_reports_command: {e}")
            self.clientmessage(f"❌ خطأ في عرض التقارير: {str(e)[:50]}", color=(1, 0, 0))

    def process_report_done_command(self, msg: str, client_id: int):
        """حذف تقرير بعد معالجته"""
        try:
            if not self.fct.user_is_admin(client_id):
                self.clientmessage(getlanguage("AdminOnly"), color=(1, 0, 0))
                return
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /reportdone <report-number>", color=(1,0,0))
                self.clientmessage("📝 Example: /reportdone 3", color=(1,1,0))
                return
            try:
                report_id = int(parts[1])
            except ValueError:
                self.clientmessage("❌ Report number must be a number", color=(1,0,0))
                return
            reports = Uts.reports_data.get('reports', [])
            if not reports:
                self.clientmessage("📋 No reports to delete", color=(0.5,0.5,1))
                return
            found_index = None
            for i, report in enumerate(reports):
                if report.get('id') == report_id:
                    found_index = i
                    break
            if found_index is None:
                self.clientmessage(f"❌ Report #{report_id} not found", color=(1,0,0))
                return
            deleted_report = reports.pop(found_index)
            Uts.save_reports_data()
            reporter_name = deleted_report.get('reporter_name', 'Unknown')
            reported_name = deleted_report.get('reported_name', 'Unknown')
            reason = deleted_report.get('reason', 'No reason')
            self.clientmessage(f"✅ Report #{report_id} deleted", color=(0,1,0))
            self.util.cm(f"📋 Admin {Uts.usernames.get(client_id, 'Admin')} closed report #{report_id} ({reporter_name} reported {reported_name} for: {reason})")
        except Exception as e:
            print(f"❌ Error in process_report_done_command: {e}")
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1,0,0))

    def process_banlist_command(self, client_id: int):
        """عرض قائمة المحظورين"""
        try:
            if not self.fct.user_is_admin(client_id):
                self.clientmessage(getlanguage("AdminOnly"), color=(1, 0, 0))
                return
            if not Uts.bans_data:
                self.clientmessage(getlanguage("NoBans"), color=(0.5, 0.5, 1))
                return
            self.send_chat_message("=" * 60 + "[ BAN LIST ]" + "=" * 60)
            self.send_chat_message("||           PB-ID / Client ID          ||            Reason              ||       Banned By      ||")
            self.send_chat_message("=" * 120)
            bans_list = list(Uts.bans_data.items())
            for i, (ban_key, ban_data) in enumerate(bans_list[-10:], 1):
                identifier = ban_data.get('account_id') or f"Client_{ban_data.get('client_id')}" or ban_key
                identifier = str(identifier)[:30]
                reason = ban_data.get('reason', 'No reason')[:30]
                banned_by = ban_data.get('banned_by', 'Unknown')[:20]
                row = f"|| {i:<2} || {identifier:<35} || {reason:<25} || {banned_by:<18} ||"
                self.send_chat_message(row)
            self.send_chat_message("=" * 120)
            self.send_chat_message(f"🔨 إجمالي المحظورين: {len(Uts.bans_data)} | عرض آخر 10")
        except Exception as e:
            print(f"❌ Error in process_banlist_command: {e}")
            self.clientmessage(f"❌ خطأ في عرض قائمة الحظر: {str(e)[:50]}", color=(1, 0, 0))

    def find_target_data(self, target):
        """البحث عن لاعب باستخدام PB-ID أو Client ID أو الاسم"""
        try:
            if target.startswith('pb-') or '=' in target or (len(target) > 10 and '-' in target):
                print(f"🔍 Searching by PB-ID: {target}")
                for client_id, account_id in list(Uts.userpbs.items()):
                    if account_id == target:
                        name = Uts.usernames.get(client_id, f"Player {client_id}")
                        print(f"✅ Found player by PB-ID: {name} (Client ID: {client_id})")
                        return {
                            'client_id': client_id,
                            'account_id': account_id,
                            'name': name,
                            'type': 'pb_id'
                        }
                for r in roster():
                    account_id = r.get('account_id')
                    if account_id == target:
                        client_id = r.get('client_id')
                        name = r.get('display_string', f"Player {client_id}")
                        print(f"✅ Found in roster by PB-ID: {name} (Client ID: {client_id})")
                        return {
                            'client_id': client_id,
                            'account_id': account_id,
                            'name': name,
                            'type': 'pb_id'
                        }
            try:
                target_client_id = int(target)
                print(f"🔍 Searching by Client ID: {target_client_id}")
                if target_client_id in Uts.usernames:
                    name = Uts.usernames[target_client_id]
                    account_id = Uts.userpbs.get(target_client_id, None)
                    print(f"✅ Found player by Client ID: {name} (Account ID: {account_id})")
                    return {
                        'client_id': target_client_id,
                        'account_id': account_id,
                        'name': name,
                        'type': 'client_id'
                    }
                for r in roster():
                    client_id = r.get('client_id')
                    if client_id == target_client_id:
                        account_id = r.get('account_id')
                        name = r.get('display_string', f"Player {client_id}")
                        print(f"✅ Found in roster by Client ID: {name} (Account ID: {account_id})")
                        return {
                            'client_id': client_id,
                            'account_id': account_id,
                            'name': name,
                            'type': 'client_id'
                        }
            except ValueError:
                pass
            print(f"🔍 Searching by name: {target}")
            for client_id, name in list(Uts.usernames.items()):
                if name.lower() == target.lower():
                    account_id = Uts.userpbs.get(client_id, None)
                    print(f"✅ Found player by name in usernames: {name} (Client ID: {client_id}, Account ID: {account_id})")
                    return {
                        'client_id': client_id,
                        'account_id': account_id,
                        'name': name,
                        'type': 'name'
                    }
            for r in roster():
                display_name = r.get('display_string', '')
                if display_name.lower() == target.lower():
                    client_id = r.get('client_id')
                    account_id = r.get('account_id', None)
                    print(f"✅ Found in roster by name: {display_name} (Client ID: {client_id}, Account ID: {account_id})")
                    return {
                        'client_id': client_id,
                        'account_id': account_id,
                        'name': display_name,
                        'type': 'name'
                    }
            if target.lower() in ['all', 'الكل', 'كل', 'جميع']:
                print(f"🔍 Target is 'all'")
                return {
                    'client_id': -999,
                    'account_id': 'all',
                    'name': 'All Players',
                    'type': 'all'
                }
            print(f"❌ Target not found: {target}")
            return None
        except Exception as e:
            print(f"❌ Error in find_target_data: {e}")
            return None

    def process_help_command(self, msg: str, client_id: int):
        """قائمة المساعدة"""
        parts = msg.split()
        if len(parts) == 1:
            self.clientmessage("📚 **HELP MENU**", color=(0,1,1))
            self.send_chat_message("/help 1  -  Player commands (all players)", color=(1,1,0))
            self.send_chat_message("/help 2  -  Admin commands (admins only)")
            self.send_chat_message("/help 3  -  Tag commands (admins only)")
            self.send_chat_message("/help 4  -  Ban/Report commands")
            return
        if len(parts) >= 2:
            try:
                page = int(parts[1])
            except ValueError:
                self.clientmessage("❌ Invalid help page number", color=(1,0,0))
                return
            if page == 1:
                self.clientmessage("📋 **PLAYER COMMANDS**", color=(0,1,0))
                cmds = [
                    "-pan      : Receive a bread",
                    "-ceb      : Celebrate!",
                    "-colors   : Show available colors",
                    "-mp       : Show max players",
                    "-pb       : Show your PB-ID",
                    "-effects  : Show available effects",
                    "/list     : List all players",
                    "/report   : Report a player",
                    "test      : Test if CheatMax works",
                    "help      : This menu"
                ]
                for cmd in cmds:
                    self.send_chat_message(cmd)
            elif page == 2:
                if not self.fct.user_is_admin(client_id):
                    self.clientmessage(getlanguage("AdminOnly"), color=(1,0,0))
                    return
                self.clientmessage("🔧 **ADMIN COMMANDS**", color=(1,0.5,0))
                cmds = [
                    "/name <id> <name>     : Change player's name",
                    "/imp                 : Strong impulse",
                    "/box                 : Transform into box",
                    "/addAdmin <clientID> : Add admin",
                    "/delAdmin <clientID> : Remove admin",
                    "/kill <id>           : Kill player",
                    "-pause               : Pause/Resume game",
                    "/infoHost <text>     : Set host name",
                    "/infoDes <text>      : Set description",
                    "-info                : Toggle server info",
                    "/infoColor <color>   : Set info color",
                    "-end                 : End game",
                    "/kick <clientID>     : Kick player",
                    "-chatLive            : Toggle live chat",
                    "/freeze <id>         : Freeze player",
                    "/playerColor <id> <c>: Change player color",
                    "/maxPlayers <num>    : Set max players",
                    "-showMessages        : Toggle popup messages",
                    "/sleep <id>          : Sleep player",
                    "/mute <clientID>     : Mute player",
                    "/unmute <clientID>   : Unmute player",
                    "/gm <id>             : Toggle god mode",
                    "-slow                : Toggle slow motion",
                    "/speed <id>          : Toggle speed boost",
                    "/effect <id> <eff>   : Add effect",
                    "/punch <id>          : Super punch",
                    "/mbox <id>           : Spawn magic box",
                    "/drop <id>           : Drop bombs",
                    "/gift <id>           : Explosive gift",
                    "/curse <id>          : Curse",
                    "/superjump <id>      : Super jump (ground only)",
                    "/closeserver <h> <tag> : Close server for training",
                    "/stopcloseserver     : Stop server closure",
                    "/closestatus         : Show closure status",
                    "/teleport <x> <y> <z> <client-id> : Teleport player",
                    "/fly <client-id>     : Toggle flight mode",
                    "/warn <id> <reason>  : Warn a player",
                    "/warns [id]          : Show warnings",
                    "/clearwarns <id>     : Clear warnings",
                    "/invisible [id]      : Toggle invisibility",
                    "",
                    "🎨 **VISUAL COMMANDS (NO LIMITS)**",
                    "/tint <r> <g> <b>    : Change global tint",
                    "/upwall <r> <g> <b>  : Change upper wall color (Soccer Stadium) - saved",
                    "/downwall <r> <g> <b>: Change lower wall color (Soccer Stadium) - saved",
                    "/floor <r> <g> <b>   : Change floor color (Soccer Stadium) - saved",
                    "/spawnball [x y z]   : Spawn a soccer ball (hittable)",
                    "/explosion           : Massive explosion (kills all)",
                    "/locator <x,y,z> <color> <shape> : Place a glowing marker",
                    "/ping                : Show your ping",
                    "",
                    "🌦️ **WEATHER SYSTEM**",
                    "/weather <type>      : Set global weather (snow, rock, metal, ice, spark, slime, fire, splinter, smoke, rainbow, none)",
                ]
                for cmd in cmds:
                    self.send_chat_message(cmd)
            elif page == 3:
                if not self.fct.user_is_admin(client_id):
                    self.clientmessage(getlanguage("AdminOnly"), color=(1,0,0))
                    return
                self.clientmessage("🏷️ **TAG COMMANDS**", color=(0,1,1))
                cmds = [
                    "/customtag <text> <color> <scale> <id>  : Create custom tag",
                    "/animationtag <text> <scale> <speed> <id> <c1> <c2>... : Animated tag",
                    "/removetag <id>                         : Remove tag",
                    "/savetag <name> <text> <color> <scale>  : Save as template",
                    "/tagdata <name> <id>                    : Apply saved template",
                    "/listtags                               : List templates"
                ]
                for cmd in cmds:
                    self.send_chat_message(cmd)
            elif page == 4:
                if not self.fct.user_is_admin(client_id):
                    self.clientmessage("📢 **REPORT COMMANDS**", color=(1,0.5,0))
                    self.clientmessage("/report <pb-id/name/client> <reason>  : Report a player", color=(0.8,0.8,0.8))
                else:
                    self.clientmessage("🚫 **BAN / REPORT COMMANDS**", color=(1,0,0))
                    cmds = [
                        "/ban <pb-id/name/client> <reason>   : Ban player",
                        "/unban <pb-id/name/client>          : Unban player",
                        "/reports                            : View reports",
                        "/reportdone <id>                    : Delete processed report",
                        "/banlist                            : View banned players",
                        "/report <pb-id/name/client> <reason>  : Report a player"
                    ]
                    for cmd in cmds:
                        self.send_chat_message(cmd)
            else:
                self.clientmessage("❌ Invalid help page. Use 1-4", color=(1,0,0))

    def process_list_players(self):
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game found", color=(1,0,0))
                return
            self.util.update_usernames()
            players_data = []
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
                        players_list = r.get('players', [])
                        if players_list:
                            player_name = players_list[0].get('name_full', player_name)
                        role = "Player"
                        if client_id == -1:
                            role = "Owner"
                        elif account_id in self.util.pdata:
                            if self.util.pdata[account_id].get('Admin', False):
                                role = "Admin"
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
            players_data.sort(key=lambda x: x['client_id'])
            self.send_chat_message("=============================================[Players_list]==================================================")
            self.send_chat_message("||        PB-ID        ||    Role    ||  Account_name   ||        Name         || Client ID ||   Name Tag  ||")
            self.send_chat_message("=============================================================================================================")
            for data in players_data:
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
                row = f"|| {pb_id} || {role} || {account_name} || {player_name} || {client_id} || {tag} ||"
                self.send_chat_message(row)
            self.send_chat_message("==========================[Players_list]=============================")
            self.send_chat_message(f"👥 Total Players: {len(players_data)}")
            self.send_chat_message("👑 = Owner/Host | ⭐ = Admin | 👤 = Player")
        except Exception as e:
            print(f"❌ Error in process_list_players: {e}")
            self.clientmessage("❌ Error showing players list", color=(1,0,0))

class CommandFunctions:
    @staticmethod
    def all_cmd() -> list[str]:
        return [
            '-pan', '-ceb', '-colors', '-mp', '-pb', '-effects', 
            '/list', 'test', 'help', 'party', 'stats', '/report'
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
            '/closeserver', '/stopcloseserver', '/closestatus', '/testclosure',
            '/ban', '/unban', '/reports', '/banlist', '/reportdone',
            '/teleport', '/fly','/warn', '/warns', '/clearwarns', '/ride', '/invisible',
            '/tint', '/upwall', '/downwall', '/floor', '/spawnball', '/explosion', '/locator', '/ping',
            '/weather'   # ← تمت إضافة أمر الطقس هنا
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
    def spaz_visible(node: bs.Node) -> None:
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                node.torso_mesh = None
                node.head_mesh = None
                node.pelvis_mesh = None
                node.forearm_mesh = None
                node.color_texture = node.color_mask_texture = None
                node.color = None
                node.style = None

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
                bs.screenmessage(txt, clients=[c_id])
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
        bs.screenmessage(txt, clients=[c_id])
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
        if c_id == -1:
            return True
        if c_id in Uts.accounts:
            account_id = None
            for acc_id, data in Uts.pdata.items():
                if data.get('Owner', False):
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
        position = (-0.0, 1.5, 0.0)
        m = bs.newnode('math', owner=actor.node, attrs={'input1':
            (position[0], position[1], position[2]), 'operation': 'add'})
        actor.node.connectattr('position_center', m, 'input2')
        actor.my_message = popup = PopupText(
             text=msg, color=c, scale=1.5).autoretain()
        m.connectattr('output', popup.node, 'position')
        bs.timer(5.0, bs.CallStrict(die, popup.node))

# ------------------ Effects ------------------
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
                count=1,
                spread=0.08,
                scale=0.5,
                chunk_type='slime',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=1,
                spread=0.08,
                scale=0.5,
                chunk_type='slime',
                emit_type='stickers')
        bs.emitfx(position=self.node.position,
                count=1,
                spread=0.08,
                scale=0.5,
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

# ------------------ Chat filter ------------------
def filter_chat_message(msg: str, client_id: int) -> None:
    try:
        activity = bs.get_foreground_host_activity()
        if activity is None and msg.strip() != '':
            if msg.strip() in ['-pan', '-pb', '-mp', '-colors', '-effects']:
                try:
                    command = Commands(msg, client_id, msg.split(' '))
                    return command.get
                except:
                    return None
            return None
        command = Commands(msg, client_id, msg.split(' '))
        return command.get
    except Exception as e:
        print(f"⚠️ Error in filter_chat_message: {e}")
        import traceback
        traceback.print_exc()
        return None

# ------------------ Hooking (runtime monkey patch) ------------------
def hook_chat_filter():
    """تثبيت فلتر الشات بدون تعديل أي ملفات"""
    try:
        import bascenev1._hooks
        original = bascenev1._hooks.filter_chat_message
        def wrapped_filter(msg, client_id):
            # استدعاء الدالة الأصلية أولاً
            ret = original(msg, client_id)
            # ثم استدعاء فلترنا
            try:
                cm = bs.app.cheatmax_filter_chat(msg, client_id)
                if cm == '@':
                    return None
            except:
                pass
            return ret
        bascenev1._hooks.filter_chat_message = wrapped_filter
        print("✅ Chat filter hooked successfully (runtime)")
    except Exception as e:
        print(f"⚠️ Failed to hook chat filter: {e}")

# ------------------ Game Activity hooks ------------------
def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)
    # إعادة تطبيق الطقس المحفوظ عند بدء نشاط جديد
    weather_type = cfg.get('Commands', {}).get('Weather', 'none')
    Uts.weather_effect.start(weather_type)

def new_on_player_join(self, player: bs.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    if Uts.check_player_ban_on_join(player):
        return
    Uts.player_join(player)
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
    if user and user in Uts.tags:
        tag_data = Uts.tags[user]
        text = tag_data.get('text', '')
        color = tag_data.get('color', (1, 1, 1))
        scale = tag_data.get('scale', 0.02)
        current_act = bs.get_foreground_host_activity()
        if current_act is not None:
            with current_act.context:
                bs.timer(0.5, lambda: create_custom_tag_for_spaz(self, text, color, scale))

def create_custom_tag_for_spaz(spaz, text, color, scale):
    if not spaz.node or not spaz.node.exists():
        return
    if hasattr(spaz.node, 'custom_tag') and spaz.node.custom_tag:
        if spaz.node.custom_tag.exists():
            spaz.node.custom_tag.delete()
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
    spaz.node.connectattr('position_center', tag, 'position')
    spaz.node.custom_tag = tag
            
def new_playerspaz_on_jump_press(self) -> None:
    calls['OnJumpPress'](self)

    # --- Super Jump (فقط على الأرض) ---
    if getattr(self, 'cm_superjump', False):
        if self.node and self.node.is_on_ground:
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                with current_act.context:
                    msg = bs.HitMessage(pos=self.node.position,
                                        velocity=self.node.velocity,
                                        magnitude=160*2,
                                        hit_subtype='imp',
                                        radius=460*2)
                    if isinstance(msg, bs.HitMessage):
                        for i in range(2):
                            self.node.handlemessage(
                                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                                msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                                msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                                msg.force_direction[1], msg.force_direction[2])

    # --- Fly Mode – طيران باتجاه الكاميرا + الجويستيك ---
    if getattr(self, 'cm_fly', False):
        if self.node and self.node.exists():
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                # محاولة الحصول على الكاميرا
                camera = getattr(current_act, 'camera', None)
                if camera and camera.exists():
                    # الحصول على موضع وهدف الكاميرا
                    cam_pos = camera.position
                    cam_target = camera.target
                else:
                    # إذا لم توجد كاميرا، نستخدم اتجاه افتراضي (Z+)
                    cam_pos = (0, 0, -10)
                    cam_target = (0, 0, 0)

                with current_act.context:
                    # 1. حساب المتجه الأمامي (في المستوى الأفقي)
                    forward = (cam_target[0] - cam_pos[0], 0, cam_target[2] - cam_pos[2])
                    flen = (forward[0]**2 + forward[2]**2)**0.5
                    if flen > 0:
                        forward = (forward[0]/flen, 0, forward[2]/flen)
                    else:
                        forward = (0, 0, 1)  # افتراضي

                    # 2. المتجه الأيمن (عمودي على forward و up)
                    right = (-forward[2], 0, forward[0])

                    # 3. قراءة مدخلات الجويستيك
                    lr = self.node.move_left_right   # -1 .. 1
                    ud = self.node.move_up_down      # -1 .. 1

                    # 4. حساب سرعة الدفع في الاتجاهات الأفقية (قوة 80)
                    fx = (right[0] * lr + forward[0] * ud) * 80
                    fz = (right[2] * lr + forward[2] * ud) * 80

                    # 5. الدفع الرأسي – قوي جداً (150)
                    fy = 150

                    # 6. إرسال رسالة impulse
                    self.node.handlemessage(
                        'impulse',
                        self.node.position[0], self.node.position[1], self.node.position[2],
                        fx, fy, fz,
                        (fx**2 + fy**2 + fz**2)**0.5,  # magnitude
                        0, 0, 0,
                        0, 1, 0
                    )

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
    tags: dict[str, dict] = {}
    tag_system = None
    
    # نظام الطقس
    weather_effect = WeatherEffect()
    
    # متغيرات إغلاق السيرفر
    server_close_active = False
    server_close_end_time = 0.0
    server_close_tag_name = ""
    server_close_countdown_text = None
    server_close_original_players = []
    server_close_last_update = 0.0
    
    # بيانات الحظر والإبلاغات
    bans_data = {}
    reports_data = {"reports": []}
    # بيانات التحذيرات
    warns_data = {}

    @staticmethod
    def create_bans_data():
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxBansData.json'
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')
        try:
            with open(file) as f:
                r = f.read()
                if r.strip():
                    Uts.bans_data = json.loads(r)
                else:
                    Uts.bans_data = {}
            print(f"✅ Bans data loaded: {len(Uts.bans_data)} bans")
            for k, v in Uts.bans_data.items():
                print(f"   - {k}: {v.get('account_id')} | {v.get('client_id')} | {v.get('name')}")
        except Exception as e:
            print(f"⚠️ Error loading bans data: {e}")
            Uts.bans_data = {}
    
    @staticmethod
    def save_bans_data():
        try:
            folder = Uts.directory_user + '/Configs'
            file = folder + '/CheatMaxBansData.json'
            with open(file, 'w') as f:
                w = json.dumps(Uts.bans_data, indent=4)
                f.write(w)
            print(f"✅ Bans data saved: {len(Uts.bans_data)} bans")
        except Exception as e:
            print(f"❌ Error saving bans data: {e}")
    
    @staticmethod
    def create_reports_data():
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxReportsData.json'
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{"reports": []}')
        try:
            with open(file) as f:
                r = f.read()
                if r.strip():
                    Uts.reports_data = json.loads(r)
                else:
                    Uts.reports_data = {"reports": []}
        except:
            Uts.reports_data = {"reports": []}
    
    @staticmethod
    def save_reports_data():
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxReportsData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.reports_data, indent=4)
            f.write(w)

    # ✅ FIX: Ban enforcement – only by PB-ID (account_id), client_id check removed
    @staticmethod
    def check_player_ban_on_join(player: bs.Player) -> bool:
        try:
            sessionplayer = player.sessionplayer
            client_id = sessionplayer.inputdevice.client_id
            if client_id == -1:
                print("👑 Host is joining - skip ban check.")
                return False

            account_id = None
            try:
                account_id = sessionplayer.get_v1_account_id()
            except:
                if client_id in Uts.userpbs:
                    account_id = Uts.userpbs[client_id]

            player_name = None
            try:
                player_name = sessionplayer.getname(full=True)
            except:
                if client_id in Uts.usernames:
                    player_name = Uts.usernames[client_id]

            print(f"🔍 Checking ban for: {player_name} (Client: {client_id}, PB-ID: {account_id})")
            Uts.create_bans_data()

            # ✅ ONLY check by account_id (pb‑ID) – client_id check removed
            if account_id:
                for ban_key, ban_info in Uts.bans_data.items():
                    if ban_info.get('account_id') == account_id:
                        print(f"🚫 Ban match (PB-ID): {ban_key}")
                        Uts.kick_banned_player(client_id, ban_info)
                        return True

            # Optional: still check by exact name match (only if no account_id)
            if player_name and not account_id:
                player_name_lower = player_name.lower()
                for ban_key, ban_info in Uts.bans_data.items():
                    banned_name = ban_info.get('name', '').lower()
                    if banned_name and banned_name == player_name_lower:
                        print(f"🚫 Ban match (Name – no PB-ID): {ban_key}")
                        Uts.kick_banned_player(client_id, ban_info)
                        return True

            print(f"✅ Player is not banned: {player_name}")
            return False
        except Exception as e:
            print(f"❌ Error in check_player_ban_on_join: {e}")
            return False
    
    @staticmethod
    def kick_banned_player(client_id: int, ban_data: dict):
        try:
            reason = ban_data.get('reason', 'No reason provided')
            banned_by = ban_data.get('banned_by', 'Admin')
            player_name = ban_data.get('name', f'Player {client_id}')
            message = getlanguage("BannedMessage", subs=[reason, banned_by])
            # إضافة transient=True لإرسال الرسالة لعميل محدد
            Uts.sm(message, color=(1,0,0), clients=[client_id], transient=True)
            def kick():
                try:
                    bs.disconnect_client(client_id)
                    print(f"✅ Kicked banned player: {player_name} (Client: {client_id})")
                except Exception as e:
                    print(f"❌ Error kicking player {client_id}: {e}")
            bs.apptimer(2.0, lambda: bs.pushcall(kick))
        except Exception as e:
            print(f"❌ Error in kick_banned_player: {e}")

    @staticmethod
    def start_server_closure(hours: float, tag_name: str, admin_client_id: int) -> bool:
        try:
            current_time = time.time()
            if Uts.server_close_active:
                return False
            Uts.server_close_active = True
            Uts.server_close_end_time = current_time + (hours * 3600)
            Uts.server_close_tag_name = tag_name
            Uts.server_close_original_players = []
            Uts.server_close_last_update = current_time
            print(f"✅ Server closure started at {current_time}. End time: {Uts.server_close_end_time} for tag: {tag_name}")
            activity = bs.get_foreground_host_activity()
            if activity:
                for player in activity.players:
                    try:
                        client_id = player.sessionplayer.inputdevice.client_id
                        Uts.server_close_original_players.append(client_id)
                    except:
                        continue
            Uts.start_close_server_countdown()
            Uts.cm(f"Server closed for {hours} hours for '{tag_name}' tag training")
            return True
        except Exception as e:
            print(f"❌ Error starting server closure: {e}")
            return False

    @staticmethod
    def create_warns_data():
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxWarnsData.json'
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')
        try:
            with open(file) as f:
                r = f.read()
                if r.strip():
                    Uts.warns_data = json.loads(r)
                else:
                    Uts.warns_data = {}
            print(f"✅ Warns data loaded: {sum(len(v) for v in Uts.warns_data.values())} warnings")
        except Exception as e:
            print(f"⚠️ Error loading warns data: {e}")
            Uts.warns_data = {}

    @staticmethod
    def save_warns_data():
        try:
            folder = Uts.directory_user + '/Configs'
            file = folder + '/CheatMaxWarnsData.json'
            with open(file, 'w') as f:
                w = json.dumps(Uts.warns_data, indent=4)
                f.write(w)
        except Exception as e:
            print(f"❌ Error saving warns data: {e}")

    @staticmethod
    def add_warning(account_id: str, warner_name: str, warner_account: str, reason: str):
        """إضافة تحذير لحساب معين"""
        if account_id not in Uts.warns_data:
            Uts.warns_data[account_id] = []
        warning = {
            'warner_name': warner_name,
            'warner_account': warner_account,
            'reason': reason,
            'timestamp': time.time(),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        Uts.warns_data[account_id].append(warning)
        Uts.save_warns_data()
        return len(Uts.warns_data[account_id])  # عدد التحذيرات بعد الإضافة

    @staticmethod
    def get_warnings(account_id: str):
        """استرجاع قائمة التحذيرات لحساب"""
        return Uts.warns_data.get(account_id, [])

    @staticmethod
    def clear_warnings(account_id: str):
        """مسح كل التحذيرات لحساب"""
        if account_id in Uts.warns_data:
            del Uts.warns_data[account_id]
            Uts.save_warns_data()
            return True
        return False

    @staticmethod
    def is_player_allowed_during_closure(client_id: int, tag_name: str) -> bool:
        try:
            if client_id == -1 or CommandFunctions.user_is_admin(client_id):
                return True
            player_name = Uts.usernames.get(client_id, None)
            if not player_name:
                for r in roster():
                    if r['client_id'] == client_id:
                        player_name = r['display_string']
                        break
            if not player_name:
                return False
            account_id = None
            for acc_id, acc_data in Uts.pdata.items():
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
                    if player_tag == required_tag:
                        return True
            if client_id in Uts.server_close_original_players:
                return True
            return False
        except Exception as e:
            print(f"❌ Error checking player allowance: {e}")
            return False
    
    @staticmethod
    def start_close_server_countdown():
        try:
            def update_countdown():
                try:
                    if not Uts.server_close_active:
                        if Uts.server_close_countdown_text and Uts.server_close_countdown_text.exists():
                            Uts.server_close_countdown_text.delete()
                            Uts.server_close_countdown_text = None
                        return
                    activity = bs.get_foreground_host_activity()
                    if not activity:
                        bs.apptimer(1.0, update_countdown)
                        return
                    current_time = time.time()
                    remaining_time = Uts.server_close_end_time - current_time
                    if remaining_time <= 0:
                        Uts.stop_server_closure()
                        Uts.cm("✅ Server closure ended. Everyone can join now.")
                        return
                    hours = int(remaining_time // 3600)
                    minutes = int((remaining_time % 3600) // 60)
                    seconds = int(remaining_time % 60)
                    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    if hasattr(activity, 'context'):
                        with activity.context:
                            if Uts.server_close_countdown_text is None or not Uts.server_close_countdown_text.exists():
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
                                try:
                                    Uts.server_close_countdown_text.node.text = f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}"
                                except:
                                    Uts.server_close_countdown_text = text.Text(
                                        f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}",
                                        position=(0, 250),
                                        scale=1.0,
                                        color=(1, 0, 0),
                                        h_align=text.Text.HAlign.CENTER,
                                        v_align=text.Text.VAlign.CENTER
                                    )
                                    Uts.server_close_countdown_text.node.opacity = 0.7
                    bs.apptimer(1.0, update_countdown)
                except Exception as e:
                    print(f"❌ Error in countdown update: {e}")
                    bs.apptimer(2.0, update_countdown)
            bs.apptimer(0.5, update_countdown)
            print(f"✅ Countdown started for server closure")
        except Exception as e:
            print(f"❌ Error starting countdown: {e}")
    
    @staticmethod
    def stop_server_closure():
        try:
            Uts.server_close_active = False
            Uts.server_close_end_time = 0.0
            Uts.server_close_tag_name = ""
            Uts.server_close_original_players = []
            if Uts.server_close_countdown_text and Uts.server_close_countdown_text.exists():
                Uts.server_close_countdown_text.delete()
                Uts.server_close_countdown_text = None
            print("✅ Server closure stopped.")
        except Exception as e:
            print(f"❌ Error stopping server closure: {e}")
    
    @staticmethod
    def check_player_allowed_on_join(player: bs.Player):
        try:
            if not Uts.server_close_active:
                return
            client_id = player.sessionplayer.inputdevice.client_id
            if not Uts.is_player_allowed_during_closure(client_id, Uts.server_close_tag_name):
                current_time = time.time()
                remaining_time = Uts.server_close_end_time - current_time
                if remaining_time <= 0:
                    Uts.stop_server_closure()
                    return
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                seconds = int(remaining_time % 60)
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                message = f"There's a training match for {Uts.server_close_tag_name}. Please try to join again after {time_str}"
                Uts.sm(message, color=(1, 0, 0), clients=[client_id])
                def kick_player():
                    try:
                        bs.disconnect_client(client_id)
                    except:
                        pass
                bs.apptimer(2.0, kick_player)
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
        if not hasattr(Uts, 'pdata'): 
            Uts.create_players_data()
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'none',
                'Admin': True,
                'Owner': True,
                'Accounts': []
            }
        else:
            Uts.pdata[account_id]['Admin'] = True
            Uts.pdata[account_id]['Owner'] = True
        Uts.save_players_data()
        print(f"Added owner: {account_id}")

    @staticmethod
    def create_players_data() -> None:
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
        # إضافة إعداد الطقس الافتراضي
        if 'Commands' not in cfg:
            cfg['Commands'] = {}
        if 'Weather' not in cfg['Commands']:
            cfg['Commands']['Weather'] = 'none'
            Uts.save_settings()

    @staticmethod
    def create_user_system_scripts() -> None:
        import shutil
        app = _babase.app.env
        if app.python_directory_user is None:
            raise RuntimeError('user python dir unset')
        if app.python_directory_app is None:
            raise RuntimeError('app python dir unset')
        path = app.python_directory_user + '/sys/' + app.engine_version + '_' + str(_babase.app.env.engine_build_number)
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

## ==================== نظام التيجان المتطور ====================
class TagSystem:
    def __init__(self):
        self.current_tags = {}
        self.animated_tags = {}
        self.char_animations = {}
        self.animation_states = {}
        self.saved_tag_templates = {}
        self.icons = {
            'left': '\ue001', 'right': '\ue002', 'up': '\ue003', 'down': '\ue004',
            'dleft': '\ue005', 'dup': '\ue006', 'dright': '\ue007', 'ddown': '\ue008',
            'back': '\ue009', 'joystick': '\ue010', 'circles': '\ue019',
            'android': '\ue020', 'rbyp': '\ue021',
            'dice1': '\ue022', 'dice2': '\ue023', 'dice3': '\ue024', 'dice4': '\ue025',
            'volley': '\ue026', 'gather': '\ue027', 't': '\ue028', 'ticket': '\ue029',
            'pc': '\ue030', 'rbyp2': '\ue031',
            'us': '\ue032', 'italy': '\ue033', 'germany': '\ue034', 'brazil': '\ue035',
            'russia': '\ue036', 'china': '\ue037', 'uk': '\ue038', 'canada': '\ue039',
            'rwb': '\ue040', 'hat': '\ue041', 'fire': '\ue042', 'crown': '\ue043',
            'zen': '\ue044', 'eye': '\ue045', 'skull': '\ue046', 'heart': '\ue047',
            'dragon': '\ue048', 'helmet': '\ue049', 'rgwb': '\ue050', 'mw': '\ue051',
            'syria': '\ue052', 'bgwr': '\ue053', 'gwl': '\ue054', 'saudi': '\ue055',
            'malaysia': '\ue056', 'bwr': '\ue057', 'australia': '\ue058', 'rws': '\ue059',
            'up2': '\ue00a', 'down2': '\ue00b', 'bslogo': '\ue00c', 'back2': '\ue00d',
            'pause': '\ue00e', 'forward': '\ue00f', 'u': '\ue01a', 'y': '\ue01b',
            'a': '\ue01c', 'usmall': '\ue01d', 'logo': '\ue01e', 'ticket2': '\ue01f',
            'bronze': '\ue02a', 'silver': '\ue02b', 'gold': '\ue02c', 'badge1': '\ue02d',
            'badge2': '\ue02e', 'trophy': '\ue02f',
            'india': '\ue03a', 'japan': '\ue03b', 'france': '\ue03c', 'rw': '\ue03d',
            'gwr': '\ue03e', 'korea': '\ue03f',
            'mushroom': '\ue04a', 'nstar': '\ue04b', 'bull': '\ue04c', 'moon': '\ue04d',
            'spider': '\ue04e', 'fireball': '\ue04f', 'rect': '\ue05a', 'steam': '\ue05b',
            'nvidia': '\ue05c',
            'ns': '\ue04b', 'dr': '\ue048', 'fb': '\ue04f', 'cr': '\ue043', 'sk': '\ue046',
            'ht': '\ue047', 'hl': '\ue049', 'ms': '\ue04a', 'bl': '\ue04c', 'mn': '\ue04d',
            'sp': '\ue04e', 'la': '\ue001', 'ra': '\ue002', 'ua': '\ue003', 'da': '\ue004'
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
            'top': (0, 2.0, 0),
            'down': (0, -2.0, 0),
            'right': (2.0, 1.0, 0),
            'left': (-2.0, 1.0, 0),
            'center': (0, 2.0, 0),
            'head': (0, 2.5, 0),
            'feet': (0, -1.0, 0)
        }
        print("🎮 TagMaster Advanced System Loading...")
        self.templates_file = Uts.directory_user + '/Configs/tag_templates.json'
        self.load_templates()
        bs.apptimer(3.0, lambda: self.start_game_monitoring())

    def start_game_monitoring(self):
        def game_monitor():
            try:
                activity = bs.get_foreground_host_activity()
                if activity and hasattr(activity, 'players'):
                    try:
                        self.quick_apply_tags(activity)
                        self.cleanup_dead_players(activity)
                        self.check_player_respawns(activity)
                    except Exception as e:
                        print(f"⚠️ Tag monitor error: {e}")
                bs.apptimer(2.0, game_monitor)
            except Exception as e:
                print(f"❌ Game monitor error: {e}")
                bs.apptimer(5.0, game_monitor)
        bs.apptimer(1.0, game_monitor)
        print("🎮 Tag monitoring started (server optimized)")

    def quick_apply_tags(self, activity):
        try:
            if not activity or not hasattr(activity, 'players'):
                return
            for player in activity.players:
                try:
                    if not player.is_alive() or not player.actor or not player.actor.node:
                        continue
                    client_id = player.sessionplayer.inputdevice.client_id
                    account_id = None
                    if client_id in Uts.userpbs:
                        account_id = Uts.userpbs[client_id]
                    if account_id and account_id in Uts.pdata:
                        player_data = Uts.pdata[account_id]
                        if 'Tag' in player_data:
                            tag_data = player_data['Tag']
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
                    'flatness': 1.0,
                    'h_align': 'center',
                    'v_align': 'center',
                    'scale': tag_data['scale'],
                    'color': first_color,
                    'opacity': 0.0
                }
                tag_node = bs.newnode('text', attrs=attrs)
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
        try:
            for player in activity.players:
                try:
                    client_id = player.sessionplayer.inputdevice.client_id
                    account_id = None
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

    # ✅ الدالة الأساسية لإنشاء تاج عادي مع كتابة حرف حرف (معدلة بالكامل – بدون أخطاء)
    def create_tag_with_char_animation(self, player, client_id, text: str, color, scale: float, activity) -> bool:
        try:
            player_name = player.getname()
            if not player.actor or not player.actor.node:
                return False

            with activity.context:
                self.remove_tag_visual(client_id)
                self.stop_char_animation(client_id)

                tag_node = bs.newnode('text',
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'h_align': 'center',
                        'v_align': 'center',
                        'scale': scale,
                        'color': color,
                        'opacity': 0.0
                    })

                math_node = bs.newnode('math',
                    attrs={'input1': (0.0, 1.5, 0.0), 'operation': 'add'})

                player.actor.node.connectattr('position_center', math_node, 'input2')
                math_node.connectattr('output', tag_node, 'position')

                self.current_tags[str(client_id)] = {
                    'type': 'normal',
                    'tag_node': tag_node,
                    'math_node': math_node,
                    'text': text,
                    'color': color,
                    'scale': scale
                }

                # دالة كتابة النص حرفاً حرفاً
                def animate_text():
                    try:
                        if str(client_id) not in self.current_tags:
                            return
                        tag_node = self.current_tags[str(client_id)]['tag_node']
                        if not tag_node.exists():
                            return
                        if not text:
                            tag_node.text = ''
                            tag_node.opacity = 1.0
                            return

                        # جدولة تحديث النص كل 0.05 ثانية
                        for i in range(len(text) + 1):
                            bs.apptimer(i * 0.05, lambda idx=i: self._update_text_animation(client_id, text, idx, color))

                        # دالة إنهاء (تثبيت الشفافية)
                        def finalize():
                            if str(client_id) in self.current_tags:
                                tag_node = self.current_tags[str(client_id)]['tag_node']
                                if tag_node.exists():
                                    tag_node.opacity = 1.0

                        bs.apptimer(len(text) * 0.05 + 0.5, finalize)

                    except Exception as e:
                        print(f"Error in animate_text: {e}")

                # بدأ الكتابة بعد 0.1 ثانية
                bs.apptimer(0.1, animate_text)
                print(f"Created tag '{text}' for {player_name}")
                return True

        except Exception as e:
            print(f"Error creating tag with char animation: {e}")
            return False

    def _update_text_animation(self, client_id, full_text, index, color):
        try:
            if str(client_id) not in self.current_tags:
                return
            tag_node = self.current_tags[str(client_id)]['tag_node']
            if not tag_node.exists():
                return
            partial_text = full_text[:index]
            tag_node.text = partial_text
            tag_node.color = color
            opacity = min(1.0, index / len(full_text))
            tag_node.opacity = opacity
        except Exception as e:
            print(f"Error in _update_text_animation: {e}")

    def remove_tag_visual(self, client_id):
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
        try:
            client_id_str = str(client_id)
            if client_id_str in self.char_animations:
                del self.char_animations[client_id_str]
        except:
            pass

    def stop_animation(self, client_id):
        try:
            client_id_str = str(client_id)
            if client_id_str in self.animation_states:
                del self.animation_states[client_id_str]
        except:
            pass

    def load_templates(self):
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r') as f:
                    self.saved_tag_templates = json.load(f)
            else:
                self.saved_tag_templates = {}
        except:
            self.saved_tag_templates = {}

    def save_templates(self):
        try:
            with open(self.templates_file, 'w') as f:
                json.dump(self.saved_tag_templates, f, indent=4)
        except:
            pass

    def send_client_message(self, client_id, message, color=(1,1,1)):
        try:
            bs.screenmessage(message, color=color, clients=[client_id])
        except:
            pass

    def parse_color(self, color_str: str):
        color_str = color_str.lower()
        if color_str in self.colors:
            return self.colors[color_str]
        if ',' in color_str:
            try:
                parts = color_str.split(',')
                if len(parts) == 3:
                    r = float(parts[0].strip())
                    g = float(parts[1].strip())
                    b = float(parts[2].strip())
                    return (r, g, b)
            except:
                pass
        if color_str.startswith('#') and len(color_str) == 7:
            try:
                r = int(color_str[1:3], 16) / 255.0
                g = int(color_str[3:5], 16) / 255.0
                b = int(color_str[5:7], 16) / 255.0
                return (r, g, b)
            except:
                pass
        return (1.0, 1.0, 1.0)

    def generate_rainbow_colors(self, count: int):
        colors = []
        for i in range(count):
            hue = i / count
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
# ==================== إنشاء مثيل نظام التيجان ====================
Uts.tag_system = TagSystem()

def _install() -> None:
    """تهيئة البيانات الأساسية للنظام"""
    try:
        Uts.create_players_data()
        Uts.save_players_data()
        if not hasattr(Uts, 'tags'):
            Uts.create_tags_data()

        # المالك الأساسي (غيّره حسب رغبتك)
        owner_account = 'pb-IF4yVRIDXA=='
        if owner_account not in Uts.pdata:
            Uts.add_owner(owner_account)
            print(f"✅ Added owner: {owner_account}")

        Uts.create_bans_data()
        Uts.create_reports_data()
        Uts.create_warns_data()

        bs.apptimer(3.0, lambda: Uts.sm("Owner added!", color=(1.0, 0.5, 0.0)))
    except Exception as e:
        print(f"❌ Error initializing data: {e}")

    if not hasattr(Uts, 'tag_system'):
        Uts.tag_system = TagSystem()
        print("✅ Tag system initialized")


def settings():
    """تحميل إعدادات CheatMax"""
    global cfg
    Uts.create_settings()
    if cfg.get('Commands') is None:
        cfg['Commands'] = {
            'ShowInfo': False,
            'ShowMessages': False,
            'ChatLive': False,
            'HostName': "CheatMax Server",
            'Description': "Powered by CheatMax System",
            'InfoColor': list(Uts.colors()['white']),
            'Weather': 'none'
        }
        Uts.save_settings()
        print("✅ Default settings created")

    try:
        Uts.create_bans_data()
        Uts.create_reports_data()
        print("✅ Bans and reports systems initialized")
    except Exception as e:
        print(f"⚠️ Error loading bans/reports data: {e}")

    print("✅ Settings loaded successfully")


def plugin():
    """ربط الدوال الخاصة بالنشاط واللاعبين"""
    try:
        calls['GA_OnTransitionIn'] = bs.GameActivity.on_transition_in
        calls['OnJumpPress'] = PlayerSpaz.on_jump_press
        calls['OnPlayerJoin'] = Activity.on_player_join
        calls['PlayerSpazInit'] = PlayerSpaz.__init__

        bs.GameActivity.on_transition_in = new_ga_on_transition_in
        PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
        Activity.on_player_join = new_on_player_join
        PlayerSpaz.__init__ = new_playerspaz_init_

        try:
            bui.set_party_icon_always_visible(True)
        except:
            pass

        print("✅ Plugin functions connected successfully")
    except Exception as e:
        print(f"❌ Error connecting plugin functions: {e}")


def additional_features():
    """ميزات إضافية: حماية، إحصائيات، مكافآت يومية"""
    class AbuseProtection:
        def __init__(self):
            self.warning_count = {}
            self.kick_threshold = 3
            self.mute_duration = 300

        def warn_player(self, client_id, reason):
            if client_id not in self.warning_count:
                self.warning_count[client_id] = 0
            self.warning_count[client_id] += 1
            name = Uts.usernames.get(client_id, f"Player {client_id}")
            Uts.sm(f"⚠️ Warning to {name}: {reason}", color=(1, 1, 0), clients=[client_id])
            if self.warning_count[client_id] >= self.kick_threshold:
                bs.disconnect_client(client_id)
                bs.chatmessage(f"🚫 {name} was kicked for repeated warnings")
                del self.warning_count[client_id]

    Uts.abuse_protection = AbuseProtection()

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
                streak = self.rewards_data[account_id]['streak']
                reward_msg = f"🎁 Daily Reward! Streak: {streak} days"
                bs.chatmessage(reward_msg)
                return True
            return False

    Uts.daily_rewards = DailyRewards()
    print("✅ Additional features initialized")


def setup_automatic_backup():
    """نسخ احتياطي تلقائي كل ساعة"""
    import shutil
    from datetime import datetime

    backup_dir = Uts.directory_user + '/Backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    def backup_data():
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            players_file = Uts.directory_user + '/Configs/CheatMaxPlayersData.json'
            if os.path.exists(players_file):
                backup_file = f"{backup_dir}/players_backup_{timestamp}.json"
                shutil.copy2(players_file, backup_file)

            settings_file = Uts.directory_user + '/Configs/CheatMaxSettings.json'
            if os.path.exists(settings_file):
                backup_file = f"{backup_dir}/settings_backup_{timestamp}.json"
                shutil.copy2(settings_file, backup_file)

            bans_file = Uts.directory_user + '/Configs/CheatMaxBansData.json'
            if os.path.exists(bans_file):
                backup_file = f"{backup_dir}/bans_backup_{timestamp}.json"
                shutil.copy2(bans_file, backup_file)

            reports_file = Uts.directory_user + '/Configs/CheatMaxReportsData.json'
            if os.path.exists(reports_file):
                backup_file = f"{backup_dir}/reports_backup_{timestamp}.json"
                shutil.copy2(reports_file, backup_file)

            # الاحتفاظ بآخر 10 نسخ فقط
            backup_files = sorted([f for f in os.listdir(backup_dir) if f.endswith('.json')])
            for old_file in backup_files[:-10]:
                try:
                    os.remove(os.path.join(backup_dir, old_file))
                except:
                    pass
        except Exception as e:
            print(f"⚠️ Backup error: {e}")

    def backup_loop():
        backup_data()
        bs.apptimer(3600.0, backup_loop)

    bs.apptimer(3600.0, backup_loop)
    print("✅ Automatic backup system activated")


def setup_performance_monitor():
    """مراقبة أداء السيرفر (FPS)"""
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
    """إضافة أوامر خاصة غير موجودة في القائمة الأساسية"""
    special_commands = {
        'party': {
            'description': 'بدء حفلة!',
            'admin_only': False,
            'function': lambda client_id: start_party(client_id)
        },
        'stats': {
            'description': 'عرض إحصائياتك',
            'admin_only': False,
            'function': lambda client_id: show_stats(client_id)
        },
        'ban': {
            'description': 'حظر لاعب (لـAdmins فقط)',
            'admin_only': True,
            'function': lambda client_id: Uts.sm("Use: /ban <player> <reason>", clients=[client_id])
        },
        'unban': {
            'description': 'إلغاء حظر لاعب (لـAdmins فقط)',
            'admin_only': True,
            'function': lambda client_id: Uts.sm("Use: /unban <player>", clients=[client_id])
        },
        'report': {
            'description': 'الإبلاغ عن لاعب',
            'admin_only': False,
            'function': lambda client_id: Uts.sm("Use: /report <player> <reason>", clients=[client_id])
        },
        'reports': {
            'description': 'عرض الإبلاغات (لـAdmins فقط)',
            'admin_only': True,
            'function': lambda client_id: Uts.sm("Use: /reports", clients=[client_id])
        },
        'banlist': {
            'description': 'عرض قائمة الحظر (لـAdmins فقط)',
            'admin_only': True,
            'function': lambda client_id: Uts.sm("Use: /banlist", clients=[client_id])
        }
    }

    def start_party(client_id):
        activity = bs.get_foreground_host_activity()
        if activity:
            for _ in range(50):
                pos = (random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-5, 5))
                Bomb(position=pos, bomb_type='impact', bomb_scale=0.5).autoretain()
            Uts.sm("🎉 PARTY TIME! 🎉", clients=[client_id], color=(1, 0, 1))

    def show_stats(client_id):
        if client_id in Uts.statistics.player_stats:
            stats = Uts.statistics.player_stats[client_id]
            message = f"📊 Kills: {stats['kills']} | Deaths: {stats['deaths']}"
            Uts.sm(message, clients=[client_id])
        else:
            Uts.sm("📊 No stats yet", clients=[client_id])

    for cmd, data in special_commands.items():
        CommandFunctions.all_cmd().append(cmd)

    print(f"✅ Added {len(special_commands)} special commands")


def final_setup():
    """الإعدادات النهائية بعد تحميل كل شيء"""
    if not hasattr(bs, 'app') or not hasattr(bs.app, 'cheatmax_filter_chat'):
        print("⚠️ CheatMax system not fully initialized")
        try:
            bs.app.cheatmax_filter_chat = filter_chat_message
        except:
            pass

    welcome_msg = f"""
╔══════════════════════════════════════════╗
║       🎮 CheatMax System v2.0.2 🎮      ║
║      Advanced Tag & Admin System         ║
╠══════════════════════════════════════════╣
║ • Tag System: ✓ Active                  ║
║ • Commands: ✓ Loaded                    ║
║ • Multi-Language: ✓ Supported           ║
║ • Protection: ✓ Enabled                 ║
║ • Ban System: ✓ Active (PB-ID Verified)║
║ • Report System: ✓ Active              ║
║ • Teleport: ✓ Fixed (uses client ID)   ║
║ • Fly Mode: ✓ Fixed (uses client ID)   ║
║ • Super Jump: ✓ Ground Only            ║
║ • Ride: ✓ Fixed (RideMessage)          ║
║ • Invisible: ✓ Fixed (mesh removal)    ║
║ • Tint/Wall/Floor: ✓ NO LIMITS!        ║
║   └─ Any RGB values accepted (0.5,2,100)║
║ • SpawnBall: ✓ Added (Hittable)       ║
║ • Explosion: ✓ Added                  ║
║ • Locator: ✓ Added (Glowing)          ║
║ • Ping: ✓ Fixed (No errors)           ║
║ • /List Fixed: ✓ Shows PB-ID          ║
║ • A-Soccer Integration: ✓ Auto-save   ║
║ • Weather System: ✓ Added & Saved     ║
║   └─ Snow, Rock, Metal, Ice, Spark,   ║
║      Slime, Fire, Splinter, Smoke,     ║
║      Rainbow, None                     ║
╚══════════════════════════════════════════╝
    """
    for line in welcome_msg.split('\n'):
        print(line)

    try:
        Uts.tag_system.start_game_monitoring()
    except:
        pass

    print("✅ CheatMax system ready!")


# ==================== الفئة الرئيسية للمود ====================
# ba_meta export babase.Plugin
class CheatMaxSystem(bs.Plugin):
    def __init__(self):
        self.initialized = False
        self.version = "2.0.2"
        self.author = "CheatMax Team"
        self._hooked = False

    def on_app_running(self) -> None:
        try:
            print(f"🚀 Loading CheatMax System v{self.version}...")
            if self.initialized:
                return
            bs.apptimer(0.5, self.initialize_system)
        except Exception as e:
            print(f"❌ Error in on_app_running: {e}")

    def initialize_system(self):
        if self.initialized:
            return
        try:
            hook_chat_filter()
            bs.app.cheatmax_filter_chat = filter_chat_message
            plugin()
            settings()
            _install()
            bs.apptimer(2.0, additional_features)
            bs.apptimer(3.0, setup_automatic_backup)
            bs.apptimer(4.0, setup_performance_monitor)
            bs.apptimer(5.0, add_special_commands)
            bs.apptimer(6.0, final_setup)
            self.initialized = True
            print("✅ CheatMax System initialization sequence started")
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            try:
                plugin()
                settings()
                print("⚠️ System loaded with minimal features")
            except:
                print("❌ Failed to load minimal system")


def error_handler(func):
    """مزين (decorator) لالتقاط الأخطاء وتسجيلها"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ Error in {func.__name__}: {e}")
            try:
                error_log = Uts.directory_user + '/Configs/cheatmax_errors.log'
                with open(error_log, 'a') as f:
                    f.write(f"{datetime.now()}: {func.__name__} - {e}\n")
            except:
                pass
            return None
    return wrapper


# تطبيق مزين الأخطاء على الدوال الحساسة
filter_chat_message = error_handler(filter_chat_message)
new_ga_on_transition_in = error_handler(new_ga_on_transition_in)
new_on_player_join = error_handler(new_on_player_join)
new_playerspaz_init_ = error_handler(new_playerspaz_init_)
new_playerspaz_on_jump_press = error_handler(new_playerspaz_on_jump_press)


def system_test():
    """اختبار سلامة النظام بعد التحميل"""
    def run_tests():
        print("🧪 Running system tests...")
        tests_passed = 0
        tests_failed = 0

        try:
            if os.path.exists(Uts.directory_user + '/Configs'):
                print("✅ Test 1: Config directory exists")
                tests_passed += 1
            else:
                print("❌ Test 1: Config directory missing")
                tests_failed += 1
        except:
            tests_failed += 1

        try:
            if hasattr(Uts, 'tag_system'):
                print("✅ Test 2: Tag system initialized")
                tests_passed += 1
            else:
                print("❌ Test 2: Tag system not initialized")
                tests_failed += 1
        except:
            tests_failed += 1

        try:
            if hasattr(Uts, 'pdata'):
                print("✅ Test 3: Player data loaded")
                tests_passed += 1
            else:
                print("❌ Test 3: Player data not loaded")
                tests_failed += 1
        except:
            tests_failed += 1

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

        try:
            if hasattr(Uts, 'bans_data'):
                print(f"✅ Test 5: Ban system initialized ({len(Uts.bans_data)} bans)")
                tests_passed += 1
            else:
                print("❌ Test 5: Ban system not initialized")
                tests_failed += 1
        except:
            tests_failed += 1

        try:
            if hasattr(Uts, 'reports_data'):
                reports_count = len(Uts.reports_data.get('reports', []))
                print(f"✅ Test 6: Reports system initialized ({reports_count} reports)")
                tests_passed += 1
            else:
                print("❌ Test 6: Reports system not initialized")
                tests_failed += 1
        except:
            tests_failed += 1

        try:
            import bascenev1._hooks
            if hasattr(bascenev1._hooks.filter_chat_message, '__wrapped__') or hasattr(bs.app, 'cheatmax_filter_chat'):
                print("✅ Test 7: Chat filter hooked successfully")
                tests_passed += 1
            else:
                print("❌ Test 7: Chat filter not hooked")
                tests_failed += 1
        except:
            tests_failed += 1

        print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
        if tests_failed == 0:
            print("🎉 All tests passed! System is ready.")
        else:
            print("⚠️ Some tests failed. System may have issues.")

    bs.apptimer(10.0, run_tests)


bs.apptimer(8.0, system_test)

print("=" * 50)
print("CheatMax System Code Loaded Successfully!")
print("=" * 50)
