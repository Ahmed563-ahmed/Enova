# ba_meta require api 9

from __future__ import annotations

import json
import datetime
import math
import inspect
import babase
import random
import bauiv1 as bui
import bascenev1 as bs
from os import listdir
from bascenev1lib import maps
import bascenev1
from os import makedirs, path
from typing import TYPE_CHECKING, Any, Sequence, Dict, Type, List, Optional, Union, Tuple
from bascenev1lib.actor import playerspaz
from bascenev1lib.actor.bomb import Bomb
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1 import get_foreground_host_activity as ga
import os
import _babase

if TYPE_CHECKING:
    from typing import Any, Sequence, Dict, Type, List, Optional, Union, Tuple

DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

# ==================== مسار ملف إعدادات A-Soccer ====================
CONFIG_DIR = os.path.join(_babase.app.env.python_directory_user, 'Configs')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'A-SoccerConfig.json')

# ==================== مسار ملف بيانات CheatMax ====================
CHEATMAX_PLAYERS_FILE = os.path.join(CONFIG_DIR, 'CheatMaxPlayersData.json')

# ---------- وظائف مساعدة للتعامل مع إحصائيات CheatMax ----------
def _load_cheatmax_data() -> dict:
    """تحميل بيانات جميع اللاعبين من CheatMaxPlayersData.json"""
    if not os.path.exists(CHEATMAX_PLAYERS_FILE):
        return {}
    try:
        with open(CHEATMAX_PLAYERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def _save_cheatmax_data(data: dict):
    """حفظ بيانات جميع اللاعبين إلى CheatMaxPlayersData.json"""
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        with open(CHEATMAX_PLAYERS_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        debug_print(f"⚠️ Failed to save CheatMax data: {e}")

def _ensure_player_stats(account_id: str) -> dict:
    """تأكد من وجود قسم Stats للاعب – مع إضافة Draws"""
    data = _load_cheatmax_data()
    if account_id not in data:
        data[account_id] = {
            'Mute': False,
            'Effect': 'none',
            'Admin': False,
            'Owner': False,
            'Accounts': [],
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
    elif 'Stats' not in data[account_id]:
        data[account_id]['Stats'] = {
            'goals': 0,
            'assists': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'games': 0,
            'score': 0.0,
            'rank': 0
        }
    elif 'draws' not in data[account_id]['Stats']:
        # ترقية للاعبين القدامى
        data[account_id]['Stats']['draws'] = 0
    _save_cheatmax_data(data)
    return data[account_id]['Stats']

def _update_player_stats(account_id: str, goals=0, assists=0, win=False, loss=False, draw=False):
    """تحديث إحصائيات لاعب – مع دعم التعادل"""
    data = _load_cheatmax_data()
    _ensure_player_stats(account_id)
    stats = data[account_id]['Stats']
    stats['goals'] += goals
    stats['assists'] += assists
    if win:
        stats['wins'] += 1
    if loss:
        stats['losses'] += 1
    if draw:
        stats['draws'] += 1
    stats['games'] = stats['wins'] + stats['losses'] + stats['draws']
    # النقاط: أهداف*3 + تمريرات*2 + فوز*10 - خسارة*5 + تعادل*3
    stats['score'] = stats['goals']*3 + stats['assists']*2 + stats['wins']*10 - stats['losses']*5 + stats['draws']*3
    _save_cheatmax_data(data)

def _recalculate_all_ranks():
    """إعادة ترتيب جميع اللاعبين حسب score – يحفظ الرتبة"""
    data = _load_cheatmax_data()
    players_with_stats = []
    for acc_id, pdata in data.items():
        if 'Stats' in pdata:
            players_with_stats.append((acc_id, pdata['Stats']['score']))
    players_with_stats.sort(key=lambda x: x[1], reverse=True)
    for idx, (acc_id, _) in enumerate(players_with_stats, start=1):
        data[acc_id]['Stats']['rank'] = idx
    _save_cheatmax_data(data)

def _get_rank_icon(rank: int) -> tuple[str, tuple]:
    """إرجاع (رمز_الأيقونة, اللون) – أيقونات من قائمة CheatMax"""
    if rank == 1:
        return '\ue02f', (1.0, 0.84, 0.0)   
    elif rank == 2 or rank == 3:
        return '\ue02c', (0.75, 0.75, 0.75) 
    elif 4 <= rank <= 15:
        return '\ue02b', (0.8, 0.5, 0.2)    
    else:
        return '', (1,1,1)

# -------------------------------------------------------------

NormalPlayerSpaz = playerspaz.PlayerSpaz

class NewPlayerSpaz(playerspaz.PlayerSpaz):
    def __init__(self, player: bascenev1.Player, color: Sequence[float] = (1.0, 1.0, 1.0), 
                 highlight: Sequence[float] = (0.5, 0.5, 0.5), character: str = 'Spaz', 
                 powerups_expire: bool = True, start_invincible: bool = False):
        super().__init__(player=player, color=color, highlight=highlight, 
                        character=character, powerups_expire=powerups_expire)
        self.equip_boxing_gloves()
        self.player = player
        # أيقونة الرتبة (تحفظ كمرجع)
        self.rank_icon = None
        self.rank_icon_math = None
    
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.HitMessage):
            self.node.handlemessage('flash')
            pass
        else:
            return super().handlemessage(msg)

class BallDiedMessage:
    def __init__(self, ball: Ball):
        self.ball = ball

class Ball(bs.Actor):
    def __init__(self, position: Sequence[float] = (0.0, 0.0, 0.0), is_area_of_interest: bool = True):
        super().__init__()
        activity = self.getactivity()
        assert activity is not None
        assert isinstance(activity, SoccerGame)
        self.scale = 1
        self.mesh_scale = self.scale * 0.25
        self.gravity = 1
        shared = SharedObjects.get()
        
        ball_material = [shared.object_material, activity.ball_material]
        self.all_players_hitted: List[bs.Player] = []
        self.all_players_touched: Dict[int, bs.Player] = {}
        self.spawn_pos = (position[0], position[1] + 0.6, position[2])
        self.original_texture = activity.ball_tex
        
        self.node = bs.newnode('prop', delegate=self, attrs={
            'mesh': activity.ball_model,
            'color_texture': self.original_texture,
            'body': 'sphere',
            'body_scale': self.scale,
            'mesh_scale': self.mesh_scale,
            'reflection': 'soft',
            'reflection_scale': [0.3],
            'shadow_size': 3,
            'is_area_of_interest': is_area_of_interest,
            'position': self.spawn_pos,
            'materials': ball_material,
            'gravity_scale': 0
        })
        bs.animate(self.node, 'mesh_scale', {0: 0, 0.01: self.mesh_scale})
        
        self.last_hit_time = 0
        self.texture_changed = False
        self.hit_timestamps = []

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            assert self.node
            self.node.delete()
            activity = self._activity()
            if activity and not msg.immediate:
                activity.handlemessage(BallDiedMessage(self))
        
        elif isinstance(msg, bs.OutOfBoundsMessage):
            assert self.node
            self.node.position = self._spawn_pos
        
        elif isinstance(msg, bs.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1], msg.force_direction[2])
            
            s_player = msg.get_source_player(bs.Player)
            if s_player is not None:
                activity = self._activity()
                if activity:
                    if s_player in activity.players:
                        current_time = bs.time()
                        
                        self.all_players_touched[s_player.team.id] = s_player
                        
                        if s_player not in self.all_players_hitted:
                            self.all_players_hitted.append(s_player)
                        
                        self.hit_timestamps.append((s_player, current_time))
                        
                        print(f"Ball HIT by: {s_player.getname()} at {current_time:.1f}s (DIRECT HIT)")
            
            current_time = bs.time()
            if current_time - self.last_hit_time > 0.001:
                self.last_hit_time = current_time
                if not self.texture_changed:
                    self.texture_changed = True
                    self.node.color_texture = bs.gettexture('ouyaYButton')
                    
                    def revert_texture():
                        if self.node and self.texture_changed:
                            self.node.color_texture = self.original_texture
                            self.texture_changed = False
                    
                    bs.timer(0.1, revert_texture)
        else:
            super().handlemessage(msg)

    @property
    def _spawn_pos(self):
        return self.spawn_pos

class Wall(bs.Actor):
    def __init__(self, position: Tuple[float, float, float] = (0, 0, 0), 
                 scale: Tuple[int, int, int] = (10, 10, 10)):
        super().__init__()
        activity = self.getactivity()
        assert activity is not None
        assert isinstance(activity, SoccerGame)
        self.node = bs.newnode('region', attrs={
            'position': position,
            'scale': scale,
            'type': 'box',
            'materials': [activity.wall_material]
        })

class Dot(bs.Actor):
    def __init__(self, position: Tuple[float, float, float] = (0, 0, 0), 
                 size: List[float] = None, color: Tuple[float, float, float] = (1, 0, 0)):
        super().__init__()
        activity = bs.getactivity()
        if size is None:
            size = [0.3, 0.3, 0.3]
        elif isinstance(size, list) and len(size) == 1:
            size = [size[0], size[0], size[0]]
        elif isinstance(size, (int, float)):
            size = [float(size), float(size), float(size)]
            
        self.node = bs.newnode('locator', attrs={
            'shape': 'circle',
            'color': color,
            'opacity': 1,
            'position': position,
            'size': size,
            'drawShadow': False
        })

class Text(bs.Actor):
    def __init__(self, text: str = '', scale: float = 1.0, 
                 position: Tuple[float, float, float] = (0, 0, 0),
                 color: Tuple[float, float, float] = (1, 0, 0), shadow: float = 1.0,
                 h_align=None, v_attach=None, in_world=True):
        super().__init__()
        
        activity = self._activity()
        if activity is None:
            activity = bs.getactivity()
        
        if activity is None:
            try:
                self.node = bs.newnode('text', attrs={
                    'text': text,
                    'color': color,
                    'opacity': 1,
                    'position': position,
                    'scale': scale,
                    'in_world': in_world,
                    'shadow': shadow
                })
            except Exception as e:
                self.node = None
        else:
            self.node = bs.newnode('text', attrs={
                'text': text,
                'color': color,
                'opacity': 1,
                'position': position,
                'scale': scale,
                'in_world': in_world,
                'shadow': shadow
            })
        
        if self.node is not None:
            if h_align is not None:
                self.node.h_align = h_align
            if v_attach is not None:
                self.node.v_attach = v_attach

    def delete(self) -> None:
        try:
            if hasattr(self, 'node') and self.node is not None:
                if self.node.exists():
                    self.node.delete()
        except Exception as e:
            pass

class Player(bs.Player['Team']):
    pass

class Team(bs.Team[Player]):
    def __init__(self) -> None:
        self.score = 0

NEON_COLORS = {
    'cyan': (0, 1, 1),
    'pink': (1, 0, 1),
    'green': (0, 1, 0),
    'yellow': (1, 1, 0),
    'blue': (0, 0.5, 1),
    'orange': (1, 0.5, 0),
    'red': (1, 0, 0),
    'purple': (0.5, 0, 1)
}

# ثابت لمدة العداد الزمني المستقل (بالثواني)
CUSTOM_TIMER_DURATION = 300  # 5 دقائق

# ba_meta export bascenev1.GameActivity
class SoccerGame(bs.TeamGameActivity[Player, Team]):
    creator = "XERO Club"
    name = 'ㅤ'
    description = f"Showup Your Soccer Skills\nin a Very Customizable Soccer Game \ue047."
    gk_easy, gk_medium, gk_hard = 300, 350, 380
    
    available_settings = [
        bs.IntSetting('Target Score',
            min_value=1,
            default=10,
            increment=1
        ),
        bs.IntChoiceSetting('Game Time', choices=[
            ('None', 0),
            ('1 Minute', 60),
            ('2 Minutes', 120),
            ('5 Minutes', 300),
            ('10 Minutes', 600),
            ('20 Minutes', 1200)
        ], default=300),
        bs.FloatChoiceSetting('Respawn Times', choices=[
            ('Shorter', 0.1),
            ('Short', 0.5),
            ('Normal', 1.0),
            ('Long', 2.0),
            ('Longer', 4.0)
        ], default=0.1),
        bs.IntChoiceSetting('GK Practice Mode', choices=[
            ('Disabled', 0),
            ('Beginner', gk_easy),
            ('Amatuer', gk_medium),
            ('Intermediate', gk_hard),
        ], default=0),
        bs.IntChoiceSetting('Ball Texture', choices=[
            ('Blue Stripes', 1),
            ('Orange Stripes', 2),
            ('Yellow Stripes', 3),
            ('Volley Ball', 4),
        ], default=1),
        bs.BoolSetting('Epic SlowMotion', True),
        bs.BoolSetting('Map Posters', True),
        bs.BoolSetting('Night Mode', True),
        bs.BoolSetting('Invincible Players', True),
        bs.BoolSetting('Icy Ground', False),
        bs.BoolSetting('Enable Pickup', False),
        bs.BoolSetting('Assisted Ball', False)
    ]
    
    allow_pausing = False
    default_music = bs.MusicType.HOCKEY

    @classmethod
    def supports_session_type(cls, sessiontype: Type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        return ['Soccer Stadium']
    
    def __init__(self, settings: dict):
        super().__init__(settings)
        self._expired = False
        
        shared = SharedObjects.get()
        
        # Game Modes
        self.gk_mode = int(settings.get('GK Practice Mode', 0))
        self.gk_level = {0: None, self.gk_easy: 'Easy ★', self.gk_medium: 'Medium ★★', 
                        self.gk_hard: 'Hard ★★★'}.get(self.gk_mode, None)
        self.assistant_mode = bool(settings.get('Assisted Ball', False))
        
        # حفظ إعدادات الـTextures
        self.wall_down_texture_setting = 0
        self.wall_up_texture_setting = 0
        self.goals_texture_setting = 0
        
        # ========== ألوان قابلة للتخصيص من ملف JSON ==========
        self.wall_up_color = [0.1, 0.1, 0.7]      # افتراضي أزرق غامق
        self.wall_down_color = [2.0, 2.0, 2.0]   # افتراضي أبيض ساطع
        self.floor_color = [0.2, 0.75, 0.2]      # افتراضي أخضر
        
        # تحميل الإعدادات من ملف JSON إن وجد
        self.load_config()
        
        # حفظ الإعدادات
        self.weather_mode = 0
        
        # Game Settings
        self.map_posters = bool(settings.get('Map Posters', True))
        self.invincible_mode = bool(settings.get('Invincible Players', True))
        self.enable_pickup = bool(settings.get('Enable Pickup', False))
        self.icy_ground = bool(settings.get('Icy Ground', False))
        self.slow_motion = bool(settings.get('Epic SlowMotion', True))
        self.night_mode = bool(settings.get('Night Mode', True))
        self.score_to_win = int(settings.get('Target Score', 10))
        self.time_limit = float(settings.get('Game Time', 300))
        
        # ⭐ متغيرات العد التنازلي ⭐
        if self.time_limit > 0:
            self.match_time = int(self.time_limit)
        else:
            self.match_time = 300
        self.wall_timer_running = False
        
        # الأصوات - تم إضافة ding_sound هنا
        self.cheer_sound = bui.getsound('cheer')
        self.chant_sound = bui.getsound('crowdChant')
        self.foghorn_sound = bui.getsound('foghorn')
        self.swipsound = bui.getsound('swip')
        self.whistle_sound = bui.getsound('refWhistle')
        self.ding_sound = bui.getsound('ding')
        
        self.ball_textures = {
            1: bs.gettexture('ouyaUButton'),
            2: bs.gettexture('ouyaIcon'),
            3: bs.gettexture('ouyaYButton'),
            4: bs.gettexture('gameCircleIcon'),
        }
        self.ball_tex = self.ball_textures.get(int(settings.get('Ball Texture', 1)), 
                                              bs.gettexture('ouyaUButton'))
        self.ball_model = bs.getmesh('shield')
        self.ball_sound = bs.getsound('metalHit')
        
        # المواد
        self.ball_material = bs.Material()
        self.ball_material.add_actions(
            actions=(('modify_part_collision', 'friction', 1.1),
                    ('modify_part_collision', 'bounce', 0.7)))
        self.ball_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', True))
        self.ball_material.add_actions(
            conditions=(('we_are_younger_than', 100), 'and',
                        ('they_have_material', shared.object_material)),
            actions=('modify_node_collision', 'collide', True))
        self.ball_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('impact_sound', self.ball_sound, 0.2, 5))
        self.ball_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('call', 'at_connect', self.handle_ball_player_collide)))
        
        self.bomb_material = bs.Material()
        self.bomb_material.add_actions(
            actions=(('modify_part_collision', 'friction', 0.8),
                    ('modify_part_collision', 'bounce', 0.6)))
        
        self.score_region_material = bs.Material()
        self.score_region_material.add_actions(
            conditions=('they_have_material', self.ball_material),
            actions=(('modify_part_collision', 'collide', True),
                    ('call', 'at_connect', self.handle_score_gk_mode if self.gk_mode else self.handle_score)))
        
        self.wall_material = bs.Material()
        self.wall_material.add_actions(
            conditions=('they_have_material', self.ball_material),
            actions=(('modify_part_collision', 'collide', True),
                    ('call', 'at_connect', self.handle_ball_wall_collide)))
        
        self.item_material = bs.Material()
        self.item_material.add_actions(
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', True)))
        
        self.score_regions: Optional[List[bs.NodeActor]] = []
        self.ball_spawn_pos: Optional[Sequence[float]] = None
        self.ball: Optional[Ball] = None
        
        self.player_lights = []
        self.border_lights = []
        
        self.red_dot_y = 9 / 1000
        self.rainbow_animate = {0: (1, 0, 0), 0.5: (1, 1, 0), 1: (0, 1, 0), 
                               1.5: (0, 1, 1), 2: (0, 0, 1), 2.5: (1, 0, 1), 3: (1, 0, 0)}
        self.bsd = 3.5
        self.celebrater = 2
        self.delete_text = 1.5
        self.ctt = 0.03
        self.att = self.ctt
        self.glt = 0.1
        self.gtt = self.ctt
        self.sgt = 0.2
        self.gd = "Welcome To XERO Football Club"
        self.hdag = 'Score a Goal To Win'
        self.hd = f"ㅤ"
        self.gmgd = f"Save Your Goal « LEVEL : {self.gk_level} »" if self.gk_level else "Goal Keeper Mode"
        self.gmhd = f"Goal Keaper Mode « LEVEL : {self.gk_level} »" if self.gk_level else "GK Mode"
        self.gmbsd = 0.5
        self.activated = False
        self.left_right, self.up_down = 1, 1
        
        if self.gk_mode:
            self.tips = [bs.GameTip(
                'Shoot The Ball Towards Purple Lines So You Score.',
                icon=bs.gettexture('storeCharacter'),
                sound=bs.getsound('ding')
            )]
        else:
            self.scoreboard = Scoreboard()
        
        # متغيرات العداد الزمني المخصص (مستقل عن الإعدادات)
        self.timer_text: Optional[bs.Node] = None
        self.timer_running = False
        self.remaining_time = CUSTOM_TIMER_DURATION  # استخدام القيمة الثابتة

    # ==================== تحميل الإعدادات من JSON ====================
    def load_config(self):
        """تحميل ألوان الجدران والأرضية من ملف الإعدادات"""
        try:
            if not os.path.exists(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
            
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                
                if 'wall_up_color' in config:
                    self.wall_up_color = config['wall_up_color']
                if 'wall_down_color' in config:
                    self.wall_down_color = config['wall_down_color']
                if 'floor_color' in config:
                    self.floor_color = config['floor_color']
                
                print(f"✅ A-Soccer config loaded: UP={self.wall_up_color}, DOWN={self.wall_down_color}, FLOOR={self.floor_color}")
            else:
                # إنشاء ملف افتراضي
                self.save_default_config()
        except Exception as e:
            print(f"⚠️ Error loading A-Soccer config: {e}")

    def save_default_config(self):
        """حفظ الإعدادات الافتراضية في ملف JSON"""
        try:
            config = {
                'wall_up_color': self.wall_up_color,
                'wall_down_color': self.wall_down_color,
                'floor_color': self.floor_color
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            print("✅ A-Soccer default config saved.")
        except Exception as e:
            print(f"⚠️ Error saving default A-Soccer config: {e}")

    # ==================== نظام الإحصائيات والرتب – جديد ====================
    def _update_stats_goal(self, scorer_player: bs.Player, assister_player: bs.Player = None):
        """تحديث إحصائيات الهدف والتمريرة الحاسمة"""
        try:
            scorer_account = scorer_player.sessionplayer.get_v1_account_id()
            if scorer_account:
                _update_player_stats(scorer_account, goals=1)
            if assister_player:
                assister_account = assister_player.sessionplayer.get_v1_account_id()
                if assister_account:
                    _update_player_stats(assister_account, assists=1)
            _recalculate_all_ranks()
            self._update_all_rank_icons()
        except Exception as e:
            debug_print(f"Error updating goal stats: {e}")

    def _update_stats_game_end(self, winning_team: Team = None, losing_team: Team = None, draw: bool = False):
        """تحديث إحصائيات الفوز / الخسارة / التعادل"""
        try:
            if draw:
                for team in (self.teams[0], self.teams[1]):
                    for player in team.players:
                        acc = player.sessionplayer.get_v1_account_id()
                        if acc:
                            _update_player_stats(acc, draw=True)
            else:
                if winning_team:
                    for player in winning_team.players:
                        acc = player.sessionplayer.get_v1_account_id()
                        if acc:
                            _update_player_stats(acc, win=True)
                if losing_team:
                    for player in losing_team.players:
                        acc = player.sessionplayer.get_v1_account_id()
                        if acc:
                            _update_player_stats(acc, loss=True)
            _recalculate_all_ranks()
        except Exception as e:
            debug_print(f"Error updating end game stats: {e}")

    def _create_rank_icon(self, player: bs.Player, account_id: str):
        """إنشاء أيقونة الرتبة فوق رأس اللاعب (مرتفعة y=2.2)"""
        spaz = player.actor
        if not spaz or not spaz.node:
            return
        self._remove_rank_icon(spaz)
        data = _load_cheatmax_data()
        rank = data.get(account_id, {}).get('Stats', {}).get('rank', 0)
        icon, color = _get_rank_icon(rank)
        if not icon:
            return
        with self.context:
            math_node = bs.newnode('math',
                attrs={'input1': (0.0, 2.025, 0.0), 'operation': 'add'})
            spaz.node.connectattr('position_center', math_node, 'input2')
            icon_node = bs.newnode('text',
                attrs={
                    'text': icon,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'h_align': 'center',
                    'v_align': 'bottom',
                    'scale': 0.0095,
                    'color': color,
                    'opacity': 1.0
                })
            math_node.connectattr('output', icon_node, 'position')
            spaz.rank_icon = icon_node
            spaz.rank_icon_math = math_node

    def _remove_rank_icon(self, spaz):
        try:
            if hasattr(spaz, 'rank_icon') and spaz.rank_icon:
                if spaz.rank_icon.exists():
                    spaz.rank_icon.delete()
                spaz.rank_icon = None
            if hasattr(spaz, 'rank_icon_math') and spaz.rank_icon_math:
                if spaz.rank_icon_math.exists():
                    spaz.rank_icon_math.delete()
                spaz.rank_icon_math = None
        except:
            pass

    def _update_all_rank_icons(self):
        """تحديث أيقونات الرتب لجميع اللاعبين الأحياء"""
        for player in self.players:
            if player.is_alive() and player.actor:
                try:
                    acc = player.sessionplayer.get_v1_account_id()
                    if acc:
                        self._create_rank_icon(player, acc)
                except:
                    pass

    # ==================== باقي دوال اللعبة ====================
    def handle_ball_player_collide(self) -> None:
        """تصادم الكرة مع اللاعب"""
        collision = bs.getcollision()
        try:
            ball = collision.sourcenode.getdelegate(Ball, True)
            player = collision.opposingnode.getdelegate(PlayerSpaz, True).getplayer(Player, True)
            ball.all_players_touched[player.team.id] = player
        except:
            return

    def handle_ball_wall_collide(self) -> None:
        """تصادم الكرة مع الحائط (بما في ذلك الحائط المخفي)"""
        collision = bs.getcollision()
        try:
            if hasattr(self, 'roof_wall') and collision.sourcenode == self.roof_wall:
                ball = collision.opposingnode.getdelegate(Ball, True)
                if ball and ball.node:
                    current_velocity = ball.node.velocity
                    new_velocity = (
                        current_velocity[0] * 0.8,
                        -abs(current_velocity[1]) * 0.5,
                        current_velocity[2] * 0.8
                    )
                    ball.node.velocity = new_velocity
                    return
        except:
            pass
        if not self.gk_mode:
            return
        if hasattr(self, 'gk_saves_num_txt'):
            self.gk_saves_num_txt.node.text = str(int(self.gk_saves_num_txt.node.text) + 1)
        self.update_score_gk_mode()
        self.kill_ball()
        bs.timer(self.gmbsd, self.gk_setup)

    def handle_score(self) -> None:
        try:
            assert self.ball is not None
            assert self.score_regions is not None
            gnode = bs.getactivity().globalsnode
            region = bs.getcollision().sourcenode
            index = 0
            
            for i in range(len(self.score_regions)):
                if region == self.score_regions[i].node:
                    index = i
                    break
            
            scoring_team = None
            team_color = (1, 1, 1)  
            
            for team in self.teams:
                if team.id == index:
                    team.score += 1
                    scoring_team = team
                    team_color = team.color
                    
                    for player in scoring_team.players:
                        if player.actor:
                            player.actor.handlemessage(bs.CelebrateMessage(self.bsd))
            
            if scoring_team is not None:
                goal_time = bs.time()
                
                scorer = None
                assister = None
                
                if scoring_team.id in self.ball.all_players_touched:
                    scorer = self.ball.all_players_touched[scoring_team.id]
                    
                if hasattr(self.ball, 'hit_timestamps') and self.ball.hit_timestamps:
                    sorted_timestamps = sorted(self.ball.hit_timestamps, key=lambda x: x[1], reverse=True)
                    
                    for player, hit_time in sorted_timestamps:
                        if player is None or not hasattr(player, 'team') or player.team is None:
                            continue
                        
                        if player == scorer:
                            continue
                        
                        if player.team.id == scoring_team.id:
                            time_diff = goal_time - hit_time
                            
                            if time_diff <= 3.0:
                                assister = player
                                break
                
                if scorer is None:
                    for player in scoring_team.players:
                        if player is not None and player in self.ball.all_players_hitted:
                            scorer = player
                            try:
                                if hasattr(scorer, 'getname'):
                                    scorer_name = scorer.getname()
                            except Exception as e:
                                print(f"Error in fallback scorer: {e}")
                            break
                
                # ⭐ تحديث الإحصائيات – هدف + تمريرة حاسمة
                if scorer is not None:
                    self._update_stats_goal(scorer, assister)
                
                try:
                    pos = bs.getcollision().position
                    explosion = bs.newnode('explosion', attrs={
                        'position': pos,
                        'color': team_color,
                        'radius': 4
                    })
                except:
                    pass
                
                try:
                    bs.animate_array(gnode, 'tint', 3, {0: gnode.tint, 0.07: (0, 0, 0), 0.3: gnode.tint})
                    bs.cameraflash(duration=1 if int(self.bsd) < 1 else int(self.bsd))
                    self.foghorn_sound.play()
                    self.cheer_sound.play()
                except:
                    pass
                
                self.kill_ball()
                
                self._update_scoreboard()
                
                if scoring_team.score >= self.score_to_win:
                    self.end_game()
            
            if scorer is not None and hasattr(scorer, 'getname'):
                try:
                    icon_info = scorer.get_icon()
                    
                    border_node = bs.newnode('image',
                                            attrs={
                                                'texture': bs.gettexture('circle'),
                                                'color': team_color,
                                                'position': (-160, 140),
                                                'scale': (140, 140),
                                                'opacity': 0.8,
                                                'attach': 'center',
                                                'has_alpha_channel': True
                                            })
                    
                    char_node = bs.newnode('image',
                                            attrs={
                                                'texture': icon_info['texture'],
                                                'tint_texture': icon_info['tint_texture'],
                                                'tint_color': icon_info['tint_color'],
                                                'tint2_color': icon_info['tint2_color'],
                                                'position': (-160, 140),
                                                'scale': (120, 120),
                                                'opacity': 1.0,
                                                'attach': 'center',
                                                'mask_texture': bs.gettexture('characterIconMask'),
                                                'vr_depth': -10
                                            })

                    name_node = bs.newnode('text',
                                        attrs={
                                            'text': scorer.getname(),
                                            'scale': 1.4,
                                            'color': team_color,
                                            'h_align': 'left',
                                            'v_align': 'center',
                                            'shadow': 0.8,
                                            'flatness': 1.0,
                                            'position': (-80, 80),
                                            'h_attach': 'center',
                                            'v_attach': 'center',
                                            'maxwidth': 200,
                                            'big': True
                                        })

                    scores_node = bs.newnode('text',
                                            attrs={
                                                'text': 'SCORES!',
                                                'scale': 1.4,
                                                'color': (1.0, 0.9, 0.0),
                                                'h_align': 'left',
                                                'v_align': 'center',
                                                'shadow': 1.0,
                                                'flatness': 1.0,
                                                'position': (-80, 10),
                                                'h_attach': 'center',
                                                'v_attach': 'center',
                                                'big': True,
                                                'maxwidth': 250
                                            })

                    display_time = 2.5
                    
                    bs.animate_array(border_node, 'scale', 2, {
                        0.0: (0, 0), 
                        0.2: (150, 150),
                        0.3: (140, 140)
                    })
                    bs.animate(border_node, 'opacity', {
                        0.0: 0, 
                        0.1: 0.6,
                        0.2: 0.8,
                        display_time - 0.2: 0.8, 
                        display_time: 0
                    })
                    
                    bs.animate_array(char_node, 'scale', 2, {
                        0.1: (0, 0),
                        0.3: (130, 130),
                        0.4: (120, 120)
                    })
                    bs.animate(char_node, 'opacity', {
                        0.0: 0, 
                        0.2: 0.8, 
                        0.3: 1,
                        display_time - 0.2: 1, 
                        display_time: 0
                    })
                    
                    bs.animate(char_node, 'rotate', {
                        0.3: 0,
                        0.6: 5,
                        0.9: -5,
                        1.2: 0
                    })
                    
                    bs.animate(name_node, 'scale', {
                        0.0: 0, 
                        0.15: 0.8,
                        0.25: 0.65
                    })
                    bs.animate(name_node, 'opacity', {
                        0.0: 0, 
                        0.1: 0.8,
                        0.2: 1, 
                        display_time - 0.2: 1, 
                        display_time: 0
                    })
                    
                    bs.animate_array(name_node, 'color', 3, {
                        0.0: team_color,
                        0.5: (1, 1, 1),
                        1.0: team_color,
                        1.5: (1, 1, 1),
                        2.0: team_color
                    })
                    
                    bs.animate(scores_node, 'scale', {
                        0.0: 0, 
                        0.1: 1,
                        0.15: 0.8,
                        0.3: 0.7,
                        0.35: 0.6
                    })
                    bs.animate(scores_node, 'opacity', {
                        0.0: 0, 
                        0.1: 1, 
                        display_time - 0.3: 1, 
                        display_time: 0
                    })
                    
                    bs.animate_array(scores_node, 'color', 3, {
                        0.0: (1.0, 0.9, 0.0),
                        0.2: (1.0, 1.0, 1.0),
                        0.4: (1.0, 0.9, 0.0),
                        0.6: (1.0, 1.0, 1.0),
                        0.8: (1.0, 0.9, 0.0),
                        1.0: (1.0, 1.0, 1.0),
                        1.2: (1.0, 0.9, 0.0),
                        1.4: (1.0, 1.0, 1.0),
                        1.6: (1.0, 0.9, 0.0),
                        1.8: (1.0, 1.0, 1.0),
                        2.0: (1.0, 0.9, 0.0)
                    })

                    bs.timer(display_time + 0.1, border_node.delete)
                    bs.timer(display_time + 0.1, char_node.delete)
                    bs.timer(display_time + 0.1, name_node.delete)
                    bs.timer(display_time + 0.1, scores_node.delete)
                    
                    self.ding_sound.play()  
                    
                except Exception as e:
                    print(f"Error showing scorer UI: {e}")

            if assister is not None and hasattr(assister, 'getname'):
                def show_assister_info():
                    try:
                        icon_info = assister.get_icon()
                        
                        border_node = bs.newnode('image',
                                                attrs={
                                                    'texture': bs.gettexture('circle'),
                                                    'color': (0.7, 0.7, 1.0),
                                                    'position': (145, 35),
                                                    'scale': (40, 40),
                                                    'opacity': 0.8,
                                                    'attach': 'center',
                                                    'has_alpha_channel': True
                                                })
                        
                        char_node = bs.newnode('image',
                                                attrs={
                                                    'texture': icon_info['texture'],
                                                    'tint_texture': icon_info['tint_texture'],
                                                    'tint_color': icon_info['tint_color'],
                                                    'tint2_color': icon_info['tint2_color'],
                                                    'position': (145, 35),
                                                    'scale': (40, 40),
                                                    'opacity': 1.0,
                                                    'attach': 'center',
                                                    'mask_texture': bs.gettexture('characterIconMask'),
                                                    'vr_depth': -10
                                                })

                        name_node = bs.newnode('text',
                                            attrs={
                                                'text': assister.getname(),
                                                'scale': 0.3,
                                                'color': (0.7, 0.7, 1.0),
                                                'h_align': 'right',
                                                'v_align': 'center',
                                                'shadow': 0.8,
                                                'flatness': 1.0,
                                                'position': (80, -50),
                                                'h_attach': 'center',
                                                'v_attach': 'center',
                                                'maxwidth': 200,
                                                'big': True
                                            })

                        assist_node = bs.newnode('text',
                                                attrs={
                                                    'text': 'ASSIST',
                                                    'scale': 0.6,
                                                    'color': (0.5, 1.0, 0.5),
                                                    'h_align': 'right',
                                                    'v_align': 'center',
                                                    'shadow': 1.0,
                                                    'flatness': 1.0,
                                                    'position': (80, -95),
                                                    'h_attach': 'center',
                                                    'v_attach': 'center',
                                                    'big': True,
                                                    'maxwidth': 250
                                                })

                        display_time = 2.0
                        
                        bs.animate_array(border_node, 'scale', 2, {
                            0.0: (0, 0), 
                            0.15: (140, 140),
                            0.25: (80,80)
                        })
                        bs.animate(border_node, 'opacity', {
                            0.0: 0, 
                            0.1: 0.6,
                            0.15: 0.8,
                            display_time - 0.15: 0.8, 
                            display_time: 0
                        })
                        
                        bs.animate_array(char_node, 'scale', 2, {
                            0.1: (0, 0), 
                            0.25: (120, 120),
                            0.3: (70, 70)
                        })
                        bs.animate(char_node, 'opacity', {
                            0.0: 0, 
                            0.15: 0.9,
                            0.2: 1, 
                            display_time - 0.15: 1, 
                            display_time: 0
                        })
                        
                        bs.animate(name_node, 'scale', {
                            0.0: 0, 
                            0.1: 0.6,
                            0.15: 0.35
                        })
                        bs.animate(name_node, 'opacity', {
                            0.0: 0, 
                            0.1: 1, 
                            display_time - 0.15: 1, 
                            display_time: 0
                        })
                        
                        bs.animate_array(name_node, 'color', 3, {
                            0.0: (0.7, 0.7, 1.0),
                            0.5: (1.0, 1.0, 1.0),
                            1.0: (0.7, 0.7, 1.0),
                            1.5: (1.0, 1.0, 1.0)
                        })
                        
                        bs.animate(assist_node, 'scale', {
                            0.0: 0, 
                            0.08: 1,
                            0.12: 0.4
                        })
                        bs.animate(assist_node, 'opacity', {
                            0.0: 0, 
                            0.08: 1, 
                            display_time - 0.15: 1, 
                            display_time: 0
                        })
                        
                        bs.animate_array(assist_node, 'color', 3, {
                            0.0: (0.5, 1.0, 0.5),
                            0.2: (1.0, 1.0, 1.0),
                            0.4: (0.5, 1.0, 0.5),
                            0.6: (1.0, 1.0, 1.0),
                            0.8: (0.5, 1.0, 0.5),
                            1.0: (1.0, 1.0, 1.0),
                            1.2: (0.5, 1.0, 0.5)
                        })

                        bs.timer(display_time + 0.1, border_node.delete)
                        bs.timer(display_time + 0.1, char_node.delete)
                        bs.timer(display_time + 0.1, name_node.delete)
                        bs.timer(display_time + 0.1, assist_node.delete)
                        
                        self.ding_sound.play()  
                        
                    except Exception as e:
                        print(f"Error showing assister UI: {e}")
                
                bs.timer(0.5, show_assister_info)
        except Exception as e:
            print(f"Error in handle_score: {e}")
            import traceback
            traceback.print_exc()
            
            if hasattr(self, 'kill_ball'):
                self.kill_ball()

    def update_score_gk_mode(self) -> None:
        """تحديث النقاط في وضع حارس المرمى"""
        try:
            if hasattr(self, 'gk_goals_num_txt') and hasattr(self, 'gk_saves_num_txt'):
                goals = int(self.gk_goals_num_txt.node.text)
                saves = int(self.gk_saves_num_txt.node.text)
                total = goals + saves
                
                if total > 0:
                    percentage = (saves / total) * 100
                    new_txt = f"{percentage:.1f}%"
                    self.gk_total_num_txt.node.text = new_txt
                    red_val = 1.0 - (percentage / 100)
                    green_val = percentage / 100
                    self.gk_total_num_txt.node.color = (red_val, green_val, 0.2)
                else:
                    self.gk_total_num_txt.node.text = "0.0%"
                    self.gk_total_num_txt.node.color = (1, 0, 0.2)
        except Exception as e:
            print(f"Error in update_score_gk_mode: {e}")

    def on_begin(self) -> None:
        super().on_begin()
        shared = SharedObjects.get()
        self.title_text = Text('Enova Soccer', 0.04, (-3.06, 0.66, -8.5), (0.6,0.8,1,0.6), 1.0, in_world=True,)
        self.title_text = Text('Enova Soccer', 0.04, (-3, 0.7, -8.5), (1,1,1,0.6), 1.0, in_world=True)
        bs.newnode('text',
                                            attrs={
                                                'text': 'Enova',
                                                'scale': 0.6,
                                                'color': (0.6, 0.8, 1),
                                                'h_align': 'right',
                                                'v_align': 'center',
                                                'shadow': 0.8,
                                                'flatness': 1.0,
                                                'position': (-482, 228),
                                                'maxwidth': 200,
                                                'big': True
                                            })
        bs.newnode('text',
                                            attrs={
                                                'text': 'Enova',
                                                'scale': 0.6,
                                                'color': (1, 1, 1),
                                                'h_align': 'right',
                                                'v_align': 'center',
                                                'shadow': 0.8,
                                                'flatness': 1.0,
                                                'position': (-480, 230),
                                                'maxwidth': 200,
                                                'big': True
                                            })
        try:
            if hasattr(self.map, 'is_hockey'):
                self.map.is_hockey = False
            self._apply_textures_from_settings()
            bs.timer(0.3, self._fix_floor_friction)
        except Exception as e:
            pass
        
        def remove_excess_lights():
            try:
                lights_removed = 0
                for node in bs.getnodes():
                    try:
                        if hasattr(node, 'getNodeType'):
                            node_type = node.getNodeType()
                            if node_type == 'light':
                                node.delete()
                                lights_removed += 1
                    except:
                        continue
            except Exception as e:
                pass
        bs.timer(0.5, remove_excess_lights)
        
        self.team1 = self.teams[0]
        self.team2 = self.teams[1]
        
        goal1 = Wall(self.map.defs.boxes['goal1'][0:3], self.map.defs.boxes['goal1'][6:9])
        goal2 = Wall(self.map.defs.boxes['goal2'][0:3], self.map.defs.boxes['goal2'][6:9])
        goal1.node.materials = [self.score_region_material]
        goal2.node.materials = [self.score_region_material]
        self.score_regions.append(bs.NodeActor(goal1.node))
        self.score_regions.append(bs.NodeActor(goal2.node))
        
        self.chant_sound.play()
        
        self.apply_weather()
        
        self.map_highlights()
        
        # إعداد العداد الزمني المخصص (يعمل دائماً)
        self._setup_custom_timer()
        
        self.ball_spawn_pos = self.map.get_flag_position(None)
        
        if self.gk_mode:
            self.gk_setup()
        else:
            self._update_scoreboard()
            self.spawn_ball()
            self.start_border_lights_animation()

    def _setup_custom_timer(self):
        """إنشاء عداد زمني مخصص في أعلى منتصف الشاشة"""
        # إنشاء نص العداد
        self.timer_text = bs.newnode('text',
            attrs={
                'text': self._format_time(self.remaining_time),
                'scale': 0.7,
                'color': (1, 1, 1),
                'h_align': 'center',
                'v_align': 'center',
                'position': (0, -250),  # أعلى المنتصف بقليل
                'shadow': 1.0,
                'flatness': 1.0,
                'big': True,
                'v_attach': 'top'
            })
        
        # بدء العد التنازلي
        self.timer_running = True
        self._update_timer()

    def _format_time(self, seconds: int) -> str:
        """تحويل الثواني إلى صيغة MM:SS"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def _update_timer(self):
        """تحديث العداد كل ثانية"""
        if not self.timer_running or self.has_ended():
            return
        
        if self.remaining_time <= 0:
            # انتهاء الوقت - إنهاء اللعبة
            self.timer_text.text = "00:00"
            self.end_game()
            return
        
        # تحديث النص
        time_str = self._format_time(self.remaining_time)
        self.timer_text.text = time_str
        
        # تأثيرات عند اقتراب النهاية (آخر 10 ثوانٍ)
        if self.remaining_time <= 10:
            # لون أحمر وميض
            if self.remaining_time % 2 == 0:
                self.timer_text.color = (1, 0, 0)
            else:
                self.timer_text.color = (1, 1, 1)
            
            # تكبير النص قليلاً مع كل ثانية
            bs.animate(self.timer_text, 'scale', {
                0: 0.7,
                0.1: 0.9,
                0.2: 0.7
            })
        else:
            # لون عادي مع نبض خفيف كل ثانية
            bs.animate(self.timer_text, 'scale', {
                0: 0.7,
                0.05: 1.0,
                0.1: 0.7
            })
        
        # تقليل الوقت
        self.remaining_time -= 1
        
        # جدولة التحديث التالي بعد ثانية
        bs.timer(1.0, self._update_timer)

    def show_points_animation(self, player, points, color):
        """عرض أنيميشن للنقاط مع خلفية جميلة"""
        try:
            if not player or not player.actor or not player.actor.node:
                return
            
            pos = player.actor.node.position
            
            points_node = bs.newnode('text',
                attrs={
                    'text': f"+{points}",
                    'scale': 0.025,
                    'color': color,
                    'position': (pos[0], pos[1] + 1.8, pos[2]),
                    'h_align': 'center',
                    'v_align': 'center',
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0
                })
            
            def animate_all():
                current_time = bs.time()
                bs.animate_array(points_node, 'position', 3, {
                    0: (pos[0], pos[1] + 1.8, pos[2]),
                    0.5: (pos[0], pos[1] + 2.3, pos[2]),
                    1.0: (pos[0], pos[1] + 3.0, pos[2])
                })
            
            animate_all()
            
            bs.animate(points_node, 'opacity', {
                0: 1.0,
                0.7: 0.8,
                1.0: 0.0
            })
            
            bs.animate(points_node, 'scale', {
                0: 0.025,
                0.2: 0.03,
                0.5: 0.025
            })
            
            def cleanup():
                try:
                    if points_node.exists():
                        points_node.delete()
                except:
                    pass
            
            bs.timer(1.1, cleanup)
            
        except Exception as e:
            pass

    def on_player_join(self, player: Player) -> None:
        """عند دخول لاعب جديد"""
        try:
            super().on_player_join(player)
        except Exception as e:
            print(f"Warning: Error in on_player_join: {e}")
            print(f"Player {player.getname()} joined - continuing despite error")
            
            if player not in self.players:
                self.players.append(player)
            
            try:
                self.spawn_player(player)
            except Exception as spawn_error:
                print(f"Error spawning player: {spawn_error}")

    def on_player_leave(self, player: Player) -> None:
        """عند خروج لاعب من السيرفر"""
        if player.actor:
            self._remove_rank_icon(player.actor)
        super().on_player_leave(player)
        
        try:
            if hasattr(player, 'team_light') and player.team_light:
                if player.team_light.exists():
                    player.team_light.delete()
                
                if player.team_light in self.player_lights:
                    self.player_lights.remove(player.team_light)
                
                player.team_light = None
                
        except Exception as e:
            pass

    def cleanup_team_references(self):
        """تنظيف جميع المراجع للفرق"""
        try:
            if hasattr(self, 'team1'):
                self.team1 = None
            if hasattr(self, 'team2'):
                self.team2 = None
                
        except Exception as e:
            pass

    def end_game(self) -> None:
        """إنهاء المباراة – تحديث إحصائيات الفوز/الخسارة/التعادل"""
        # إيقاف العداد
        self.timer_running = False
        
        # ⭐ تحديد الفائز والخاسر أو التعادل
        winner = None
        loser = None
        draw = False
        if self.teams[0].score > self.teams[1].score:
            winner = self.teams[0]
            loser = self.teams[1]
        elif self.teams[1].score > self.teams[0].score:
            winner = self.teams[1]
            loser = self.teams[0]
        else:
            draw = True

        # تحديث الإحصائيات
        self._update_stats_game_end(winner, loser, draw)
        # تحديث أيقونات الرتب بعد انتهاء اللعبة
        bs.timer(0.5, self._update_all_rank_icons)

        self.wall_timer_running = False
        
        if hasattr(self, 'roof_wall') and self.roof_wall:
            try:
                if self.roof_wall.exists():
                    self.roof_wall.delete()
            except:
                pass
        
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        
        bs.timer(1.5, lambda: self.end(results=results))

    def apply_weather(self):
        """تطبيق تأثيرات الطقس - النهاري فقط بدون ثلج"""
        try:
            gnode = bs.getactivity().globalsnode
            
            gnode.tint = (0.85, 0.85, 1.0)
            gnode.ambient_color = (0.9, 0.9, 0.9)
            gnode.vignette_outer = (0.9, 0.9, 0.9)
            gnode.vignette_inner = (1.0, 1.0, 1.0)
                
        except Exception as e:
            pass

    def create_border_lights(self):
        """إنشاء الأضواء على حواف الملعب وحواف المرمى"""
        pass
        
    def start_border_lights_animation(self):
        """بدء أنيميشن تغيير ألوان الأضواء"""
        self.create_border_lights()

    def cycle_border_lights_colors(self):
        """تثبيت الأضواء على اللون السماوي (لا أنيميشن)"""
        try:
            if not hasattr(self, 'border_lights') or not self.border_lights:
                return
            
            for light in self.border_lights:
                light.color = (0, 1, 1)
                
        except Exception as e:
            pass

    # ==================== تطبيق الأنسجة مع الألوان المحملة ====================
    def _apply_textures_from_settings(self):
        """تطبيق الـTextures حسب الإعدادات مع استخدام الألوان المحفوظة"""
        try:
            self._apply_wall_down_texture()
            self._apply_wall_up_texture()
            self._apply_ground_texture()
            self._apply_goals_texture()
        except Exception as e:
            pass

    def _apply_ground_texture(self):
        """تطبيق تيكستشر الأرضية - أرضية خضراء مع انعكاس عالي"""
        try:
            texture = bs.gettexture('reflectionSoft_+z')
            color = self.floor_color
            
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'mesh'):
                        mesh_str = str(node.mesh)
                        if "hockeyStadiumInner" in mesh_str or "Inner" in mesh_str:
                            if hasattr(node, 'color_texture'):
                                node.color_texture = texture
                                node.color = color
                                
                                shared = SharedObjects.get()
                                gnode = bs.getactivity().globalsnode
                                self.use_fixed_vr_overlay = False
                                self.node.materials = [shared.footing_material]
                                gnode.floor_reflection = True
                                gnode.floor_reflection = 100
                            
                            return
                except:
                    continue
        except Exception as e:
            pass

    def _apply_wall_down_texture(self):
        """تطبيق تيكستشر الحيطان السفلية"""
        try:
            wall_textures = {
                0: (bs.gettexture('doomShroomBGColor'), self.wall_down_color),
            }
            
            texture_key = self.wall_down_texture_setting
            texture, color = wall_textures.get(texture_key, (bs.gettexture('bg'), self.wall_down_color))
            
            walls_found = 0
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'mesh'):
                        mesh_name = str(node.mesh)
                        if "hockeyStadiumOuter" in mesh_name:
                            if hasattr(node, 'color_texture'):
                                node.color_texture = texture
                            node.color = color
                            if texture_key == 0:
                                node.additive = True
                                node.opacity = 0.8
                            walls_found += 1
                            shared = SharedObjects.get()
                            gnode = bs.getactivity().globalsnode
                            self.use_fixed_vr_overlay = False
                except:
                    continue
        except Exception as e:
            pass
            
    def _apply_wall_up_texture(self):
        """تطبيق تيكستشر الحيطان العلوية"""
        try:
            wall_textures = {
                0: (bs.gettexture('doomShroomBGColor'), self.wall_up_color),
            }
            
            texture_key = self.wall_up_texture_setting
            texture, color = wall_textures.get(texture_key, (bs.gettexture('bg'), self.wall_up_color))
            
            walls_found = 0
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'mesh'):
                        mesh_name = str(node.mesh)
                        if 'stand' in mesh_name.lower() or 'Stands' in mesh_name:
                            if hasattr(node, 'color_texture'):
                                node.color_texture = texture
                            node.color = color
                            if texture_key == 0:
                                node.additive = True
                                node.opacity = 0.8
                            walls_found += 1
                except:
                    continue
        except Exception as e:
            pass
            
    def _apply_goals_texture(self):
        """تطبيق تيكستشر المرمى"""
        try:
            goal_textures = {
                0: (bs.gettexture('doomShroomBGColor'), (0.8, 0.8, 8)),
            }
            
            texture_key = self.goals_texture_setting
            texture, color = goal_textures.get(texture_key, (None, (1, 1, 1)))
            
            goals_found = 0
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'position'):
                        pos = node.position
                        if pos and len(pos) >= 3:
                            x, y, z = pos[0], pos[1], pos[2]
                            if abs(z) > 8:
                                if abs(x) < 3:
                                    if y < 5:
                                        if texture_key == 0:
                                            node.color = (1, 1, 1, 0.8)
                                            node.additive = True
                                            node.opacity = 0.8
                                        else:
                                            if texture and hasattr(node, 'color_texture'):
                                                node.color_texture = texture
                                            node.color = color
                                        goals_found += 1
                except:
                    continue
        except Exception as e:
            pass
            
    def _fix_floor_friction(self):
        """إصلاح احتكاك الأرضية"""
        try:
            for node in bs.getnodes():
                try:
                    if hasattr(node, 'mesh'):
                        mesh_str = str(node.mesh)
                        if "hockeyStadiumInner" in mesh_str:
                            if hasattr(node, 'friction'):
                                node.friction = 1.0
                            if hasattr(node, 'rolling_friction'):
                                node.rolling_friction = 1.0
                            return
                except:
                    continue
        except Exception as e:
            pass
            
    def on_transition_in(self) -> None:
        """عند الانتقال"""
        super().on_transition_in()
        try:
            activity = bs.getactivity()
            gnode = bs.getactivity().globalsnode
            if hasattr(activity.map, 'is_hockey'):
                activity.map.is_hockey = False
            if self.night_mode:
                gnode.tint = (0.82, 0.82, 0.82)
            if self.icy_ground:
                bs.timer(0.5, lambda: self._add_ice_layer())
        except Exception as e:
            pass
            
    def _add_ice_layer(self):
        """إضافة طبقة جليد"""
        try:
            ice_material = bs.Material()
            ice_material.add_actions(
                actions=(('modify_part_collision', 'friction', 0.1))
            )
            self.ice_layer = bs.newnode('locator',
                attrs={
                    'mesh': bs.getmesh('shield'),
                    'color': (0.8, 0.9, 1.0),
                    'position': (0, 0.02, 0),
                    'mesh_scale': 30.0,
                    'body': 'sphere',
                    'body_scale': 30.0,
                    'opacity': 0.2,
                    'materials': [ice_material],
                    'density': 0.0,
                    'gravity_scale': 0.0,
                }
            )
        except Exception as e:
            pass

    def spawn_player(self, player: Player) -> bs.Actor:
        """إضافة لاعب – مع إنشاء أيقونة الرتبة"""
        try:
            if hasattr(player, 'team_light') and player.team_light:
                try:
                    if player.team_light.exists():
                        player.team_light.delete()
                    if player.team_light in self.player_lights:
                        self.player_lights.remove(player.team_light)
                except:
                    pass
                player.team_light = None
            
            if self.invincible_mode:
                playerspaz.PlayerSpaz = NewPlayerSpaz
            else:
                playerspaz.PlayerSpaz = NormalPlayerSpaz
            
            spaz = self.spawn_player_spaz(player)
            
            if self.enable_pickup:
                spaz.connect_controls_to_player(enable_pickup=True)
            else:
                spaz.connect_controls_to_player(enable_pickup=False)
            
            self.add_player_light(player)
            
            # ⭐ تأكد من وجود إحصائيات اللاعب وأنشئ أيقونة الرتبة
            try:
                acc = player.sessionplayer.get_v1_account_id()
                if acc:
                    _ensure_player_stats(acc)
                    bs.timer(0.3, lambda: self._create_rank_icon(player, acc))
            except:
                pass
            
            return spaz
        except Exception as e:
            return self.spawn_player_spaz(player)
    
    def cleanup_player_lights(self):
        """تنظيف جميع أضواء اللاعبين"""
        try:
            for light in self.player_lights:
                try:
                    if light.exists():
                        light.delete()
                except:
                    pass
            self.player_lights.clear()
        except:
            pass
    
    def add_player_light(self, player: Player) -> None:
        """إضافة ضوء للاعب بلون فريقه"""
        try:
            team_color = player.team.color
            
            light = bs.newnode('light', attrs={
                'color': team_color,
                'intensity': 0.1,
                'radius': 0.1,
                'height_attenuated': False
            })
            
            player.actor.node.connectattr('position', light, 'position')
            player.team_light = light
            self.player_lights.append(light)
            
            bs.animate(light, 'intensity', {
                0: 0.1,
                1.0: 0.3,
                2.0: 0.1
            }, loop=True)
            
        except Exception as e:
            pass

    def map_highlights(self) -> None:
        """إضافة النصوص والأضواء على الخريطة"""
        self.create_pitch_lines()
        
        if self.gk_mode:
            gk_saves_txt = Text('Saves', 0.03, (0.35, 2, -6), (0, 1, 0), 1.5)
            gk_goals_txt = Text('Goals', 0.03, (-2.2, 2, -6), (1, 0, 0), 1.5)
            gk_total_txt = Text('Total', 0.03, (3.9, 2, -6), (0.3, 1, 1), 1.5)
            self.gk_saves_num_txt = Text('0', 0.03, (1.1, 1, -6), (0, 1, 0), 1.5)
            self.gk_goals_num_txt = Text('0', 0.03, (-1.5, 1, -6), (1, 0, 0), 1.5)
            self.gk_total_num_txt = Text('0.0%', 0.03, (4, 1, -6), (1, 0, 0.1), 1.5)
            front_wall = Wall((0, 5, -3), (50, 36, 0.5))
            near_wall = Wall((0, 5, 3), (50, 36, 0.5))
            mid_map_wall = Wall((-1, 5, 0), (0.5, 36, 20))
            dots_color = (1, 0, 1)
            y, z, x_start, x_end = 0.009, 2.45, -0.45, 8
            diameter = 0.1
            dots_len1 = int((-x_start + x_end) / diameter)
            dots_len2 = int(z / diameter)
            for i in range(0, dots_len1 + 1):
                Dot((x_start + i / (1 / diameter), y, -z), [diameter], dots_color)
                Dot((x_start + i / (1 / diameter), y, z), [diameter], dots_color)
            for i in range(0, dots_len2 + 1):
                Dot((x_start, y, z - i / (1 / diameter)), [diameter], dots_color)
                Dot((x_start, y, -z + i / (1 / diameter)), [diameter], dots_color)
        

    def create_pitch_lines(self):
        """إنشاء خطوط ملعب باستخدام الكود المطلوب"""
        try:
            color = (1, 1, 1)
            opacity = 1                                    
            pos1 = [(0.00000001, 0.02, 0.00000001)]
            
            for m_pos in pos1:
                bs.newnode('locator', 
                    attrs={
                        'shape': 'circleOutline',
                        'position': m_pos, 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': [2.8]
                    })  
                
                bs.newnode('locator',
                    attrs={
                        'shape': 'box',
                        'position': (-7.3, 0.00, 0.0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': (1.7, 0.01, 3.7)
                    })       
                bs.newnode('locator',
                    attrs={
                        'shape': 'box',
                        'position': (-6.65, 0.00, 0.0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': (3, 0.01, 6)
                    }) 
                bs.newnode('locator',
                    attrs={
                        'shape': 'box',
                        'position': (7.3, 0.00, 0.0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': (1.7, 0.01, 3.7)
                    })        
                bs.newnode('locator',
                    attrs={
                        'shape': 'box',
                        'position': (6.65, 0.00, 0.0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': (3, 0.01, 6)
                    }) 


            pos2 = [(0.000001, 0.02, 0.0000001)]
            
            for m_pos1 in pos2:  
                bs.newnode('locator',
                    attrs={
                        'shape': 'circle',
                        'position': m_pos1, 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': [0.3]
                    })
                
                bs.newnode('locator',
                    attrs={
                        'shape': 'circle',
                        'position': (5.8, 0.02, 0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': [0.2]
                    })
                
                bs.newnode('locator',
                    attrs={
                        'shape': 'circle',
                        'position': (-5.8, 0.02, 0), 
                        'color': color, 
                        'opacity': opacity, 
                        'drawShadow': False,  
                        'draw_beauty': True, 
                        'additive': False, 
                        'size': [0.2]
                    })
            
            bs.newnode('locator',
                attrs={
                    'shape': 'circle',
                    'position': (0, 0.02, 0.0), 
                    'color': color, 
                    'opacity': opacity, 
                    'drawShadow': False,  
                    'draw_beauty': True, 
                    'additive': False, 
                    'size': (0.09, 10, 1000.5)
                })
            
            bs.newnode('locator',
                attrs={
                    'shape': 'circle',
                    'position': (-8.1, 0.02, 0.0), 
                    'color': color, 
                    'opacity': opacity, 
                    'drawShadow': False,  
                    'draw_beauty': True, 
                    'additive': False, 
                    'size': (0.09, 10, 1000.5)
                })
            
            bs.newnode('locator',
                attrs={
                    'shape': 'circle',
                    'position': (8.1, 0.02, 0.0), 
                    'color': color, 
                    'opacity': opacity, 
                    'drawShadow': False,  
                    'draw_beauty': True, 
                    'additive': False, 
                    'size': (0.09, 10, 1000.5)
                })
            
            return {'status': 'success'}
            
        except Exception as e:
            return None

    def create_bomb_explosion(self, position: Sequence[float], team_color: Sequence[float]):
        """إنشاء انفجار قنبلة عند تسجيل أي هدف"""
        try:
            explosion = bs.newnode('explosion', attrs={
                'position': position,
                'color': team_color,
                'radius': 4.0
            })
            
            for i in range(6):
                angle = (i * 60) * 3.14159 / 180
                distance = random.uniform(0.8, 2.0)
                offset_pos = (
                    position[0] + math.cos(angle) * distance,
                    position[1] + random.uniform(0.3, 1.2),
                    position[2] + math.sin(angle) * distance
                )
                
                bs.newnode('explosion', attrs={
                    'position': offset_pos,
                    'color': team_color,
                    'radius': 1.8
                })
            
            bs.emitfx(
                position=position,
                velocity=(0, 3, 0),
                count=35,
                scale=2.0,
                spread=1.2,
                chunk_type='spark'
            )
            
            light = bs.newnode('light', attrs={
                'position': (position[0], position[1] + 1.5, position[2]),
                'color': team_color,
                'radius': 5.0,
                'intensity': 2.0,
                'height_attenuated': False
            })
            
            bs.animate(light, 'intensity', {
                0: 2.5,
                0.1: 3.0,
                0.3: 2.0,
                0.8: 1.0,
                1.5: 0.3,
                2.0: 0.0
            })
            
            bs.timer(2.1, light.delete)
            
            try:
                gnode = bs.getactivity().globalsnode
                original_pos = gnode.camera_position
                
                for i in range(4):
                    shake_offset = (
                        random.uniform(-0.2, 0.2),
                        random.uniform(-0.1, 0.1),
                        random.uniform(-0.2, 0.2)
                    )
                    shake_pos = (
                        original_pos[0] + shake_offset[0],
                        original_pos[1] + shake_offset[1],
                        original_pos[2] + shake_offset[2]
                    )
                    gnode.camera_position = shake_pos
                    bs.timer(i * 0.15, lambda p=original_pos: setattr(gnode, 'camera_position', p))
            except:
                pass
            
        except Exception as e:
            pass

    def follow_ball(self) -> None:
        """متابعة الكرة"""
        if self.ball is None:
            return
        pos = self.ball.node.position
        if hasattr(self, 'red_dot'):
            self.red_dot.node.position = (pos[0], self.red_dot_y, pos[2])
        if self.ball.node.gravity_scale == 0:
            if str(pos[0])[:5] != str(self.ball.spawn_pos[0])[:5]:
                self.ball.node.gravity_scale = self.ball.gravity
        bs.timer(0, self.follow_ball)

    def _update_scoreboard(self) -> None:
        """تحديث لوحة النتائج"""
        try:
            win_score = self.score_to_win
            for team in self.teams:
                self.scoreboard.set_team_value(team, team.score, win_score)
        except:
            pass

    def create_red_dot(self) -> None:
        """إنشاء النقطة الحمراء"""
        self.red_dot = Dot((0, self.red_dot_y, 0), [0.2])

    def kill_ball(self) -> None:
        """إزالة الكرة"""
        if hasattr(self, 'red_dot'):
            self.red_dot.node.delete()
        self.ball = None

    def spawn_ball(self) -> None:
        """إنشاء الكرة"""
        if self.gk_mode:
            try:
                if not hasattr(self, 'red_dot') or not self.red_dot.node:
                    self.create_red_dot()
            except:
                self.create_red_dot()
            self.ball = Ball(position=(0, 0, 0), is_area_of_interest=False)
            self.follow_ball()
            return
        
        self.swipsound.play()
        self.whistle_sound.play()
        assert self.ball_spawn_pos is not None
        self.ball = Ball(position=self.ball_spawn_pos, is_area_of_interest=True)
        self.create_red_dot()
        self.follow_ball()

    def handlemessage(self, msg: Any) -> Any:
        """معالجة الرسائل"""
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
            self.respawn_player(msg.getplayer(Player))
        elif isinstance(msg, BallDiedMessage):
            if self.gk_mode:
                return
            if not self.has_ended():
                bs.timer(self.bsd, self.spawn_ball)
        else:
            super().handlemessage(msg)

    def assistant_setup(self) -> None:
        """إعداد المساعد"""
        if self.gk_mode:
            return
        ball = self.ball
        if not ball:
            return
        last_player = ball.all_players_hitted[0]
        pos = last_player.actor.node.position
        if not self.left_right or not self.up_down:
            self.activated = False
            return
        self.left_right = last_player.actor.node.move_left_right / 1.75
        self.up_down = last_player.actor.node.move_up_down / 1.75
        if not self.left_right or not self.up_down:
            self.activated = False
            return
        pos = (pos[0] + self.left_right, pos[1] + 0.8, pos[2] - self.up_down)
        ball.node.position = pos
        self.activated = True
        bs.timer(0, self.assistant_setup)

    def on_team_join(self, team: Team) -> None:
        pass

    def get_instance_description(self) -> Union[str, Sequence]:
        if self.gk_mode:
            return self.gmgd
        if self.score_to_win == 1:
            return self.hdag
        return self.hd

    def get_instance_description_short(self) -> Union[str, Sequence]:
        if self.gk_mode:
            return self.gmhd
        if self.score_to_win == 1:
            return self.hdag
        return f"ㅤ"

    def gk_setup(self) -> None:
        """إعداد وضع حارس المرمى"""
        if self.ball:
            self.kill_ball()
        self.spawn_ball()
        magnitude = random.randint(self.gk_mode, self.gk_mode + 10)
        velocity_magnitude = self.gk_mode / 6
        force_x = 15
        force_y = 3
        force_z = random.uniform(-2.7, 2.7)
        self.ball.node.handlemessage('impulse', 
            0, 0, 0, 3, 3, 3, 
            magnitude,
            velocity_magnitude,
            0, 0,
            force_x, force_y, force_z)

class SoccerMap(maps.HockeyStadium):
    name = 'Soccer Stadium'

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hockeyStadiumPreview'

    @classmethod
    def is_flat_ground(cls) -> bool:
        return True
    
    @classmethod
    def on_preload(cls) -> Any:
        data: dict[int, Any] = {
            'meshes': (
                bs.getmesh('hockeyStadiumOuter'),
                bs.getmesh('hockeyStadiumInner'),
                bs.getmesh('hockeyStadiumStands')
            ),
            'vr_fill_mesh': bs.getmesh('footballStadiumVRFill'),
            'collision_mesh': bs.getcollisionmesh('hockeyStadiumCollide'),
            'tex': bs.gettexture('hockeyStadium'),
            'stands_tex': bs.gettexture('bg'),
        }
        material = bs.Material()
        data['ice_material'] = material
        return data
    
    def __init__(self) -> None:
        super().__init__()
        pass

# ba_meta export babase.Plugin
class SoccerPlugin(babase.Plugin):
    def on_app_running(self) -> None:
        bs._map.register_map(SoccerMap)
