"""
J.A.R.V.I.S v9.0 — Project Generator
Run this script to create the complete project structure.
Usage: python setup_jarvis.py
"""
import os
import sys

BASE = "jarvis_native"

FILES = {}

# ════════════════════════════════════════════════════════════════════
# ROOT FILES
# ════════════════════════════════════════════════════════════════════

FILES["main.py"] = '''"""J.A.R.V.I.S v9.0 — Main Entry Point"""
import flet as ft
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app.theme import COLORS
from app.views.chat_view import ChatView
from app.views.settings_view import SettingsView
from app.views.router_view import RouterView
from app.views.memory_view import MemoryView
from app.views.evolution_view import EvolutionView
from app.views.plugins_view import PluginsView
from core.jarvis_core import JarvisCore


class JarvisApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.core = JarvisCore(BASE_DIR)
        self.current_view = "chat"
        self._setup_page()
        self._build_ui()

    def _setup_page(self):
        self.page.title = "J.A.R.V.I.S v9.0"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = COLORS["bg_primary"]
        self.page.padding = 0
        self.page.spacing = 0
        self.page.theme = ft.Theme(color_scheme_seed="#00d4ff")
        try:
            self.page.window_width = 1200
            self.page.window_height = 800
            self.page.window_min_width = 900
            self.page.window_min_height = 650
        except AttributeError:
            pass

    def _build_ui(self):
        self.content_area = ft.Container(expand=True, bgcolor=COLORS["bg_primary"], padding=0)

        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=90,
            bgcolor=COLORS["bg_secondary"],
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.CHAT_BUBBLE_OUTLINED, selected_icon=ft.Icons.CHAT_BUBBLE, label="Chat"),
                ft.NavigationRailDestination(icon=ft.Icons.ROUTER_OUTLINED, selected_icon=ft.Icons.ROUTER, label="Router"),
                ft.NavigationRailDestination(icon=ft.Icons.MEMORY_OUTLINED, selected_icon=ft.Icons.MEMORY, label="Memory"),
                ft.NavigationRailDestination(icon=ft.Icons.AUTO_FIX_HIGH_OUTLINED, selected_icon=ft.Icons.AUTO_FIX_HIGH, label="Evolution"),
                ft.NavigationRailDestination(icon=ft.Icons.EXTENSION_OUTLINED, selected_icon=ft.Icons.EXTENSION, label="Plugins"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
            ],
            on_change=self._on_nav_change
        )

        brain_status = "Online" if self.core.brain else "Offline"
        status_color = COLORS["success"] if self.core.brain else COLORS["error"]

        status_bar = ft.Container(
            height=32,
            bgcolor=COLORS["bg_secondary"],
            padding=ft.padding.only(left=16, right=16),
            content=ft.Row(
                controls=[
                    ft.Text("J.A.R.V.I.S v9.0", size=11, color=COLORS["text_secondary"], weight=ft.FontWeight.W_500),
                    ft.Container(expand=True),
                    ft.Icon(ft.Icons.CIRCLE, size=8, color=status_color),
                    ft.Text(f"Brain: {brain_status}", size=11, color=COLORS["text_secondary"]),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            )
        )

        self.page.add(
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Row(expand=True, spacing=0, controls=[
                        self.nav_rail,
                        ft.VerticalDivider(width=1, color=COLORS["border"], thickness=1),
                        self.content_area
                    ]),
                    status_bar
                ]
            )
        )
        self._show_view("chat")

    def _on_nav_change(self, e):
        views = ["chat", "router", "memory", "evolution", "plugins", "settings"]
        if 0 <= e.control.selected_index < len(views):
            self._show_view(views[e.control.selected_index])

    def _show_view(self, name):
        self.current_view = name
        try:
            if name == "chat": view = ChatView(self)
            elif name == "router": view = RouterView(self)
            elif name == "memory": view = MemoryView(self)
            elif name == "evolution": view = EvolutionView(self)
            elif name == "plugins": view = PluginsView(self)
            elif name == "settings": view = SettingsView(self)
            else: view = ChatView(self)
            self.content_area.content = view.build()
            self.page.update()
        except Exception as e:
            print(f"View error ({name}): {e}")

    def show_snackbar(self, message, color=None):
        try:
            self.page.open(ft.SnackBar(
                content=ft.Text(message, color=COLORS["text_primary"]),
                bgcolor=color or COLORS["accent"],
                duration=2500
            ))
        except Exception:
            pass


def main(page: ft.Page):
    JarvisApp(page)


if __name__ == "__main__":
    ft.app(target=main)
'''

FILES["config.json"] = '''{
  "app_name": "J.A.R.V.I.S",
  "version": "9.0.0",
  "brain_backend": "ollama",
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.1",
  "max_history": 16,
  "reflection_enabled": true,
  "hitl_enabled": true
}'''

FILES["requirements.txt"] = '''# Core UI
flet>=0.21.0
requests>=2.31.0
chromadb>=0.4.0
keyboard>=0.13.5

# API Server
fastapi>=0.109.0
uvicorn[standard]>=0.27.0

# Advanced Features
networkx>=3.0
cryptography>=42.0.0

# Voice (optional)
pvporcupine>=3.0.0
sounddevice>=0.4.6

# Bots (optional)
discord.py>=2.3.0
slack-bolt>=1.18.0

# IoT (optional)
paho-mqtt>=1.6.0
'''

FILES["README.md"] = '''# 🤖 J.A.R.V.I.S v9.0 — Complete AIOS

A cross-platform AI Operating System with 30+ modules.

## Features
- 🧠 Multi-Brain Router with 6 specialist roles
- 🌳 Tree of Thoughts reasoning
- 🧬 Self-Evolution engine
- 🕸️ Knowledge Graph with temporal reasoning
- 🔌 Plugin system
- 🏠 IoT Bridge (Home Assistant + MQTT)
- 🔒 Encrypted memory + Docker sandbox
- 🔄 Multi-device sync
- 🎤 Wake word detection
- 💬 Discord + Slack bots
- 🌐 Browser extension
- 📱 Native apps (Windows/Linux/Android)

## Quick Start
