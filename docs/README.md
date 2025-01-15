<img src='https://github.com/user-attachments/assets/fdef5933-fd25-4bd2-ac0e-b69d583f7ddf'>

<div align="center">
  <h1><strong>🎮RPG Eldoria🎮</strong></h1>

  
</div>
<br>
<img src='https://github.com/user-attachments/assets/29986fe7-23d2-4662-bc62-96244db0e1c7'>

---

## 🛠️ Tecnologias Utilizadas

<ul>
    <li><strong>Python</strong> 🐍</li>
    <li><strong>PyGame</strong> 🎮</li>
</ul>

<br>
<hr>


## 🖥️ Como Instalar e Rodar

Para jogar **Eldoria** no seu computador, siga os passos abaixo:

### 1. Clone o repositório

```bash
git clone https://github.com/GabrielNat1/RPG-Eldoria.git
```

2. Navegue até o diretório do projeto
```bash 
cd {rpgeldoria/code}
```


3. Instale as dependências
```bash
Certifique-se de ter o Pygame instalado:
python -m pip install pygame
```



4. Execute o jogo
Execute o jogo com o seguinte comando:

```bash
python main.py
```

---

## 🚀 Como Jogar

### 🏃‍♂️ Movimentação

- **W**, **A**, **S**, **D** ou as **Setas Direcionais**: Movimenta o personagem no mapa.

### ⚔️ Combate

- **Espaço**: Atacar inimigos.
- **Ctrl**: Habilidades especiais (quando disponível).
- **Q** ou **E**: Trocar itens.

---

## 📂 Estrutura de Diretórios  

A estrutura de diretórios do projeto é organizada da seguinte forma:

```bash
RPG-ELDORIA/  
├── assets/  
│   ├── audio/                   # Arquivos de áudio do jogo  
│   │   ├── attack/              # Sons de ataque  
│   │   ├── death.wav            # Som de morte  
│   │   ├── Fire.wav             # Som de fogo  
│   │   ├── heal.wav             # Som de cura  
│   │   ├── hit.wav              # Som de impacto  
│   │   ├── main_menu.wav        # Música do menu principal  
│   │   ├── main.wav             # Música principal do jogo  
│   │   └── sword.wav            # Som de espada  
│   ├── code/                    # Scripts e código do jogo  
│   ├── docs/                    # Documentação do projeto  
│   ├── graphics/                # Recursos visuais do jogo  
│   │   ├── font/                # Fontes usadas no jogo  
│   │   ├── grass/               # Imagens de grama  
│   │   ├── icon/                # Ícones do jogo  
│   │   ├── monsters/            # Sprites de monstros  
│   │   ├── movies/              # Vídeos e cutscenes  
│   │   ├── objects/             # Objetos interativos do jogo  
│   │   ├── particles/           # Efeitos de partículas  
│   │   ├── player/              # Sprites do personagem principal  
│   │   ├── test/                # Recursos de teste para desenvolvimento  
│   │   ├── tilemap/             # Mapas e tilesets do jogo  
│   │   └── weapons/             # Sprites de armas  
├── map/                         # Arquivos relacionados aos mapas do jogo  
├── requirements.txt             # Dependências do projeto  
```

---

## 🌍 Sistema de Renderização por Chunks  

O projeto utiliza um **sistema de renderização por chunks** para otimizar o desempenho, evitando sobrecarregar a aplicação e economizando memória durante a execução.  

### 🔧 Como Funciona  
- O mapa do jogo é dividido em **pequenas regiões chamadas chunks**, que são carregadas e renderizadas dinamicamente com base na posição do jogador.  
- Apenas os chunks próximos ao jogador são carregados na memória, enquanto os demais são descarregados ou mantidos em um estado de baixa prioridade.  

### 🛠️ Benefícios  
- **Desempenho Aprimorado:** Reduz o uso de recursos do sistema, garantindo uma experiência mais fluida.  
- **Gerenciamento de Memória:** Apenas o necessário é mantido na memória, permitindo que o jogo rode em dispositivos com especificações limitadas.  
- **Escalabilidade:** Suporte para mapas maiores sem impactar negativamente o desempenho.  

<br>

---

🏆 Créditos
Desenvolvedores:

```bash
GabrielNat1

ClearCode

Pack:NinjaAdventurePack
```

---

<img src='https://github.com/user-attachments/assets/fdef5933-fd25-4bd2-ac0e-b69d583f7ddf'>
