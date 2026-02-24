#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module du dialogue de sélection du mode de l'application ZymDeploy.
Permet de choisir entre le mode installation complète et le mode validation de plaque seule.
"""

import logging
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from zymosoft_assistant.utils.constants import COLOR_SCHEME

logger = logging.getLogger(__name__)

# Mode constants
MODE_FULL = "full"
MODE_VALIDATION_ONLY = "validation_only"


class ModeSelectionDialog(QDialog):
    """
    Dialogue de sélection du mode de fonctionnement de l'application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_mode = MODE_FULL
        self.setWindowTitle("ZymDeploy")
        
        # Configuration de la fenêtre avec tous les boutons de contrôle
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        self.setMinimumSize(800, 500)
        self.setModal(True)
        self._create_widgets()

    def _create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header section with gradient background
        header_widget = QFrame()
        header_widget.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLOR_SCHEME['primary']},
                    stop:1 #00b377);
                border: none;
            }}
        """)
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(40, 25, 40, 25)

        # Title
        title_label = QLabel("ZymDeploy")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("", 22, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent;")
        header_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Assistant de déploiement et validation")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 11pt; background: transparent;")
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_widget)

        # Content section
        content_widget = QFrame()
        content_widget.setStyleSheet("background-color: #f8f9fa; border: none;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(60, 40, 60, 40)

        # Section title
        section_title = QLabel("Que voulez-vous faire ?")
        section_title.setAlignment(Qt.AlignCenter)
        section_title.setFont(QFont("", 13, QFont.Bold))
        section_title.setStyleSheet(f"color: {COLOR_SCHEME['text']}; background: transparent;")
        content_layout.addWidget(section_title)

        # Modules cards container
        cards_container = QWidget()
        cards_container.setStyleSheet("background: transparent;")
        cards_main_layout = QHBoxLayout(cards_container)
        cards_main_layout.setContentsMargins(0, 0, 0, 0)
        cards_main_layout.addStretch()
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)
        cards_main_layout.addLayout(cards_layout)

        # Full installation mode card
        self.full_mode_card = self._create_module_card(
            "Installation Complète",
            "Processus complet de déploiement ZymoSoft incluant la saisie des informations, les vérifications préalables, la validation par acquisitions et la clôture.",
            MODE_FULL
        )
        cards_layout.addWidget(self.full_mode_card)

        # Validation-only mode card
        self.validation_mode_card = self._create_module_card(
            "Validation de Plaque",
            "Valider rapidement une plaque d'acquisition : sélection des dossiers, analyse des résultats et génération du rapport.",
            MODE_VALIDATION_ONLY
        )
        cards_layout.addWidget(self.validation_mode_card)
        
        self.validation_mode_card = self._create_module_card(
            "Validation de Plaque",
            "Valider rapidement une plaque d'acquisition : sélection des dossiers, analyse des résultats et génération du rapport.",
            MODE_VALIDATION_ONLY
        )
        cards_layout.addWidget(self.validation_mode_card)

        cards_main_layout.addStretch()
        content_layout.addWidget(cards_container)
        content_layout.addStretch()

        layout.addWidget(content_widget)

    def _create_module_card(self, title, description, mode):
        """
        Crée une carte avec titre et description.
        
        Args:
            title: Titre
            description: Description
            mode: Mode associé
        """
        card = QFrame()
        card.setFixedWidth(360)
        card.setFixedHeight(300)
        card.setCursor(Qt.PointingHandCursor)
        
        card.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {COLOR_SCHEME['border']};
                border-radius: 10px;
                background-color: white;
                padding: 0px;
            }}
            QFrame:hover {{
                border-color: {COLOR_SCHEME['primary']};
                background-color: rgba(0, 153, 103, 0.05);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(18)
        card_layout.setContentsMargins(25, 30, 25, 25)

        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("", 15, QFont.Bold))
        title_label.setWordWrap(True)
        title_label.setStyleSheet(f"color: {COLOR_SCHEME['primary']}; background: transparent; border: none;")
        card_layout.addWidget(title_label)

        # Description
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setMinimumHeight(80)
        desc_label.setStyleSheet(f"color: {COLOR_SCHEME['text_secondary']}; font-size: 10pt; background: transparent; border: none; padding: 0px 10px;")
        card_layout.addWidget(desc_label)

        card_layout.addStretch()

        # Action button
        select_button = QPushButton("Sélectionner")
        select_button.setCursor(Qt.PointingHandCursor)
        select_button.setFixedHeight(42)
        select_button.setFont(QFont("", 11, QFont.Bold))
        select_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_SCHEME['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_SCHEME['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_SCHEME['primary_pressed']};
            }}
        """)
        
        select_button.clicked.connect(lambda: self._select_mode(mode))
        card_layout.addWidget(select_button)

        # Make the whole card clickable
        card.mousePressEvent = lambda event: self._select_mode(mode)
        
        return card

    def _select_mode(self, mode):
        """
        Sélectionne le mode et ferme le dialogue.
        """
        self.selected_mode = mode
        logger.info(f"Mode sélectionné : {mode}")
        self.accept()
