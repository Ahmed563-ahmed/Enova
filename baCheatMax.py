# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING


import os, random, json, time

import bascenev1 as bs

import bauiv1 as bui

import babase as ba

import _babase


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
                {"Spanish": f"'{subs}' no es válido. \n Ingresa el ID del jugador. consulta el comando '-i'",
                 "English": f"'{subs}' no es válido. \n Add the player ID. use the '-i' command for more information.",
                 "Portuguese": f"'{subs}' no es válido. \n Adicione o ID do jogador. use o comando '-i' para obter mais informações."},
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
                 "Portuguese": f"O tempo está ahora '{subs}'"},
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
           "Use -i Command":
                {"Spanish": "Le sugerimos usar el comando '-i'",
                 "English": "We suggest you use the '-i' command",
                 "Portuguese": "Sugerimos que você use o comando '-i'"},
           "Add Effect Message":
                {"Spanish": f"Se agregó el efecto '{subs[0]}' a {subs[1]}",
                 "English": f"Added '{subs[0]}' effect to {subs[1]}",
                 "Portuguese": f"Adicionado efeito '{subs[0]}' para {subs[1]}"},
           "You Are Amazing":
                {"Spanish": "¡¡Eres ASOMBROSO!!",
                 "English": "You Are Amazing!!",
                 "Portuguese": "Você é incrível!!"},
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
                {"Spanish": "Agrega el ID del cliente. \n utilice el comando '-i' para más información.",
                 "English": "Add the client ID.  \n use the '-i' command for more information.",
                 "Portuguese": "Adicione o ID do cliente. \n use o comando '-i' para mais informações."},
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
            # الجمل الجديدة
           "Custom Tag Set":
                {"Spanish": f"Tag personalizado establecido para {subs}",
                 "English": f"Custom tag set for {subs}",
                 "Portuguese": f"Tag personalizado definido para {subs}"},
           "Animation Tag Set":
                {"Spanish": f"Tag animado establecido para {subs}",
                 "English": f"Animation tag set for {subs}",
                 "Portuguese": f"Tag animado definido para {subs}"},
           "Ban Message":
                {"Spanish": f"{subs[0]} ha sido baneado. Razón: {subs[1]}",
                 "English": f"{subs[0]} has been banned. Reason: {subs[1]}",
                 "Portuguese": f"{subs[0]} foi banido. Razão: {subs[1]}"},
           "Unban Message":
                {"Spanish": f"{subs} ha sido desbaneado",
                 "English": f"{subs} has been unbanned",
                 "Portuguese": f"{subs} foi desbanido"},
           "Already Banned":
                {"Spanish": f"{subs} ya está baneado",
                 "English": f"{subs} is already banned",
                 "Portuguese": f"{subs} já está banido"},
           "Not Banned":
                {"Spanish": f"{subs} no está baneado",
                 "English": f"{subs} is not banned",
                 "Portuguese": f"{subs} não está banido"},
           "Banned Players":
                {"Spanish": "Jugadores baneados:",
                 "English": "Banned players:",
                 "Portuguese": "Jogadores banidos:"},
           "Player Banned Join":
                {"Spanish": f"{subs} está baneado y no puede unirse",
                 "English": f"{subs} is banned and cannot join",
                 "Portuguese": f"{subs} está banido e não pode entrar"},
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
act = bs.get_foreground_host_activity
mutelist = list()


cfg = dict()


class PopupText(ptext.PopupText):
    """New PopupText.
    
    category: **Messages In Game**
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node.shadow = 10.0
        self.node.color = (1.5, 1.5, 1.5, 1.0)
        bs.animate(self._combine, 'input3', {0: 0, 0.1: 1.0})
        
    def handlemessage(self, msg: Any) -> Any:
        pass

class TagManager:
    """مدير العلامات (التيجان) فوق رؤوس اللاعبين"""
    
    def __init__(self):
        self.tags = {}
        self.animated_tags = {}
        self.load_tags()
    
    def load_tags(self):
        """تحميل العلامات المحفوظة"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxTags.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                self.tags = data.get('tags', {})
                self.animated_tags = data.get('animated_tags', {})
    
    def save_tags(self):
        """حفظ العلامات"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxTags.json'
        
        data = {
            'tags': self.tags,
            'animated_tags': self.animated_tags
        }
        
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def set_custom_tag(self, client_id: int, text: str, color: str, scale: float = 1.0):
        """تعيين علامة مخصصة للاعب"""
        self.tags[str(client_id)] = {
            'text': text,
            'color': color,
            'scale': scale,
            'type': 'custom'
        }
        # إزالة إذا كان متحرك
        if str(client_id) in self.animated_tags:
            del self.animated_tags[str(client_id)]
        self.save_tags()
        self.apply_tag_to_player(client_id)
    
    def set_animation_tag(self, client_id: int, text: str, scale: float, 
                         speed: float, colors: list[str]):
        """تعيين علامة متحركة"""
        self.animated_tags[str(client_id)] = {
            'text': text,
            'scale': scale,
            'speed': speed,
            'colors': colors,
            'type': 'animated',
            'current_color_index': 0
        }
        # إزالة إذا كان مخصص
        if str(client_id) in self.tags:
            del self.tags[str(client_id)]
        self.save_tags()
        self.apply_tag_to_player(client_id)
    
    def remove_tag(self, client_id: int):
        """إزالة العلامة من اللاعب"""
        client_str = str(client_id)
        if client_str in self.tags:
            del self.tags[client_str]
        if client_str in self.animated_tags:
            del self.animated_tags[client_str]
        self.save_tags()
        self.remove_tag_from_player(client_id)
    
    def apply_tag_to_player(self, client_id: int):
        """تطبيق العلامة على اللاعب في اللعبة"""
        with act().context:
            actor = CommandFunctions.get_actor(client_id)
            if actor:
                self._apply_tag_to_actor(actor, client_id)
    
    def _apply_tag_to_actor(self, actor, client_id: int):
        """تطبيق العلامة على الـ actor"""
        client_str = str(client_id)
        
        # إزالة أي علامة موجودة
        if hasattr(actor, '_custom_tag_timer'):
            actor._custom_tag_timer = None
        
        # تطبيق علامة مخصصة
        if client_str in self.tags:
            tag_data = self.tags[client_str]
            
            # إنشاء عقدة نصية
            pos = (-0.0, 1.5 * tag_data['scale'], 0.0)
            
            m = bs.newnode('math', owner=actor.node, attrs={'input1':
                (pos[0], pos[1], pos[2]), 'operation': 'add'})
            actor.node.connectattr('position_center', m, 'input2')
            
            color = Uts.colors().get(tag_data['color'], (1, 1, 1))
            
            actor._custom_tag = text.Text(
                text=tag_data['text'],
                color=color,
                scale=tag_data['scale'],
                h_align=text.Text.HAlign.CENTER
            ).autoretain()
            
            m.connectattr('output', actor._custom_tag.node, 'position')
        
        # تطبيق علامة متحركة
        elif client_str in self.animated_tags:
            tag_data = self.animated_tags[client_str]
            
            # إنشاء عقدة نصية
            pos = (-0.0, 1.5 * tag_data['scale'], 0.0)
            
            m = bs.newnode('math', owner=actor.node, attrs={'input1':
                (pos[0], pos[1], pos[2]), 'operation': 'add'})
            actor.node.connectattr('position_center', m, 'input2')
            
            actor._custom_tag = text.Text(
                text=tag_data['text'],
                color=Uts.colors().get(tag_data['colors'][0], (1, 1, 1)),
                scale=tag_data['scale'],
                h_align=text.Text.HAlign.CENTER
            ).autoretain()
            
            m.connectattr('output', actor._custom_tag.node, 'position')
            
            # إنشاء مؤقت لتغيير الألوان
            def change_color():
                if not actor.node.exists():
                    actor._custom_tag_timer = None
                    return
                
                tag_data = self.animated_tags.get(client_str)
                if not tag_data:
                    return
                
                current_idx = tag_data.get('current_color_index', 0)
                colors = tag_data.get('colors', [])
                
                if colors:
                    next_idx = (current_idx + 1) % len(colors)
                    color_name = colors[next_idx]
                    color = Uts.colors().get(color_name, (1, 1, 1))
                    
                    if hasattr(actor, '_custom_tag') and actor._custom_tag.node.exists():
                        actor._custom_tag.node.color = color
                    
                    # تحديث الفهرس
                    tag_data['current_color_index'] = next_idx
                    self.animated_tags[client_str] = tag_data
            
            actor._custom_tag_timer = bs.Timer(tag_data['speed'], change_color, repeat=True)
    
    def remove_tag_from_player(self, client_id: int):
        """إزالة العلامة من اللاعب في اللعبة"""
        with act().context:
            actor = CommandFunctions.get_actor(client_id)
            if actor and hasattr(actor, '_custom_tag'):
                if actor._custom_tag.node.exists():
                    actor._custom_tag.node.delete()
                actor._custom_tag = None
                
                if hasattr(actor, '_custom_tag_timer'):
                    actor._custom_tag_timer = None
    
    def get_tag_info(self, client_id: int) -> dict:
        """الحصول على معلومات العلامة للاعب"""
        client_str = str(client_id)
        if client_str in self.tags:
            return self.tags[client_str]
        elif client_str in self.animated_tags:
            return self.animated_tags[client_str]
        return None

class BanManager:
    """مدير النظام لحظر اللاعبين"""
    
    def __init__(self):
        self.bans = {}
        self.load_bans()
    
    def load_bans(self):
        """تحميل قائمة المحظورين"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxBans.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if os.path.exists(file):
            with open(file, 'r') as f:
                self.bans = json.load(f)
        else:
            self.bans = {}
    
    def save_bans(self):
        """حفظ قائمة المحظورين"""
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxBans.json'
        
        with open(file, 'w') as f:
            json.dump(self.bans, f, indent=4)
    
    def ban_player(self, identifier, reason: str, banned_by: str):
        """حظر لاعب"""
        # البحث عن المعرف (قد يكون client_id أو pb_id)
        player_info = self._find_player_info(identifier)
        
        if not player_info:
            return False, "Player not found"
        
        player_id = player_info.get('pb_id', identifier)
        
        if str(player_id) in self.bans:
            return False, "Player already banned"
        
        self.bans[str(player_id)] = {
            'name': player_info.get('name', 'Unknown'),
            'reason': reason,
            'banned_by': banned_by,
            'timestamp': time.time(),
            'client_id': player_info.get('client_id'),
            'pb_id': player_info.get('pb_id')
        }
        
        self.save_bans()
        
        # فصل اللاعب إذا كان متصل
        if player_info.get('client_id') != -1:
            bs.disconnect_client(player_info['client_id'])
        
        return True, f"Player {player_info.get('name')} banned"
    
    def unban_player(self, identifier):
        """إلغاء حظر لاعب"""
        # البحث في المحظورين
        for player_id, ban_info in list(self.bans.items()):
            if (str(identifier) == player_id or 
                str(identifier) == str(ban_info.get('client_id')) or
                str(identifier).lower() in ban_info.get('name', '').lower()):
                player_name = ban_info.get('name', 'Unknown')
                del self.bans[player_id]
                self.save_bans()
                return True, f"Player {player_name} unbanned"
        
        return False, "Player not found in ban list"
    
    def is_banned(self, client_id: int, pb_id: str = None) -> bool:
        """التحقق إذا كان اللاعب محظور"""
        # التحقق بالـ client_id
        for ban_info in self.bans.values():
            if ban_info.get('client_id') == client_id:
                return True
        
        # التحقق بالـ pb_id
        if pb_id and str(pb_id) in self.bans:
            return True
            
        return False
    
    def get_banned_player_info(self, client_id: int):
        """الحصول على معلومات اللاعب المحظور"""
        for ban_info in self.bans.values():
            if ban_info.get('client_id') == client_id:
                return ban_info
        return None
    
    def get_ban_list(self) -> str:
        """الحصول على قائمة المحظورين كنص"""
        if not self.bans:
            return "No banned players"
        
        result = getlanguage('Banned Players') + "\n"
        result += "=" * 30 + "\n"
        
        for player_id, ban_info in self.bans.items():
            name = ban_info.get('name', 'Unknown')
            reason = ban_info.get('reason', 'No reason')
            banned_by = ban_info.get('banned_by', 'Unknown')
            
            # تحويل التوقيت
            timestamp = ban_info.get('timestamp', 0)
            if timestamp:
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            else:
                time_str = "Unknown"
            
            result += f"Name: {name}\n"
            result += f"Reason: {reason}\n"
            result += f"Banned by: {banned_by}\n"
            result += f"Time: {time_str}\n"
            result += "-" * 20 + "\n"
        
        return result
    
    def _find_player_info(self, identifier):
        """البحث عن معلومات اللاعب"""
        # محاولة كـ client_id
        try:
            client_id = int(identifier)
            if client_id in Uts.usernames:
                return {
                    'client_id': client_id,
                    'name': Uts.usernames[client_id],
                    'pb_id': Uts.userpbs.get(client_id)
                }
        except ValueError:
            pass
        
        # البحث بالاسم
        for cid, name in Uts.usernames.items():
            if str(identifier).lower() in name.lower():
                return {
                    'client_id': cid,
                    'name': name,
                    'pb_id': Uts.userpbs.get(cid)
                }
        
        # البحث بالـ pb_id
        if identifier in Uts.userpbs.values():
            for cid, pid in Uts.userpbs.items():
                if pid == identifier:
                    return {
                        'client_id': cid,
                        'name': Uts.usernames.get(cid, 'Unknown'),
                        'pb_id': pid
                    }
        
        return None

# إنشاء مديري النظام
tag_manager = TagManager()
ban_manager = BanManager()


class Commands:
    """Usa los distintos comandos dependiendo tu rango (All, Admins).
    
    Category: **Command Class**
    """

    fct: CommandFunctions
    "Llama los distintos comandos"
    
    util: Uts
    "Llama a las distintas utilidades"
    
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

        self.filter_chat()
        
    def clientmessage(self, msg: str,
            color: Sequence[float] = None):
                
        self.util.sm(msg, color=color,
            transient=True,
            clients=[self.client_id])
    
    def filter_chat(self) -> None:
        ms = self.arguments
        self.util.update_usernames()
                
        if self.client_id in self.util.accounts:
            if self.util.accounts[self.client_id]['Mute']:
                return setattr(self, 'value', '@')
        
        if cfg['Commands'].get('ShowMessages'):
            cls_node = self.fct.get_actor(self.client_id)
            if cls_node is not None:
                ActorMessage(self.msg, cls_node)
        
        if 'info' in ms[0].lower():
            with act().context:
                bs.timer(0.01, bs.Call(self.util.create_data_text, act()))
                
        with act().context:
            bs.timer(0.01, bs.Call(self.util.create_live_chat, act(),
                chat=[self.client_id, self.message],
                admin=self.fct.user_is_admin(self.client_id)))
    
        self.command_all()
        
        if self.fct.user_is_admin(self.client_id):
            self.admin_commands()
    
    def command_all(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cmd = self.fct.all_cmd()
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage
    
        if msg.lower() == cmd[0]: # -i
            self.fct.get_user_list(self.client_id)
    
        elif msg.lower() == cmd[1]: # -pan
            self.util.cm("¡Haz recibido pan de \ue061Sr.Palomo!")
            #return setattr(self, 'value', '@')
            
        elif msg.lower() == cmd[2]: # -ceb
            with act().context:
                cls_node.handlemessage(
                    bs.CelebrateMessage(duration=3.0))
            ClientMessage(getlanguage('Happy'), color=(1.0, 1.0, 0.0))
            
        elif msg.lower() == cmd[3]: # -colors
            cols = str()
            cols_list = self.util.sort_list(self.util.colors())
            for c in cols_list:
                cols += (' | '.join(c) + '\n')
            ClientMessage(cols)
            
        elif msg.lower() == cmd[4]: # -mp (max players)
            mp = bs.get_public_party_max_size()
            ClientMessage(bs.Lstr(value='${LSTR}: ${COUNT}',
                    subs=[('${LSTR}', bs.Lstr(resource='maxPartySizeText')),
                          ('${COUNT}', str(mp))]))

        elif msg.lower() == cmd[5]: # -pb
            self.fct.get_my_pb(self.client_id)
    
        elif msg.lower() == cmd[6]: # -effects
            cols = str()
            for e in self.fct.effects():
                cols += (' | ' + e)
            ClientMessage(cols)
    
    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]
    
        if ms[0] == cmd[0]: # /name 0 La Pulga
            try: name = ms[2]
            except:
                color = self.util.colors()['orange']
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' 0  La Pulga | ' + ms[0] + ' all La Pulga'), color=color)
            else:
                self.fct.actor_command(ms=ms,
                    call=bs.Call(self.fct.actor_name, ' '.join(ms[2:])),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[1]: # /imp
            self.fct.actor_command(ms=ms,
                call=self.fct.impulse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            
        elif ms[0] == cmd[2]: # /box
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_box,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[3] or ms[0] == cmd[4]: # /addAdmin
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except ValueError:
                    ClientMessage(
                            getlanguage('Error Entering Client ID',
                                subs=[ms[1], '/addAdmin 113']))
                else:
                    if c_id not in self.util.usernames:
                            ClientMessage(getlanguage('User Invalid', subs=c_id))
                    else:
                        if ms[0] == cmd[3]:
                            self.util.add_or_del_user(c_id, add=True)
                        else:
                            self.util.add_or_del_user(c_id, add=False)
                        
        elif ms[0] == cmd[5]: # /kill
            self.fct.actor_command(ms=ms,
                call=self.fct.kill_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                        
        elif ms[0] == cmd[6]: # -pause
            self.fct.pause()
                        
        elif ms[0] == cmd[7]: # /infoHost
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Agrega un texto'))
                else:
                    cfg['Commands']['HostName'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage(getlanguage('Cambios Guardados'), color=(0.0, 1.0, 0.0))
                
        elif ms[0] == cmd[8]: # /infoDes
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Agrega un texto'))
                else:
                    cfg['Commands']['Description'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage(getlanguage('Cambios Guardados'), color=(0.0, 1.0, 0.0))
    
        elif ms[0] == cmd[9]: # -info
            if cfg['Commands'].get('ShowInfo'):
                cfg['Commands']['ShowInfo'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowInfo'] = True
                color = self.util.colors()['green']
                
            self.util.save_settings()
            ClientMessage(getlanguage('Cambios Guardados'), color=color)
    
        elif ms[0] == cmd[10]: # /infoColor
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Info Color'))
                else:
                    if ms[1] not in self.util.colors():
                        ClientMessage(getlanguage('Info Color'), color=(1, 0.5, 0))
                    else:
                        cfg['Commands']['InfoColor'] = self.util.colors()[ms[1]]
                        self.util.save_settings()
                        ClientMessage(getlanguage('Cambios Guardados'), color=(1, 1, 0))
    
        elif ms[0] == cmd[11]: # -end
            with act().context:
                act().end_game()
    
        elif ms[0] == cmd[12]: # /kick
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as exc:
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(
                            getlanguage('Error Entering Client ID',
                                subs=[ms[1], ms[0] + ' 113']))
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                else:
                    if self.client_id == c_id:
                        ClientMessage(getlanguage('Same Player'))
                    else:
                        if c_id not in self.util.usernames:
                            ClientMessage(getlanguage('User Invalid', subs=c_id))
                        else:
                            user1 = self.util.usernames[self.client_id]
                            user2 = self.util.usernames[c_id]
                            if self.fct.user_is_admin(c_id):
                                ClientMessage(getlanguage('Ban A Admin Mensaje', subs=user2))
                            else:
                                self.util.cm(getlanguage('Kick Msg', subs=[user1, user2]))
                                bs.disconnect_client(c_id)
    
        elif ms[0] == cmd[13]: # /-chatLive
            if cfg['Commands'].get('ChatLive'):
                cfg['Commands']['ChatLive'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ChatLive'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('Cambios Guardados'), color=color)
    
        elif ms[0] == cmd[14]: # /freeze
            self.fct.actor_command(ms=ms,
                call=self.fct.freeze_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            
        elif ms[0] == cmd[15]: # /playerColor
            try: color = ms[2]
            except IndexError:
                ClientMessage(getlanguage('Info Color'))
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' 0  yellow | ' + ms[0] + ' all green'))
            else:
                self.fct.actor_command(ms=ms,
                    call=bs.Call(self.fct.player_color, color),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[16]: # /maxPlayers
            try:
                val = int(ms[1])
            except:
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 5'))
            else:
                bs.set_public_party_max_size(val)
                ClientMessage(
                    bs.Lstr(value='${LSTR}: ${COUNT}',
                        subs=[('${LSTR}', bs.Lstr(resource='maxPartySizeText')),
                              ('${COUNT}', ms[1])]))
    
        elif ms[0] == cmd[17]: # -showMessages
            if cfg['Commands'].get('ShowMessages'):
                cfg['Commands']['ShowMessages'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowMessages'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('Show Spaz Messages'), color=color)
    
        elif ms[0] == cmd[18]: # /sleep
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sleep,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[19] or ms[0] == cmd[20]: # /mute /unmute
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as e:
                    ClientMessage(
                        getlanguage('Error Entering Client ID',
                            subs=[ms[1], ms[0] + ' 113']))
                else:
                    if c_id not in self.util.accounts:
                        ClientMessage(getlanguage('User Invalid', subs=c_id))
                    else:
                        user = self.util.usernames[c_id]
                        if ms[0] == cmd[19]:
                            if self.fct.user_is_admin(c_id):
                                self.util.cm(getlanguage('Not In Admins', subs=Uts.usernames[c_id]))
                                return
                            if not self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = True
                                self.util.cm(getlanguage('Mute Message', subs=user))
                        elif ms[0] == cmd[20]:
                            if self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = False
                                self.util.cm(getlanguage('Unmute Message', subs=user))
                        Uts.save_players_data()

        elif ms[0] == cmd[21]: # /gm
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gm,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[22]: # -slow
            self.fct.slow()

        elif ms[0] == cmd[23]: # /speed
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_speed,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                      
        elif ms[0] == cmd[24]: # /effect
            try:
                c_id = int(ms[1])
                eff = ms[2]
            except ValueError:
                ClientMessage(getlanguage('Error ID User', subs=ms[1]), color=(1, 0, 0))
            except IndexError:
                ClientMessage(getlanguage('ID Cliente Msj'), color=(1, 0.5, 0))
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 113 fire'), color=(1, 0.5, 0))
            else:
                if c_id not in self.util.accounts:
                    ClientMessage(getlanguage('User Invalid', subs=c_id), color=(1, 0.5, 0))
                    ClientMessage(getlanguage('Use -i Command'), color=(1, 0.5, 0))
                else:
                    if eff not in self.fct.effects():
                        ClientMessage(getlanguage('Effect Invalid', subs=eff), color=(1, 0.5, 0))
                    else:
                        self.util.accounts[c_id]['Effect'] = eff
                        self.util.save_players_data()
                        user = self.util.usernames[c_id]
                        ClientMessage(getlanguage('Add Effect Message',
                            subs=[eff, user]), color=(0, 0.5, 1))

        elif ms[0] == cmd[25]: # /punch
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_punch,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
        
        elif ms[0] == cmd[26]: # /mbox
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_mgb,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[27]: # /drop
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_drop,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})

        elif ms[0] == cmd[28]: # /gift
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gift,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[29]: # /curse
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_curse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[30]: # /superjump
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sjump,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
        
        # === الأوامر الجديدة ===
        elif ms[0] == '/customtag':
            if len(ms) < 5:
                ClientMessage(getlanguage('EJ', subs='/customtag Hello red 1.0 113'))
            else:
                try:
                    text = ms[1]
                    color = ms[2]
                    scale = float(ms[3])
                    target_id = int(ms[4])
                    
                    if color not in self.util.colors():
                        ClientMessage(getlanguage('Info Color'))
                        return
                    
                    if target_id not in self.util.usernames:
                        ClientMessage(getlanguage('User Invalid', subs=target_id))
                        return
                    
                    # التحقق من الصلاحيات (أدمنز وأونرز فقط)
                    if not self.fct.user_is_admin(self.client_id):
                        ClientMessage("You need admin permissions!")
                        return
                    
                    tag_manager.set_custom_tag(target_id, text, color, scale)
                    
                    user = self.util.usernames[target_id]
                    ClientMessage(getlanguage('Custom Tag Set', subs=user), color=(0, 1, 0))
                    
                except Exception as e:
                    ClientMessage(f"Error: {e}")
        
        elif ms[0] == '/animationtag':
            if len(ms) < 7:
                ClientMessage(getlanguage('EJ', subs='/animationtag Hello 1.0 0.5 113 red green blue'))
            else:
                try:
                    text = ms[1]
                    scale = float(ms[2])
                    speed = float(ms[3])
                    target_id = int(ms[4])
                    colors = ms[5:]
                    
                    if target_id not in self.util.usernames:
                        ClientMessage(getlanguage('User Invalid', subs=target_id))
                        return
                    
                    # التحقق من الألوان
                    for color in colors:
                        if color not in self.util.colors():
                            ClientMessage(getlanguage('Info Color'))
                            return
                    
                    # التحقق من الصلاحيات (أدمنز وأونرز فقط)
                    if not self.fct.user_is_admin(self.client_id):
                        ClientMessage("You need admin permissions!")
                        return
                    
                    tag_manager.set_animation_tag(target_id, text, scale, speed, colors)
                    
                    user = self.util.usernames[target_id]
                    ClientMessage(getlanguage('Animation Tag Set', subs=user), color=(0, 1, 0))
                    
                except Exception as e:
                    ClientMessage(f"Error: {e}")
        
        elif ms[0] == '/ban':
            if len(ms) < 3:
                ClientMessage(getlanguage('EJ', subs='/ban 113 cheating'))
            else:
                identifier = ms[1]
                reason = ' '.join(ms[2:])
                
                # التحقق من الصلاحيات
                if not self.fct.user_is_admin(self.client_id):
                    ClientMessage("You need admin permissions!")
                    return
                
                banned_by = self.util.usernames.get(self.client_id, "Admin")
                success, message = ban_manager.ban_player(identifier, reason, banned_by)
                
                if success:
                    ClientMessage(getlanguage('Ban Message', subs=[identifier, reason]), color=(1, 0, 0))
                else:
                    ClientMessage(message, color=(1, 0.5, 0))
        
        elif ms[0] == '/unban':
            if len(ms) < 2:
                ClientMessage(getlanguage('EJ', subs='/unban 113'))
            else:
                identifier = ms[1]
                
                # التحقق من الصلاحيات
                if not self.fct.user_is_admin(self.client_id):
                    ClientMessage("You need admin permissions!")
                    return
                
                success, message = ban_manager.unban_player(identifier)
                
                if success:
                    ClientMessage(getlanguage('Unban Message', subs=identifier), color=(0, 1, 0))
                else:
                    ClientMessage(message, color=(1, 0.5, 0))
        
        elif ms[0] == '/banlist':
            # التحقق من الصلاحيات
            if not self.fct.user_is_admin(self.client_id):
                ClientMessage("You need admin permissions!")
                return
            
            ban_list = ban_manager.get_ban_list()
            ClientMessage(ban_list)
                       
class CommandFunctions:
    def all_cmd() -> list[str]:
        return [
            '-i', '-pan', '-ceb', '-colors',
            '-mp', '-pb', '-effects',
            ]
            
    def admins_cmd() -> list[str]:
        return [
            '/name', '/imp', '/box', '/addAdmin',
            '/delAdmin', '/kill', '-pause', '/infoHost',
            '/infoDes', '-info', '/infoColor', '-end',
            '/kick', '-chatLive', '/freeze', '/playerColor',
            '/maxPlayers', '-showMessages', '/sleep',
            '/mute', '/unmute', '/gm', '-slow', '/speed',
            '/effect', '/punch', '/mbox', '/drop', '/gift',
            '/curse', '/superjump',
            '/customtag', '/animationtag', '/ban', '/unban', '/banlist'  # الأوامر الجديدة
            ]

    def effects() -> list[str]:
        return ['none', 'footprint', 'fire', 'darkmagic',
                'spark', 'stars', 'aure', 'chispitas', 'rainbow']

    def get_my_pb(client_id: int) -> None:
        print(Uts.userpbs)
        if Uts.userpbs.get(client_id):
            pb = Uts.userpbs[client_id]
            Uts.sm(pb, transient=True, clients=[client_id])
    
    def spaz_sjump(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            if getattr(actor, 'cm_superjump', None):
                actor.cm_superjump = False
            else:
                actor.cm_superjump = True
    
    def spaz_curse(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(bs.PowerupMessage('curse', node))
    
    def spaz_gift(node: bs.Node) -> None:
        with act().context:
            ExplosiveGift(owner=node)
    
    def spaz_mgb(node: bs.Node) -> None:
        with act().context:
            MagicBox(pos=node.position).autoretain()
            
    def spaz_punch(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            actor._punch_power_scale = 8.0
            
    def spaz_speed(node: bs.Node) -> None:
        with act().context:
            if node.hockey:
                node.hockey = False
            else:
                node.hockey = True

    def slow() -> None:
        with act().context:
            gnode = act().globalsnode
            if gnode.slow_motion:
                gnode.slow_motion = False
            else:
                gnode.slow_motion = True
            
    def spaz_gm(node: bs.Node) -> None:
        with act().context:
            if node.invincible:
                node.invincible = False
            else:
                node.invincible = True
            
    def spaz_sleep(node: bs.Node) -> None:
        with act().context:
            for x in range(5):
                bs.timer(x, bs.Call(node.handlemessage, 'knockout', 5000.0))
            
    def player_color(color: str, node: bs.Node) -> None:
        with act().context:
            node.color = Uts.colors()[color]
            
    def freeze_spaz(node: bs.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with act().context:
            if actor.shield:
                actor.shield.delete()
                
            actor.handlemessage(bs.FreezeMessage())

    def pause() -> None:
        with act().context:
            globs = act().globalsnode
            if globs.paused:
                globs.paused = False
            else:
                globs.paused = True

    def kill_spaz(node: bs.Node) -> None:
        with act().context:
            node.handlemessage(
                bs.DieMessage())

    def spaz_box(node: bs.Node) -> None:
        with act().context:
            node.torso_mesh = bs.getmesh('tnt')
            node.head_mesh = None
            node.pelvis_mesh = None
            node.forearm_mesh = None
            node.color_texture = node.color_mask_texture = bs.gettexture('tnt')
            node.color = node.highlight = (1,1,1)
            node.style = 'cyborg'

    def impulse(node: bs.Node) -> None:
        msg = bs.HitMessage(pos=node.position,
                            velocity=node.velocity,
                            magnitude=500 * 4,
                            hit_subtype='imp',
                            radius=7840)
                          
        if isinstance(msg, bs.HitMessage):
            for i in range(2):
                with act().context:
                    node.handlemessage(
                        'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                        msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                        msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                        msg.force_direction[1], msg.force_direction[2])

    def actor_name(name: str, node: bs.Node) -> None:
        with act().context:
            node.name = name

    def actor_command(
            ms: list[str],
            call: Callable,
            attrs: dict[str, Any]) -> None:
        ClientMessage = attrs['ClientMessage']
                
        def new_call(node: bs.Node):
            ClientMessage(getlanguage('Exe'), color=(0, 1, 0))
            call(node)
                
        if len(ms) == 1:
            if attrs['Actor'] is None:
                ClientMessage(getlanguage('Not Exists Node'))
            else:
                actor = attrs['Actor']
                new_call(actor.node)
        else:
            if ms[1] == 'all':
                for p in act().players:
                    node = p.actor.node
                    new_call(node)
            else:
                try:
                    p_id = int(ms[1])
                    node = act().players[p_id].actor.node
                except Exception as exc:
                    color = Uts.colors()['orange']
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(getlanguage('Error Entering Player ID', subs=ms[1]), color=color)
                    elif type_error is IndexError:
                        ClientMessage(getlanguage('User Invalid', subs=p_id), color=color)
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                    ClientMessage(getlanguage('EX', subs=ms[0] + ' 0 | ' + ms[0] + ' all'))
                else:
                    new_call(node)

    def spaz_drop(node: bs.Node) -> None:
        self = node.source_player.actor
        del node # Unused by default.

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
            with act().context:
                bs.timer(x * 0.308, drop)

    def get_user_list(c_id: int) -> None:
        def delete_text(t_id: int):
            if t_id == id(act()._ids.node):
                act()._ids.node.opacity = 0.0
            
        def gText(txt: str):
            act()._ids = text.Text(txt, position=(-0.0, 270.0),
                h_align=text.Text.HAlign.CENTER, scale=1.1,
                transition=text.Text.Transition.FADE_IN).autoretain()
            act()._ids.node.opacity = 0.5
            
            t_id = id(act()._ids.node)
            bs.timer(8.0, bs.Call(delete_text, t_id))
    
        txt = str()
        txts = [getlanguage('Players Data'),
                "______________________"]

        try:
            players = act().players
        except Exception:
            players = []
        else:
            for idx, p in enumerate(players):
                if p.is_alive():
                    s = p.sessionplayer
                    txts.append(f"{s.getname(False)} | {idx} | {s.inputdevice.client_id}")
        
        txt = '\n'.join(txts)

        with act().context:
            try:
                if act()._ids.node.exists():
                    act()._ids.node.delete()
                    gText(txt)
            except AttributeError:
                gText(txt)
        bs.screenmessage(txt, clients=[c_id], transient=True)
    
    def get_characters() -> list[str]:
        return bs.app.spaz_appearances
    
    def user_is_admin(c_id: int) -> bool:
        if c_id == -1:
            return True
    
        if c_id in Uts.accounts:
            return Uts.accounts[c_id]['Admin']
        else:
            return False
    
    def get_actor(c_id: int) -> spaz.Spaz:
        act = bs.get_foreground_host_activity()
        for player in act.players:
            if c_id == player.sessionplayer.inputdevice.client_id:
                return player.actor
        
def ActorMessage(msg: str, actor: spaz.Spaz):
    def die(node: bs.Node):
        if node.exists():
            bs.animate(popup.node, 'opacity', {0: 1.0, 0.1: 0.0})
            bs.timer(0.1, popup.node.delete)
        
    with act().context:
        if getattr(actor, 'my_message', None):
            actor.my_message.node.delete()
        
        c = (1.0, 1.0, 1.0)
        position = (-0.0, 0.5, 0.0)

        m = bs.newnode('math', owner=actor.node, attrs={'input1':
            (position[0], position[1], position[2]), 'operation': 'add'})
        actor.node.connectattr('position_center', m, 'input2')
        
        actor.my_message = popup = PopupText(
             text=msg, color=c, scale=1.5).autoretain()
        m.connectattr('output', popup.node, 'position')
        bs.timer(5.0, bs.Call(die, popup.node))








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
        bs.timer(2.0, loc.delete)
    
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
        bs.timer(0.1 * i, bs.Call(anim, loc))
    
def stars(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.1, node.delete)
    
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
            bs.timer(0.25, bs.Call(die, node))
            
def chispitas(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.1, node.delete)
    
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
            bs.timer(0.25, bs.Call(die, node))
            
def darkmagic(self) -> None:
    def die(node: bs.Node) -> None:
        if node:
            m = node.mesh_scale
            bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
            bs.timer(0.1, node.delete)
    
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
            bs.timer(0.25, bs.Call(die, node))
            
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
        bs.timer(time, bs.Call(_changecolor, color))
           
def apply_effect(self, eff: str) -> None:
    if eff == 'fire':
        call = bs.Call(_fire, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'spark':
        call = bs.Call(_spark, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'footprint':
        call = bs.Call(footprint, self)
        self._cm_effect_timer = bs.Timer(0.15, call, repeat=True)
    elif eff == 'stars':
        call = bs.Call(stars, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'chispitas':
        call = bs.Call(chispitas, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'darkmagic':
        call = bs.Call(darkmagic, self)
        self._cm_effect_timer = bs.Timer(0.1, call, repeat=True)
    elif eff == 'rainbow':
        call = bs.Call(_rainbow, self)
        self._cm_effect_timer = bs.Timer(1.2, call, repeat=True)
    elif eff == 'aure':
        aure(self)
    
# -----------


def filter_chat_message(msg: str, client_id: int) -> None:
    command = Commands(msg, client_id, msg.split(' '))
    return command.get
    
def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    # bui.set_party_icon_always_visible(True)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)

def new_on_player_join(self, player: bs.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    
    # التحقق من الحظر قبل السماح للاعب بالانضمام
    try:
        client_id = player.sessionplayer.inputdevice.client_id
        pb_id = player.sessionplayer.get_v1_account_id()
        
        if ban_manager.is_banned(client_id, pb_id):
            ban_info = ban_manager.get_banned_player_info(client_id)
            if ban_info:
                reason = ban_info.get('reason', 'No reason specified')
                name = ban_info.get('name', 'Unknown')
                bs.disconnect_client(client_id)
                
                # إرسال رسالة للمضيف
                host_msg = getlanguage('Player Banned Join', subs=name)
                Uts.sm(host_msg, color=(1, 0, 0), transient=True)
                return
    except:
        pass
    
    Uts.player_join(player)
    
    # تطبيق التيجان إذا كان اللاعب لديه
    client_id = player.sessionplayer.inputdevice.client_id
    tag_info = tag_manager.get_tag_info(client_id)
    if tag_info:
        bs.timer(0.5, bs.Call(tag_manager.apply_tag_to_player, client_id))
    
def new_playerspaz_init_(self, *args, **kwargs) -> None:
    calls['PlayerSpazInit'](self, *args, **kwargs)
    Uts.update_usernames()

    try:
        user = self._player.sessionplayer.get_v1_account_id()
    except (AttributeError, ba.SessionPlayerNotFoundError):
        user = None
        
    if not hasattr(Uts, 'pdata'): 
        Uts.create_players_data()
    
    if user in Uts.pdata:
        eff = Uts.pdata[user]['Effect']
        apply_effect(self, eff)
    
    # تطبيق التيجان
    try:
        client_id = self._player.sessionplayer.inputdevice.client_id
        bs.timer(0.1, bs.Call(tag_manager.apply_tag_to_player, client_id))
    except:
        pass
            
def new_playerspaz_on_jump_press(self) -> None:    
    calls['OnJumpPress'](self)
    
    if not getattr(self, 'cm_superjump', False):
        return
        
    if (not self.node or not self.node.jump_pressed):
        return
    
    msg = bs.HitMessage(pos=self.node.position,
                        velocity=self.node.velocity,
                        magnitude=160*2,
                        hit_subtype='imp',
                        radius=460*2)
                      
    if isinstance(msg, bs.HitMessage):
        for i in range(2):
            with act().context:
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
            
# -----------


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
        bs.timer(0.1, bs.Call(
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

    def get_user_name(c_id: int) -> str:
        for r in roster():
            if r['client_id'] == c_id:
                if r['players'] == []:
                    return r['display_string']
                else:
                    return r['players'][0]['name_full']
            break
        return 'UNNAMED'

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

    def get_admins() -> list[str]:
        admins = []
        if not hasattr(Uts, 'pdata'): 
            Uts.create_players_data()
        
        if len(Uts.pdata) > 0:
            for p, d in getattr(Uts, 'pdata', {}).items():
                if d['Admin']:
                    admins.append(p)
        return admins

    def add_or_del_user(c_id: int, add: bool = True) -> None:
        if c_id == -1:
            return Uts.sm(getlanguage('You Are Amazing', subs=c_id), color=(0.5, 0, 1), clients=[c_id], transient=True)
            
        if c_id not in Uts.userpbs:
            Uts.sm(getlanguage('User Invalid', subs=c_id), clients=[c_id], transient=True)
        else:
            user = Uts.userpbs[c_id]
            if add:
                if not hasattr(Uts, 'pdata'): 
                    Uts.create_players_data()
                
                if user in Uts.pdata:
                    if not Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Add Admin Msg', subs=Uts.usernames[c_id]))
            else:
                if not hasattr(Uts, 'pdata'): 
                    Uts.create_players_data()
                
                if user in Uts.pdata:
                    if Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Delete Admin Msg', subs=Uts.usernames[c_id]))
            Uts.save_players_data()

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

    def save_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxPlayersData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.pdata, indent=4)
            f.write(w)

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
                    Uts.sm(getlanguage('Guardando Informacion'), color=(0.35, 0.7, 0.1), transient=True, clients=[client_id])
                
                accounts = Uts.pdata[account_id]['Accounts']
                if account_name not in accounts:
                    accounts.append(account_name)
                    Uts.save_players_data()
                    
                Uts.accounts[client_id] = Uts.pdata[account_id]
            
            Uts.usernames[client_id] = account_name
            Uts.useraccounts[client_id] = account_name
            Uts.players[client_id] = sessionplayer
                
    def update_usernames() -> None:
        for r in roster():
            c_id = r['client_id']
            if c_id not in Uts.accounts:
                if r['account_id'] in Uts.pdata:
                    Uts.accounts[c_id] = Uts.pdata[r['account_id']]
            if c_id not in Uts.usernames:
                Uts.usernames[c_id] = r['display_string']
                
            acc = r['display_string']
            for acc_id, dt in Uts.pdata.items():
                for ac in dt['Accounts']:
                    if ac == acc:
                        Uts.accounts[c_id] = Uts.pdata[acc_id]
                        Uts.userpbs[c_id] = acc_id
                        
        for c_id, p in Uts.players.items():
            if p.exists():
                Uts.usernames[c_id] = p.getname(full=True)
                Uts.shortnames[c_id] = p.getname(full=False)
                
                if p.get_v1_account_id() is not None:
                    Uts.userpbs[c_id] = p.get_v1_account_id()
            
    def add_player_data(account_id: str) -> None:
        if not hasattr(Uts, 'pdata'):
            Uts.create_players_data()
        
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'none',
                'Admin': False,
                'Accounts': []}
            Uts.save_players_data()

    def save_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxSettings.json'
        
        with open(file, 'w') as f:
            w = json.dumps(cfg, indent=4)
            f.write(w)

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

    def create_data_text(self) -> None:
        if isinstance(act(), MainMenuActivity):
            return

        if getattr(self, '_text_data', None):
            self._text_data.node.delete()

        if cfg['Commands'].get('ShowInfo'):
            info = getlanguage('Party Info', subs=[
                cfg['Commands'].get('HostName', '???'),
                cfg['Commands'].get('Description', '???')])
            color = tuple(list(cfg['Commands'].get('InfoColor', Uts.colors()['white'])) + [1])
                
            self._text_data = text.Text(info,
                position=(-650.0, -200.0), color=color)

    def create_live_chat(self,
                         live: bool = True,
                         chat: list[int, str] = None,
                         admin: bool = False) -> None:
        if isinstance(act(), MainMenuActivity):
            return
        
        if getattr(self, '_live_chat', None):
            self._live_chat.node.delete()
            
        if cfg['Commands'].get('ChatLive'):
            max = 6
            chats = list()
            txt = str()
            icon = bui.charstr(bui.SpecialChar.STEAM_LOGO) if admin else ''
            
            if any(bs.get_chat_messages()):
                if len(Chats) == max:
                    Chats.pop(0)
                    
                if live:
                    name = Uts.shortnames.get(chat[0], chat[0])
                    msg = chat[1]
                    Chats.append(f'{icon}{name}: {msg}')
                
                for msg in Chats:
                    if len(chats) != max:
                        chats.append(msg)
                    else: break
                txt = '\n'.join(chats)
            
            livetext = getlanguage('Chat Live')
            txt = (livetext + '\n' + ''.join(['=' for s 
                in range(len(livetext))]) + '\n') + txt

            self._live_chat = text.Text(txt, position=(650.0, 200.0),
                color=(1, 1, 1, 1), h_align=text.Text.HAlign.RIGHT)

    def funtion() -> str:
        return """    %s
    try:
        cm = babase.app.cheatmax_filter_chat(msg, client_id)
        if cm == '@':
            return None
    except Exception:
        pass
        """ % Uts.key




def _install() -> None:
    from bascenev1 import _hooks
    from babase import _app, modutils
    _file = Uts.directory_sys + "/bascenev1/_hooks.py"
    bs.app.cheatmax_filter_chat = filter_chat_message
    
    def seq():
        bs.screenmessage(getlanguage("Installing"))
        bs.apptimer(2.0, bs.Call(Uts.sm, getlanguage("Installed"), (0.0, 1.0, 0.0)))
        bs.apptimer(4.0, bs.Call(Uts.sm, getlanguage("Restart Msg")))
        bs.apptimer(6.0, bui.quit)
    
    # Create directories if they don't exist
    if not os.path.exists(Uts.directory_sys):
        os.makedirs(os.path.dirname(_file), exist_ok=True)
    
    try:
        if os.path.exists(_file):
            with open(_file, 'r') as s:
                read = s.read()
                read_l = read.split("\n")
            
            if Uts.key not in read:
                f_list = Uts.funtion().split("\n")
                try:
                    ix = read_l.index("def filter_chat_message(msg: str, client_id: int) -> str | None:")
                    for i, lt in enumerate(f_list):
                        read_l.insert(i + (ix + 1), lt)
                    read = "\n".join(read_l)
                    
                    # Try to write with backup
                    backup_file = _file + ".backup"
                    if os.path.exists(backup_file):
                        os.remove(backup_file)
                    os.rename(_file, backup_file)
                    
                    with open(_file, "w") as s:
                        s.write(read)
                    seq()
                except (ValueError, IndexError):
                    print("Could not find filter_chat_message function in _hooks.py")
                except PermissionError:
                    print("Permission denied to modify _hooks.py - skipping auto-injection")
                    # Try to continue without injection
        else:
            print(f"_hooks.py not found at {_file}")
    except Exception as e:
        print(f"Install error: {e}")
        # Continue anyway
    
    # Initialize data
    Uts.create_players_data()
    Uts.save_players_data()


def settings():
    global cfg
    Uts.create_settings()
    
    if cfg.get('Commands') is None:
        cfg['Commands'] = dict()
        Uts.save_settings()
 
def plugin():
    calls['GA_OnTransitionIn'] = bs.GameActivity.on_transition_in
    calls['OnJumpPress'] = PlayerSpaz.on_jump_press
    calls['OnPlayerJoin'] = Activity.on_player_join
    calls['PlayerSpazInit'] = PlayerSpaz.__init__

    
    bs.GameActivity.on_transition_in = new_ga_on_transition_in
    PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
    Activity.on_player_join = new_on_player_join
    PlayerSpaz.__init__ = new_playerspaz_init_
    # bui.set_party_icon_always_visible(True)


# ba_meta export babase.Plugin
class Install(bs.Plugin):
    def on_app_running(self) -> None:
        bs.apptimer(0.1, self.mod)

    def mod(self) -> None:
        plugin()
        settings()
        bs.apptimer(1.3, _install)
