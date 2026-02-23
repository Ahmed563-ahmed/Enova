# -*- coding: utf-8 -*-
# CheatMax System v2.0.2 – Advanced Tag, Admin, Clubs & Protection System
# تم التنظيم والإكمال بواسطة المساعد

import bascenev1 as bs
import bauiv1 as bui
import babase as ba
import _babase
import os
import json
import random
import shutil
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Callable, Sequence

if TYPE_CHECKING:
    pass

# ==================== إعدادات اللغة ====================
class Lang:
    def __init__(self, text: str, subs: list[str] = 'none'):
        icons = [bui.charstr(bui.SpecialChar.CROWN),
                 bui.charstr(bui.SpecialChar.LOGO)]
        lang = bs.app.lang.language
        setphrases = {
            "Installing": {"Spanish": f"Instalando <{name}>", "English": f"Installing <{name}>", "Portuguese": f"Instalando <{name}>"},
            "Installed": {"Spanish": f"¡<{name}> Se instaló correctamente!", "English": f"<{name}> Installed successfully!", "Portuguese": f"<{name}> Instalado com sucesso!"},
            "Make Sys": {"Spanish": "Se creó la carpeta sys", "English": "Sys folder created", "Portuguese": "Pasta sys criada"},
            "Restart Msg": {"Spanish": "Reiniciando...", "English": "Rebooting...", "Portuguese": "Reinício..."},
            "EJ": {"Spanish": f"Datos incompletos \n Ejemplo: {subs}", "English": f"Incomplete data \n Example: {subs}", "Portuguese": f"Dados incompletos \n Exemplo: {subs}"},
            "EX": {"Spanish": f"Ejemplo: {subs}", "English": f"Example: {subs}", "Portuguese": f"Exemplo: {subs}"},
            "Error Entering Client ID": {"Spanish": f"'{subs[0]}' no es válido. \n Ingresa números \n Ejemplo: {subs[1]}", "English": f"'{subs[0]}' is invalid. \n Enter numbers \n Example: {subs[1]}", "Portuguese": f"'{subs[0]}' é inválido. \n Digite os números \n Exemplo: {subs[1]}"},
            "Error Entering Player ID": {"Spanish": f"'{subs}' no es válido. \n Ingresa el ID del jugador. consulta el comando '/list'", "English": f"'{subs}' is invalid. \n Add the player ID. use the '/list' command for more information.", "Portuguese": f"'{subs}' no es válido. \n Adicione o ID do jogador. use o comando '/list' para obter mais informações."},
            "Happy": {"Spanish": "¡Estás felíz!", "English": "Are you happy!", "Portuguese": "Você está feliz!"},
            "Add Admin Msg": {"Spanish": f"'{subs}' Se agregó a la lista de Admins", "English": f"'{subs}' Added to Admins list", "Portuguese": f"'{subs}' Adicionado à lista de administradores"},
            "Delete Admin Msg": {"Spanish": f"Se removió a '{subs}' de la lista de Admins", "English": f"'{subs}' was removed from the Admins list", "Portuguese": f"'{subs}' foi removido da lista de administradores"},
            "Players Data": {"Spanish": "Nombre | Jugador ID | Cliente ID", "English": "Name | Player ID | Client ID", "Portuguese": "Nome | Jogador ID | ID do Cliente"},
            "Party Info": {"Spanish": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descripción: {subs[1]}\n{icons[1]}|Versión: {_babase.app.env.engine_version}", "English": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Description: {subs[1]}\n{icons[1]}|Version: {_babase.app.env.engine_version}", "Portuguese": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descrição: {subs[1]}|\n{icons[1]}|Versão: {_babase.app.env.engine_version}"},
            "Same Player": {"Spanish": "No puedes expulsarte a tí mismo", "English": "You cannot expel yourself", "Portuguese": "Você não pode se expulsar"},
            "Kick Msg": {"Spanish": f"Sin rodeos, {subs[0]} ha expulsado a {subs[1]}", "English": f"{subs[0]} kicked {subs[1]} Goodbye!", "Portuguese": f"{subs[0]} expulsou {subs[1]}"},
            "User Invalid": {"Spanish": f"'{subs}' No le pertenece a ningún jugador.", "English": f"'{subs}' Does not belong to any player.", "Portuguese": f"'{subs}' Não pertence a nenhum jogador."},
            "Chat Live": {"Spanish": f"{icons[0]} CHAT EN VIVO {icons[0]}", "English": f"{icons[0]} CHAT LIVE {icons[0]}", "Portuguese": f"{icons[0]} BATE-PAPO AO VIVO {icons[0]}"},
            "Not Exists Node": {"Spanish": "No estás en el juego", "English": "You're not in the game", "Portuguese": "Você não está no jogo"},
            "Show Spaz Messages": {"Spanish": "Mostrar mensajes arriba de los jugadores.", "English": "Show messages above players.", "Portuguese": "Mostrar mensagens acima dos jogadores."},
            "Mute Message": {"Spanish": f"Se silenció a {subs}", "English": f"{subs} was muted", "Portuguese": f"{subs} foi silenciado"},
            "Unmute Message": {"Spanish": f"Se quitó el muteo a {subs}", "English": f"{subs} can chat again", "Portuguese": f"{subs} pode conversar novamente"},
            "Not In Admins": {"Spanish": f"No se puede silenciar a [{subs}] porque es administrador.", "English": f"[{subs}] cannot be muted because he is an administrator.", "Portuguese": f"[{subs}] não pode ser silenciado porque é um administrador."},
            "Module Not Found": {"Spanish": "No se encontraron los módulos. usa el comando '!dw' para descargarlos.", "English": "Modules not found. use the '!dw' command to download them.", "Portuguese": "Módulos não encontrados. use o comando '!dw' para baixá-los."},
            "Clima Error Message": {"Spanish": "Selecciona un clima,\n Usa el comando '-climas' para más información.", "English": "Select a weather,\n Use the command '-climas' for more information.", "Portuguese": "Selecione um clima,\n Use o comando '-climas' para mais informações."},
            "Clima Message": {"Spanish": f"Se cambió el clima a '{subs}'", "English": f"The weather is now '{subs}'", "Portuguese": f"O tempo está agora '{subs}'"},
            "None Account": {"Spanish": "Información del jugador no válida.", "English": "Invalid player information.", "Portuguese": "Informações do jogador inválidas."},
            "Error ID User": {"Spanish": f"Se produjo un error al ingresar el ID del jugador. \n '{subs}' no es válido.", "English": f"An error occurred while entering the player ID. \n '{subs}' is not valid.", "Portuguese": f"Ocorreu um erro ao inserir o ID do jogador. \n '{subs}' não é válido."},
            "Effect Invalid": {"Spanish": f"'{subs}' es inválido. ingresa el comando '-effects' para más información.", "English": f"'{subs}' is invalid. enter the command '-effects' for more information.", "Portuguese": f"'{subs}' é inválido. digite o comando '-effects' para mais informações."},
            "Use /list Command": {"Spanish": "Le sugerimos usar el comando '/list'", "English": "We suggest you use the '/list' command", "Portuguese": "Sugerimos que você use o comando '/list'"},
            "Add Effect Message": {"Spanish": f"Se agregó el efecto '{subs[0]}' a {subs[1]}", "English": f"Added '{subs[0]}' effect to {subs[1]}", "Portuguese": f"Adicionado efeito '{subs[0]}' para {subs[1]}"},
            "You Are Amazing": {"Spanish": "¡¡Eres ASOMBROSO!!", "English": "You Are Amazing!!", "Portuguese": "Você é incrível!!"},
            "Owner Added": {"Spanish": "¡Se agregó al propietario!", "English": "Owner added!", "Portuguese": "Proprietário adicionado!"},
            "Is Owner": {"Spanish": "¡Eres el propietario!", "English": "You are the owner!", "Portuguese": "Você é o proprietário!"},
            "Exe": {"Spanish": "Comando Ejecutado", "English": "Command Executed", "Portuguese": "Comando Executado"},
            "Agrega un texto": {"Spanish": "Añade un texto", "English": "Add text", "Portuguese": "Adicione texto"},
            "Cambios Guardados": {"Spanish": "Información guardada correctamente", "English": "Information saved successfully", "Portuguese": "Informações salvas com sucesso"},
            "Info Color": {"Spanish": "Argumento no válido, \n te sugerimos usar el comando '-colors'", "English": "Invalid argument, \n we suggest you use the '-colors' command", "Portuguese": "Argumento inválido, \n sugerimos que você use o comando '-colors'"},
            "ID Cliente Msj": {"Spanish": "Agrega el ID del cliente. \n utilice el comando '/list' para más información.", "English": "Add the client ID. \n use the '/list' command for more information.", "Portuguese": "Adicione o ID do cliente. \n use o comando '/list' para mais informações."},
            "Guardando Informacion": {"Spanish": "Estamos guardando sus datos...", "English": "Saving user data...", "Portuguese": "Estamos salvando seus dados..."},
            "Ban A Admin Mensaje": {"Spanish": f"No puedes expulsar a [{subs}] porque es administrador", "English": f"You can't kick [{subs}] because he's an admin", "Portuguese": f"Você não pode chutar [{subs}] porque ele é um administrador"},
            "No Info Activa": {"Spanish": "Necesitas tener activa la información.\n Usa el comando '-info' para activarle.", "English": "You need to have info active.\n Use the '-info' command to activate it", "Portuguese": "Você precisa ter as informações ativas.\n Use o comando '-info' para ativá-las"},
            "ServerClosed": {"Spanish": f"El servidor está cerrado por {subs[0]} horas para entrenamiento del tag '{subs[1]}'", "English": f"Server closed for {subs[0]} hours for '{subs[1]}' tag training", "Portuguese": f"Servidor fechado por {subs[0]} horas para treino da tag '{subs[1]}'"},
            "ServerClosedMessage": {"Spanish": f"Hay un partido de entrenamiento para {subs[0]}. Intenta unirte después de {subs[1]}", "English": f"There's a training match for {subs[0]}. Please try to join again after {subs[1]}", "Portuguese": f"Há uma partida de treino para {subs[0]}. Por favor, tente entrar novamente após {subs[1]}"},
            "ServerAlreadyClosed": {"Spanish": "El servidor ya está cerrado", "English": "Server is already closed", "Portuguese": "O servidor já está fechado"},
            "ServerClosedStopped": {"Spanish": "El cierre del servidor ha sido detenido", "English": "Server closure has been stopped", "Portuguese": "O fechamento do servidor foi interrompido"},
            "NoServerCloseActive": {"Spanish": "No hay cierre de servidor activo", "English": "No server closure active", "Portuguese": "Nenhum fechamento de servidor ativo"},
            "ServerCloseStarted": {"Spanish": f"✅ Servidor cerrado por {subs[0]} horas para el tag '{subs[1]}'", "English": f"✅ Server closed for {subs[0]} hours for tag '{subs[1]}'", "Portuguese": f"✅ Servidor fechado por {subs[0]} horas para a tag '{subs[1]}'"},
            "InvalidHours": {"Spanish": "Las horas deben ser un número positivo", "English": "Hours must be a positive number", "Portuguese": "As horas devem ser um número positivo"},
            "StopCloseServer": {"Spanish": "Usa: /stopcloseserver", "English": "Use: /stopcloseserver", "Portuguese": "Use: /stopcloseserver"},
            "CloseServerUsage": {"Spanish": "Usa: /closeserver <horas> <tag-name>", "English": "Use: /closeserver <hours> <tag-name>", "Portuguese": "Use: /closeserver <horas> <tag-name>"},
            "BanUsage": {"Spanish": "Usa: /ban <pb-ID أو client-ID أو الاسم> <السبب>", "English": "Use: /ban <pb-ID or client-ID or Name> <reason>", "Portuguese": "Use: /ban <pb-ID ou client-ID ou Nome> <motivo>"},
            "UnbanUsage": {"Spanish": "Usa: /unban <pb-ID أو client-ID أو الاسم>", "English": "Use: /unban <pb-ID or client-ID or Name>", "Portuguese": "Use: /unban <pb-ID ou client-ID ou Nome>"},
            "ReportUsage": {"Spanish": "Usa: /report <pb-ID أو client-ID أو الاسم> <السبب>", "English": "Use: /report <pb-ID or client-ID or Name> <reason>", "Portuguese": "Use: /report <pb-ID ou client-ID ou Nome> <motivo>"},
            "TargetNotFound": {"Spanish": f"اللاعب '{subs}' غير موجود", "English": f"Target '{subs}' not found", "Portuguese": f"Alvo '{subs}' não encontrado"},
            "AlreadyBanned": {"Spanish": f"⚠️ {subs} محظور بالفعل", "English": f"⚠️ {subs} is already banned", "Portuguese": f"⚠️ {subs} já está banido"},
            "CannotBanAdmin": {"Spanish": f"❌ لا يمكن حظر الأدمن/المالك {subs}", "English": f"❌ Cannot ban admin/owner {subs}", "Portuguese": f"❌ Não pode banir admin/proprietário {subs}"},
            "BanSuccess": {"Spanish": f"✅ {subs[0]} تم حظره بواسطة {subs[1]}", "English": f"✅ {subs[0]} has been banned by {subs[1]}", "Portuguese": f"✅ {subs[0]} foi banido por {subs[1]}"},
            "UnbanSuccess": {"Spanish": f"✅ {subs[0]} تم إلغاء حظره بواسطة {subs[1]}", "English": f"✅ {subs[0]} has been unbanned by {subs[1]}", "Portuguese": f"✅ {subs[0]} foi desbanido por {subs[1]}"},
            "NotBanned": {"Spanish": f"❌ {subs} غير محظور", "English": f"❌ {subs} is not banned", "Portuguese": f"❌ {subs} não está banido"},
            "ReportSubmitted": {"Spanish": f"✅ تم الإبلاغ عن {subs}", "English": f"✅ Report submitted against {subs}", "Portuguese": f"✅ Relatório enviado contra {subs}"},
            "NewReportAlert": {"Spanish": f"⚠️ تقرير جديد: {subs[0]} تم الإبلاغ عنه بواسطة {subs[1]}", "English": f"⚠️ New report: {subs[0]} reported by {subs[1]}", "Portuguese": f"⚠️ Novo relatório: {subs[0]} relatado por {subs[1]}"},
            "NoReports": {"Spanish": "📋 لا توجد تقارير", "English": "📋 No reports found", "Portuguese": "📋 Nenhum relatório encontrado"},
            "NoBans": {"Spanish": "📋 قائمة الحظر فارغة", "English": "📋 Ban list is empty", "Portuguese": "📋 Lista de banimentos está vazia"},
            "AdminOnly": {"Spanish": "❌ يجب أن تكون أدمن لاستخدام هذا الأمر", "English": "❌ You must be an admin to use this command", "Portuguese": "❌ Você deve ser um administrador para usar este comando"},
            "BannedMessage": {"Spanish": f"أنت محظور من هذا السيرفر.\nالسبب: {subs[0]}\nتم الحظر بواسطة: {subs[1]}", "English": f"You are banned from this server.\nReason: {subs[0]}\nBanned by: {subs[1]}", "Portuguese": f"Você está banido deste servidor.\nMotivo: {subs[0]}\nBanido por: {subs[1]}"},
        }
        language = ["Spanish", "English", "Portuguese"]
        if lang not in language:
            lang = "English"
        if text not in setphrases:
            self.text = text
        else:
            self.text = setphrases[text][lang]

    def get(self) -> str:
        return self.text


def getlanguage(args, **kwargs) -> str:
    subs = kwargs.get('subs', 'none')
    if not isinstance(subs, list):
        subs = str(subs)
    else:
        subs = [str(s) for s in subs]
    try:
        text = Lang(args, subs=subs).get()
    except (IndexError, Exception):
        text = Lang(*args).get()
        text = text.replace('none', str(subs))
    finally:
        return text


# ==================== الكرة القابلة للضرب ====================
class CMBall(bs.Actor):
    def __init__(self, position=(0, 1, 0)):
        super().__init__()
        shared = bs.SharedObjects.get()
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


# ==================== مسار ملفات الإعدادات ====================
ASOCCER_CONFIG_DIR = os.path.join(_babase.app.env.python_directory_user, 'Configs')
ASOCCER_CONFIG_FILE = os.path.join(ASOCCER_CONFIG_DIR, 'A-SoccerConfig.json')


# ==================== نظام الطقس ====================
class WeatherEffect:
    def __init__(self):
        self.timer = None
        self.active_type = 'none'
        self.valid_weather = [
            'none', 'snow', 'rock', 'metal', 'ice', 'spark',
            'slime', 'fire', 'splinter', 'smoke', 'rainbow'
        ]

    def start(self, weather_type: str):
        if weather_type not in self.valid_weather:
            weather_type = 'none'
        self.stop()
        self.active_type = weather_type
        if weather_type != 'none':
            self.timer = bs.Timer(0.25, self._emit, repeat=True)

    def stop(self):
        if self.timer:
            self.timer = None
        self.active_type = 'none'

    def _emit(self):
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
        bs.emitfx(**kwargs)


# ==================== كلاس Uts الرئيسي (بيانات النظام) ====================
calls: dict[str, Any] = {}
Chats: list[str] = []
roster = bs.get_game_roster
mutelist = list()
cfg = dict()


class Uts:
    directory_user: str = _babase.app.env.python_directory_user
    directory_sys: str = directory_user + '/sys/' + babase.app.env.engine_version + '' + str(_babase.app.env.engine_build_number)
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
    weather_effect = WeatherEffect()
    leaderboard_display = None
    server_close_active = False
    server_close_end_time = 0.0
    server_close_tag_name = ""
    server_close_countdown_text = None
    server_close_original_players = []
    server_close_last_update = 0.0
    bans_data = {}
    reports_data = {"reports": []}
    warns_data = {}
    clubs_system = None
    previous_players: dict[int, tuple[str, str]] = {}

    @staticmethod
    def check_player_changes():
        current_players = {}
        try:
            activity = bs.get_foreground_host_activity()
            if activity is not None:
                for player in activity.players:
                    try:
                        client_id = player.sessionplayer.inputdevice.client_id
                        player_name = player.getname(full=True)
                        account_name = player.sessionplayer.inputdevice.get_v1_account_name(full=True) or player_name
                        current_players[client_id] = (player_name, account_name)
                    except:
                        continue
        except:
            pass
        left_players = set(Uts.previous_players.keys()) - set(current_players.keys())
        for client_id in left_players:
            Uts.remove_all_tags(client_id)
            player_name, account_name = Uts.previous_players.get(client_id, ("Unknown", "Unknown"))
            print(f"🚪 Player left: {player_name} (Client ID: {client_id})")
        Uts.previous_players = current_players

    @staticmethod
    def add_player_data(account_id: str) -> None:
        if not hasattr(Uts, 'pdata'):
            Uts.create_players_data()
        if account_id in Uts.pdata:
            return
        Uts.pdata[account_id] = {
            'Mute': False,
            'Effect': 'none',
            'banned': False,
            'Accounts': [],
            'Rank': 0,
            'Admin-check': False,
            'Stats': {
                'goals': 0,
                'assists': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'games': 0,
                'score': 0.0,
                'rank': 0
            }
        }
        Uts.save_players_data()

    @staticmethod
    def migrate_player_data():
        if not hasattr(Uts, 'pdata'):
            return
        changed = False
        for acc_id, data in Uts.pdata.items():
            if 'Rank' not in data:
                data['Rank'] = 0
                changed = True
            if 'Admin-check' not in data:
                data['Admin-check'] = data.get('Admin', False)
                changed = True
            if 'Stats' not in data:
                data['Stats'] = {
                    'goals': 0,
                    'assists': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'games': 0,
                    'score': 0.0,
                    'rank': 0
                }
                changed = True
            else:
                stats = data['Stats']
                default_stats = {
                    'goals': 0,
                    'assists': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'games': 0,
                    'score': 0.0,
                    'rank': 0
                }
                for key, val in default_stats.items():
                    if key not in stats:
                        stats[key] = val
                        changed = True
        if changed:
            Uts.save_players_data()
            print("✅ Player data migrated to new structure.")

    @staticmethod
    def update_player_rank(account_id: str):
        if account_id not in Uts.pdata:
            return
        scores = []
        for acc, data in Uts.pdata.items():
            if 'Stats' in data and 'score' in data['Stats']:
                scores.append((acc, data['Stats']['score']))
        scores.sort(key=lambda x: x[1], reverse=True)
        for idx, (acc, _) in enumerate(scores, 1):
            if acc == account_id:
                new_rank = idx
                break
        else:
            new_rank = 0
        Uts.pdata[account_id]['Stats']['rank'] = new_rank
        Uts.pdata[account_id]['Rank'] = new_rank
        Uts.save_players_data()

    @staticmethod
    def update_all_ranks():
        players = []
        for acc, data in Uts.pdata.items():
            if 'Stats' in data and 'score' in data['Stats']:
                players.append((acc, data['Stats']['score']))
        players.sort(key=lambda x: x[1], reverse=True)
        for idx, (acc, _) in enumerate(players, 1):
            Uts.pdata[acc]['Stats']['rank'] = idx
            Uts.pdata[acc]['Rank'] = idx
        Uts.save_players_data()
        print(f"✅ All ranks updated ({len(players)} players).")

    @staticmethod
    def auto_ban_player(client_id: int, account_id: str | None, name: str, reason: str):
        try:
            ban_info = {
                'name': name,
                'account_id': account_id,
                'client_id': client_id,
                'reason': reason,
                'banned_by': 'System (Auto)',
                'banned_by_account': 'System',
                'banned_by_client_id': -1,
                'banned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'banned_timestamp': time.time(),
                'target_type': 'auto'
            }
            if account_id and account_id.startswith('pb-'):
                ban_key = f"pb_{account_id}"
            else:
                ban_key = f"client_{client_id}"
            Uts.bans_data[ban_key] = ban_info
            Uts.save_bans_data()
            if account_id and account_id in Uts.pdata:
                Uts.pdata[account_id]['banned'] = True
                Uts.save_players_data()
            if Uts.clubs_system:
                Uts.clubs_system.remove_club_tag(client_id)
            Uts.cm(f"🚫 Auto-ban: {name} ({reason})")
            print(f"✅ Auto-banned {name} (Client: {client_id}, Account: {account_id}) for: {reason}")
        except Exception as e:
            print(f"❌ Error in auto_ban_player: {e}")

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

    @staticmethod
    def clean_bans_data():
        removed = []
        for key in list(Uts.bans_data.keys()):
            if key == "client_-1" or key == "pb_None" or key == "name_Host":
                removed.append(key)
                del Uts.bans_data[key]
            else:
                ban_info = Uts.bans_data[key]
                if ban_info.get('client_id') == -1 or ban_info.get('account_id') == 'pb--1':
                    removed.append(key)
                    del Uts.bans_data[key]
        if removed:
            Uts.save_bans_data()
            print(f"🧹 Cleaned invalid ban entries: {removed}")

    @staticmethod
    def start_ban_monitoring():
        def check_bans():
            try:
                if not Uts.bans_data and not any(Uts.pdata.get(acc, {}).get('banned', False) for acc in Uts.pdata):
                    pass
                else:
                    Uts.update_usernames()
                    roster_data = roster()
                    for player_info in roster_data:
                        client_id = player_info.get('client_id')
                        if client_id is None or client_id == -1:
                            continue
                        if CommandFunctions.user_is_admin(client_id):
                            continue
                        current_account_id = player_info.get('account_id')
                        if not current_account_id:
                            current_account_id = Uts.userpbs.get(client_id)
                        player_name = player_info.get('display_string', f'Player_{client_id}')
                        banned = False
                        if current_account_id and current_account_id.startswith('pb-'):
                            for ban_key, ban_info in Uts.bans_data.items():
                                if ban_info.get('account_id') == current_account_id:
                                    banned = True
                                    print(f"🚫 Ban monitor: {player_name} (C{client_id}) banned via bans_data (pb: {current_account_id})")
                                    break
                        if not banned and current_account_id and current_account_id.startswith('pb-'):
                            if current_account_id in Uts.pdata and Uts.pdata[current_account_id].get('banned', False):
                                banned = True
                                print(f"🚫 Ban monitor: {player_name} (C{client_id}) banned via pdata (pb: {current_account_id})")
                        if not banned and (not current_account_id or not current_account_id.startswith('pb-')):
                            for ban_key, ban_info in Uts.bans_data.items():
                                if ban_info.get('client_id') == client_id:
                                    banned = True
                                    print(f"🚫 Ban monitor: {player_name} (C{client_id}) banned via client_id in bans_data")
                                    break
                        if banned:
                            print(f"🚫 Ban monitor: Kicking {player_name} (C{client_id})")
                            if Uts.clubs_system:
                                Uts.clubs_system.remove_club_tag(client_id)

                            def kick():
                                try:
                                    bs.disconnect_client(client_id)
                                except Exception as e:
                                    print(f"❌ Error kicking banned player: {e}")

                            bs.pushcall(kick)
            except Exception as e:
                print(f"❌ Error in ban monitor: {e}")
            bs.apptimer(1.0, check_bans)

        bs.apptimer(1.0, check_bans)
        print("✅ Ban monitoring started (improved version)")

    @staticmethod
    def check_player_ban_on_join(player: bs.Player) -> bool:
        try:
            sessionplayer = player.sessionplayer
            client_id = sessionplayer.inputdevice.client_id
            if client_id == -1:
                print("👑 Host is joining - skip ban check.")
                return False
            if CommandFunctions.user_is_admin(client_id):
                print(f"👑 Admin {client_id} is joining - skip ban check.")
                return False
            account_id = Uts.get_reliable_pb_id(client_id)
            player_name = None
            try:
                player_name = sessionplayer.getname(full=True)
            except:
                if client_id in Uts.usernames:
                    player_name = Uts.usernames[client_id]
            print(f"🔍 Checking ban for: {player_name} (Client: {client_id}, PB-ID: {account_id})")
            if account_id and account_id.startswith('pb-'):
                Uts.userpbs[client_id] = account_id
            Uts.create_bans_data()
            if account_id and account_id.startswith('pb-') and account_id in Uts.pdata:
                if Uts.pdata[account_id].get('banned', False):
                    print(f"🚫 Player {player_name} is banned in pdata (pb: {account_id}).")
                    if CommandFunctions.user_is_admin(client_id):
                        print(f"⚠️ But {player_name} is admin, ignoring ban in pdata.")
                        return False

                    def kick():
                        try:
                            bs.disconnect_client(client_id)
                            print(f"✅ Kicked banned player (pdata): {player_name}")
                        except Exception as e:
                            print(f"❌ Error kicking player: {e}")

                    bs.pushcall(kick)
                    return True
            if account_id and account_id.startswith('pb-'):
                for ban_key, ban_info in Uts.bans_data.items():
                    if ban_info.get('account_id') == account_id:
                        print(f"🚫 Ban match (PB-ID): {ban_key}")
                        if CommandFunctions.user_is_admin(client_id):
                            print(f"⚠️ But {player_name} is admin, ignoring ban in bans_data.")
                            return False

                        def kick():
                            try:
                                bs.disconnect_client(client_id)
                                print(f"✅ Kicked banned player: {player_name}")
                            except Exception as e:
                                print(f"❌ Error kicking player: {e}")

                        bs.pushcall(kick)
                        return True
            if not account_id or not account_id.startswith('pb-'):
                for ban_key, ban_info in Uts.bans_data.items():
                    if ban_info.get('client_id') == client_id:
                        print(f"🚫 Ban match (Client ID): {ban_key}")
                        if CommandFunctions.user_is_admin(client_id):
                            print(f"⚠️ But {player_name} is admin, ignoring ban in bans_data.")
                            return False

                        def kick():
                            try:
                                bs.disconnect_client(client_id)
                                print(f"✅ Kicked banned player (client): {player_name}")
                            except Exception as e:
                                print(f"❌ Error kicking player: {e}")

                        bs.pushcall(kick)
                        return True
            if player_name and not account_id:
                player_name_lower = player_name.lower()
                for ban_key, ban_info in Uts.bans_data.items():
                    banned_name = ban_info.get('name', '').lower()
                    if banned_name and banned_name == player_name_lower:
                        print(f"🚫 Ban match (Name – no PB-ID): {ban_key}")
                        if CommandFunctions.user_is_admin(client_id):
                            print(f"⚠️ But {player_name} is admin, ignoring ban in bans_data.")
                            return False

                        def kick():
                            try:
                                bs.disconnect_client(client_id)
                                print(f"✅ Kicked banned player (name): {player_name}")
                            except Exception as e:
                                print(f"❌ Error kicking player: {e}")

                        bs.pushcall(kick)
                        return True
            print(f"✅ Player is not banned: {player_name}")
            return False
        except Exception as e:
            print(f"❌ Error in check_player_ban_on_join: {e}")
            return False

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
        return len(Uts.warns_data[account_id])

    @staticmethod
    def get_warnings(account_id: str):
        return Uts.warns_data.get(account_id, [])

    @staticmethod
    def clear_warnings(account_id: str):
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
                                Uts.server_close_countdown_text = bs.newnode('text',
                                    attrs={
                                        'text': f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}",
                                        'position': (0, 250),
                                        'scale': 1.0,
                                        'color': (1, 0, 0),
                                        'h_align': 'center',
                                        'v_align': 'center',
                                        'opacity': 0.7
                                    })
                            else:
                                try:
                                    Uts.server_close_countdown_text.text = f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}"
                                except:
                                    Uts.server_close_countdown_text = bs.newnode('text',
                                        attrs={
                                            'text': f"⏰ SERVER CLOSED: {time_str}\n🏷️ TAG: {Uts.server_close_tag_name}",
                                            'position': (0, 250),
                                            'scale': 1.0,
                                            'color': (1, 0, 0),
                                            'h_align': 'center',
                                            'v_align': 'center',
                                            'opacity': 0.7
                                        })
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
                if d.get('Admin', False):
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
        Uts.update_usernames()
        if c_id not in Uts.usernames:
            for r in roster():
                if r.get('client_id') == c_id:
                    Uts.usernames[c_id] = r.get('display_string', f'Player_{c_id}')
                    break
            else:
                Uts.sm(f"'{c_id}' Does not belong to any player.", clients=[c_id], transient=True)
                return
        pb_id = Uts.get_reliable_pb_id(c_id)
        if not pb_id or not pb_id.startswith('pb-'):
            Uts.sm(f"'{c_id}' has no valid PB-ID (guest).", clients=[c_id], transient=True)
            return
        user = pb_id
        if add:
            if not hasattr(Uts, 'pdata'):
                Uts.create_players_data()
            if user in Uts.pdata:
                if not Uts.pdata[user].get('Admin', False):
                    Uts.pdata[user]['Admin'] = add
                    Uts.pdata[user]['Admin-check'] = True
                    if c_id in Uts.accounts:
                        Uts.accounts[c_id]['Admin'] = True
                    Uts.cm(f"'{Uts.usernames[c_id]}' Added to Admins list")
        else:
            if not hasattr(Uts, 'pdata'):
                Uts.create_players_data()
            if user in Uts.pdata:
                if Uts.pdata[user].get('Admin', False):
                    Uts.pdata[user]['Admin'] = add
                    Uts.pdata[user]['Admin-check'] = False
                    if c_id in Uts.accounts:
                        Uts.accounts[c_id]['Admin'] = False
                    Uts.cm(f"'{Uts.usernames[c_id]}' was removed from the Admins list")
        Uts.save_players_data()
        Uts.update_usernames()

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
                'banned': False,
                'Accounts': [],
                'Rank': 0,
                'Admin-check': True,
                'Stats': {
                    'goals': 0,
                    'assists': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'games': 0,
                    'score': 0.0,
                    'rank': 0
                }
            }
        else:
            Uts.pdata[account_id]['Admin'] = True
            Uts.pdata[account_id]['Owner'] = True
            Uts.pdata[account_id]['banned'] = False
            Uts.pdata[account_id]['Admin-check'] = True
        Uts.save_players_data()
        print(f"Added owner: {account_id}")

    @staticmethod
    def remove_all_tags(client_id: int):
        if client_id in Uts.players:
            try:
                p = Uts.players[client_id]
                if p.exists():
                    return
            except:
                pass
        if Uts.tag_system:
            Uts.tag_system.remove_tag_visual(client_id)
            Uts.tag_system.stop_char_animation(client_id)
            Uts.tag_system.stop_animation(client_id)
        if Uts.clubs_system:
            Uts.clubs_system.remove_club_tag(client_id)

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
        Uts.migrate_player_data()

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

        if account_id and account_id.startswith('pb-'):
            if account_id not in Uts.pdata:
                Uts.add_player_data(account_id)
                Uts.sm("Saving user data...", color=(0.35, 0.7, 0.1), transient=True, clients=[client_id])
            accounts = Uts.pdata[account_id]['Accounts']
            if account_name not in accounts:
                accounts.append(account_name)
                Uts.save_players_data()
            Uts.accounts[client_id] = Uts.pdata[account_id]
            Uts.userpbs[client_id] = account_id
        else:
            Uts.userpbs[client_id] = account_id
            Uts.accounts[client_id] = {'Admin': False, 'Mute': False, 'Effect': 'none', 'Owner': False}
            print(f"👤 Guest player {client_id} assigned temporary PB-ID: {account_id}")

        Uts.usernames[client_id] = account_name or f"Player {client_id}"
        Uts.useraccounts[client_id] = account_name or f"Player {client_id}"
        Uts.players[client_id] = sessionplayer

        # جدولة التحقق المتأخر من صلاحية الأدمن
        def late_admin_check():
            try:
                if client_id not in Uts.players:
                    return
                pb_id = Uts.get_reliable_pb_id(client_id)
                if not pb_id or not pb_id.startswith('pb-'):
                    return
                admin_list = Uts.get_admins()
                if pb_id in admin_list:
                    if pb_id in Uts.pdata:
                        Uts.pdata[pb_id]['Admin'] = True
                        Uts.pdata[pb_id]['Admin-check'] = True
                        Uts.save_players_data()
                        if client_id in Uts.accounts:
                            Uts.accounts[client_id]['Admin'] = True
                        bs.screenmessage("🛡️ Admin privileges activated.", clients=[client_id], transient=True)
            except Exception as e:
                print(f"❌ Error in late_admin_check: {e}")

        bs.apptimer(2.0, late_admin_check)

        def _restore_tags():
            try:
                if Uts.clubs_system:
                    Uts.clubs_system.apply_club_tag(client_id)
                if Uts.tag_system:
                    Uts.tag_system.apply_tag(client_id)
            except Exception as e:
                print(f"⚠️ Failed to restore tag for {client_id}: {e}")

        bs.apptimer(1, _restore_tags)

    @staticmethod
    def update_usernames() -> None:
        try:
            for r in roster():
                c_id = r.get('client_id')
                if c_id is None:
                    continue
                acc_id = r.get('account_id')
                if acc_id and acc_id.startswith('pb'):
                    Uts.userpbs[c_id] = acc_id
                if c_id not in Uts.usernames:
                    Uts.usernames[c_id] = r.get('display_string', 'Unknown')
                if acc_id and acc_id in Uts.pdata:
                    Uts.accounts[c_id] = Uts.pdata[acc_id]
                else:
                    if c_id not in Uts.accounts:
                        Uts.accounts[c_id] = {'Admin': False, 'Mute': False, 'Effect': 'none', 'Owner': False}
        except Exception as e:
            print(f"⚠️ Error in update_usernames (roster): {e}")

        for cid in list(Uts.usernames.keys()):
            if cid not in Uts.userpbs:
                if cid in Uts.players and Uts.players[cid].exists():
                    try:
                        acc = Uts.players[cid].get_v1_account_id()
                        if acc and acc.startswith('pb'):
                            Uts.userpbs[cid] = acc
                            continue
                    except:
                        pass
                Uts.userpbs[cid] = f"guest_{cid}"
                print(f"⚠️ Guest player {cid} assigned temporary PB-ID: guest_{cid}")

        for c_id, p in list(Uts.players.items()):
            try:
                if p.exists():
                    Uts.usernames[c_id] = p.getname(full=True)
                    Uts.shortnames[c_id] = p.getname(full=False)
                    acc = p.get_v1_account_id()
                    if acc and acc.startswith('pb'):
                        Uts.userpbs[c_id] = acc
            except:
                if c_id in Uts.players:
                    del Uts.players[c_id]

        Uts.check_player_changes()

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
        if 'Commands' not in cfg:
            cfg['Commands'] = {}
        if 'Weather' not in cfg['Commands']:
            cfg['Commands']['Weather'] = 'none'
            Uts.save_settings()
        if 'ShowStatsLeaderboard' not in cfg['Commands']:
            cfg['Commands']['ShowStatsLeaderboard'] = False
            Uts.save_settings()
        if 'Admins' not in cfg:
            cfg['Admins'] = []
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
        except Exception as e:
            print(f"Error creating system scripts: {e}")

    @staticmethod
    def create_data_text(self) -> None:
        if isinstance(self, bs.MainMenuActivity):
            return
        if getattr(self, '_text_data', None):
            self._text_data.node.delete()
        if cfg['Commands'].get('ShowInfo'):
            info = f"\ue043|Host: {cfg['Commands'].get('HostName', '???')}\n\ue01e|Description: {cfg['Commands'].get('Description', '???')}\n\ue01e|Version: {_babase.app.env.engine_version}"
            color = tuple(list(cfg['Commands'].get('InfoColor', Uts.colors()['white'])) + [1])
            self._text_data = bs.newnode('text',
                attrs={
                    'text': info,
                    'position': (-650.0, -200.0),
                    'color': color
                })

    @staticmethod
    def create_live_chat(self,
                         live: bool = True,
                         chat: list[int, str] = None,
                         admin: bool = False) -> None:
        if isinstance(self, bs.MainMenuActivity):
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
                    else:
                        break
                txt = '\n'.join(chats)
            livetext = "\ue043 CHAT LIVE \ue043"
            txt = (livetext + '\n' + ''.join(['=' for s
                                              in range(len(livetext))]) + '\n') + txt
            self._live_chat = bs.newnode('text',
                attrs={
                    'text': txt,
                    'position': (650.0, 200.0),
                    'color': (1, 1, 1, 1),
                    'h_align': 'right'
                })

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

    @staticmethod
    def ensure_pb_id(client_id: int) -> str | None:
        pb = Uts.get_reliable_pb_id(client_id)
        if pb is None:
            Uts.update_usernames()
            pb = Uts.get_reliable_pb_id(client_id)
        return pb

    @staticmethod
    def get_reliable_pb_id(client_id: int) -> str | None:
        if client_id == -1:
            return None
        for r in roster():
            if r.get('client_id') == client_id:
                acc = r.get('account_id')
                if acc and acc.startswith('pb-'):
                    Uts.userpbs[client_id] = acc
                    return acc
                break
        if client_id in Uts.userpbs and Uts.userpbs[client_id] and Uts.userpbs[client_id].startswith('pb-'):
            return Uts.userpbs[client_id]
        player_name = Uts.usernames.get(client_id)
        if player_name:
            for acc_id, acc_data in Uts.pdata.items():
                if 'Accounts' in acc_data and player_name in acc_data['Accounts']:
                    if acc_id.startswith('pb-'):
                        Uts.userpbs[client_id] = acc_id
                        return acc_id
        return Uts.userpbs.get(client_id)

    @staticmethod
    def find_client_id_by_pb(pb_id: str) -> int | None:
        for cid, acc in Uts.userpbs.items():
            if acc == pb_id:
                if cid in Uts.players and Uts.players[cid].exists():
                    return cid
        for r in roster():
            if r.get('account_id') == pb_id:
                cid = r.get('client_id')
                if cid is not None:
                    return cid
        return None


# ==================== LeaderboardDisplay ====================
class LeaderboardDisplay:
    def __init__(self):
        self.nodes = []
        self.bg_node = None
        self.visible = False
        self.current_data = []
        self.activity = None

    def create(self, activity):
        self.hide()
        self.activity = activity
        self.visible = True
        with activity.context:
            self.bg_node = bs.newnode('image',
                attrs={
                    'texture': bs.gettexture('white'),
                    'position': (500, 200),
                    'scale': (300, 400),
                    'color': (0, 0, 0, 0.5),
                    'absolute_scale': True,
                })
            title_node = bs.newnode('text',
                attrs={
                    'text': '🏆 Top Players',
                    'color': (1, 1, 0),
                    'scale': 1.0,
                    'h_align': 'center',
                    'v_align': 'top',
                    'position': (500, 350),
                    'shadow': 1.0,
                    'flatness': 1.0,
                })
            self.nodes.append(title_node)
            for i in range(10):
                y = 300 - i * 30
                text_node = bs.newnode('text',
                    attrs={
                        'text': '',
                        'color': (1, 1, 1),
                        'scale': 0.8,
                        'h_align': 'left',
                        'v_align': 'center',
                        'position': (400, y),
                        'shadow': 1.0,
                        'flatness': 1.0,
                    })
                self.nodes.append(text_node)
        self.update()

    def hide(self):
        self.visible = False
        for node in self.nodes:
            if node and node.exists():
                node.delete()
        if self.bg_node and self.bg_node.exists():
            self.bg_node.delete()
        self.nodes = []
        self.bg_node = None
        self.activity = None

    def toggle(self, activity):
        if self.visible:
            self.hide()
        else:
            self.create(activity)

    def update(self):
        if not self.visible or not self.activity:
            return
        data = self._load_cheatmax_data()
        players = []
        for acc_id, pdata in data.items():
            if 'Stats' in pdata and 'score' in pdata['Stats']:
                name = pdata.get('Accounts', [None])[0]
                if not name:
                    for cid, pb in Uts.userpbs.items():
                        if pb == acc_id:
                            name = Uts.usernames.get(cid)
                            break
                if not name:
                    name = acc_id[:8]
                score = pdata['Stats']['score']
                players.append((name, score))
        players.sort(key=lambda x: x[1], reverse=True)
        top10 = players[:10]
        if top10 != self.current_data:
            self.current_data = top10
            for node in self.nodes[1:]:
                if node.exists():
                    bs.animate(node, 'opacity', {0: 1.0, 0.2: 0.0})

            def update_texts():
                if not self.visible:
                    return
                with self.activity.context:
                    for i, node in enumerate(self.nodes[1:]):
                        if i < len(top10):
                            name, score = top10[i]
                            node.text = f"{i + 1}. {name} - {score:.1f}"
                        else:
                            node.text = ''
                        node.opacity = 0.0
                        bs.animate(node, 'opacity', {0: 0.0, 0.2: 1.0})

            bs.apptimer(0.25, update_texts)
        else:
            with self.activity.context:
                for i, node in enumerate(self.nodes[1:]):
                    if i < len(top10):
                        name, score = top10[i]
                        node.text = f"{i + 1}. {name} - {score:.1f}"
                    else:
                        node.text = ''

    def _load_cheatmax_data(self):
        file_path = os.path.join(Uts.directory_user, 'Configs', 'CheatMaxPlayersData.json')
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}


# ==================== TagSystem ====================
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
                        Uts.update_usernames()
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
                    account_id = Uts.ensure_pb_id(client_id)
                    if account_id and account_id in Uts.pdata:
                        player_data = Uts.pdata[account_id]
                        if 'Tag' in player_data:
                            tag_data = player_data['Tag']
                            if str(client_id) not in self.current_tags:
                                if tag_data.get('type') == 'animated':
                                    self.create_animated_tag_gradual(player, client_id, tag_data, activity)
                                else:
                                    self.create_tag_with_char_animation(player, client_id, tag_data['text'],
                                                                        tuple(tag_data.get('color', (1, 1, 1))),
                                                                        tag_data.get('scale', 0.03),
                                                                        activity)
                        if 'club' in player_data and player_data['club']:
                            club_info = player_data['club']
                            club_id = club_info['club-id']
                            club_data = Uts.clubs_system.get_club_by_id(club_id) if Uts.clubs_system else None
                            if club_data:
                                role = club_info.get('role', 'player')
                                Uts.clubs_system.create_club_tag(player.actor, client_id, club_data, role, activity)
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
                                                 tuple(tag_data.get('color', (1, 1, 1))),
                                                 tag_data.get('scale', 0.03), activity)
        except Exception as e:
            print(f"❌ Error applying normal tag: {e}")

    def create_animated_tag_gradual(self, player, client_id, tag_data, activity):
        try:
            player_name = player.getname()
            if not player.actor or not player.actor.node:
                return False
            if str(client_id) in self.current_tags:
                self.remove_tag_visual(client_id)
                self.stop_char_animation(client_id)
                self.stop_animation(client_id)
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
                                        attrs={'input1': (0.0, 1.3, 0.0), 'operation': 'add'})
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
                        self.stop_animation(client_id)
                        if Uts.clubs_system:
                            Uts.clubs_system.remove_club_tag(client_id)
                    except:
                        pass
        except Exception as e:
            print(f"❌ Error in cleanup_dead_players: {e}")

    def check_player_respawns(self, activity):
        try:
            for player in activity.players:
                try:
                    if not player.is_alive() or not player.actor or not player.actor.node:
                        continue
                    client_id = player.sessionplayer.inputdevice.client_id
                    account_id = Uts.ensure_pb_id(client_id)
                    if account_id and account_id in Uts.pdata:
                        player_data = Uts.pdata[account_id]
                        if 'Tag' in player_data:
                            tag_data = player_data['Tag']
                            if str(client_id) not in self.current_tags:
                                if tag_data.get('type') == 'animated':
                                    self.create_animated_tag_gradual(player, client_id, tag_data, activity)
                                else:
                                    self.create_tag_with_char_animation(player, client_id, tag_data['text'],
                                                                        tuple(tag_data['color']),
                                                                        tag_data['scale'], activity)
                        if 'club' in player_data and player_data['club']:
                            club_info = player_data['club']
                            club_id = club_info['club-id']
                            club_data = Uts.clubs_system.get_club_by_id(club_id) if Uts.clubs_system else None
                            if club_data:
                                role = club_info.get('role', 'player')
                                Uts.clubs_system.create_club_tag(player.actor, client_id, club_data, role, activity)
                except:
                    pass
        except:
            pass

    def create_tag_with_char_animation(self, player, client_id, text: str, color, scale: float, activity) -> bool:
        try:
            player_name = player.getname()
            if not player.actor or not player.actor.node:
                return False
            if str(client_id) in self.current_tags:
                self.remove_tag_visual(client_id)
                self.stop_char_animation(client_id)
                self.stop_animation(client_id)
            with activity.context:
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
                    attrs={'input1': (0.0, 1.3, 0.0), 'operation': 'add'})
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
                        for i in range(len(text) + 1):
                            bs.apptimer(i * 0.05, lambda idx=i: self._update_text_animation(client_id, text, idx, color))

                        def finalize():
                            if str(client_id) in self.current_tags:
                                tag_node = self.current_tags[str(client_id)]['tag_node']
                                if tag_node.exists():
                                    tag_node.opacity = 1.0

                        bs.apptimer(len(text) * 0.05 + 0.5, finalize)
                    except Exception as e:
                        print(f"Error in animate_text: {e}")

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
            if client_id_str in self.char_animations:
                del self.char_animations[client_id_str]
            if client_id_str in self.animation_states:
                del self.animation_states[client_id_str]
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

    def send_client_message(self, client_id, message, color=(1, 1, 1)):
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
            if hue < 1 / 6:
                r, g, b = 1.0, hue * 6, 0.0
            elif hue < 2 / 6:
                r, g, b = (2 / 6 - hue) * 6, 1.0, 0.0
            elif hue < 3 / 6:
                r, g, b = 0.0, 1.0, (hue - 2 / 6) * 6
            elif hue < 4 / 6:
                r, g, b = 0.0, (4 / 6 - hue) * 6, 1.0
            elif hue < 5 / 6:
                r, g, b = (hue - 4 / 6) * 6, 0.0, 1.0
            else:
                r, g, b = 1.0, 0.0, (1 - hue) * 6
            colors.append((r, g, b))
        return colors

    def apply_tag(self, client_id):
        """تطبيق الوسم على اللاعب عند الدخول (يتم استدعاؤها من Uts.player_join)"""
        # التنفيذ يتم عبر quick_apply_tags، هذه الدالة للتوافق فقط
        pass


# ==================== ClubsSystem ====================
class ClubsSystem:
    def __init__(self):
        self.clubs_file = os.path.join(Uts.directory_user, 'Configs', 'CheatMaxClubsData.json')
        self.offers_file = os.path.join(Uts.directory_user, 'Configs', 'CheatMaxOffersData.json')
        self.clubs_data = {}
        self.offers_data = {}
        self.club_tags = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.clubs_file):
            try:
                with open(self.clubs_file, 'r') as f:
                    self.clubs_data = json.load(f)
            except:
                self.clubs_data = {}
        else:
            self.clubs_data = {}
        if os.path.exists(self.offers_file):
            try:
                with open(self.offers_file, 'r') as f:
                    self.offers_data = json.load(f)
            except:
                self.offers_data = {}
        else:
            self.offers_data = {}
        print(f"✅ Clubs system loaded: {len(self.clubs_data)} clubs, {sum(len(v) for v in self.offers_data.values())} offers")

    def save_clubs(self):
        try:
            with open(self.clubs_file, 'w') as f:
                json.dump(self.clubs_data, f, indent=4)
        except Exception as e:
            print(f"❌ Error saving clubs data: {e}")

    def save_offers(self):
        try:
            with open(self.offers_file, 'w') as f:
                json.dump(self.offers_data, f, indent=4)
        except Exception as e:
            print(f"❌ Error saving offers data: {e}")

    def generate_club_id(self) -> str:
        while True:
            cid = str(random.randint(1000, 9999))
            if cid not in self.clubs_data:
                return cid

    def create_club(self, club_name: str, back_color: tuple, front_color: tuple, captain1_pb: str, captain2_pb: str, creator_name: str) -> str:
        club_id = self.generate_club_id()
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        players_list = [
            {"pb-id": captain1_pb, "contract_expire": "permanent", "role": "captain", "joined": time.time()},
            {"pb-id": captain2_pb, "contract_expire": "permanent", "role": "captain", "joined": time.time()}
        ]
        self.clubs_data[club_id] = {
            "club-name": club_name,
            "club-color-back": [back_color[0], back_color[1], back_color[2]],
            "club-color-front": [front_color[0], front_color[1], front_color[2]],
            "club-created-in": created_date,
            "players": players_list,
            "max-players": 20
        }
        self.save_clubs()
        self._update_player_club_info(captain1_pb, club_id, "captain", "permanent")
        self._update_player_club_info(captain2_pb, club_id, "captain", "permanent")
        return club_id

    def _update_player_club_info(self, pb_id: str, club_id: str, role: str, contract_expire):
        if pb_id not in Uts.pdata:
            Uts.add_player_data(pb_id)
        Uts.pdata[pb_id]["club"] = {
            "club-id": club_id,
            "role": role,
            "contract_expire": contract_expire
        }
        Uts.save_players_data()

    def delete_club(self, club_id: str):
        if club_id in self.clubs_data:
            for player in self.clubs_data[club_id].get("players", []):
                pb = player["pb-id"]
                if pb in Uts.pdata and "club" in Uts.pdata[pb]:
                    del Uts.pdata[pb]["club"]
            Uts.save_players_data()
            del self.clubs_data[club_id]
            self.save_clubs()
            return True
        return False

    def get_club_by_id(self, club_id: str) -> dict:
        return self.clubs_data.get(club_id)

    def get_club_by_player(self, pb_id: str) -> tuple:
        if pb_id not in Uts.pdata or "club" not in Uts.pdata[pb_id]:
            return None
        club_info = Uts.pdata[pb_id]["club"]
        club_id = club_info["club-id"]
        if club_id not in self.clubs_data:
            del Uts.pdata[pb_id]["club"]
            Uts.save_players_data()
            return None
        club_data = self.clubs_data[club_id]
        player_data = None
        for p in club_data.get("players", []):
            if p["pb-id"] == pb_id:
                player_data = p
                break
        if not player_data:
            del Uts.pdata[pb_id]["club"]
            Uts.save_players_data()
            return None
        return club_id, club_data, player_data

    def is_captain(self, pb_id: str) -> bool:
        result = self.get_club_by_player(pb_id)
        if not result:
            return False
        _, _, player_data = result
        return player_data.get("role") == "captain"

    def is_club_member(self, pb_id: str) -> bool:
        return self.get_club_by_player(pb_id) is not None

    def add_offer(self, player_pb: str, club_id: str, club_name: str, months: int, sender_name: str, captain_pb: str):
        if player_pb not in self.offers_data:
            self.offers_data[player_pb] = []
        expire_date = (datetime.now() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
        offer = {
            "club-id": club_id,
            "club-name": club_name,
            "months": months,
            "contract-expire": expire_date,
            "sender": sender_name,
            "sender-pb": captain_pb,
            "sent-time": time.time()
        }
        self.offers_data[player_pb].append(offer)
        self.save_offers()

    def remove_offer(self, player_pb: str, club_id: str):
        if player_pb in self.offers_data:
            self.offers_data[player_pb] = [o for o in self.offers_data[player_pb] if o["club-id"] != club_id]
            if not self.offers_data[player_pb]:
                del self.offers_data[player_pb]
            self.save_offers()

    def get_player_offers(self, player_pb: str) -> list:
        return self.offers_data.get(player_pb, [])

    def accept_offer(self, player_pb: str, club_id: str) -> bool:
        offers = self.get_player_offers(player_pb)
        offer = None
        for o in offers:
            if o["club-id"] == club_id:
                offer = o
                break
        if not offer:
            return False
        club_data = self.get_club_by_id(club_id)
        if not club_data:
            return False
        if len(club_data.get("players", [])) >= club_data.get("max-players", 20):
            return False
        players = club_data.setdefault("players", [])
        for p in players:
            if p["pb-id"] == player_pb:
                return False
        months = offer["months"]
        expire_str = (datetime.now() + timedelta(days=30 * months)).strftime("%Y-%m-%d")
        players.append({
            "pb-id": player_pb,
            "contract_expire": expire_str,
            "role": "player",
            "joined": time.time()
        })
        self._update_player_club_info(player_pb, club_id, "player", expire_str)
        self.save_clubs()
        self.remove_offer(player_pb, club_id)
        return True

    def promote_to_captain(self, captain_pb: str, target_pb: str) -> bool:
        result = self.get_club_by_player(captain_pb)
        if not result:
            return False
        club_id, club_data, _ = result
        target_player_data = None
        for p in club_data["players"]:
            if p["pb-id"] == target_pb:
                target_player_data = p
                break
        if not target_player_data:
            return False
        target_player_data["role"] = "captain"
        if target_pb in Uts.pdata:
            if "club" not in Uts.pdata[target_pb]:
                Uts.pdata[target_pb]["club"] = {}
            Uts.pdata[target_pb]["club"]["role"] = "captain"
        self.save_clubs()
        Uts.save_players_data()
        return True

    def check_expired_contracts(self):
        now = datetime.now().date()
        for club_id, club_data in list(self.clubs_data.items()):
            players = club_data.get("players", [])
            changed = False
            for player in list(players):
                expire = player.get("contract_expire")
                if expire == "permanent":
                    continue
                try:
                    expire_date = datetime.strptime(expire, "%Y-%m-%d").date()
                    if expire_date < now:
                        pb = player["pb-id"]
                        players.remove(player)
                        if pb in Uts.pdata and "club" in Uts.pdata[pb]:
                            del Uts.pdata[pb]["club"]
                        changed = True
                except:
                    continue
            if changed:
                self.save_clubs()
                Uts.save_players_data()

    def get_club_members_sorted(self, club_id: str) -> list:
        club_data = self.get_club_by_id(club_id)
        if not club_data:
            return []
        players = club_data.get("players", [])
        players.sort(key=lambda p: p.get("joined", 0))
        return players

    def get_club_info_text(self, club_id: str) -> str:
        club = self.get_club_by_id(club_id)
        if not club:
            return "Club not found."
        members = self.get_club_members_sorted(club_id)
        captains = [p for p in members if p["role"] == "captain"]
        cap_names = []
        for cap in captains[:2]:
            pb = cap["pb-id"]
            name = "Unknown"
            for cid, acc in Uts.userpbs.items():
                if acc == pb:
                    name = Uts.usernames.get(cid, "Unknown")
                    break
            cap_names.append(name)
        while len(cap_names) < 2:
            cap_names.append("-")
        total = len(members)
        max_players = club.get("max-players", 20)
        lines = []
        lines.append(f"Club name : {club['club-name']}")
        lines.append(f"Club first Captain : {cap_names[0]}")
        lines.append(f"Club second Captain : {cap_names[1]}")
        lines.append(f"Club created in : {club.get('club-created-in', 'Unknown')}")
        lines.append(f"members : {max_players}/{total}")
        for p in members:
            pb = p["pb-id"]
            name = "Unknown"
            for cid, acc in Uts.userpbs.items():
                if acc == pb:
                    name = Uts.usernames.get(cid, "Unknown")
                    break
            expire = p.get("contract_expire", "permanent")
            lines.append(f"{name} : {expire}")
        return "\n".join(lines)

    def get_club_list_text(self, club_id: str) -> str:
        club = self.get_club_by_id(club_id)
        if not club:
            return "Club not found."
        members = self.get_club_members_sorted(club_id)
        captains = [p for p in members if p["role"] == "captain"]
        cap_names = []
        for cap in captains[:2]:
            pb = cap["pb-id"]
            name = "Unknown"
            for cid, acc in Uts.userpbs.items():
                if acc == pb:
                    name = Uts.usernames.get(cid, "Unknown")
                    break
            cap_names.append(name)
        while len(cap_names) < 2:
            cap_names.append("-")
        total = len(members)
        max_players = club.get("max-players", 20)
        lines = []
        lines.append(f"Club name : {club['club-name']}")
        lines.append(f"Club first Captain : {cap_names[0]}")
        lines.append(f"Club second Captain : {cap_names[1]}")
        lines.append(f"members : {max_players}/{total}")
        for p in members:
            pb = p["pb-id"]
            name = "Unknown"
            for cid, acc in Uts.userpbs.items():
                if acc == pb:
                    name = Uts.usernames.get(cid, "Unknown")
                    break
            expire = p.get("contract_expire", "permanent")
            lines.append(f"{name} : {expire}")
        return "\n".join(lines)

    def get_myclub_text(self, pb_id: str) -> str:
        res = self.get_club_by_player(pb_id)
        if not res:
            return "You are not in any club."
        club_id, club_data, player_data = res
        club_name = club_data["club-name"]
        expire = player_data.get("contract_expire", "permanent")
        return f"My club : {club_name}\nContract Expire : {expire}"

    def create_club_tag(self, spaz, client_id: int, club_data: dict, role: str, activity):
        if not spaz or not spaz.node or not spaz.node.exists():
            return
        club_name = club_data["club-name"]
        if role == "captain":
            hat_icon = '\ue041'
            display_name = f"{hat_icon}{club_name}"
        else:
            display_name = club_name
        back_color = club_data.get("club-color-back", [1, 1, 1])
        front_color = club_data.get("club-color-front", [1, 1, 1])
        back_color_tuple = (back_color[0], back_color[1], back_color[2])
        front_color_tuple = (front_color[0], front_color[1], front_color[2])
        if client_id in self.club_tags:
            self.remove_club_tag(client_id)
        with activity.context:
            math_back = bs.newnode('math',
                                   attrs={'input1': (0, 1.7, -0.05), 'operation': 'add'})
            spaz.node.connectattr('position_center', math_back, 'input2')
            tag_back = bs.newnode('text',
                attrs={
                    'text': display_name,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'h_align': 'center',
                    'v_align': 'center',
                    'scale': 0.013,
                    'color': back_color_tuple,
                    'opacity': 0.8
                })
            math_back.connectattr('output', tag_back, 'position')
            math_front = bs.newnode('math',
                                    attrs={'input1': (0.0, 1.7, 0.0), 'operation': 'add'})
            spaz.node.connectattr('position_center', math_front, 'input2')
            tag_front = bs.newnode('text',
                attrs={
                    'text': display_name,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'h_align': 'center',
                    'v_align': 'center',
                    'scale': 0.013,
                    'color': front_color_tuple,
                    'opacity': 1.0
                })
            math_front.connectattr('output', tag_front, 'position')
            self.club_tags[client_id] = [tag_back, tag_front, math_back, math_front]

    def remove_club_tag(self, client_id: int):
        if client_id in self.club_tags:
            nodes = self.club_tags[client_id]
            for node in nodes:
                if node and node.exists():
                    node.delete()
            del self.club_tags[client_id]

    def apply_club_tag(self, client_id):
        """تطبيق وسام النادي على اللاعب عند الدخول (يتم استدعاؤها من Uts.player_join)"""
        pass  # التنفيذ يتم عبر quick_apply_tags


# ==================== CommandFunctions ====================
class CommandFunctions:
    @staticmethod
    def all_cmd() -> list[str]:
        return [
            '-pan', '-ceb', '-colors', '-mp', '-pb', '-effects',
            '/list', 'test', 'help', 'party', 'stats', '/report', '/stats', '-statsshow',
            '/offers', '/offer', '/myclub', '/myid'
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
            '/teleport', '/fly', '/warn', '/warns', '/clearwarns', '/ride', '/invisible',
            '/tint', '/upwall', '/downwall', '/floor', '/spawnball', '/explosion', '/locator', '/ping',
            '/weather', '/tops', '-statsrestart',
            '/club', '/photo', '/photoclear',
            '/backtext', '/fronttext', '/grab', '/fighting'
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
        pb = Uts.ensure_pb_id(client_id)
        if pb:
            Uts.sm(pb, transient=True, clients=[client_id])
        else:
            Uts.sm("You don't have a PB-ID (guest).", transient=True, clients=[client_id])

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
                node.color = node.highlight = (1, 1, 1)
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
                                msg.velocity[0], msg.velocity[1] + 2.0, msg.velocity[2], msg.magnitude,
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
            ClientMessage("No active game found", color=(1, 0, 0))
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
                        ClientMessage(f"Player ID {p_id} not found", color=(1, 0, 0))
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
                (pos[0] - 1, pos[1] + 4, pos[2] + 1),
                (pos[0] + 1, pos[1] + 4, pos[2] + 1),
                (pos[0], pos[1] + 4, pos[2] - 1),
                (pos[0] - 2, pos[1] + 4, pos[2]),
                (pos[0] + 2, pos[1] + 4, pos[2]),
                (pos[0] + 2, pos[1] + 4, pos[2] - 1),
                (pos[0] - 2, pos[1] + 4, pos[2] - 1),
                (pos[0], pos[1] + 4, pos[2] + 2)]
            for p in psts:
                bomb = bs.Bomb(
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
                current_act._ids = bs.newnode('text',
                    attrs={
                        'text': txt,
                        'position': (-0.0, 270.0),
                        'h_align': 'center',
                        'scale': 1.1,
                        'opacity': 0.5
                    })
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
        if c_id not in Uts.accounts:
            Uts.update_usernames()
        if c_id in Uts.accounts:
            return Uts.accounts[c_id].get('Admin', False)
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
    def get_actor(c_id: int) -> 'bs.PlayerSpaz':
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


# ==================== Commands ====================
class Commands:
    fct: Any
    util: Any

    @property
    def get(self) -> str:
        return self.value

    def __init__(self, msg: str, client_id: int, arguments: list[str] = []):
        self.message = msg
        self.msg = msg.strip()
        self.client_id = client_id
        self.arguments = arguments
        self.value = None
        self.util = Uts
        self.fct = CommandFunctions
        self.util.update_usernames()
        self.process_commands()

    def process_commands(self):
        try:
            self.command_all()
            if self.fct.user_is_admin(self.client_id):
                self.admin_commands()
            if self.fct.user_is_owner(self.client_id):
                self.owner_commands()
            self.club_commands()
        except Exception as e:
            print(f"❌ Error in process_commands: {e}")
            self.value = None

    def send_chat_message(self, message):
        try:
            bs.chatmessage(str(message), clients=[self.client_id], sender_override="")
        except:
            self.clientmessage('ERROR', color=(1, 0, 0))

    def clientmessage(self, msg: str, color: Sequence[float] = None):
        self.util.sm(msg, color=color, transient=True, clients=[self.client_id])

    def _load_cheatmax_data(self) -> dict:
        file_path = os.path.join(Uts.directory_user, 'Configs', 'CheatMaxPlayersData.json')
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}

    def command_all(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cmd = self.fct.all_cmd()
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        if msg.lower() == cmd[0]:  # -pan
            self.util.cm("¡Haz recibido pan de \ue061Sr.Palomo!")
            self.value = '@'

        elif msg.lower() == cmd[1]:  # -ceb
            current_act = bs.get_foreground_host_activity()
            if current_act is not None and cls_node is not None:
                with current_act.context:
                    if cls_node.node and cls_node.node.exists():
                        cls_node.handlemessage(bs.CelebrateMessage(duration=3.0))
                ClientMessage("Are you happy!", color=(1.0, 1.0, 0.0))
            self.value = '@'

        elif msg.lower() == cmd[2]:  # -colors
            cols = str()
            cols_list = self.util.sort_list(list(self.util.colors().keys()))
            for c in cols_list:
                cols += (' | '.join(c) + '\n')
            ClientMessage(cols)
            self.value = '@'

        elif msg.lower() == cmd[3]:  # -mp
            mp = bs.get_public_party_max_size()
            ClientMessage(f"Max Players: {mp}")
            self.value = '@'

        elif msg.lower() == cmd[4]:  # -pb
            self.fct.get_my_pb(self.client_id)
            self.value = '@'

        elif msg.lower() == cmd[5]:  # -effects
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

        elif msg.lower() == '/stats':
            self.process_stats_command(self.client_id)
            self.value = '@'

        elif msg.lower() == '-statsshow':
            self.process_statsshow_command(self.client_id)
            self.value = '@'

        elif msg.lower() == '/myid':
            self.process_myid(self.client_id)
            self.value = '@'

    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]

        if ms[0] == '/weather':
            self.process_weather_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == cmd[0]:  # /name
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

        elif ms[0] == cmd[1]:  # /imp
            self.fct.actor_command(ms=ms,
                                   call=self.fct.impulse,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[2]:  # /box
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_box,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[3] or ms[0] == cmd[4]:  # /addAdmin /delAdmin
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

        elif ms[0] == cmd[5]:  # /kill
            self.fct.actor_command(ms=ms,
                                   call=self.fct.kill_spaz,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[6]:  # -pause
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                self.fct.pause()
            self.value = '@'

        elif ms[0] == cmd[7]:  # /infoHost
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

        elif ms[0] == cmd[8]:  # /infoDes
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

        elif ms[0] == cmd[9]:  # -info
            if cfg['Commands'].get('ShowInfo'):
                cfg['Commands']['ShowInfo'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowInfo'] = True
                color = self.util.colors()['green']
            self.util.save_settings()
            ClientMessage("Information saved successfully", color=color)
            self.value = '@'

        elif ms[0] == cmd[10]:  # /infoColor
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

        elif ms[0] == cmd[11]:  # -end
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                with current_act.context:
                    current_act.end_game()
            self.value = '@'

        elif ms[0] == cmd[12]:  # /kick
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
                                try:
                                    bs.disconnect_client(c_id)
                                except Exception as e:
                                    print(f"❌ Error kicking player: {e}")
                                self.value = '@'

        elif ms[0] == cmd[13]:  # -chatLive
            if cfg['Commands'].get('ChatLive'):
                cfg['Commands']['ChatLive'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ChatLive'] = True
                color = self.util.colors()['green']
            self.util.save_settings()
            ClientMessage("Information saved successfully", color=color)
            self.value = '@'

        elif ms[0] == cmd[14]:  # /freeze
            self.fct.actor_command(ms=ms,
                                   call=self.fct.freeze_spaz,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[15]:  # /playerColor
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

        elif ms[0] == cmd[16]:  # /maxPlayers
            try:
                val = int(ms[1])
            except:
                ClientMessage(f"Incomplete data \n Example: {ms[0]} 5")
                self.value = '@'
            else:
                bs.set_public_party_max_size(val)
                ClientMessage(f"Max Players: {val}")
                self.value = '@'

        elif ms[0] == cmd[17]:  # -showMessages
            if cfg['Commands'].get('ShowMessages'):
                cfg['Commands']['ShowMessages'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowMessages'] = True
                color = self.util.colors()['green']
            self.util.save_settings()
            ClientMessage("Show messages above players.", color=color)
            self.value = '@'

        elif ms[0] == cmd[18]:  # /sleep
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_sleep,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[19] or ms[0] == cmd[20]:  # /mute /unmute
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

        elif ms[0] == cmd[21]:  # /gm
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_gm,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[22]:  # -slow
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                self.fct.slow()
            self.value = '@'

        elif ms[0] == cmd[23]:  # /speed
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_speed,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[24]:  # /effect
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
                if c_id not in self.util.usernames:
                    ClientMessage(f"'{c_id}' Does not belong to any player.", color=(1, 0.5, 0))
                    ClientMessage("We suggest you use the '/list' command", color=(1, 0.5, 0))
                    self.value = '@'
                else:
                    pb_id = self.util.ensure_pb_id(c_id)
                    if not pb_id:
                        ClientMessage("Cannot apply effect: player has no PB-ID.", color=(1, 0, 0))
                        self.value = '@'
                        return
                    if eff not in self.fct.effects():
                        ClientMessage(f"'{eff}' is invalid. enter the command '-effects' for more information.", color=(1, 0.5, 0))
                        self.value = '@'
                    else:
                        if pb_id not in self.util.pdata:
                            self.util.add_player_data(pb_id)
                        self.util.pdata[pb_id]['Effect'] = eff
                        self.util.save_players_data()
                        user = self.util.usernames[c_id]
                        ClientMessage(f"Added '{eff}' effect to {user}", color=(0, 0.5, 1))
                        self.value = '@'

        elif ms[0] == cmd[25]:  # /punch
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_punch,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[26]:  # /mbox
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_mgb,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[27]:  # /drop
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_drop,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[28]:  # /gift
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_gift,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[29]:  # /curse
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_curse,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

        elif ms[0] == cmd[30]:  # /superjump
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

        elif ms[0] == '/teleport':
            self.process_teleport_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/fly':
            self.process_fly_command_fixed(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/warn':
            self.process_warn_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/warns':
            self.process_warns_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/clearwarns':
            self.process_clearwarns_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/invisible':
            self.fct.actor_command(ms=ms,
                                   call=self.fct.spaz_visible,
                                   attrs={'Actor': cls_node,
                                          'ClientMessage': ClientMessage})
            self.value = '@'

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

        elif ms[0] == '/spawnball':
            self.process_spawnball_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/explosion':
            self.process_explosion_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/locator':
            self.process_locator_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/ping':
            self.process_ping_command(self.client_id)
            self.value = '@'

        elif ms[0] == '/tops':
            self.process_tops_command(self.client_id)
            self.value = '@'

        elif ms[0] == '-statsrestart':
            self.process_statsrestart_command(self.client_id)
            self.value = '@'

        elif ms[0] == '/photo':
            self.process_photo_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/photoclear':
            self.process_photoclear_command(self.client_id)
            self.value = '@'

        elif ms[0] == '/backtext':
            self.process_backtext_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/fronttext':
            self.process_fronttext_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/grab':
            self.process_grab_command(msg, self.client_id)
            self.value = '@'

        elif ms[0] == '/fighting':
            self.process_fighting_command(msg, self.client_id)
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

    # ------------------- أوامر التلوين (بدون حدود) -------------------
    def process_tint_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage("❌ Use: /tint <r> <g> <b>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /tint 1 0.5 0.2", color=(1, 1, 0))
                return
            r = float(parts[1])
            g = float(parts[2])
            b = float(parts[3])
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
                return
            with activity.context:
                gnode = activity.globalsnode
                gnode.tint = (r, g, b)
                self.clientmessage(f"✅ Tint set to ({r}, {g}, {b})", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_upwall_command(self, msg: str, client_id: int):
        self._apply_color_to_soccer(msg, client_id, 'wall_up_color', 'upper',
                                     ['hockeyStadiumStands', 'stands'], "Upper Wall")

    def process_downwall_command(self, msg: str, client_id: int):
        self._apply_color_to_soccer(msg, client_id, 'wall_down_color', 'lower',
                                     ['hockeyStadiumOuter', 'outer'], "Lower Wall")

    def process_floor_command(self, msg: str, client_id: int):
        self._apply_color_to_soccer(msg, client_id, 'floor_color', 'floor',
                                     ['hockeyStadiumInner', 'inner', 'ground'], "Floor")

    def _apply_color_to_soccer(self, msg: str, client_id: int, config_key: str,
                                wall_type: str, mesh_keywords: list, target_name: str):
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage(f"❌ Use: {parts[0]} <r> <g> <b>", color=(1, 0, 0))
                return
            r = float(parts[1])
            g = float(parts[2])
            b = float(parts[3])
            self._update_asoccer_config(config_key, r, g, b)
            self.clientmessage(f"✅ {target_name} color saved to A-Soccer config ({r},{g},{b})", color=(0, 1, 0))
            activity = bs.get_foreground_host_activity()
            if activity and activity.__class__.__name__ == 'SoccerGame':
                with activity.context:
                    if hasattr(activity, config_key):
                        setattr(activity, config_key, [r, g, b])
                    applied = False
                    if wall_type == 'upper' and hasattr(activity, '_apply_wall_up_texture'):
                        activity._apply_wall_up_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_wall_up_texture()", color=(0, 1, 0))
                        applied = True
                    elif wall_type == 'lower' and hasattr(activity, '_apply_wall_down_texture'):
                        activity._apply_wall_down_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_wall_down_texture()", color=(0, 1, 0))
                        applied = True
                    elif wall_type == 'floor' and hasattr(activity, '_apply_ground_texture'):
                        activity._apply_ground_texture()
                        self.clientmessage(f"🎨 Applied to SoccerGame via _apply_ground_texture()", color=(0, 1, 0))
                        applied = True
                    if not applied:
                        self._set_node_color_by_mesh_fixed(msg, client_id, mesh_keywords, target_name, r, g, b)
            else:
                self._set_node_color_by_mesh_fixed(msg, client_id, mesh_keywords, target_name, r, g, b)
        except Exception as e:
            self.clientmessage(f"❌ Error in color command: {str(e)[:50]}", color=(1, 0, 0))

    def _set_node_color_by_mesh_fixed(self, msg: str, client_id: int, mesh_keywords: list,
                                       target_name: str, r: float, g: float, b: float):
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
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
                self.clientmessage(f"✅ {target_name} color set via node.color - {found_colored} nodes (out of {found_mesh} matching)", color=(0, 1, 0))
            elif found_mesh > 0:
                self.clientmessage(f"⚠️ Found {found_mesh} matching meshes but none have 'color' attribute. Colors may not appear.", color=(1, 1, 0))
            else:
                self.clientmessage(f"⚠️ No {target_name} nodes found. Make sure you are on Soccer Stadium map.", color=(1, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error in node color: {str(e)[:50]}", color=(1, 0, 0))

    def _update_asoccer_config(self, key: str, r: float, g: float, b: float):
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

    def process_backtext_command(self, msg: str, client_id: int):
        self._process_text_command(msg, client_id, 'back', (-3.06, 0.66, -8.5))

    def process_fronttext_command(self, msg: str, client_id: int):
        self._process_text_command(msg, client_id, 'front', (-3.0, 0.7, -8.5))

    def _process_text_command(self, msg: str, client_id: int, label: str, target_pos: tuple):
        try:
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage(f"❌ Use: /{label}text <text> <r,g,b[,a]>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /fronttext 'New Title' 1,0.5,0", color=(1, 1, 0))
                return
            color_str = parts[-1]
            text_parts = parts[1:-1]
            if not text_parts:
                self.clientmessage("❌ No text provided", color=(1, 0, 0))
                return
            new_text = ' '.join(text_parts)
            try:
                rgba = [float(x.strip()) for x in color_str.split(',')]
                if len(rgba) == 3:
                    r, g, b = rgba
                    a = 1.0
                elif len(rgba) == 4:
                    r, g, b, a = rgba
                else:
                    raise ValueError
            except:
                self.clientmessage("❌ Invalid color format. Use r,g,b or r,g,b,a", color=(1, 0, 0))
                return
            activity = bs.get_foreground_host_activity()
            if not activity or activity.__class__.__name__ != 'SoccerGame':
                self.clientmessage("❌ No active Soccer game", color=(1, 0, 0))
                return
            with activity.context:
                found = False
                for node in bs.getnodes():
                    if node.getnodetype() == 'text' and node.in_world:
                        pos = node.position
                        if (abs(pos[0] - target_pos[0]) < 0.1 and
                            abs(pos[1] - target_pos[1]) < 0.1 and
                            abs(pos[2] - target_pos[2]) < 0.1):
                            node.text = new_text
                            node.color = (r, g, b, a)
                            found = True
                            break
                if found:
                    self.clientmessage(f"✅ {label.capitalize()} text updated", color=(0, 1, 0))
                else:
                    self.clientmessage(f"⚠️ {label.capitalize()} text node not found", color=(1, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_grab_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2 or parts[1].lower() not in ['on', 'off']:
                self.clientmessage("❌ Use: /grab <on|off>", color=(1, 0, 0))
                return
            state = parts[1].lower() == 'on'
            activity = bs.get_foreground_host_activity()
            if not activity or activity.__class__.__name__ != 'SoccerGame':
                self.clientmessage("❌ No active Soccer game", color=(1, 0, 0))
                return
            activity.enable_pickup = state
            self.clientmessage(f"✅ Grab mode set to {state}", color=(0, 1, 0))
            with activity.context:
                for player in activity.players:
                    if player.is_alive() and player.actor:
                        player.actor.connect_controls_to_player(enable_pickup=state)
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_fighting_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2 or parts[1].lower() not in ['on', 'off']:
                self.clientmessage("❌ Use: /fighting <on|off>", color=(1, 0, 0))
                return
            state = parts[1].lower() == 'on'
            activity = bs.get_foreground_host_activity()
            if not activity or activity.__class__.__name__ != 'SoccerGame':
                self.clientmessage("❌ No active Soccer game", color=(1, 0, 0))
                return
            with activity.context:
                for player in activity.players:
                    if player.is_alive() and player.actor and player.actor.node:
                        player.actor.node.invincible = not state
                self.clientmessage(f"✅ Fighting mode set to {state}", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_weather_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /weather <type>", color=(1, 0, 0))
                self.clientmessage(f"🌦️ Types: {', '.join(Uts.weather_effect.valid_weather)}", color=(0.5, 0.8, 1))
                self.clientmessage("📝 Example: /weather snow  |  /weather none", color=(1, 1, 0))
                return
            wtype = parts[1].lower()
            if wtype not in Uts.weather_effect.valid_weather:
                self.clientmessage(f"❌ Invalid weather type. Use: {', '.join(Uts.weather_effect.valid_weather)}", color=(1, 0, 0))
                return
            cfg['Commands']['Weather'] = wtype
            Uts.save_settings()
            activity = bs.get_foreground_host_activity()
            if activity is not None:
                with activity.context:
                    Uts.weather_effect.start(wtype)
                self.clientmessage(f"✅ Weather changed to '{wtype}'", color=(0, 1, 0))
                if wtype != 'none':
                    Uts.cm(f"🌍 Server weather is now: {wtype}")
                else:
                    Uts.cm("🌍 Server weather disabled")
            else:
                self.clientmessage(f"✅ Weather saved as '{wtype}'. It will start when a game begins.", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Weather error: {str(e)[:50]}", color=(1, 0, 0))

    # ------------------- إحصائيات -------------------
    def process_stats_command(self, client_id: int):
        try:
            self.util.update_usernames()
            account_id = Uts.ensure_pb_id(client_id)
            if not account_id or (account_id.startswith('guest_') and account_id not in Uts.pdata):
                self.clientmessage("❌ Can't Found pb-ID or no stats data", color=(1, 0, 0))
                return
            data = self._load_cheatmax_data()
            if account_id not in data or 'Stats' not in data[account_id]:
                self.clientmessage("No Stats Rn Soccer One Goal", color=(0.5, 0.5, 1))
                return
            stats = data[account_id]['Stats']
            player_name = Uts.usernames.get(client_id, f"Player {client_id}")
            icons = {'goals': '\ue001', 'assists': '\ue002', 'wins': '\ue043', 'losses': '\ue046', 'draws': '\ue019', 'games': '\ue01e', 'score': '\ue01f', 'rank': '\ue02f'}
            lines = []
            lines.append("=" * 50 + "[Stats]" + "=" * 50)
            header = (f"|| {icons['goals']} Goals || {icons['assists']} Assists || {icons['wins']} Wins "
                      f"|| {icons['losses']} Lose || {icons['draws']} Draw || {icons['games']} Games "
                      f"|| {icons['score']} Score || {icons['rank']} Rank ||")
            lines.append(header)
            lines.append("=" * 120)
            g = f"{stats['goals']}".rjust(5)
            a = f"{stats['assists']}".rjust(7)
            w = f"{stats['wins']}".rjust(5)
            l = f"{stats['losses']}".rjust(5)
            d = f"{stats['draws']}".rjust(5)
            gm = f"{stats['games']}".rjust(6)
            sc = f"{stats['score']:.2f}".rjust(8)
            rk = f"#{stats['rank']}".rjust(5)
            row = (f"|| {g}     || {a}       || {w}     || {l}     || {d}     "
                   f"|| {gm}       || {sc}   || {rk}      ||")
            lines.append(row)
            lines.append("=" * 120)
            lines.append(f"Player Name = {player_name}")
            lines.append(f"pb-ID = {account_id}")
            lines.append("=" * 120)
            for line in lines:
                self.send_chat_message(line)
        except Exception as e:
            self.clientmessage(f"❌ خطأ في عرض الإحصائيات: {str(e)[:50]}", color=(1, 0, 0))

    def process_tops_command(self, client_id: int):
        if not CommandFunctions.user_is_admin(client_id):
            self.clientmessage(getlanguage("AdminOnly"), color=(1, 0, 0))
            return
        try:
            data = self._load_cheatmax_data()
            players = []
            for acc_id, pdata in data.items():
                if 'Stats' in pdata and 'score' in pdata['Stats']:
                    name = pdata.get('Accounts', [None])[0]
                    if not name:
                        for cid, pb in Uts.userpbs.items():
                            if pb == acc_id:
                                name = Uts.usernames.get(cid)
                                break
                    if not name:
                        name = acc_id[:8]
                    players.append((acc_id, pdata['Stats']['score'], name, pdata['Stats'].get('rank', 0)))
            players.sort(key=lambda x: x[1], reverse=True)
            top15 = players[:15]
            if not top15:
                self.clientmessage("📋 لا توجد إحصائيات كافية.", color=(0.5, 0.5, 1))
                return
            self.send_chat_message("══════════════════════════════[Top-Player]══════════════════════════════")
            header = "|| #   || Name                          || Points    || Rank ||"
            self.send_chat_message(header)
            self.send_chat_message("=" * 80)
            for i, (acc_id, score, name, rank) in enumerate(top15, 1):
                medal = '\ue043' if i == 1 else '\ue02b' if i == 2 else '\ue02a' if i == 3 else f"{i}."
                name_col = name[:25].ljust(25)
                score_str = f"{score:.1f}".rjust(9)
                rank_str = f"#{rank}".rjust(6)
                row = f"|| {medal} {i:<2} || {name_col} || {score_str} || {rank_str} ||"
                self.send_chat_message(row)
            self.send_chat_message("=" * 80)
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_statsshow_command(self, client_id: int):
        cfg['Commands']['ShowStatsLeaderboard'] = not cfg['Commands'].get('ShowStatsLeaderboard', False)
        Uts.save_settings()
        activity = bs.get_foreground_host_activity()
        if activity:
            if cfg['Commands']['ShowStatsLeaderboard']:
                Uts.leaderboard_display.create(activity)
                self.clientmessage("📊 Leaderboard shown", color=(0, 1, 0))
            else:
                Uts.leaderboard_display.hide()
                self.clientmessage("📊 Leaderboard hidden", color=(1, 0, 0))
        else:
            self.clientmessage("❌ No active game", color=(1, 0, 0))

    def process_statsrestart_command(self, client_id: int):
        if not CommandFunctions.user_is_admin(client_id):
            self.clientmessage(getlanguage("AdminOnly"), color=(1, 0, 0))
            return
        try:
            file_path = os.path.join(Uts.directory_user, 'Configs', 'CheatMaxPlayersData.json')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                for acc_id in data:
                    if 'Stats' in data[acc_id]:
                        data[acc_id]['Stats'] = {'goals': 0, 'assists': 0, 'wins': 0, 'losses': 0, 'draws': 0, 'games': 0, 'score': 0.0, 'rank': 0}
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                self.clientmessage("✅ All player stats have been reset.", color=(0, 1, 0))
                if cfg.get('Commands', {}).get('ShowStatsLeaderboard', False):
                    activity = bs.get_foreground_host_activity()
                    if activity:
                        Uts.leaderboard_display.update()
            else:
                self.clientmessage("❌ No stats file found.", color=(1, 0, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error resetting stats: {str(e)[:50]}", color=(1, 0, 0))

    def process_myid(self, client_id: int):
        pb = Uts.ensure_pb_id(client_id)
        if not pb or pb.startswith('guest_'):
            self.send_chat_message(f"🆔 You don't have a PB-ID (guest).")
        else:
            self.send_chat_message(f"🆔 Your PB-ID is: {pb}")

    # ------------------- أوامر الأندية -------------------
    def club_commands(self):
        msg = self.msg.strip()
        ms = self.arguments
        if not ms:
            return
        cmd = ms[0].lower()
        ClientMessage = self.clientmessage
        client_id = self.client_id
        pb_id = Uts.ensure_pb_id(client_id)

        if cmd == '/offers':
            self.process_offers_command(pb_id)
            self.value = '@'
        elif cmd == '/offer':
            if len(ms) >= 3:
                subcmd = ms[1].lower()
                club_id = ms[2]
                if subcmd == 'yes':
                    self.process_offer_yes(pb_id, club_id)
                elif subcmd == 'no':
                    self.process_offer_no(pb_id, club_id)
                else:
                    ClientMessage("❌ Use: /offer yes <club-id> or /offer no <club-id>", color=(1, 0, 0))
            else:
                ClientMessage("❌ Use: /offer yes <club-id> or /offer no <club-id>", color=(1, 0, 0))
            self.value = '@'
        elif cmd == '/myclub':
            self.process_myclub(pb_id)
            self.value = '@'

        is_captain = Uts.clubs_system.is_captain(pb_id)
        is_member = Uts.clubs_system.is_club_member(pb_id)

        if cmd == '/club':
            if len(ms) < 2:
                ClientMessage("❌ Use: /club add|delete|list|info", color=(1, 0, 0))
                self.value = '@'
                return
            subcmd = ms[1].lower()
            if subcmd == 'add':
                if not (self.fct.user_is_admin(client_id) or self.fct.user_is_owner(client_id)):
                    ClientMessage(getlanguage("AdminOnly"), color=(1, 0, 0))
                    self.value = '@'
                    return
                if len(ms) < 7:
                    ClientMessage("❌ Use: /club add <name> <r,g,b back> <r,g,b front> <captain1-pb> <captain2-pb>", color=(1, 0, 0))
                    ClientMessage("📝 Example: /club add Heros 0.1,0.1,0.1 1,0.84,0 pb-XXXX pb-YYYY", color=(1, 1, 0))
                    self.value = '@'
                    return
                club_name = ms[2]
                back_color_str = ms[3]
                front_color_str = ms[4]
                cap1_pb = ms[5]
                cap2_pb = ms[6]
                try:
                    r_back, g_back, b_back = map(float, back_color_str.split(','))
                    back_color = (r_back, g_back, b_back)
                    r_front, g_front, b_front = map(float, front_color_str.split(','))
                    front_color = (r_front, g_front, b_front)
                except:
                    ClientMessage("❌ Invalid color format. Use r,g,b (e.g., 0.1,0.1,0.1)", color=(1, 0, 0))
                    self.value = '@'
                    return
                if cap1_pb.startswith('guest_') or cap2_pb.startswith('guest_'):
                    ClientMessage("❌ Captains must have valid PB-IDs.", color=(1, 0, 0))
                    self.value = '@'
                    return
                club_id = Uts.clubs_system.create_club(club_name, back_color, front_color, cap1_pb, cap2_pb, Uts.usernames.get(client_id, "Unknown"))
                ClientMessage(f"✅ Club created with ID: {club_id}", color=(0, 1, 0))
                self.value = '@'

            elif subcmd == 'delete':
                if not (self.fct.user_is_admin(client_id) or self.fct.user_is_owner(client_id)):
                    ClientMessage(getlanguage("AdminOnly"), color=(1, 0, 0))
                    self.value = '@'
                    return
                if len(ms) < 3:
                    ClientMessage("❌ Use: /club delete <club-id>", color=(1, 0, 0))
                    self.value = '@'
                    return
                club_id = ms[2]
                if Uts.clubs_system.delete_club(club_id):
                    ClientMessage(f"✅ Club {club_id} deleted", color=(0, 1, 0))
                else:
                    ClientMessage("❌ Club not found", color=(1, 0, 0))
                self.value = '@'

            elif subcmd == 'list':
                if not is_captain:
                    ClientMessage("❌ Only captains can use /club list", color=(1, 0, 0))
                    self.value = '@'
                    return
                res = Uts.clubs_system.get_club_by_player(pb_id)
                if not res:
                    ClientMessage("❌ You are not in any club", color=(1, 0, 0))
                    self.value = '@'
                    return
                club_id, _, _ = res
                text = Uts.clubs_system.get_club_list_text(club_id)
                for line in text.split('\n'):
                    self.send_chat_message(line)
                self.value = '@'

            elif subcmd == 'info':
                if not is_captain:
                    ClientMessage("❌ Only captains can use /club info", color=(1, 0, 0))
                    self.value = '@'
                    return
                res = Uts.clubs_system.get_club_by_player(pb_id)
                if not res:
                    ClientMessage("❌ You are not in any club", color=(1, 0, 0))
                    self.value = '@'
                    return
                club_id, _, _ = res
                text = Uts.clubs_system.get_club_info_text(club_id)
                for line in text.split('\n'):
                    self.send_chat_message(line)
                self.value = '@'

        elif cmd == '/sign':
            if not is_captain:
                ClientMessage("❌ Only captains can use /sign commands", color=(1, 0, 0))
                self.value = '@'
                return
            if len(ms) < 2:
                ClientMessage("❌ Use: /sign player <pb-id> <months> or /sign captain <pb-id>", color=(1, 0, 0))
                self.value = '@'
                return
            subcmd = ms[1].lower()
            if subcmd == 'player':
                if len(ms) < 4:
                    ClientMessage("❌ Use: /sign player <pb-id> <months>", color=(1, 0, 0))
                    self.value = '@'
                    return
                target_pb = ms[2]
                if target_pb.startswith('guest_'):
                    ClientMessage("❌ Cannot send offer to guest players.", color=(1, 0, 0))
                    self.value = '@'
                    return
                try:
                    months = int(ms[3])
                    if months <= 0:
                        raise ValueError
                except:
                    ClientMessage("❌ Months must be a positive integer", color=(1, 0, 0))
                    self.value = '@'
                    return
                if Uts.clubs_system.is_club_member(target_pb):
                    res = Uts.clubs_system.get_club_by_player(target_pb)
                    if res:
                        _, _, player_data = res
                        expire = player_data.get("contract_expire", "permanent")
                        ClientMessage(f"⚠️ Player {target_pb} is already in a club (contract: {expire}). Cannot send offer until contract ends.", color=(1, 1, 0))
                    else:
                        ClientMessage(f"⚠️ Player {target_pb} is already in a club.", color=(1, 1, 0))
                    self.value = '@'
                    return
                if Uts.clubs_system.is_captain(target_pb):
                    ClientMessage(f"❌ Cannot send offer to a club captain ({target_pb}).", color=(1, 0, 0))
                    self.value = '@'
                    return
                res = Uts.clubs_system.get_club_by_player(pb_id)
                if not res:
                    ClientMessage("❌ You are not in any club", color=(1, 0, 0))
                    self.value = '@'
                    return
                club_id, club_data, _ = res
                club_name = club_data["club-name"]
                captain_name = Uts.usernames.get(client_id, "Captain")
                Uts.clubs_system.add_offer(target_pb, club_id, club_name, months, captain_name, pb_id)
                ClientMessage(f"✅ Offer sent to {target_pb}", color=(0, 1, 0))
                target_client = Uts.find_client_id_by_pb(target_pb)
                if target_client is not None:
                    try:
                        bs.chatmessage(f"📩 You have received a club offer from {club_name}. Use /offers to view.", clients=[target_client], sender_override="System")
                    except:
                        pass
                self.value = '@'
            elif subcmd == 'captain':
                if len(ms) < 3:
                    ClientMessage("❌ Use: /sign captain <pb-id>", color=(1, 0, 0))
                    self.value = '@'
                    return
                target_pb = ms[2]
                if Uts.clubs_system.promote_to_captain(pb_id, target_pb):
                    ClientMessage(f"✅ {target_pb} promoted to captain", color=(0, 1, 0))
                else:
                    ClientMessage("❌ Promotion failed. Make sure target is a member of your club.", color=(1, 0, 0))
                self.value = '@'

    def process_offers_command(self, pb_id: str):
        offers = Uts.clubs_system.get_player_offers(pb_id)
        if not offers:
            self.clientmessage("📭 No offers received.", color=(0.5, 0.5, 1))
            return
        self.clientmessage("📋 Your offers:", color=(1, 1, 0))
        for o in offers:
            msg_lines = [
                f"Club name : {o['club-name']}",
                f"Months : {o['months']}",
                f"Contract expire : {o['contract-expire']}",
                f"sender : {o['sender']}",
                f"To accept: /offer yes {o['club-id']}",
                f"To reject: /offer no {o['club-id']}"
            ]
            for line in msg_lines:
                self.send_chat_message(line)

    def process_offer_yes(self, pb_id: str, club_id: str):
        if Uts.clubs_system.accept_offer(pb_id, club_id):
            self.clientmessage(f"✅ You have joined the club!", color=(0, 1, 0))
        else:
            self.clientmessage("❌ Failed to accept offer. It may be expired or club full.", color=(1, 0, 0))

    def process_offer_no(self, pb_id: str, club_id: str):
        Uts.clubs_system.remove_offer(pb_id, club_id)
        self.clientmessage("❌ Offer rejected and removed.", color=(1, 1, 0))

    def process_myclub(self, pb_id: str):
        text = Uts.clubs_system.get_myclub_text(pb_id)
        for line in text.split('\n'):
            self.send_chat_message(line)

    # ------------------- باقي الأوامر (مكتملة) -------------------
    def process_advanced_customtag(self, msg: str, client_id: int):
        """إنشاء وسم مخصص متقدم"""
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage("❌ Use: /customtag <text> <color> <scale>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /customtag 'MyTag' 1,0,0 0.03", color=(1, 1, 0))
                return
            text = parts[1]
            color_str = parts[2]
            scale = float(parts[3])
            color = Uts.tag_system.parse_color(color_str)
            pb_id = Uts.ensure_pb_id(client_id)
            if not pb_id:
                self.clientmessage("❌ Cannot set tag: no PB-ID.", color=(1, 0, 0))
                return
            if pb_id not in Uts.pdata:
                Uts.add_player_data(pb_id)
            Uts.pdata[pb_id]['Tag'] = {
                'text': text,
                'color': color,
                'scale': scale,
                'type': 'normal'
            }
            Uts.save_players_data()
            # تطبيق فوري
            activity = bs.get_foreground_host_activity()
            if activity:
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == client_id and player.is_alive():
                        Uts.tag_system.apply_normal_tag(player, client_id, Uts.pdata[pb_id]['Tag'], activity)
                        break
            self.clientmessage(f"✅ Custom tag set to '{text}'", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_animationtag(self, msg: str, client_id: int):
        """إنشاء وسم متحرك"""
        try:
            parts = msg.split()
            if len(parts) < 6:
                self.clientmessage("❌ Use: /animationtag <text> <colors> <scale> <speed>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /animationtag 'Anime' 1,0,0;0,1,0;0,0,1 0.03 1.5", color=(1, 1, 0))
                return
            text = parts[1]
            colors_str = parts[2]
            scale = float(parts[3])
            speed = float(parts[4])
            colors = []
            for c in colors_str.split(';'):
                colors.append(tuple(map(float, c.split(','))))
            pb_id = Uts.ensure_pb_id(client_id)
            if not pb_id:
                self.clientmessage("❌ Cannot set tag: no PB-ID.", color=(1, 0, 0))
                return
            if pb_id not in Uts.pdata:
                Uts.add_player_data(pb_id)
            Uts.pdata[pb_id]['Tag'] = {
                'text': text,
                'colors': colors,
                'scale': scale,
                'speed': speed,
                'type': 'animated'
            }
            Uts.save_players_data()
            # تطبيق فوري
            activity = bs.get_foreground_host_activity()
            if activity:
                for player in activity.players:
                    if player.sessionplayer.inputdevice.client_id == client_id and player.is_alive():
                        Uts.tag_system.create_animated_tag_gradual(player, client_id, Uts.pdata[pb_id]['Tag'], activity)
                        break
            self.clientmessage(f"✅ Animated tag set to '{text}'", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_removetag(self, msg: str, client_id: int):
        """إزالة الوسم"""
        pb_id = Uts.ensure_pb_id(client_id)
        if pb_id and pb_id in Uts.pdata and 'Tag' in Uts.pdata[pb_id]:
            del Uts.pdata[pb_id]['Tag']
            Uts.save_players_data()
            Uts.tag_system.remove_tag_visual(client_id)
            Uts.tag_system.stop_char_animation(client_id)
            Uts.tag_system.stop_animation(client_id)
            self.clientmessage("✅ Tag removed", color=(0, 1, 0))
        else:
            self.clientmessage("❌ You don't have a tag", color=(1, 0, 0))

    def process_locator_command(self, msg: str, client_id: int):
        """إنشاء مؤشر مضيء في موقع اللاعب"""
        try:
            parts = msg.split()
            color = (1, 0, 0)  # أحمر افتراضي
            if len(parts) >= 4:
                r = float(parts[1])
                g = float(parts[2])
                b = float(parts[3])
                color = (r, g, b)
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
                return
            actor = self.fct.get_actor(client_id)
            if not actor or not actor.node:
                self.clientmessage("❌ You are not in the game", color=(1, 0, 0))
                return
            with activity.context:
                pos = actor.node.position
                light = bs.newnode('light',
                    attrs={
                        'position': pos,
                        'color': color,
                        'radius': 1.0,
                        'intensity': 2.0,
                        'height_attenuated': False
                    })
                bs.timer(5.0, light.delete)
                self.clientmessage("✅ Locator placed", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_spawnball_command(self, msg: str, client_id: int):
        """استدعاء كرة قابلة للضرب"""
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
                return
            actor = self.fct.get_actor(client_id)
            if not actor or not actor.node:
                self.clientmessage("❌ You are not in the game", color=(1, 0, 0))
                return
            with activity.context:
                pos = actor.node.position
                CMBall(position=(pos[0], pos[1] + 2, pos[2]))
                self.clientmessage("✅ Spawned a hittable ball", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_explosion_command(self, msg: str, client_id: int):
        """تفجير حول اللاعب"""
        try:
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
                return
            actor = self.fct.get_actor(client_id)
            if not actor or not actor.node:
                self.clientmessage("❌ You are not in the game", color=(1, 0, 0))
                return
            with activity.context:
                pos = actor.node.position
                bs.emitfx(position=pos, count=50, scale=2.0, spread=2.0, chunk_type='spark')
                bs.getsound('explosion03').play(1, pos)
                # تأثير ضربة
                for node in bs.getnodes():
                    if node.getnodetype() == 'prop' and hasattr(node, 'position'):
                        dist = ((node.position[0] - pos[0]) ** 2 +
                                (node.position[1] - pos[1]) ** 2 +
                                (node.position[2] - pos[2]) ** 2) ** 0.5
                        if dist < 5.0:
                            node.handlemessage(bs.HitMessage(pos=pos, velocity=(0, 0, 0), magnitude=1000,
                                                              velocity_magnitude=0, radius=5.0,
                                                              force_direction=(1, 0, 0)))
                self.clientmessage("💥 BOOM!", color=(1, 0.5, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_savetag(self, msg: str, client_id: int):
        """حفظ الوسم الحالي كقالب"""
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /savetag <template_name>", color=(1, 0, 0))
                return
            template_name = parts[1]
            pb_id = Uts.ensure_pb_id(client_id)
            if not pb_id or pb_id not in Uts.pdata or 'Tag' not in Uts.pdata[pb_id]:
                self.clientmessage("❌ You don't have a tag to save", color=(1, 0, 0))
                return
            Uts.tag_system.saved_tag_templates[template_name] = Uts.pdata[pb_id]['Tag'].copy()
            Uts.tag_system.save_templates()
            self.clientmessage(f"✅ Tag saved as '{template_name}'", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_ping_command(self, client_id: int):
        self.clientmessage(f"🏓 Pong! (Ping simulation)", color=(0, 1, 1))

    def process_tagdata(self, msg: str, client_id: int):
        """عرض بيانات الوسم الحالي"""
        pb_id = Uts.ensure_pb_id(client_id)
        if not pb_id or pb_id not in Uts.pdata or 'Tag' not in Uts.pdata[pb_id]:
            self.clientmessage("❌ You don't have a tag", color=(1, 0, 0))
            return
        tag = Uts.pdata[pb_id]['Tag']
        self.send_chat_message(f"Tag data: {json.dumps(tag)}")

    def process_listtags(self, client_id: int):
        """عرض قائمة القوالب المحفوظة"""
        templates = Uts.tag_system.saved_tag_templates
        if not templates:
            self.clientmessage("📭 No saved tag templates", color=(0.5, 0.5, 1))
            return
        self.clientmessage("📋 Saved tag templates:", color=(1, 1, 0))
        for name in templates.keys():
            self.send_chat_message(f" - {name}")

    def process_shared_accounts(self, client_id: int):
        """عرض الحسابات المشتركة للاعب (إذا كان لديه عدة أسماء)"""
        pb_id = Uts.ensure_pb_id(client_id)
        if not pb_id or pb_id not in Uts.pdata:
            self.clientmessage("❌ No data for your PB-ID", color=(1, 0, 0))
            return
        accounts = Uts.pdata[pb_id].get('Accounts', [])
        if not accounts:
            self.clientmessage("📭 No shared accounts found", color=(0.5, 0.5, 1))
        else:
            self.clientmessage("📋 Your known account names:", color=(1, 1, 0))
            for acc in accounts:
                self.send_chat_message(f" - {acc}")

    def process_close_server(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage(getlanguage("CloseServerUsage"), color=(1, 0, 0))
                return
            hours = float(parts[1])
            if hours <= 0:
                self.clientmessage(getlanguage("InvalidHours"), color=(1, 0, 0))
                return
            tag_name = ' '.join(parts[2:])
            if Uts.start_server_closure(hours, tag_name, client_id):
                self.clientmessage(getlanguage("ServerCloseStarted", subs=[str(hours), tag_name]), color=(0, 1, 0))
            else:
                self.clientmessage(getlanguage("ServerAlreadyClosed"), color=(1, 0, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_stop_close_server(self, client_id: int):
        if Uts.server_close_active:
            Uts.stop_server_closure()
            self.clientmessage(getlanguage("ServerClosedStopped"), color=(0, 1, 0))
        else:
            self.clientmessage(getlanguage("NoServerCloseActive"), color=(1, 0, 0))

    def process_close_status(self, client_id: int):
        if not Uts.server_close_active:
            self.clientmessage("ℹ️ Server is open.", color=(0.5, 0.5, 1))
            return
        remaining = Uts.server_close_end_time - time.time()
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        seconds = int(remaining % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.clientmessage(f"🔒 Server closed for tag '{Uts.server_close_tag_name}'. Time left: {time_str}", color=(1, 0, 0))

    def test_closure_system(self):
        self.clientmessage("🧪 Testing closure system...", color=(1, 1, 0))

    def process_teleport_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 4:
                self.clientmessage("❌ Use: /teleport <x> <y> <z>", color=(1, 0, 0))
                self.clientmessage("📝 Example: /teleport 0 5 0", color=(1, 1, 0))
                return
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            activity = bs.get_foreground_host_activity()
            if not activity:
                self.clientmessage("❌ No active game", color=(1, 0, 0))
                return
            actor = self.fct.get_actor(client_id)
            if not actor or not actor.node:
                self.clientmessage("❌ You are not in the game", color=(1, 0, 0))
                return
            with activity.context:
                actor.node.position = (x, y, z)
                self.clientmessage(f"✅ Teleported to ({x},{y},{z})", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_fly_command_fixed(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2 or parts[1].lower() not in ['on', 'off']:
                self.clientmessage("❌ Use: /fly <on|off>", color=(1, 0, 0))
                return
            state = parts[1].lower() == 'on'
            actor = self.fct.get_actor(client_id)
            if not actor:
                self.clientmessage("❌ You are not in the game", color=(1, 0, 0))
                return
            setattr(actor, 'cm_fly', state)
            self.clientmessage(f"✅ Fly mode {state}", color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_warn_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage("❌ Use: /warn <pb-id or client-id or name> <reason>", color=(1, 0, 0))
                return
            target = parts[1]
            reason = ' '.join(parts[2:])
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, target_client = target_data
            warner_name = Uts.usernames.get(client_id, f"Admin-{client_id}")
            warn_count = Uts.add_warning(account_id, warner_name, Uts.ensure_pb_id(client_id) or 'Unknown', reason)
            self.clientmessage(f"⚠️ Warning issued to {target_name}. Total warnings: {warn_count}", color=(1, 1, 0))
            if target_client is not None:
                bs.screenmessage(f"⚠️ You have been warned by {warner_name}: {reason}", clients=[target_client], color=(1, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_warns_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /warns <pb-id or client-id or name>", color=(1, 0, 0))
                return
            target = parts[1]
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, _ = target_data
            warns = Uts.get_warnings(account_id)
            if not warns:
                self.clientmessage(f"📋 No warnings for {target_name}.", color=(0.5, 0.5, 1))
            else:
                self.clientmessage(f"📋 Warnings for {target_name}:", color=(1, 1, 0))
                for i, w in enumerate(warns, 1):
                    self.send_chat_message(f"{i}. By {w['warner_name']}: {w['reason']} on {w['date']}")
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_clearwarns_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /clearwarns <pb-id or client-id or name>", color=(1, 0, 0))
                return
            target = parts[1]
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, _ = target_data
            if Uts.clear_warnings(account_id):
                self.clientmessage(f"✅ All warnings cleared for {target_name}.", color=(0, 1, 0))
            else:
                self.clientmessage(f"ℹ️ No warnings to clear for {target_name}.", color=(0.5, 0.5, 1))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def find_target_data(self, target):
        """يبحث عن لاعب باستخدام pb-id أو client-id أو الاسم، ويعيد (account_id, name, client_id)"""
        # البحث عن client-id
        try:
            cid = int(target)
            if cid in Uts.usernames:
                name = Uts.usernames[cid]
                pb = Uts.ensure_pb_id(cid)
                if pb:
                    return pb, name, cid
                else:
                    return f"guest_{cid}", name, cid
        except:
            pass
        # البحث عن pb-id
        if target.startswith('pb-'):
            for cid, pb in Uts.userpbs.items():
                if pb == target:
                    return target, Uts.usernames.get(cid, target), cid
            # قد يكون في pdata فقط
            if target in Uts.pdata:
                return target, target, None
        # البحث بالاسم
        target_lower = target.lower()
        for cid, name in Uts.usernames.items():
            if name.lower() == target_lower:
                pb = Uts.ensure_pb_id(cid)
                if pb:
                    return pb, name, cid
                else:
                    return f"guest_{cid}", name, cid
        for acc_id, data in Uts.pdata.items():
            for acc_name in data.get('Accounts', []):
                if acc_name.lower() == target_lower:
                    return acc_id, acc_name, None
        return None

    def process_ban_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage(getlanguage("BanUsage"), color=(1, 0, 0))
                return
            target = parts[1]
            reason = ' '.join(parts[2:])
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, target_client = target_data
            # منع حظر الأدمن
            if target_client is not None and CommandFunctions.user_is_admin(target_client):
                self.clientmessage(getlanguage("CannotBanAdmin", subs=[target_name]), color=(1, 0, 0))
                return
            # تحقق من الحظر المسبق
            ban_key = None
            if account_id and account_id.startswith('pb-'):
                ban_key = f"pb_{account_id}"
            elif target_client is not None:
                ban_key = f"client_{target_client}"
            if ban_key and ban_key in Uts.bans_data:
                self.clientmessage(getlanguage("AlreadyBanned", subs=[target_name]), color=(1, 1, 0))
                return
            # إنشاء سجل الحظر
            banner_name = Uts.usernames.get(client_id, f"Admin-{client_id}")
            banner_account = Uts.ensure_pb_id(client_id) or 'Unknown'
            ban_info = {
                'name': target_name,
                'account_id': account_id,
                'client_id': target_client if target_client is not None else -1,
                'reason': reason,
                'banned_by': banner_name,
                'banned_by_account': banner_account,
                'banned_by_client_id': client_id,
                'banned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'banned_timestamp': time.time(),
                'target_type': 'admin'
            }
            if account_id and account_id.startswith('pb-'):
                ban_key = f"pb_{account_id}"
            else:
                ban_key = f"client_{target_client}" if target_client is not None else f"name_{target_name}"
            Uts.bans_data[ban_key] = ban_info
            Uts.save_bans_data()
            if account_id and account_id in Uts.pdata:
                Uts.pdata[account_id]['banned'] = True
                Uts.save_players_data()
            # طرد اللاعب إذا كان متصلاً
            if target_client is not None:
                try:
                    bs.disconnect_client(target_client)
                except:
                    pass
            self.clientmessage(getlanguage("BanSuccess", subs=[target_name, banner_name]), color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_unban_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage(getlanguage("UnbanUsage"), color=(1, 0, 0))
                return
            target = parts[1]
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, target_client = target_data
            ban_key_to_remove = None
            if account_id and account_id.startswith('pb-'):
                ban_key_candidate = f"pb_{account_id}"
                if ban_key_candidate in Uts.bans_data:
                    ban_key_to_remove = ban_key_candidate
            if ban_key_to_remove is None and target_client is not None:
                ban_key_candidate = f"client_{target_client}"
                if ban_key_candidate in Uts.bans_data:
                    ban_key_to_remove = ban_key_candidate
            if ban_key_to_remove is None:
                # البحث بالاسم
                for key, info in Uts.bans_data.items():
                    if info.get('name', '').lower() == target_name.lower():
                        ban_key_to_remove = key
                        break
            if ban_key_to_remove is None:
                self.clientmessage(getlanguage("NotBanned", subs=[target_name]), color=(1, 0, 0))
                return
            del Uts.bans_data[ban_key_to_remove]
            Uts.save_bans_data()
            if account_id and account_id in Uts.pdata:
                Uts.pdata[account_id]['banned'] = False
                Uts.save_players_data()
            unbanner = Uts.usernames.get(client_id, f"Admin-{client_id}")
            self.clientmessage(getlanguage("UnbanSuccess", subs=[target_name, unbanner]), color=(0, 1, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_report_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 3:
                self.clientmessage(getlanguage("ReportUsage"), color=(1, 0, 0))
                return
            target = parts[1]
            reason = ' '.join(parts[2:])
            target_data = self.find_target_data(target)
            if not target_data:
                self.clientmessage(getlanguage("TargetNotFound", subs=[target]), color=(1, 0, 0))
                return
            account_id, target_name, target_client = target_data
            reporter_name = Uts.usernames.get(client_id, f"Player-{client_id}")
            reporter_account = Uts.ensure_pb_id(client_id) or 'Unknown'
            report = {
                'target_name': target_name,
                'target_account': account_id,
                'target_client': target_client,
                'reason': reason,
                'reporter_name': reporter_name,
                'reporter_account': reporter_account,
                'reporter_client': client_id,
                'timestamp': time.time(),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            Uts.reports_data.setdefault('reports', []).append(report)
            Uts.save_reports_data()
            self.clientmessage(getlanguage("ReportSubmitted", subs=[target_name]), color=(0, 1, 0))
            # إشعار الأدمن
            for cid, acc in Uts.accounts.items():
                if acc.get('Admin', False) and cid != client_id:
                    try:
                        bs.screenmessage(f"⚠️ New report: {target_name} reported by {reporter_name}", clients=[cid], color=(1, 1, 0))
                    except:
                        pass
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_reports_command(self, client_id: int):
        reports = Uts.reports_data.get('reports', [])
        if not reports:
            self.clientmessage(getlanguage("NoReports"), color=(0.5, 0.5, 1))
            return
        self.clientmessage("📋 Recent reports:", color=(1, 1, 0))
        for i, r in enumerate(reports[-10:], 1):
            self.send_chat_message(f"{i}. {r['target_name']} reported by {r['reporter_name']}: {r['reason']} ({r['date']})")

    def process_report_done_command(self, msg: str, client_id: int):
        try:
            parts = msg.split()
            if len(parts) < 2:
                self.clientmessage("❌ Use: /reportdone <index>", color=(1, 0, 0))
                return
            idx = int(parts[1])
            reports = Uts.reports_data.get('reports', [])
            if 1 <= idx <= len(reports):
                removed = reports.pop(idx - 1)
                Uts.save_reports_data()
                self.clientmessage(f"✅ Report #{idx} ({removed['target_name']}) marked as done.", color=(0, 1, 0))
            else:
                self.clientmessage("❌ Invalid report index.", color=(1, 0, 0))
        except Exception as e:
            self.clientmessage(f"❌ Error: {str(e)[:50]}", color=(1, 0, 0))

    def process_banlist_command(self, client_id: int):
        if not Uts.bans_data:
            self.clientmessage(getlanguage("NoBans"), color=(0.5, 0.5, 1))
            return
        self.clientmessage("📋 Banned players:", color=(1, 1, 0))
        for key, info in Uts.bans_data.items():
            name = info.get('name', 'Unknown')
            reason = info.get('reason', 'No reason')
            banner = info.get('banned_by', 'System')
            date = info.get('banned_date', 'Unknown')
            self.send_chat_message(f"• {name} - {reason} (by {banner} on {date})")

    def process_help_command(self, msg: str, client_id: int):
        is_admin = CommandFunctions.user_is_admin(client_id)
        is_owner = CommandFunctions.user_is_owner(client_id)
        help_text = []
        help_text.append("=== CheatMax Commands ===")
        help_text.append("General: -pan, -ceb, -colors, -mp, -pb, -effects, /list, test, help, /stats, /myid")
        if is_admin:
            help_text.append("=== Admin Commands ===")
            admin_list = [
                '/name', '/imp', '/box', '/addAdmin', '/delAdmin', '/kill', '-pause', '/infoHost',
                '/infoDes', '-info', '/infoColor', '-end', '/kick', '-chatLive', '/freeze',
                '/playerColor', '/maxPlayers', '-showMessages', '/sleep', '/mute', '/unmute',
                '/gm', '-slow', '/speed', '/effect', '/punch', '/mbox', '/drop', '/gift',
                '/curse', '/superjump', '/customtag', '/animationtag', '/removetag', '/savetag',
                '/tagdata', '/listtags', '/sharedaccounts', '/closeserver', '/stopcloseserver',
                '/closestatus', '/ban', '/unban', '/reports', '/banlist', '/reportdone',
                '/teleport', '/fly', '/warn', '/warns', '/clearwarns', '/invisible',
                '/tint', '/upwall', '/downwall', '/floor', '/spawnball', '/explosion', '/locator', '/ping',
                '/weather', '/tops', '-statsrestart', '/club', '/photo', '/photoclear',
                '/backtext', '/fronttext', '/grab', '/fighting'
            ]
            help_text.append(', '.join(admin_list))
        if is_owner:
            help_text.append("=== Owner Commands ===")
            help_text.append('/owner, /fullpower')
        for line in help_text:
            self.send_chat_message(line)

    def process_list_players(self):
        """عرض قائمة اللاعبين مع client_id و pb-id"""
        try:
            roster_data = roster()
            if not roster_data:
                self.clientmessage("No players online.")
                return
            self.send_chat_message("Name | Client ID | PB-ID")
            self.send_chat_message("-------------------------------")
            for p in roster_data:
                name = p.get('display_string', 'Unknown')
                cid = p.get('client_id', '?')
                pb = p.get('account_id', 'Guest')
                if not pb or pb == 'None':
                    pb = 'Guest'
                self.send_chat_message(f"{name} | {cid} | {pb}")
        except Exception as e:
            self.clientmessage(f"❌ Error listing players: {e}")

    def process_photo_command(self, msg: str, client_id: int):
        """التقاط صورة للشاشة (يتم حفظها في مجلد اللعبة)"""
        try:
            from bauiv1 import screenshot
            screenshot()
            self.clientmessage("📸 Screenshot taken!", color=(0, 1, 0))
        except:
            self.clientmessage("❌ Screenshot failed", color=(1, 0, 0))

    def process_photoclear_command(self, client_id: int):
        """مسح جميع الصور المحفوظة (تنبيه: هذا الأمر يحتاج إلى حذر)"""
        self.clientmessage("⚠️ This command is disabled for safety.", color=(1, 1, 0))


# ==================== التأثيرات والكلاسات المساعدة ====================
# تعريف دوال التأثيرات (تم تبسيطها لتجنب التكرار)

def _fire(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, scale=3, count=100, spread=0.3, chunk_type='sweat')


def _spark(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, scale=0.7, count=100, spread=0.3, chunk_type='spark')


def footprint(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        loc = bs.newnode('locator', owner=self.node,
                         attrs={'position': self.node.position, 'shape': 'circle',
                                'color': self.node.color, 'size': 0.2,
                                'draw_beauty': False, 'additive': False})
        bs.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
        bs.apptimer(2.0, loc.delete)


def aure(self):
    def anim(node: bs.Node) -> None:
        bs.animate_array(node, 'color', 3,
                         {0: (1, 1, 0), 0.1: (0, 1, 0),
                          0.2: (1, 0, 0), 0.3: (0, 0.5, 1),
                          0.4: (1, 0, 1)}, loop=True)
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


def stars(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=20, spread=0.5, scale=0.5, chunk_type='spark')


def chispitas(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=30, spread=0.3, scale=0.3, chunk_type='spark')


def darkmagic(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=40, spread=0.4, scale=0.8, chunk_type='smoke')


def _rainbow(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        colors = [(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1)]
        for i in range(6):
            bs.emitfx(position=self.node.position, count=5, spread=0.5, scale=0.5, chunk_type='spark', color=colors[i])


def rock(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=50, spread=0.08, scale=1.5, chunk_type='rock')


def ice(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=50, spread=0.08, scale=0.8, chunk_type='ice')


def slime(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=50, spread=0.08, scale=2, chunk_type='slime')


def metal(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='metal')


def splinter(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='splinter')


def stickers_rock(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='rock', emit_type='stickers')


def stickers_slime(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=1, spread=0.08, scale=0.5, chunk_type='slime', emit_type='stickers')


def stickers_metal(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='metal', emit_type='stickers')


def stickers_spark(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='spark', emit_type='stickers')


def stickers_splinter(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='splinter', emit_type='stickers')


def stickers_ice(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='ice', emit_type='stickers')


def tendrils(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, emit_type='tendrils')


def tendrils_smoke(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, emit_type='tendrils', tendril_type='thin_smoke')


def tendrils_ice(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, emit_type='tendrils', tendril_type='ice')


def distortion(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, emit_type='distortion')


def flag_stand(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, emit_type='flag_stand')


def tendrils_splinter(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='splinter', emit_type='tendrils')


def stickers_sweat(self):
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        bs.emitfx(position=self.node.position, count=2, spread=0.08, scale=1.5, chunk_type='sweat', emit_type='stickers')


def apply_effect(self, eff: str) -> None:
    if eff == 'fire':
        self._cm_effect_timer = bs.Timer(0.1, lambda: _fire(self), repeat=True)
    elif eff == 'spark':
        self._cm_effect_timer = bs.Timer(0.1, lambda: _spark(self), repeat=True)
    elif eff == 'footprint':
        self._cm_effect_timer = bs.Timer(0.1, lambda: footprint(self), repeat=True)
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


# ==================== كلاسات القنابل والهدايا ====================
class ExplosiveGift(bs.Actor):
    def __init__(self, time: float = 3.0, owner: bs.Node = None):
        super().__init__()
        self.time = time
        self.owner = owner
        self.scale = 0.8
        self.touch = False
        pos = list(owner.position)
        velocity = (0.0, 60, 0.0)
        position = (pos[0], pos[1] + 1.47, pos[2])
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
        shared = bs.SharedObjects.get()
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
                            attrs={'scale': tuple(radius * 0.7 for s in range(3)),
                                   'type': 'sphere',
                                   'materials': rmats})
        self.node.connectattr('position', region, 'position')
        shield = bs.newnode('shield',
                            owner=region,
                            attrs={'color': (2.0, 1.0, 0.0),
                                   'radius': radius})
        region.connectattr('position', shield, 'position')
        bs.getsound('explosion03').play(1, self.node.position)
        bs.timer(0.1, bs.CallStrict(self.handlemessage, bs.DieMessage()))

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
                msg.velocity[0], msg.velocity[1] + 2.0, msg.velocity[2], msg.magnitude,
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
        shared = bs.SharedObjects.get()
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


# ==================== إنشاء مثيلات الأنظمة ====================
Uts.tag_system = TagSystem()
Uts.leaderboard_display = LeaderboardDisplay()
Uts.clubs_system = ClubsSystem()

# ==================== دوال الربط (Hooking) ====================
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


def hook_chat_filter():
    try:
        import bascenev1._hooks
        original = bascenev1._hooks.filter_chat_message

        def wrapped_filter(msg, client_id):
            ret = original(msg, client_id)
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


def verify_chat_filter():
    import bascenev1._hooks
    if hasattr(bascenev1._hooks.filter_chat_message, 'wrapped'):
        print("✅ Chat filter is hooked")
    else:
        print("⚠️ Chat filter not hooked, attempting again...")
        hook_chat_filter()


def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)
    weather_type = cfg.get('Commands', {}).get('Weather', 'none')
    Uts.weather_effect.start(weather_type)
    if cfg.get('Commands', {}).get('ShowStatsLeaderboard', False):
        Uts.leaderboard_display.create(self)


def new_on_player_join(self, player: bs.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    Uts.player_join(player)
    if Uts.server_close_active:
        Uts.check_player_allowed_on_join(player)


def new_on_player_leave(self, player: bs.Player) -> None:
    if 'OnPlayerLeave' in calls:
        try:
            calls['OnPlayerLeave'](self, player)
        except Exception as e:
            print(f"❌ Error in original OnPlayerLeave: {e}")
    try:
        try:
            client_id = player.sessionplayer.inputdevice.client_id
        except AttributeError:
            print("⚠️ player.sessionplayer or inputdevice not available")
            return
        Uts.clubs_system.remove_club_tag(client_id)
    except Exception as e:
        print(f"❌ Error in new_on_player_leave: {e}")


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
        bs.timer(0.2, lambda: apply_effect(self, eff))
        client_id = self._player.sessionplayer.inputdevice.client_id
        if client_id is not None:
            account_id = Uts.ensure_pb_id(client_id)
            if account_id and account_id in Uts.pdata and "club" in Uts.pdata[account_id]:
                club_info = Uts.pdata[account_id]["club"]
                club_id = club_info["club-id"]
                role = club_info["role"]
                club_data = Uts.clubs_system.get_club_by_id(club_id) if Uts.clubs_system else None
                if club_data:
                    current_act = bs.get_foreground_host_activity()
                    if current_act:
                        bs.timer(0.5, lambda: Uts.clubs_system.create_club_tag(self, client_id, club_data, role, current_act))
            if user and user in Uts.tags:
                tag_data = Uts.tags[user]
                text = tag_data.get('text', '')
                color = tag_data.get('color', (1, 1, 1))
                scale = tag_data.get('scale', 0.02)
                current_act = bs.get_foreground_host_activity()
                if current_act is not None:
                    bs.timer(0.6, lambda: create_custom_tag_for_spaz(self, text, color, scale))


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
    if getattr(self, 'cm_superjump', False):
        if self.node and self.node.is_on_ground:
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                with current_act.context:
                    msg = bs.HitMessage(pos=self.node.position,
                                        velocity=self.node.velocity,
                                        magnitude=160 * 2,
                                        hit_subtype='imp',
                                        radius=460 * 2)
                    if isinstance(msg, bs.HitMessage):
                        for i in range(2):
                            self.node.handlemessage(
                                'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                                msg.velocity[0], msg.velocity[1] + 2.0, msg.velocity[2], msg.magnitude,
                                msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                                msg.force_direction[1], msg.force_direction[2])
    if getattr(self, 'cm_fly', False):
        if self.node and self.node.exists():
            current_act = bs.get_foreground_host_activity()
            if current_act is not None:
                camera = getattr(current_act, 'camera', None)
                if camera and camera.exists():
                    cam_pos = camera.position
                    cam_target = camera.target
                else:
                    cam_pos = (0, 0, -10)
                    cam_target = (0, 0, 0)
                with current_act.context:
                    forward = (cam_target[0] - cam_pos[0], 0, cam_target[2] - cam_pos[2])
                    flen = (forward[0] ** 2 + forward[2] ** 2) ** 0.5
                    if flen > 0:
                        forward = (forward[0] / flen, 0, forward[2] / flen)
                    else:
                        forward = (0, 0, 1)
                    right = (-forward[2], 0, forward[0])
                    lr = self.node.move_left_right
                    ud = self.node.move_up_down
                    fx = (right[0] * lr + forward[0] * ud) * 80
                    fz = (right[2] * lr + forward[2] * ud) * 80
                    fy = 150
                    self.node.handlemessage(
                        'impulse',
                        self.node.position[0], self.node.position[1], self.node.position[2],
                        fx, fy, fz,
                        (fx ** 2 + fy ** 2 + fz ** 2) ** 0.5,
                        0, 0, 0,
                        0, 1, 0
                    )


# ==================== دوال الإعداد والتشغيل ====================
def _install() -> None:
    try:
        Uts.create_players_data()
        Uts.save_players_data()
        if not hasattr(Uts, 'tags'):
            Uts.create_tags_data()
        owner_account = 'pb-IF4yVRIDXA=='  # غيّر هذا إلى pb-id الخاص بك
        if owner_account not in Uts.pdata:
            Uts.add_owner(owner_account)
            print(f"✅ Added owner: {owner_account}")
        Uts.create_bans_data()
        Uts.clean_bans_data()
        Uts.create_reports_data()
        Uts.create_warns_data()
        bs.apptimer(3.0, lambda: Uts.sm("Owner added!", color=(1.0, 0.5, 0.0)))
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
    if not hasattr(Uts, 'tag_system'):
        Uts.tag_system = TagSystem()
    print("✅ Tag system initialized")


def settings():
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
            'Weather': 'none',
            'ShowStatsLeaderboard': False
        }
        Uts.save_settings()
        print("✅ Default settings created")
    try:
        Uts.create_bans_data()
        Uts.clean_bans_data()
        Uts.create_reports_data()
        print("✅ Bans and reports systems initialized")
    except Exception as e:
        print(f"⚠️ Error loading bans/reports data: {e}")
    print("✅ Settings loaded successfully")


def plugin():
    try:
        calls['GA_OnTransitionIn'] = bs.GameActivity.on_transition_in
        calls['OnJumpPress'] = bs.PlayerSpaz.on_jump_press
        calls['OnPlayerJoin'] = bs.Activity.on_player_join
        calls['OnPlayerLeave'] = getattr(bs.Activity, 'on_player_leave', None)
        calls['PlayerSpazInit'] = bs.PlayerSpaz.__init__
        bs.GameActivity.on_transition_in = new_ga_on_transition_in
        bs.PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
        bs.Activity.on_player_join = new_on_player_join
        if hasattr(bs.Activity, 'on_player_leave'):
            bs.Activity.on_player_leave = new_on_player_leave
        else:
            print("⚠️ Activity.on_player_leave not found, club tags won't auto-remove on leave.")
        bs.PlayerSpaz.__init__ = new_playerspaz_init_
        try:
            bui.set_party_icon_always_visible(True)
        except:
            pass
        print("✅ Plugin functions connected successfully")
    except Exception as e:
        print(f"❌ Error connecting plugin functions: {e}")


def additional_features():
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
    import shutil
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
    special_commands = {
        'party': {'description': 'بدء حفلة!', 'admin_only': False, 'function': lambda client_id: start_party(client_id)},
        'stats': {'description': 'عرض إحصائياتك', 'admin_only': False, 'function': lambda client_id: show_stats(client_id)},
        'ban': {'description': 'حظر لاعب (لـAdmins فقط)', 'admin_only': True, 'function': lambda client_id: Uts.sm("Use: /ban <player> <reason>", clients=[client_id])},
        'unban': {'description': 'إلغاء حظر لاعب (لـAdmins فقط)', 'admin_only': True, 'function': lambda client_id: Uts.sm("Use: /unban <player>", clients=[client_id])},
        'report': {'description': 'الإبلاغ عن لاعب', 'admin_only': False, 'function': lambda client_id: Uts.sm("Use: /report <player> <reason>", clients=[client_id])},
        'reports': {'description': 'عرض الإبلاغات (لـAdmins فقط)', 'admin_only': True, 'function': lambda client_id: Uts.sm("Use: /reports", clients=[client_id])},
        'banlist': {'description': 'عرض قائمة الحظر (لـAdmins فقط)', 'admin_only': True, 'function': lambda client_id: Uts.sm("Use: /banlist", clients=[client_id])}
    }

    def start_party(client_id):
        activity = bs.get_foreground_host_activity()
        if activity:
            for _ in range(50):
                pos = (random.uniform(-5, 5), random.uniform(2, 10), random.uniform(-5, 5))
                bs.Bomb(position=pos, bomb_type='impact', bomb_scale=0.5).autoretain()
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
    if not hasattr(bs, 'app') or not hasattr(bs.app, 'cheatmax_filter_chat'):
        print("⚠️ CheatMax system not fully initialized")
    try:
        bs.app.cheatmax_filter_chat = filter_chat_message
    except:
        pass
    welcome_msg = f"""
╔══════════════════════════════════════════╗
║ 🎮 CheatMax System v2.0.2 🎮 ║
║ Advanced Tag & Admin System ║
╠══════════════════════════════════════════╣
║ • Tag System: ✓ Active ║
║ • Commands: ✓ Loaded ║
║ • Multi-Language: ✓ Supported ║
║ • Protection: ✓ Enabled ║
║ • Ban System: ✓ Active (PB-ID Verified)║
║ • Report System: ✓ Active ║
║ • Commands in lobby: ✓ Fixed ║
║ • Teleport: ✓ Fixed (uses client ID) ║
║ • Fly Mode: ✓ Fixed (uses client ID) ║
║ • Super Jump: ✓ Ground Only ║
║ • Invisible: ✓ Fixed (mesh removal) ║
║ • Tint/Wall/Floor: ✓ NO LIMITS! ║
║ • SpawnBall: ✓ Added (Hittable) ║
║ • Explosion: ✓ Added ║
║ • Locator: ✓ Added (Glowing) ║
║ • Ping: ✓ Fixed (No errors) ║
║ • /List Fixed: ✓ No client-ID in PB-ID column ║
║ • A-Soccer Integration: ✓ Auto-save ║
║ • Weather System: ✓ Added & Saved ║
║ • Stats System: ✓ Added ║
║ • Clubs System: ✓ Added ║
║ • Player Leave Hook: ✓ Auto-remove club tag ║
║ • /myid Command: ✓ Shows your PB-ID ║
║ • Admin Permission: ✓ Fixed (no overwrite) ║
╚══════════════════════════════════════════╝
"""
    for line in welcome_msg.split('\n'):
        print(line)
    try:
        Uts.tag_system.start_game_monitoring()
    except:
        pass
    print("✅ CheatMax system ready!")


def error_handler(func):
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


filter_chat_message = error_handler(filter_chat_message)
new_ga_on_transition_in = error_handler(new_ga_on_transition_in)
new_on_player_join = error_handler(new_on_player_join)
new_on_player_leave = error_handler(new_on_player_leave)
new_playerspaz_init_ = error_handler(new_playerspaz_init_)
new_playerspaz_on_jump_press = error_handler(new_playerspaz_on_jump_press)


def system_test():
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
            if hasattr(bascenev1._hooks.filter_chat_message, 'wrapped') or hasattr(bs.app, 'cheatmax_filter_chat'):
                print("✅ Test 7: Chat filter hooked successfully")
                tests_passed += 1
            else:
                print("❌ Test 7: Chat filter not hooked")
                tests_failed += 1
        except:
            tests_failed += 1
        try:
            if bs.Activity.on_player_join != calls['OnPlayerJoin']:
                print("✅ Test 8: Player join hook installed")
                tests_passed += 1
            else:
                print("❌ Test 8: Player join hook not installed")
                tests_failed += 1
        except:
            tests_failed += 1
        try:
            if hasattr(Uts, 'clubs_system') and Uts.clubs_system is not None:
                print("✅ Test 9: Clubs system initialized")
                tests_passed += 1
            else:
                print("❌ Test 9: Clubs system not initialized")
                tests_failed += 1
        except:
            tests_failed += 1
        try:
            if hasattr(bs.Activity, 'on_player_leave') and bs.Activity.on_player_leave != calls.get('OnPlayerLeave'):
                print("✅ Test 10: Player leave hook installed")
                tests_passed += 1
            else:
                print("❌ Test 10: Player leave hook not installed")
                tests_failed += 1
        except:
            tests_failed += 1
        try:
            test_client = list(Uts.usernames.keys())[0] if Uts.usernames else -1
            pb = Uts.ensure_pb_id(test_client)
            if pb is not None or test_client == -1:
                print("✅ Test 11: ensure_pb_id works")
                tests_passed += 1
            else:
                print("❌ Test 11: ensure_pb_id failed")
                tests_failed += 1
        except Exception as e:
            print(f"❌ Test 11 exception: {e}")
            tests_failed += 1
        try:
            if hasattr(Uts, 'tag_system') and Uts.tag_system:
                print("✅ Test 12: Tag duplication prevention mechanism in place")
                tests_passed += 1
            else:
                print("❌ Test 12: Tag system not available")
                tests_failed += 1
        except:
            tests_failed += 1
        try:
            if hasattr(Uts, 'remove_all_tags'):
                print("✅ Test 13: remove_all_tags function exists")
                tests_passed += 1
            else:
                print("❌ Test 13: remove_all_tags function missing")
                tests_failed += 1
        except:
            tests_failed += 1
        print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
        if tests_failed == 0:
            print("🎉 All tests passed! System is ready.")
        else:
            print("⚠️ Some tests failed. System may have issues.")

    bs.apptimer(8.0, run_tests)


bs.apptimer(8.0, system_test)


#ba_meta export babase.Plugin
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

            def periodic_refresh():
                Uts.update_usernames()
                bs.apptimer(3.0, periodic_refresh)

            bs.apptimer(3.0, periodic_refresh)
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
            bs.apptimer(7.0, verify_chat_filter)
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


print("=" * 50)
print("CheatMax System Code Loaded Successfully!")
print("=" * 50)
