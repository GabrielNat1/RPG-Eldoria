import os
import shutil
import pygame
import datetime
from settings import * 
from paths import get_asset_path
from PIL import Image  # type: ignore

# Required resources dictionary
REQUIRED_FILES = {
        'graphics': {
        'Grass': ['grass_1.png', 'grass_2.png', 'grass_3.png'],
        'objects': [f'{i}.png' for i in range(37)],  
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
        'particles': {
            'flame': ['fire.png'],
            'flame_frames': ['0.png', '01.png', '11.png'],
            'leaf1': [...],
            'leaf2': [...],
            'slash': ['0.png', '1.png', '2.png', '3.png']
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
        'csv': [
            'map_Details.csv',
            'map_Entities.csv',
            'map_Floor.csv',
            'map_FloorBlocks.csv',
            'map_Grass.csv',
            'map_LargeObjects.csv',
            'map_Objects.csv'
        ]
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
        
        # Adicionar estado de hover para botões
        self.hover_button = None
        
        # Adicionar dicionário de retorno
        self.result = {
            'action': None,
            'repaired_files': [],
            'ignored_files': []
        }

    def repair_file(self, filepath):
        """Tenta reparar um arquivo corrompido ou ausente"""
        try:
            # Verifica se é um arquivo de backup
            backup_path = os.path.join('backup', filepath)
            if os.path.exists(backup_path):
                # Copia o arquivo de backup
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                shutil.copy2(backup_path, filepath)
                return True
            return False
        except Exception as e:
            print(f"Erro ao reparar {filepath}: {e}")
            return False

    def repair_all(self):
        """Tenta reparar todos os arquivos com problemas"""
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
        """Exporta um relatório detalhado dos problemas"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resource_check_report_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write("=== RPG Eldoria Resource Check Report ===\n\n")
                f.write(f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("Arquivos ausentes:\n")
                for file in self.missing_files:
                    f.write(f"  - {file}\n")
                    
                f.write("\nArquivos corrompidos:\n")
                for file in self.corrupted_files:
                    f.write(f"  - {file}\n")
                    
            return True, filename
        except Exception as e:
            return False, str(e)

    def draw_scrollbar(self):
        """Desenha a barra de rolagem"""
        if self.total_items <= self.max_visible_items:
            return
            
        # Calcula tamanho e posição da barra
        content_height = self.total_items * self.item_height
        visible_height = self.max_visible_items * self.item_height
        scroll_height = (visible_height / content_height) * visible_height
        scroll_pos = (self.scroll_offset / content_height) * visible_height
        
        # Desenha trilho da barra
        bar_rect = pygame.Rect(WIDTH - 20, 100, 10, visible_height)
        pygame.draw.rect(self.screen, (40, 40, 40), bar_rect)
        
        # Desenha a barra
        scroll_rect = pygame.Rect(WIDTH - 20, 100 + scroll_pos, 10, scroll_height)
        pygame.draw.rect(self.screen, (80, 80, 80), scroll_rect)

    def handle_scroll(self, event):
        """Processa eventos de rolagem"""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(
                self.scroll_offset - (event.y * self.item_height),
                self.item_height * max(0, self.total_items - self.max_visible_items)
            ))

    def draw_button(self, text, rect, hover=False, active=True):
        """Draw a button with hover effect and active state"""
        color = self.BUTTON_HOVER if hover else self.BUTTON_BG
        if not active:
            color = (30, 30, 30)  # Darker color for inactive buttons
        
        # Draw button background with rounded corners
        pygame.draw.rect(self.screen, color, rect, border_radius=4)
        
        # Add subtle border
        border_color = (255, 255, 255, 30) if hover else (255, 255, 255, 15)
        pygame.draw.rect(self.screen, border_color, rect, 1, border_radius=4)
        
        # Render text
        text_color = self.TEXT_COLOR if active else (100, 100, 100)
        text_surf = self.font_small.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        
        # Add slight offset when hovering
        if hover:
            text_rect.y -= 1
            
        self.screen.blit(text_surf, text_rect)
        
        return rect.collidepoint(pygame.mouse.get_pos())
        
    def display(self):
        # Reset screen
        self.screen.fill(self.DARK_BG)
        
        # Draw heading
        title = self.font_title.render("⚠️ Erro na verificação de recursos", True, self.WARNING_COLOR)
        title_rect = title.get_rect(centerx=WIDTH//2, top=20)
        self.screen.blit(title, title_rect)
        
        # Calculate scroll area
        content_height = len(self.missing_files + self.corrupted_files) * self.item_height
        max_scroll = max(0, content_height - (HEIGTH - 200))
        
        # Draw scrollable content area
        y = 80 - self.scroll_offset
        
        # Missing files
        for file in self.missing_files:
            if 80 <= y <= HEIGTH - 100:  # Only draw visible items
                file_text = self.font_text.render(f"⚠️ {file}", True, self.WARNING_COLOR)
                file_rect = file_text.get_rect(x=30, y=y)
                self.screen.blit(file_text, file_rect)
                
                # Buttons
                repair_rect = pygame.Rect(WIDTH - 180, y, 70, 24)
                ignore_rect = pygame.Rect(WIDTH - 100, y, 70, 24)
                
                # Draw buttons with hover effect
                mouse_pos = pygame.mouse.get_pos()
                self.draw_button("Reparar", repair_rect, repair_rect.collidepoint(mouse_pos))
                self.draw_button("Ignorar", ignore_rect, ignore_rect.collidepoint(mouse_pos))
            y += self.item_height
            
        # Corrupted files
        for file in self.corrupted_files:
            if 80 <= y <= HEIGTH - 100:
                file_text = self.font_text.render(f"❌ {file}", True, self.ERROR_COLOR)
                file_rect = file_text.get_rect(x=30, y=y)
                self.screen.blit(file_text, file_rect)
                
                # Buttons
                repair_rect = pygame.Rect(WIDTH - 180, y, 70, 24)
                ignore_rect = pygame.Rect(WIDTH - 100, y, 70, 24)
                
                # Draw buttons with hover effect
                mouse_pos = pygame.mouse.get_pos()
                self.draw_button("Reparar", repair_rect, repair_rect.collidepoint(mouse_pos))
                self.draw_button("Ignorar", ignore_rect, ignore_rect.collidepoint(mouse_pos))
            y += self.item_height
            
        # Draw scrollbar if needed
        if content_height > HEIGTH - 200:
            scrollbar_height = (HEIGTH - 200) * ((HEIGTH - 200) / content_height)
            scrollbar_pos = (self.scroll_offset / max_scroll) * (HEIGTH - 200 - scrollbar_height)
            pygame.draw.rect(self.screen, (40, 40, 40), (WIDTH - 12, 80, 4, HEIGTH - 200))
            pygame.draw.rect(self.screen, (80, 80, 80), (WIDTH - 12, 80 + scrollbar_pos, 4, scrollbar_height))
        
        # Draw bottom button bar background
        pygame.draw.rect(self.screen, (25, 25, 25), (0, HEIGTH - 60, WIDTH, 60))
        
        # Bottom buttons
        verify_rect = pygame.Rect(WIDTH//2 - 270, HEIGTH - 45, 160, 30)
        export_rect = pygame.Rect(WIDTH//2 - 80, HEIGTH - 45, 160, 30)
        close_rect = pygame.Rect(WIDTH//2 + 110, HEIGTH - 45, 160, 30)
        
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button("Verificar novamente", verify_rect, verify_rect.collidepoint(mouse_pos))
        self.draw_button("Exportar relatório", export_rect, export_rect.collidepoint(mouse_pos))
        self.draw_button("Fechar", close_rect, close_rect.collidepoint(mouse_pos))
        
        pygame.display.flip()

    # ...rest of existing code...

    def handle_events(self):
        """Handle all pygame events for the interface"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.result['action'] = 'quit'
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos botões de reparo individuais
                y = 80 - self.scroll_offset
                for file in self.missing_files + self.corrupted_files:
                    if 80 <= y <= HEIGTH - 100:
                        repair_rect = pygame.Rect(WIDTH - 180, y, 70, 24)
                        ignore_rect = pygame.Rect(WIDTH - 100, y, 70, 24)
                        
                        if repair_rect.collidepoint(mouse_pos):
                            if self.repair_file(file):
                                self.result['repaired_files'].append(file)
                                if file in self.missing_files:
                                    self.missing_files.remove(file)
                                if file in self.corrupted_files:
                                    self.corrupted_files.remove(file)
                        elif ignore_rect.collidepoint(mouse_pos):
                            self.result['ignored_files'].append(file)
                            if file in self.missing_files:
                                self.missing_files.remove(file)
                            if file in self.corrupted_files:
                                self.corrupted_files.remove(file)
                    y += self.item_height
                
                # Verifica clique nos botões do rodapé
                if self.buttons['repair_all'].collidepoint(mouse_pos):
                    repaired, failed = self.repair_all()
                    self.result['repaired_files'].extend(repaired)
                    self.result['action'] = 'repair_all'
                    
                elif self.buttons['export'].collidepoint(mouse_pos):
                    success, result = self.export_report()
                    if success:
                        self.result['action'] = 'export'
                        self.result['export_file'] = result
                        
                elif self.buttons['close'].collidepoint(mouse_pos):
                    self.result['action'] = 'close'
                    return False
                    
            if event.type == pygame.MOUSEWHEEL:
                self.handle_scroll(event)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.result['action'] = 'close'
                    return False
                    
        return True

    def run(self):
        """Main loop for the error interface"""
        running = True
        while running:
            running = self.handle_events()
            self.display()
            
            # Se não houver mais arquivos com problemas, fecha a interface
            if not self.missing_files and not self.corrupted_files:
                self.result['action'] = 'complete'
                running = False
                
        return self.result

# Modificar a classe ResourceVerifier para usar o novo sistema
class ResourceVerifier:
    def __init__(self):
        self.missing = []
        self.corrupted = []
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Verificador de Recursos')

    def show_error_interface(self):
        if self.missing or self.corrupted:
            error_ui = ErrorInterface(self.screen, self.missing, self.corrupted)
            result = error_ui.run()
            
            # Processa o resultado
            if result['action'] == 'quit':
                pygame.quit()
                sys.exit()
            elif result['action'] == 'complete':
                print("\n✅ Todos os problemas foram resolvidos!")
            elif result['action'] == 'export':
                print(f"\nRelatório exportado para: {result['export_file']}")
            
            if result['repaired_files']:
                print("\nArquivos reparados:")
                for file in result['repaired_files']:
                    print(f"  ✓ {file}")
                    
            if result['ignored_files']:
                print("\nArquivos ignorados:")
                for file in result['ignored_files']:
                    print(f"  - {file}")

    def verify_file(self, category, subcategory, filename):
        """Verify if a file exists and is not corrupted"""
        filepath = get_asset_path(f"{category}/{subcategory}/{filename}")
        
        if not os.path.exists(filepath):
            self.missing.append(filepath)
            return False
            
        try:
            # Try to load the file based on its type
            if filepath.endswith(('.png', '.jpg', '.jpeg')):
                Image.open(filepath)
            elif filepath.endswith(('.wav', '.ogg')):
                pygame.mixer.Sound(filepath)
            elif filepath.endswith('.ttf'):
                pygame.font.Font(filepath)
            elif filepath.endswith('.csv'):
                with open(filepath, 'r') as f:
                    f.read()
            return True
        except Exception as e:
            self.corrupted.append(filepath)
            return False

    def verify_all(self):
        """Verify all required game resources"""
        print("\nVerificando recursos do jogo...")
        total = 0
        verified = 0

        # Check audio files
        print("\nVerificando áudios...")
        for subdir, files in REQUIRED_FILES['audio'].items():
            for f in files:
                total += 1
                if self.verify_file('audio', subdir, f):
                    verified += 1
                    print(f"✓ {subdir}/{f}")
                else:
                    print(f"✗ {subdir}/{f}")

        # Check graphic files  
        print("\nVerificando gráficos...")
        for subdir, items in REQUIRED_FILES['graphics'].items():
            if isinstance(items, dict):
                for subsubdir, files in items.items():
                    if isinstance(files, dict):
                        for subsubsubdir, subfiles in files.items():
                            for f in subfiles:
                                total += 1
                                if self.verify_file('graphics', f"{subdir}/{subsubdir}/{subsubsubdir}", f):
                                    verified += 1
                                    print(f"✓ graphics/{subdir}/{subsubdir}/{subsubsubdir}/{f}")
                                else:
                                    print(f"✗ graphics/{subdir}/{subsubdir}/{subsubsubdir}/{f}")
                    else:
                        for f in files:
                            total += 1
                            if self.verify_file('graphics', f"{subdir}/{subsubdir}", f):
                                verified += 1
                                print(f"✓ graphics/{subdir}/{subsubdir}/{f}")
                            else:
                                print(f"✗ graphics/{subdir}/{subsubdir}/{f}")
            else:
                for f in items:
                    total += 1
                    if self.verify_file('graphics', subdir, f):
                        verified += 1
                        print(f"✓ graphics/{subdir}/{f}")
                    else:
                        print(f"✗ graphics/{subdir}/{f}")

        # Check map files
        print("\nVerificando mapas...")
        for subdir, files in REQUIRED_FILES['map'].items():
            for f in files:
                total += 1
                if self.verify_file('map', subdir, f):
                    verified += 1
                    print(f"✓ map/{subdir}/{f}")
                else:
                    print(f"✗ map/{subdir}/{f}")

        # Print summary
        print(f"\nVerificação concluída: {verified}/{total} arquivos OK")
        
        if self.missing:
            print("\nArquivos ausentes:")
            for f in self.missing:
                print(f"  - {f}")
                
        if self.corrupted:
            print("\nArquivos corrompidos:")
            for f in self.corrupted:
                print(f"  - {f}")
                
        if not self.missing and not self.corrupted:
            print("\n✅ Todos os recursos necessários estão presentes e íntegros!")
        else:
            print("\n❌ Foram encontrados problemas com alguns recursos!")
            self.show_error_interface()
            
        pygame.quit()

# Fix duplicate call
if __name__ == "__main__":
    verifier = ResourceVerifier()
    verifier.verify_all()
