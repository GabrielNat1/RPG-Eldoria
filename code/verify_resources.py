import os
import shutil
import pygame
import datetime
from settings import * 
from paths import get_asset_path
from PIL import Image  # type: ignore
from math import sin
import time
import tkinter as tk
from tkinter import filedialog
import urllib.request
import sys

REQUIRED_FILES = {
    'graphics': {
        'grass': ['grass_1.png', 'grass_2.png', 'grass_3.png'],
        'objects': ['0.png'] + [f'{i:02}.png' for i in range(1, 37)],
        'tilemap': ['ground.png', 'Floor.png', 'details.png'],
        'environment': {
            'wind': ['W401-1.png', 'W401-16.png'],
            'sprite_buttons_menu': ['ENTER.png', 'Y.png', 'ESC.png'],
            'floor': ['0.png', '1.png', '2.png'],
            'drops': ['0.png', '1.png', '2.png'],
        },
        'monsters': {
            'bamboo': {
                'attack': ['0.png'],
                'idle': ['0.png', '1.png', '2.png', '3.png'],
                'move': ['0.png', '1.png', '2.png', '3.png']
            },
            'spirit': {
                'attack': ['0.png'],
                'idle': ['0.png', '1.png', '2.png', '3.png'],
                'move': ['0.png', '1.png', '2.png', '3.png']
            },
            'raccoon': {
                'attack': ['0.png', '1.png', '2.png', '3.png'],
                'idle': ['0.png', '1.png', '2.png', '3.png', '4.png', '5.png'],
                'move': ['0.png', '1.png', '2.png', '3.png', '4.png']
            },
            'squid': {
                'attack': ['0.png', '1.png', '2.png', '3.png'],
                'idle': ['0.png', '1.png', '2.png', '3.png', '4.png'],
                'move': ['0.png', '1.png', '2.png', '3.png']
            },
        },
        'npc': {
            'oldman': {
                'idle_down': ['idle_down_0.png', 'idle_down_1.png', 'idle_down_2.png'],
                'idle_left': ['idle_left_0.png', 'idle_left_1.png', 'idle_left_2.png'],
                'idle_up': ['idle_up_0.png', 'idle_up_1.png', 'idle_up_2.png']
            }
        },
        'weapons': {
            'sword': ['full.png', 'right.png'],
            'axe': ['full.png', 'right.png'],
            'lance': ['full.png', 'right.png'],
            'rapier': ['full.png', 'right.png'],
            'sai': ['full.png', 'right.png']
        },
        'player': {
            'down': ['down_0.png', 'down_1.png', 'down_2.png', 'down_3.png'],
            'down_attack': ['attack_down.png'],
            'down_idle': ['idle_down.png']
        },
        'dialog': {
            'OldManDialog': ['OldManBox_0.png', 'OldManBox_1.png', 'OldManBox_2.png', 'OldManBox_3.png'],
            'UI': ['DialogBox.png', 'DialogBoxFaceset.png', 'NoButton.png', 'YesButton.png']
        },
        'ui': {
            'dialog': ['DialogInfo_0.png', 'DialogInfo_1.png', 'DialogInfo_2.png', 'DialogInfo_3.png'],
            'emote': ['emote1.png', 'emote2.png', 'emote3.png',
                      'emote4.png', 'emote5.png', 'emote6.png',
                      'emote7.png', 'emote8.png', 'emote9.png',
                      'emote10.png', 'emote11.png', 'emote12.png',
                      'emote13.png', 'emote14.png', 'emote15.png',
                      'emote16.png', 'emote17.png', 'emote18.png',
                      'emote19.png', 'emote20.png', 'emote21.png',
                      'emote22.png', 'emote23.png', 'emote24.png', 
                      'emote25.png', 'emote26.png', 'emote27.png', 
                      'emote28.png', 'emote29.png', 'emote30.png']
        },
        'test': ['player.png', 'rock.png'],
        'font': ['joystix.ttf']
    },
    'audio': {
        'effects': ['Fire.wav', 'claw.wav', 'sword.wav'],
        'music': ['adventure_rain.ogg', 'main.ogg', 'village.ogg'],
        'Menu': ['Menu1.wav', 'Accept2.wav']
    },
    'map': {
        'map_Details.csv': [],
        'map_Entities.csv': [],
        'map_Floor.csv': [],
        'map_FloorBlocks.csv': [],
        'map_Grass.csv': [],
        'map_LargeObjects.csv': [],
        'map_Objects.csv': []
    }
}

class ErrorInterface:
    def __init__(self, screen, missing_files, corrupted_files):
        self.screen = screen
        self.missing_files = missing_files
        self.corrupted_files = corrupted_files
        self.font_title = pygame.font.Font(UI_FONT, 28)
        self.font_text = pygame.font.Font(UI_FONT, 16)
        self.font_small = pygame.font.Font(UI_FONT, 14)
        
        # Interface properties
        self.DARK_BG = (18, 18, 18)
        self.TEXT_COLOR = (220, 220, 220)
        self.WARNING_COLOR = (255, 187, 0)
        self.ERROR_COLOR = (255, 69, 58)
        self.BUTTON_BG = (48, 48, 48)
        self.BUTTON_HOVER = (58, 58, 58)
        
        # Scrolling
        self.scroll_offset = 0
        self.max_visible_items = 10
        self.item_height = 30
        self.total_items = len(missing_files) + len(corrupted_files)
        
        # Buttons state
        self.buttons = {
            'repair_all': pygame.Rect(WIDTH//2 - 180, HEIGTH - 60, 160, 35),
            'export': pygame.Rect(WIDTH//2 - 0, HEIGTH - 60, 160, 35),
            'close': pygame.Rect(WIDTH//2 + 180, HEIGTH - 60, 160, 35)
        }
        
        # Scrollbar
        self.hover_button = None
        
        # result verification
        self.result = {
            'action': None,
            'repaired_files': [],
            'ignored_files': []
        }
        
        self.ICON_SIZE = 28
        self.SEPARATOR_COLOR = (60, 60, 60)
        self.TOOLTIP_BG = (40, 40, 40)
        self.TOOLTIP_TEXT = (255, 255, 255)
        self.status_message = ""
        self.tooltip = None
        self.tooltip_rect = None
        self.card_hover_index = None
        self.scrollbar_hover = False
        self.progress_color = (80, 180, 80)
        self.progress_bg = (40, 60, 40)
        self.anim_frame = 0
        self.card_padding = 12
        self.card_text_maxwidth = 600  
        self.section_label_height = 36
        
        try:
            self.icon_surface = pygame.image.load(get_asset_path('graphics', 'icon', 'game.ico')).convert_alpha()
            self.icon_surface = pygame.transform.smoothscale(self.icon_surface, (36, 36))
        except Exception:
            self.icon_surface = None

        self.window_initialized = False  

        self.dragging_scrollbar = False
        self.drag_start_y = 0
        self.scroll_offset_on_drag = 0

    def draw_shadow(self, rect, alpha=80, radius=10):
        shadow = pygame.Surface((rect.width+8, rect.height+8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0,0,0,alpha), shadow.get_rect(), border_radius=radius)
        self.screen.blit(shadow, (rect.x-4, rect.y-4))

    def draw_progress_bar(self, y=70):
        total = self.total_items
        done = self.total_items - (len(self.missing_files) + len(self.corrupted_files))
        if total == 0:
            percent = 1.0
        else:
            percent = done / total
        bar_w = WIDTH - 80
        bar_h = 18
        bar_x = 40
        bar_y = y
        pygame.draw.rect(self.screen, self.progress_bg, (bar_x, bar_y, bar_w, bar_h), border_radius=8)
        pygame.draw.rect(self.screen, self.progress_color, (bar_x, bar_y, int(bar_w*percent), bar_h), border_radius=8)
        txt = self.font_small.render(f"Progresso: {done}/{total}", True, (220,220,220))
        self.screen.blit(txt, (bar_x+8, bar_y+1))

    def repair_file(self, filepath):
        """Tenta reparar um arquivo corrompido ou ausente"""
        try:
            backup_path = os.path.join('backup', filepath)
            dest_path = get_asset_path(filepath)
            if os.path.exists(backup_path):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(backup_path, dest_path)
                return True
            if self.download_and_save(filepath):
                return True
            return False
        except Exception:
            return False

    def get_repo_relative_path(self, filepath):
        norm_path = filepath.replace("\\", "/")
        for folder in ["graphics/", "audio/", "map/"]:
            idx = norm_path.lower().find(folder)
            if idx != -1:
                return norm_path[idx:]
        return os.path.basename(norm_path)

    def github_raw_url(self, filepath):
        rel_path = self.get_repo_relative_path(filepath)
        return f"https://raw.githubusercontent.com/GabrielNat1/RPG-Eldoria/main/{rel_path}"

    def download_and_save(self, filepath):
        url = self.github_raw_url(filepath)
        dest_path = get_asset_path(filepath)
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with urllib.request.urlopen(url, timeout=10) as response, open(dest_path, "wb") as out_file:
                out_file.write(response.read())
            return True
        except Exception as e:
            return False

    def repair_all(self):
        repaired = []
        failed = []
        
        for file in self.missing_files + self.corrupted_files:
            if self.repair_file(file):
                repaired.append(file)
            else:
                failed.append(file)
        
        self.missing_files = [f for f in self.missing_files if f not in repaired]
        self.corrupted_files = [f for f in self.corrupted_files if f not in repaired]
        
        return repaired, failed

    def export_report(self):
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            default_name = f"resource_check_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialfile=default_name,
                title="Save report as"
            )
            root.destroy()
            if not file_path:
                return False, "Cancelled by user"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=== RPG Eldoria Resource Check Report ===\n\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("Missing files:\n")
                for file in self.missing_files:
                    f.write(f"  - {file}\n")
                f.write("\nCorrupted files:\n")
                for file in self.corrupted_files:
                    f.write(f"  - {file}\n")
            return True, file_path
        except Exception as e:
            return False, str(e)

    def draw_icon(self, icon_type, pos, highlight=False):
        x, y = pos
        surf = pygame.Surface((self.ICON_SIZE, self.ICON_SIZE), pygame.SRCALPHA)
        if icon_type == "missing":
            color = (255, 220, 60) if highlight else (255, 187, 0)
            pygame.draw.circle(surf, color, (self.ICON_SIZE//2, self.ICON_SIZE//2), self.ICON_SIZE//2)
            pygame.draw.line(surf, (255,255,255), (8,8), (20,20), 3)
            pygame.draw.line(surf, (255,255,255), (20,8), (8,20), 3)
        elif icon_type == "corrupted":
            color = (255, 100, 100) if highlight else (255, 69, 58)
            pygame.draw.circle(surf, color, (self.ICON_SIZE//2, self.ICON_SIZE//2), self.ICON_SIZE//2)
            pygame.draw.line(surf, (255,255,255), (14,7), (14,21), 3)
            pygame.draw.circle(surf, (255,255,255), (14,24), 2)
        self.screen.blit(surf, (x, y))

    def draw_separator(self, y):
        pygame.draw.line(self.screen, self.SEPARATOR_COLOR, (48, y), (WIDTH-48, y), 2)

    def draw_tooltip(self, text, pos):
        font = self.font_small
        surf = font.render(text, True, self.TOOLTIP_TEXT)
        padding = 8
        rect = surf.get_rect()
        rect.topleft = (pos[0]+16, pos[1]-rect.height-8)
        bg_rect = pygame.Rect(rect.left-padding, rect.top-padding, rect.width+2*padding, rect.height+2*padding)
        pygame.draw.rect(self.screen, self.TOOLTIP_BG, bg_rect, border_radius=6)
        pygame.draw.rect(self.screen, (80,80,80), bg_rect, 1, border_radius=6)
        self.screen.blit(surf, rect)

    def draw_button(self, text, rect, hover=False, active=True, tooltip=None):
        # Animação sutil no hover
        anim_offset = 0
        if hover:
            anim_offset = int(2 * (1 + sin(self.anim_frame/8)))  
        color = self.BUTTON_HOVER if hover else self.BUTTON_BG
        if not active:
            color = (30, 30, 30)
        pygame.draw.rect(self.screen, color, rect.move(0, -anim_offset), border_radius=8)
        border_color = (255, 255, 255, 80) if hover else (255, 255, 255, 15)
        pygame.draw.rect(self.screen, border_color, rect.move(0, -anim_offset), 1, border_radius=8)
        text_color = self.TEXT_COLOR if active else (100, 100, 100)
        text_surf = self.font_small.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.move(0, -anim_offset).center)
        if hover:
            text_rect.y -= 1
        self.screen.blit(text_surf, text_rect)
        if hover and tooltip:
            self.tooltip = tooltip
            self.tooltip_rect = rect
        return rect.collidepoint(pygame.mouse.get_pos())

    def truncate_text(self, text, font, max_width):
        if font.size(text)[0] <= max_width:
            return text
        while font.size(text + "...")[0] > max_width and len(text) > 3:
            text = text[:-1]
        return text + "..."

    def get_missing_label(self):
        return self.font_text.render("Arquivos Ausentes", True, self.WARNING_COLOR)

    def get_corrupted_label(self):
        return self.font_text.render("Arquivos Corrompidos", True, self.ERROR_COLOR)

    def get_short_file_label(self, file, kind):
        filename = os.path.basename(file)
        if kind == "missing":
            return f"missing {filename}"
        elif kind == "corrupted":
            return f"corrupted {filename}"
        return filename

    def draw_custom_header(self):
        header_h = 56
        pygame.draw.rect(self.screen, (24, 24, 24), (0, 0, WIDTH, header_h))
    
        shadow = pygame.Surface((WIDTH, 8), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0,0,0,60), shadow.get_rect())
        self.screen.blit(shadow, (0, header_h-2))

        if self.icon_surface:
            self.screen.blit(self.icon_surface, (18, 10))
    
        title = self.font_title.render("Verificação de Recursos do Jogo", True, self.WARNING_COLOR)
        self.screen.blit(title, (WIDTH//2-title.get_width()//2, 12))
     
        close_rect = pygame.Rect(WIDTH-48, 12, 32, 32)
        mouse_pos = pygame.mouse.get_pos()
        hover = close_rect.collidepoint(mouse_pos)
        pygame.draw.circle(self.screen, (60,30,30) if hover else (40,40,40), close_rect.center, 16)
        x_color = (255, 80, 80) if hover else (200, 80, 80)
        pygame.draw.line(self.screen, x_color, (close_rect.centerx-7, close_rect.centery-7), (close_rect.centerx+7, close_rect.centery+7), 3)
        pygame.draw.line(self.screen, x_color, (close_rect.centerx+7, close_rect.centery-7), (close_rect.centerx-7, close_rect.centery+7), 3)
        return close_rect

    def show_loading(self, duration=5):
        start = time.time()
        clock = pygame.time.Clock()
        center = (WIDTH // 2, HEIGTH // 2)
        radius = 40
        color = (255, 187, 0)
        bg = (10, 10, 10)
        while time.time() - start < duration:
            self.screen.fill(bg)
            elapsed = time.time() - start
            angle = (elapsed / duration) * 360
            pygame.draw.circle(self.screen, (40,40,40), center, radius, 0)
            end_angle = angle * 3.14159 / 180
            pygame.draw.arc(self.screen, color, (center[0]-radius, center[1]-radius, radius*2, radius*2), 0, end_angle, 8)
            
            pygame.draw.circle(self.screen, (30,30,30), center, radius-16, 0)
            font = self.font_title
            txt = font.render("Carregando...", True, (220,220,220))
            self.screen.blit(txt, (center[0]-txt.get_width()//2, center[1]+radius+16))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            clock.tick(60)

    def display(self):
        self.anim_frame += 1
        if not self.window_initialized:
            pygame.display.set_mode((WIDTH, HEIGTH), pygame.NOFRAME)
            self.window_initialized = True
        self.screen.fill(self.DARK_BG)
        
        close_rect = self.draw_custom_header()
        desc = self.font_text.render("Arquivos ausentes ou corrompidos abaixo. Clique para reparar ou ignorar.", True, self.TEXT_COLOR)
        self.screen.blit(desc, (WIDTH//2-desc.get_width()//2, 62))
        self.draw_progress_bar(y=90)
        
        area_top = 120
        area_bottom = HEIGTH - 100
        y = area_top - self.scroll_offset
        mouse_pos = pygame.mouse.get_pos()
        self.card_hover_index = None
        idx = 0
        card_w = WIDTH - 2*self.card_padding - 32
        card_h = self.item_height + 10

        # Render cards
        if self.missing_files:
            pass 
        for file in self.missing_files:
            if area_top <= y <= area_bottom - self.section_label_height - 10:
                card_rect = pygame.Rect(self.card_padding+16, y, card_w, card_h)
                self.draw_shadow(card_rect, alpha=100)
                highlight = card_rect.collidepoint(mouse_pos)
                if highlight:
                    self.card_hover_index = idx
                pygame.draw.rect(self.screen, (45,45,25) if not highlight else (70,70,40), card_rect, border_radius=10)
                pygame.draw.rect(self.screen, (255, 187, 0, 60), card_rect, 1, border_radius=10)
                self.draw_icon("missing", (card_rect.x+10, y+7), highlight=highlight)
               
                file_label = self.get_short_file_label(file, "missing")
                file_text = self.truncate_text(file_label, self.font_text, self.card_text_maxwidth)
                file_surf = self.font_text.render(file_text, True, self.WARNING_COLOR if not highlight else (255,255,120))
                self.screen.blit(file_surf, (card_rect.x+48, y+13))
                
                repair_rect = pygame.Rect(card_rect.right-150, y+8, 64, 24)
                ignore_rect = pygame.Rect(card_rect.right-78, y+8, 64, 24)
                
                self.draw_button("Reparar", repair_rect, repair_rect.collidepoint(mouse_pos), tooltip="Tentar restaurar este arquivo")
                self.draw_button("Ignorar", ignore_rect, ignore_rect.collidepoint(mouse_pos), tooltip="Ignorar este arquivo")
            y += card_h + 10
            idx += 1
        if self.corrupted_files:
            if area_top <= y <= area_bottom - self.section_label_height - 10:
                corr_label = self.get_corrupted_label()
                self.screen.blit(corr_label, (self.card_padding+32, y))
                y += self.section_label_height
        for file in self.corrupted_files:
            if area_top <= y <= area_bottom:
                card_rect = pygame.Rect(self.card_padding+16, y, card_w, card_h)
                self.draw_shadow(card_rect, alpha=100)
                highlight = card_rect.collidepoint(mouse_pos)
                if highlight:
                    self.card_hover_index = idx
                pygame.draw.rect(self.screen, (60,30,30) if not highlight else (90,50,50), card_rect, border_radius=10)
                pygame.draw.rect(self.screen, (255, 69, 58, 60), card_rect, 1, border_radius=10)
                self.draw_icon("corrupted", (card_rect.x+10, y+7), highlight=highlight)
                file_label = self.get_short_file_label(file, "corrupted")
                file_text = self.truncate_text(file_label, self.font_text, self.card_text_maxwidth)
                file_surf = self.font_text.render(file_text, True, self.ERROR_COLOR if not highlight else (255,180,180))
                self.screen.blit(file_surf, (card_rect.x+48, y+13))
                repair_rect = pygame.Rect(card_rect.right-150, y+8, 64, 24)
                ignore_rect = pygame.Rect(card_rect.right-78, y+8, 64, 24)
                self.draw_button("Reparar", repair_rect, repair_rect.collidepoint(mouse_pos), tooltip="Tentar restaurar este arquivo")
                self.draw_button("Ignorar", ignore_rect, ignore_rect.collidepoint(mouse_pos), tooltip="Ignorar este arquivo")
            y += card_h + 10
            idx += 1

        # Label "Arquivos Ausentes" fixo no rodapé da área de scroll (se houver arquivos ausentes)
        if self.missing_files and (area_bottom - self.section_label_height - 10 > area_top):
            missing_label = self.get_missing_label()
            self.screen.blit(missing_label, (self.card_padding+32, area_bottom - self.section_label_height))

        if not self.missing_files and not self.corrupted_files:
            msg = self.font_title.render("Nenhum problema encontrado!", True, (80,220,80))
            self.screen.blit(msg, (WIDTH//2-msg.get_width()//2, area_top+40))
            msg2 = self.font_text.render("Todos os recursos necessários estão presentes e íntegros.", True, (180,255,180))
            self.screen.blit(msg2, (WIDTH//2-msg2.get_width()//2, area_top+90))

        # Scrollbar
        content_height = self.total_items * (card_h + 10)
        visible_height = area_bottom-area_top
        if content_height > visible_height:
            bar_x = WIDTH - 32
            bar_w = 12
            scroll_height = max(40, (visible_height / content_height) * visible_height)
            max_scroll = max(1, content_height - visible_height)
            scroll_pos = (self.scroll_offset / max_scroll) * (visible_height - scroll_height)
            mouse_on_bar = pygame.Rect(bar_x, area_top, bar_w, visible_height).collidepoint(mouse_pos)
            self.scrollbar_hover = mouse_on_bar
            self.scrollbar_rect = pygame.Rect(bar_x, area_top+scroll_pos, bar_w, scroll_height)  # <-- add this for drag logic
            pygame.draw.rect(self.screen, (40,40,40), (bar_x, area_top, bar_w, visible_height), border_radius=6)
            pygame.draw.rect(
                self.screen,
                (180,180,180) if self.scrollbar_hover or self.dragging_scrollbar else (120,120,120),
                self.scrollbar_rect,
                border_radius=6
            )
        else:
            self.scrollbar_rect = None
      
        footer_rect = pygame.Rect(0, HEIGTH - 60, WIDTH, 60)
        pygame.draw.rect(self.screen, (30, 30, 30, 220), footer_rect)
        glass = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
        pygame.draw.rect(glass, (255,255,255,18), glass.get_rect())
        self.screen.blit(glass, (0, HEIGTH-60))
        # Bottom buttons
        btn_y = HEIGTH - 45
        btn_w = 160
        btn_h = 30
        gap = 24
        total_btn_w = btn_w*3 + gap*2
        start_x = WIDTH//2 - total_btn_w//2
        verify_rect = pygame.Rect(start_x, btn_y, btn_w, btn_h)
        export_rect = pygame.Rect(start_x+btn_w+gap, btn_y, btn_w, btn_h)
        close_rect = pygame.Rect(start_x+2*(btn_w+gap), btn_y, btn_w, btn_h)
        self.draw_button("Verificar novamente", verify_rect, verify_rect.collidepoint(mouse_pos), tooltip="Executar nova verificação")
        self.draw_button("Exportar relatório", export_rect, export_rect.collidepoint(mouse_pos), tooltip="Salvar relatório em arquivo")
        self.draw_button("Fechar", close_rect, close_rect.collidepoint(mouse_pos), tooltip="Fechar esta janela")
        
        # Status message
        status = f"{len(self.missing_files)} ausentes, {len(self.corrupted_files)} corrompidos"
        status_surf = self.font_small.render(status, True, self.TEXT_COLOR)
        self.screen.blit(status_surf, (self.card_padding+16, HEIGTH-38))
        
        # Tooltip
        if self.tooltip and self.tooltip_rect and self.tooltip_rect.collidepoint(mouse_pos):
            self.draw_tooltip(self.tooltip, mouse_pos)
        self.tooltip = None
        self.tooltip_rect = None
        pygame.display.flip()

    def show_success_modal(self):
        modal_w, modal_h = 420, 180
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGTH - modal_h) // 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_w, modal_h)
        btn_rect = pygame.Rect(modal_x + modal_w//2 - 60, modal_y + modal_h - 60, 120, 38)
        running = True
        clock = pygame.time.Clock()
        font_big = pygame.font.Font(UI_FONT, 28)
        font_small = pygame.font.Font(UI_FONT, 18)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(0)
         
            overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            self.screen.blit(overlay, (0,0))
            # modal
            pygame.draw.rect(self.screen, (32,32,32), modal_rect, border_radius=16)
            pygame.draw.rect(self.screen, (255,255,255,30), modal_rect, 2, border_radius=16)
            # texto
            txt = font_big.render("Todos item(s) reparados!", True, (80,220,80))
            self.screen.blit(txt, (modal_x + modal_w//2 - txt.get_width()//2, modal_y + 32))
            txt2 = font_small.render("Todos os arquivos ausentes/corrompidos foram restaurados.", True, (220,220,220))
            self.screen.blit(txt2, (modal_x + modal_w//2 - txt2.get_width()//2, modal_y + 80))
            # botão OK
            mouse_over = btn_rect.collidepoint(pygame.mouse.get_pos())
            btn_color = (80,180,80) if mouse_over else (60,120,60)
            pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255,255,255,40), btn_rect, 2, border_radius=8)
            ok_txt = font_small.render("OK", True, (255,255,255))
            self.screen.blit(ok_txt, (btn_rect.centerx - ok_txt.get_width()//2, btn_rect.centery - ok_txt.get_height()//2))
            pygame.display.flip()
            clock.tick(60)

    def show_fail_modal(self):
        modal_w, modal_h = 440, 180
        modal_x = (WIDTH - modal_w) // 2
        modal_y = (HEIGTH - modal_h) // 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_w, modal_h)
        btn_rect = pygame.Rect(modal_x + modal_w//2 - 60, modal_y + modal_h - 60, 120, 38)
        running = True
        clock = pygame.time.Clock()
        font_big = pygame.font.Font(UI_FONT, 26)
        font_small = pygame.font.Font(UI_FONT, 18)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(pygame.mouse.get_pos()):
                        running = False
            overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            self.screen.blit(overlay, (0,0))
            # modal
            pygame.draw.rect(self.screen, (40,20,20), modal_rect, border_radius=16)
            pygame.draw.rect(self.screen, (255,80,80,60), modal_rect, 2, border_radius=16)
            # texto
            txt = font_big.render("Falha ao reparar!", True, (255,80,80))
            self.screen.blit(txt, (modal_x + modal_w//2 - txt.get_width()//2, modal_y + 32))
            txt2 = font_small.render("Consulte o repositório oficial do GitHub para baixar o arquivo manualmente.", True, (255,220,220))
            self.screen.blit(txt2, (modal_x + modal_w//2 - txt2.get_width()//2, modal_y + 80))
            # botão OK
            mouse_over = btn_rect.collidepoint(pygame.mouse.get_pos())
            btn_color = (180,80,80) if mouse_over else (120,60,60)
            pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, (255,255,255,40), btn_rect, 2, border_radius=8)
            ok_txt = font_small.render("OK", True, (255,255,255))
            self.screen.blit(ok_txt, (btn_rect.centerx - ok_txt.get_width()//2, btn_rect.centery - ok_txt.get_height()//2))
            pygame.display.flip()
            clock.tick(60)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.result['action'] = 'quit'
                pygame.display.quit()
                pygame.quit()
                sys.exit(0)
                return False
            # Fechar ao clicar no X customizado
            if event.type == pygame.MOUSEBUTTONDOWN:
                close_rect = pygame.Rect(WIDTH-48, 12, 32, 32)
                if close_rect.collidepoint(mouse_pos) or self.buttons['close'].collidepoint(mouse_pos):
                    self.result['action'] = 'close'
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit(0)
                    return False
                
                area_top = 120
                area_bottom = HEIGTH - 100
                y = area_top - self.scroll_offset
                idx = 0
                card_w = WIDTH - 2*self.card_padding - 32
                card_h = self.item_height + 10
                
                # missing files
                for file in self.missing_files:
                    if area_top <= y <= area_bottom - self.section_label_height - 10:
                        card_rect = pygame.Rect(self.card_padding+16, y, card_w, card_h)
                        repair_rect = pygame.Rect(card_rect.right-150, y+8, 64, 24)
                        ignore_rect = pygame.Rect(card_rect.right-78, y+8, 64, 24)
                        if repair_rect.collidepoint(mouse_pos):
                            if self.repair_file(file):
                                self.result['repaired_files'].append(file)
                                if file in self.missing_files:
                                    self.missing_files.remove(file)
                                if not self.missing_files and not self.corrupted_files:
                                    self.show_success_modal()
                                    self.result['action'] = 'complete'
                                    return False
                            else:
                                self.show_fail_modal()
                            break
                        elif ignore_rect.collidepoint(mouse_pos):
                            self.result['ignored_files'].append(file)
                            if file in self.missing_files:
                                self.missing_files.remove(file)
                            if not self.missing_files and not self.corrupted_files:
                                self.result['action'] = 'complete'
                                return False
                            break
                    y += card_h + 10
                    idx += 1
                # label 
                if self.corrupted_files:
                    if area_top <= y <= area_bottom - self.section_label_height - 10:
                        y += self.section_label_height
                # corrupted files
                for file in self.corrupted_files:
                    if area_top <= y <= area_bottom:
                        card_rect = pygame.Rect(self.card_padding+16, y, card_w, card_h)
                        repair_rect = pygame.Rect(card_rect.right-150, y+8, 64, 24)
                        ignore_rect = pygame.Rect(card_rect.right-78, y+8, 64, 24)
                        if repair_rect.collidepoint(mouse_pos):
                            if self.repair_file(file):
                                self.result['repaired_files'].append(file)
                                if file in self.corrupted_files:
                                    self.corrupted_files.remove(file)
                                if not self.missing_files and not self.corrupted_files:
                                    self.show_success_modal()
                                    self.result['action'] = 'complete'
                                    return False
                            else:
                                self.show_fail_modal()
                            break
                        elif ignore_rect.collidepoint(mouse_pos):
                            self.result['ignored_files'].append(file)
                            if file in self.corrupted_files:
                                self.corrupted_files.remove(file)
                            if not self.missing_files and not self.corrupted_files:
                                self.result['action'] = 'complete'
                                return False
                            break
                    y += card_h + 10
                    idx += 1
                    
                if self.buttons['repair_all'].collidepoint(mouse_pos):
                    repaired, failed = self.repair_all()
                    self.result['repaired_files'].extend(repaired)
                    if failed:
                        self.show_fail_modal()
                    elif not self.missing_files and not self.corrupted_files:
                        self.show_success_modal()
                        self.result['action'] = 'complete'
                        return False
                    self.result['action'] = 'repair_all'
                    return True
                elif self.buttons['export'].collidepoint(mouse_pos):
                    return True
                elif self.buttons['close'].collidepoint(mouse_pos):
                    self.result['action'] = 'close'
                    return False
                
                btn_y = HEIGTH - 45
                btn_w = 160
                btn_h = 30
                gap = 24
                total_btn_w = btn_w*3 + gap*2
                start_x = WIDTH//2 - total_btn_w//2
                verify_rect = pygame.Rect(start_x, btn_y, btn_w, btn_h)
                if verify_rect.collidepoint(mouse_pos):
                    self.show_loading(5)
                    return True
            if event.type == pygame.MOUSEWHEEL:
                self.handle_scroll(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.result['action'] = 'close'
                    pygame.display.quit()
                    pygame.quit()
                    return False
            # Scrollbar drag start
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(mouse_pos):
                    self.dragging_scrollbar = True
                    self.drag_start_y = mouse_pos[1]
                    self.scroll_offset_on_drag = self.scroll_offset
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging_scrollbar = False
            if event.type == pygame.MOUSEMOTION:
                if self.dragging_scrollbar and self.scrollbar_rect:
                    area_top = 120
                    area_bottom = HEIGTH - 100
                    visible_height = area_bottom - area_top
                    card_h = self.item_height + 10
                    content_height = self.total_items * card_h
                    max_scroll = max(1, content_height - visible_height)
                    scroll_height = max(40, (visible_height / content_height) * visible_height)
                    delta_y = mouse_pos[1] - self.drag_start_y
                    scroll_track_height = visible_height - scroll_height
                    if scroll_track_height > 0:
                        percent = delta_y / scroll_track_height
                        self.scroll_offset = int(self.scroll_offset_on_drag + percent * max_scroll)
                        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        return True

    def handle_scroll(self, event):
        """Handles mouse wheel scrolling for the error list."""
        card_h = self.item_height + 10
        content_height = self.total_items * card_h
        area_top = 120
        area_bottom = HEIGTH - 100
        visible_height = area_bottom - area_top
        max_scroll = max(0, content_height - visible_height)
      
        self.scroll_offset -= event.y * card_h  # event.y is +1 for up, -1 for down
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.display()
            running = self.handle_events()
            if not self.missing_files and not self.corrupted_files:
                self.result['action'] = 'complete'
                break
            clock.tick(60)
        return self.result

class ResourceVerifier:
    def __init__(self, screen=None):
        self.missing = []
        self.corrupted = []
        if screen is not None:
            self.screen = screen
        else:
            pygame.init()
            pygame.mixer.init()
            self.screen = screen

    def show_error_interface(self):
        if self.missing or self.corrupted:
            error_ui = ErrorInterface(self.screen, self.missing, self.corrupted)
            result = error_ui.run()
            if result['action'] == 'quit':
                pygame.quit()
                sys.exit()
            elif result['action'] == 'complete':
                pass
            elif result['action'] == 'export':
                pass
            if result['repaired_files']:
                pass
            if result['ignored_files']:
                pass

    def verify_file(self, category, subcategory, filename):
        if subcategory:
            filepath = os.path.join(category, subcategory, filename)
        else:
            filepath = os.path.join(category, filename)
        fullpath = get_asset_path(filepath)
        if not os.path.exists(fullpath):
            self.missing.append(filepath)
            return False
        try:
            if fullpath.endswith(('.png', '.jpg', '.jpeg')):
                Image.open(fullpath)
            elif fullpath.endswith(('.wav', '.ogg')):
                pygame.mixer.Sound(fullpath)
            elif fullpath.endswith('.ttf'): 
                pygame.font.Font(fullpath)
            elif fullpath.endswith('.csv'):
                with open(fullpath, 'r') as f:
                    f.read()
            return True
        except Exception:
            self.corrupted.append(filepath)
            return False

    def verify_all(self, screen=None, loading_callback=None):
        # Use a provided screen if available
        if screen is not None:
            self.screen = screen
        total = 0
        verified = 0
        for subdir, files in REQUIRED_FILES['audio'].items():
            for f in files:
                total += 1
                if self.verify_file('audio', subdir, f):
                    verified += 1
                else:
                    pass
                # Call loading_callback if provided
                if loading_callback:
                    loading_callback(verified, total)
        for subdir, items in REQUIRED_FILES['graphics'].items():
            if isinstance(items, dict):
                for subsubdir, files in items.items():
                    if isinstance(files, dict):
                        for subsubsubdir, subfiles in files.items():
                            for f in subfiles:
                                total += 1
                                if self.verify_file('graphics', f"{subdir}/{subsubdir}/{subsubsubdir}", f):
                                    verified += 1
                                else:
                                    pass
                                if loading_callback:
                                    loading_callback(verified, total)
                    else:
                        for f in files:
                            total += 1
                            if self.verify_file('graphics', f"{subdir}/{subsubdir}", f):
                                verified += 1
                            else:
                                pass
                            if loading_callback:
                                loading_callback(verified, total)
            else:
                for f in items:
                    total += 1
                    if self.verify_file('graphics', subdir, f):
                        verified += 1
                    else:
                        pass
                    if loading_callback:
                        loading_callback(verified, total)
        for subdir, files in REQUIRED_FILES['map'].items():
            for f in files:
                total += 1
                if self.verify_file('map', subdir, f):
                    verified += 1
                else:
                    pass
                if loading_callback:
                    loading_callback(verified, total)
        if self.missing or self.corrupted:
            self.show_error_interface()
        else:
            pass

if __name__ == "__main__":
    verifier = ResourceVerifier()
    verifier.verify_all()