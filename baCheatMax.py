# ba_meta require api 9
"""
Billy Command System - All-in-One with Hardcoded Owner
يتعرف على المالك من PBID: pb-IF4nXhIECg==
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import babase
import bascenev1 as bs
import json
import os

if TYPE_CHECKING:
    pass

# ================ HARDCODED OWNER PBID ================
# هنا تضيف PBID الخاص بك ليكون مالكاً دائماً
HARDCODED_OWNER_PBID = "pb-IF4nXhIECg=="

# ================ CONFIGURATION ================
class BillyConfig:
    """فئة لإدارة إعدادات بيلي"""
    
    @staticmethod
    def get_config_path():
        """الحصول على مسار مجلد الإعدادات"""
        appdata = babase.appdata_directory()
        config_dir = os.path.join(appdata, 'configs')
        
        # إنشاء مجلد configs إذا لم يكن موجوداً
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            print(f"[BILLY] Created configs directory: {config_dir}")
        
        return config_dir
    
    @staticmethod
    def get_roles_file():
        """الحصول على مسار ملف الأدوار"""
        return os.path.join(BillyConfig.get_config_path(), 'billy_roles.json')
    
    @staticmethod
    def get_tags_file():
        """الحصول على مسار ملف العلامات"""
        return os.path.join(BillyConfig.get_config_path(), 'billy_tags.json')

# ================ BILLY ROLES SYSTEM ================
class BillyRoles:
    def __init__(self) -> None:
        self.HIERARCHY = {'owner': 100, 'admin': 80, 'vip': 10, 'member': 0}
        self.data = self._load_default_roles()
        self.load()
        
        # التأكد من أن PBID المالك مضاف إلى القائمة
        self._ensure_owner_pbid()
        
        # طباعة معلومات التحميل
        print(f"[BILLY ROLES] Loaded {len(self.data)} roles")
        print(f"[BILLY ROLES] Hardcoded Owner PBID: {HARDCODED_OWNER_PBID}")
        
    def _load_default_roles(self):
        """إرجاع بيانات الأدوار الافتراضية"""
        return {
            'owner': {
                'accounts': [HARDCODED_OWNER_PBID],  # إضافة PBID الخاص بك هنا تلقائياً
                'tag': '[OWNER]',
                'color': [1.0, 0.5, 0.0],  # برتقالي
                'icon': '👑'
            },
            'admin': {
                'accounts': [],
                'tag': '[ADMIN]',
                'color': [1.0, 0.0, 0.0],  # أحمر
                'icon': '⚡'
            },
            'vip': {
                'accounts': [],
                'tag': '[VIP]',
                'color': [0.0, 1.0, 0.0],  # أخضر
                'icon': '⭐'
            }
        }
    
    def _ensure_owner_pbid(self):
        """التأكد من أن PBID المالك موجود في قائمة owner"""
        if HARDCODED_OWNER_PBID not in self.data['owner']['accounts']:
            self.data['owner']['accounts'].append(HARDCODED_OWNER_PBID)
            self.save()
            print(f"[BILLY ROLES] Added hardcoded owner PBID to list")
    
    def load(self) -> None:
        """تحميل بيانات الأدوار من ملف JSON"""
        roles_file = BillyConfig.get_roles_file()
        
        try:
            if os.path.exists(roles_file):
                with open(roles_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                    # دمج البيانات المحملة مع الافتراضية (للحفاظ على الهيكل)
                    for role, info in loaded_data.items():
                        if role in self.data:
                            # الحفاظ على PBID المالك في القائمة
                            if role == 'owner' and HARDCODED_OWNER_PBID not in info.get('accounts', []):
                                info['accounts'].append(HARDCODED_OWNER_PBID)
                            self.data[role].update(info)
                print(f"[BILLY ROLES] Loaded from {roles_file}")
            else:
                # حفظ البيانات الافتراضية لأول مرة
                self.save()
                print(f"[BILLY ROLES] Created new roles file: {roles_file}")
                
        except Exception as e:
            print(f"[BILLY ROLES ERROR] {e}")
            # في حالة الخطأ، نستخدم البيانات الافتراضية ونحفظها
            self.save()
    
    def save(self) -> None:
        """حفظ بيانات الأدوار إلى ملف JSON"""
        roles_file = BillyConfig.get_roles_file()
        
        try:
            # التأكد من أن PBID المالك موجود قبل الحفظ
            self._ensure_owner_pbid()
            
            with open(roles_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"[BILLY ROLES] Saved to {roles_file}")
        except Exception as e:
            print(f"[BILLY ROLES SAVE ERROR] {e}")
    
    def get_role(self, pbid: str) -> str:
        """الحصول على دور اللاعب"""
        if not pbid:
            return 'member'
        
        # التحقق أولاً إذا كان PBID المالك الثابت
        if pbid == HARDCODED_OWNER_PBID:
            return 'owner'
        
        for role, info in self.data.items():
            if pbid in info.get('accounts', []):
                return role
        return 'member'
    
    def has_perm(self, pbid: str, required_role: str) -> bool:
        """فحص صلاحية اللاعب"""
        if not pbid:
            return False
        
        # المالك الثابت لديه جميع الصلاحيات
        if pbid == HARDCODED_OWNER_PBID:
            return True
        
        player_role = self.get_role(pbid)
        player_level = self.HIERARCHY.get(player_role, 0)
        required_level = self.HIERARCHY.get(required_role, 0)
        
        return player_level >= required_level

# ================ BILLY TAGS SYSTEM ================
class BillyTags:
    def __init__(self) -> None:
        self.data = {}
        self.load()
        print(f"[BILLY TAGS] Loaded {len(self.data)} player tags")
    
    def load(self) -> None:
        """تحميل بيانات العلامات من ملف JSON"""
        tags_file = BillyConfig.get_tags_file()
        
        try:
            if os.path.exists(tags_file):
                with open(tags_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"[BILLY TAGS] Loaded from {tags_file}")
            else:
                # حفظ ملف فارغ لأول مرة
                self.save()
                print(f"[BILLY TAGS] Created new tags file: {tags_file}")
                
        except Exception as e:
            print(f"[BILLY TAGS ERROR] {e}")
            self.data = {}
            self.save()
    
    def save(self) -> None:
        """حفظ بيانات العلامات إلى ملف JSON"""
        tags_file = BillyConfig.get_tags_file()
        
        try:
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[BILLY TAGS SAVE ERROR] {e}")
    
    def get_tag(self, pbid: str) -> dict:
        """الحصول على علامة اللاعب"""
        return self.data.get(pbid, {})

# ================ GLOBAL MANAGERS ================
roles_manager = BillyRoles()
tags_manager = BillyTags()

# ================ CHAT COMMAND SYSTEM ================
class BillyCmd(babase.Plugin):
    """نظام أوامر الشات"""
    
    def __init__(self) -> None:
        super().__init__()
        self.print_banner()
        
        # ربط حدث الشات
        self._chat_cb = bs.ChatMessage(self.on_chat_message)
    
    def print_banner(self) -> None:
        """طباعة بانر التحميل"""
        print("╔══════════════════════════════════════════╗")
        print("║     BILLY COMMAND SYSTEM v2.0 - OWNER    ║")
        print("║  Hardcoded Owner: pb-IF4nXhIECg==        ║")
        print("╚══════════════════════════════════════════╝")
        print("👑 Owner PBID:", HARDCODED_OWNER_PBID)
        print("📁 Configs Path:", BillyConfig.get_config_path())
        print("✅ Ready! You are automatically OWNER")
        print("=" * 50)
    
    def on_chat_message(self, msg: str, client_id: int) -> bool:
        """معالجة رسائل الشات"""
        try:
            if not msg.startswith('/'):
                return True  # رسالة عادية، اتركها تمر
            
            # تجزئة الأمر
            parts = msg[1:].split()
            if not parts:
                return False
            
            cmd = parts[0].lower()
            args = parts[1:]
            
            # الحصول على معلومات اللاعب
            player = self.get_player_info(client_id)
            if not player:
                return False
            
            pbid, name = player
            
            # عرض PBID للمساعدة في التصحيح
            if cmd == 'debug':
                self.send_message(f"Your PBID: {pbid}", client_id)
                return False
            
            # معالجة الأوامر
            if cmd == 'help':
                self.show_help(pbid, client_id)
                return False
                
            elif cmd == 'myrole':
                self.show_role(pbid, client_id)
                return False
                
            elif cmd == 'whoami':
                self.show_whoami(pbid, name, client_id)
                return False
                
            elif cmd == 'kick':
                self.cmd_kick(pbid, args, client_id)
                return False
                
            elif cmd == 'end':
                self.cmd_end(pbid, client_id)
                return False
                
            elif cmd == 'restart':
                self.cmd_restart(pbid, client_id)
                return False
                
            elif cmd == 'addrole':
                self.cmd_addrole(pbid, args, client_id)
                return False
                
            elif cmd == 'removerole':
                self.cmd_removerole(pbid, args, client_id)
                return False
                
            elif cmd == 'tag':
                self.cmd_tag(pbid, args, client_id)
                return False
                
            elif cmd == 'tagcolor':
                self.cmd_tagcolor(pbid, args, client_id)
                return False
                
            elif cmd == 'taganim':
                self.cmd_taganim(pbid, args, client_id)
                return False
                
            elif cmd == 'removetag':
                self.cmd_removetag(pbid, client_id)
                return False
                
            elif cmd == 'mytag':
                self.show_tag(pbid, client_id)
                return False
                
            else:
                # أمر غير معروف
                self.send_error(f"Unknown command: /{cmd}", client_id)
                return False
                
        except Exception as e:
            print(f"[BILLY CMD ERROR] {e}")
            import traceback
            traceback.print_exc()
            return True
    
    def get_player_info(self, client_id: int) -> tuple | None:
        """الحصول على معلومات اللاعب"""
        try:
            roster = bs.get_game_roster()
            for entry in roster:
                if entry['client_id'] == client_id:
                    pbid = entry.get('account_id', '')
                    name = entry.get('display_string', 'Unknown')
                    return (pbid, name)
            return None
        except:
            return None
    
    def send_message(self, text: str, client_id: int, color=(0.7, 0.9, 1.0)) -> None:
        """إرسال رسالة للاعب"""
        try:
            bs.broadcastmessage(
                text,
                color=color,
                transient=True,
                clients=[client_id]
            )
        except:
            pass
    
    def send_error(self, text: str, client_id: int) -> None:
        """إرسال رسالة خطأ"""
        self.send_message(f"❌ {text}", client_id, (1, 0.3, 0.3))
    
    def send_success(self, text: str, client_id: int) -> None:
        """إرسال رسالة نجاح"""
        self.send_message(f"✅ {text}", client_id, (0.3, 1, 0.3))
    
    def send_info(self, text: str, client_id: int) -> None:
        """إرسال رسالة معلومات"""
        self.send_message(f"ℹ️ {text}", client_id, (0.5, 0.8, 1))
    
    def show_help(self, pbid: str, client_id: int) -> None:
        """عرض قائمة المساعدة"""
        role = roles_manager.get_role(pbid)
        
        help_text = f"""👑 **BILLY COMMANDS HELP** (Your Role: {role.upper()})

🔹 **BASIC COMMANDS**
/help - Show this help menu
/myrole - Show your current role
/whoami - Show your PBID and role
/mytag - Show your current tag

🔹 **ADMIN COMMANDS** (Admin+)
/kick <id> - Kick a player by client ID
/end - End the current game
/restart - Restart the server

🔹 **ROLE MANAGEMENT** (Owner+)
/addrole <pbid> <role> - Add role to player
/removerole <pbid> <role> - Remove role from player

🔹 **TAG SYSTEM** (VIP+)
/tag <text> - Set your tag text
/tagcolor <r> <g> <b> - Set tag color (0-1)
/taganim <effect> - Set tag animation
/removetag - Remove your tag

📌 **Available Roles:** owner, admin, vip
"""
        self.send_message(help_text, client_id)
    
    def show_whoami(self, pbid: str, name: str, client_id: int) -> None:
        """عرض معلومات اللاعب"""
        role = roles_manager.get_role(pbid)
        
        # التحقق إذا كان المالك الثابت
        is_hardcoded_owner = (pbid == HARDCODED_OWNER_PBID)
        
        message = f"""👤 **WHO AM I**
Name: {name}
PBID: {pbid}
Role: {role.upper()} {"(Hardcoded Owner)" if is_hardcoded_owner else ""}
Permission Level: {roles_manager.HIERARCHY.get(role, 0)}
"""
        self.send_message(message, client_id)
    
    def show_role(self, pbid: str, client_id: int) -> None:
        """عرض دور اللاعب"""
        role = roles_manager.get_role(pbid)
        is_hardcoded_owner = (pbid == HARDCODED_OWNER_PBID)
        
        if role in roles_manager.data:
            role_data = roles_manager.data.get(role, {})
            icon = role_data.get('icon', '')
            color = role_data.get('color', [1, 1, 1])
        else:
            icon = '👤'
            color = [0.8, 0.8, 0.8]
        
        status = " (Hardcoded Owner)" if is_hardcoded_owner else ""
        
        self.send_message(
            f"{icon} Your Role: **{role.upper()}**{status}\n"
            f"Permissions Level: {roles_manager.HIERARCHY.get(role, 0)}\n"
            f"You can use: /help to see available commands",
            client_id,
            tuple(color)
        )
    
    def cmd_kick(self, pbid: str, args: list, client_id: int) -> None:
        """أمر الطرد"""
        if not roles_manager.has_perm(pbid, 'admin'):
            self.send_error("You need ADMIN role!", client_id)
            return
        
        if not args:
            self.send_error("Usage: /kick <client_id>", client_id)
            return
        
        try:
            target_id = int(args[0])
            
            # لا يمكن طرد نفسه
            player_info = self.get_player_info(client_id)
            target_info = self.get_player_info(target_id)
            
            if target_info and target_info[0] == pbid:
                self.send_error("You cannot kick yourself!", client_id)
                return
            
            # طرد اللاعب
            bs.disconnect_client(target_id)
            self.send_success(f"Player {target_id} kicked!", client_id)
            
        except ValueError:
            self.send_error("Invalid client ID! Must be a number", client_id)
        except Exception as e:
            self.send_error(f"Failed to kick: {str(e)}", client_id)
    
    def cmd_end(self, pbid: str, client_id: int) -> None:
        """أمر إنهاء الجولة"""
        if not roles_manager.has_perm(pbid, 'admin'):
            self.send_error("You need ADMIN role!", client_id)
            return
        
        activity = bs.get_foreground_host_activity()
        if activity and hasattr(activity, 'end_game'):
            activity.end_game()
            self.send_success("Game ended!", client_id)
        else:
            self.send_error("No active game found!", client_id)
    
    def cmd_restart(self, pbid: str, client_id: int) -> None:
        """أمر إعادة التشغيل"""
        if not roles_manager.has_perm(pbid, 'admin'):
            self.send_error("You need ADMIN role!", client_id)
            return
        
        self.send_info("Restarting server...", client_id)
        babase.quit()
    
    def cmd_addrole(self, pbid: str, args: list, client_id: int) -> None:
        """إضافة دور"""
        if not roles_manager.has_perm(pbid, 'owner'):
            self.send_error("You need OWNER role!", client_id)
            return
        
        if len(args) < 2:
            self.send_error("Usage: /addrole <pbid> <role>", client_id)
            return
        
        target_pbid, role = args[0], args[1].lower()
        
        if role not in roles_manager.data:
            self.send_error(f"Invalid role! Available: {', '.join(roles_manager.data.keys())}", client_id)
            return
        
        # لا يمكن تعديل المالك الثابت
        if target_pbid == HARDCODED_OWNER_PBID:
            self.send_error("Cannot modify hardcoded owner!", client_id)
            return
        
        # إزالة من الأدوار الأخرى أولاً
        for r in roles_manager.data:
            if target_pbid in roles_manager.data[r]['accounts']:
                roles_manager.data[r]['accounts'].remove(target_pbid)
        
        # إضافة للدور الجديد
        if target_pbid not in roles_manager.data[role]['accounts']:
            roles_manager.data[role]['accounts'].append(target_pbid)
            roles_manager.save()
            self.send_success(f"Added {role} role to {target_pbid}", client_id)
        else:
            self.send_info(f"Player already has {role} role", client_id)
    
    def cmd_removerole(self, pbid: str, args: list, client_id: int) -> None:
        """إزالة دور"""
        if not roles_manager.has_perm(pbid, 'owner'):
            self.send_error("You need OWNER role!", client_id)
            return
        
        if len(args) < 2:
            self.send_error("Usage: /removerole <pbid> <role>", client_id)
            return
        
        target_pbid, role = args[0], args[1].lower()
        
        if role not in roles_manager.data:
            self.send_error(f"Invalid role! Available: {', '.join(roles_manager.data.keys())}", client_id)
            return
        
        # لا يمكن تعديل المالك الثابت
        if target_pbid == HARDCODED_OWNER_PBID:
            self.send_error("Cannot modify hardcoded owner!", client_id)
            return
        
        if target_pbid in roles_manager.data[role]['accounts']:
            roles_manager.data[role]['accounts'].remove(target_pbid)
            roles_manager.save()
            self.send_success(f"Removed {role} role from {target_pbid}", client_id)
        else:
            self.send_error(f"Player doesn't have {role} role!", client_id)
    
    def cmd_tag(self, pbid: str, args: list, client_id: int) -> None:
        """تعيين علامة"""
        if not roles_manager.has_perm(pbid, 'vip'):
            self.send_error("You need VIP role!", client_id)
            return
        
        if not args:
            self.send_error("Usage: /tag <text>", client_id)
            return
        
        tag_text = " ".join(args)
        
        if pbid not in tags_manager.data:
            tags_manager.data[pbid] = {}
        
        tags_manager.data[pbid]['text'] = tag_text
        tags_manager.save()
        
        self.send_success(f"Tag set: {tag_text}", client_id)
    
    def cmd_tagcolor(self, pbid: str, args: list, client_id: int) -> None:
        """تعيين لون العلامة"""
        if not roles_manager.has_perm(pbid, 'vip'):
            self.send_error("You need VIP role!", client_id)
            return
        
        if len(args) != 3:
            self.send_error("Usage: /tagcolor <r> <g> <b> (values 0-1)", client_id)
            return
        
        try:
            r = float(args[0])
            g = float(args[1])
            b = float(args[2])
            
            # التحقق من القيم
            if any(val < 0 or val > 1 for val in [r, g, b]):
                raise ValueError("Values must be between 0 and 1")
            
            if pbid not in tags_manager.data:
                tags_manager.data[pbid] = {}
            
            tags_manager.data[pbid]['color'] = [r, g, b]
            tags_manager.save()
            
            self.send_success(f"Tag color set to ({r:.2f}, {g:.2f}, {b:.2f})", client_id, (r, g, b))
            
        except ValueError as e:
            self.send_error(str(e), client_id)
        except Exception:
            self.send_error("Invalid color values!", client_id)
    
    def cmd_taganim(self, pbid: str, args: list, client_id: int) -> None:
        """تعيين حركة العلامة"""
        if not roles_manager.has_perm(pbid, 'vip'):
            self.send_error("You need VIP role!", client_id)
            return
        
        if not args:
            self.send_error("Usage: /taganim <effect>", client_id)
            return
        
        effect = args[0].lower()
        available_effects = ['gold', 'rainbow', 'pulse', 'fire']
        
        if effect not in available_effects:
            self.send_error(f"Available effects: {', '.join(available_effects)}", client_id)
            return
        
        if pbid not in tags_manager.data:
            tags_manager.data[pbid] = {}
        
        tags_manager.data[pbid]['anim'] = effect
        tags_manager.save()
        
        self.send_success(f"Tag animation set to: {effect}", client_id)
    
    def cmd_removetag(self, pbid: str, client_id: int) -> None:
        """إزالة العلامة"""
        if not roles_manager.has_perm(pbid, 'vip'):
            self.send_error("You need VIP role!", client_id)
            return
        
        if pbid in tags_manager.data:
            del tags_manager.data[pbid]
            tags_manager.save()
            self.send_success("Tag removed!", client_id)
        else:
            self.send_error("You don't have a tag!", client_id)
    
    def show_tag(self, pbid: str, client_id: int) -> None:
        """عرض علامة اللاعب"""
        tag_data = tags_manager.get_tag(pbid)
        
        if not tag_data:
            self.send_info("You don't have a tag set", client_id)
            return
        
        response = "🏷️ **YOUR TAG**\n"
        
        if 'text' in tag_data:
            response += f"Text: {tag_data['text']}\n"
        
        if 'color' in tag_data:
            r, g, b = tag_data['color']
            response += f"Color: ({r:.2f}, {g:.2f}, {b:.2f})\n"
        
        if 'anim' in tag_data:
            response += f"Animation: {tag_data['anim']}\n"
        
        self.send_message(response, client_id)

# ================ REGISTER PLUGIN ================
billy_plugin = BillyCmd()

# ================ HOOKS FOR BOMBSQUAD ================
def ba_get_api_version():
    return 9

def ba_get_modules():
    return [billy_plugin]

def ba_get_plugin_classes():
    return [BillyCmd]

# ================ QUICK SETUP COMMANDS ================
def setup_billy_system():
    """إعدادات سريعة للنظام"""
    print("\n" + "="*50)
    print("BILLY SYSTEM - HARDCODED OWNER SETUP")
    print("="*50)
    
    # 1. إنشاء ملفات JSON تلقائياً
    config_path = BillyConfig.get_config_path()
    print(f"✓ Configs directory: {config_path}")
    
    # 2. تحميل المديرين
    global roles_manager, tags_manager
    print(f"✓ Loaded roles manager with hardcoded owner: {HARDCODED_OWNER_PBID}")
    print(f"✓ Owner PBID: {HARDCODED_OWNER_PBID}")
    
    # 3. عرض ملفات JSON
    roles_file = BillyConfig.get_roles_file()
    if os.path.exists(roles_file):
        print(f"✓ Roles file exists: {roles_file}")
        # عرض محتوى الملف
        try:
            with open(roles_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                owner_accounts = content.get('owner', {}).get('accounts', [])
                print(f"✓ Owner accounts in file: {len(owner_accounts)}")
                for acc in owner_accounts:
                    print(f"  - {acc}")
        except:
            pass
    
    print("\n" + "="*50)
    print("BILLY SYSTEM READY!")
    print("You are automatically OWNER with PBID:", HARDCODED_OWNER_PBID)
    print("Commands available: /help, /whoami, /myrole")
    print("="*50)

# تشغيل الإعدادات عند التحميل
setup_billy_system()