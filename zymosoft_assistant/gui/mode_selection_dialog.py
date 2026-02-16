#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module du dialogue de sélection du mode de l'application ZymDeploy.
Permet de choisir entre le mode installation complète et le mode validation de plaque seule.
"""

import logging
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame)
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
        self.setWindowTitle("ZymDeploy - Sélection du mode")
        self.setFixedSize(520, 340)
        self.setModal(True)
        self._create_widgets()

    def _create_widgets(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Bienvenue dans ZymDeploy")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("", 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLOR_SCHEME['primary']};")
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Sélectionnez le mode de fonctionnement :")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"color: {COLOR_SCHEME['text_secondary']}; font-size: 10pt;")
        layout.addWidget(subtitle_label)

        layout.addSpacing(10)

        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Full installation mode button
        self.full_mode_button = self._create_mode_button(
            "Installation complète",
            "Assistant complet avec toutes les étapes\n(informations client, vérifications,\nvalidation, clôture)",
            MODE_FULL
        )
        buttons_layout.addWidget(self.full_mode_button)

        # Validation-only mode button
        self.validation_mode_button = self._create_mode_button(
            "Validation de plaque",
            "Accès direct au module de validation\ndes plaques (sélection, analyse\net rapport)",
            MODE_VALIDATION_ONLY
        )
        buttons_layout.addWidget(self.validation_mode_button)

        layout.addLayout(buttons_layout)

    def _create_mode_button(self, title, description, mode):
        """
        Crée un bouton de sélection de mode avec titre et description.
        """
        button = QPushButton()
        button.setMinimumHeight(140)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {COLOR_SCHEME['border']};
                border-radius: 10px;
                padding: 15px;
                background-color: white;
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {COLOR_SCHEME['primary']};
                background-color: rgba(0, 153, 103, 0.05);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 153, 103, 0.1);
            }}
        """)

        # Use a layout inside the button via a frame
        btn_layout = QVBoxLayout(button)
        btn_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {COLOR_SCHEME['primary']}; background: transparent;")
        title_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        btn_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"color: {COLOR_SCHEME['text_secondary']}; font-size: 9pt; background: transparent;")
        desc_label.setWordWrap(True)
        desc_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        btn_layout.addWidget(desc_label)

        button.clicked.connect(lambda: self._select_mode(mode))
        return button

    def _select_mode(self, mode):
        """
        Sélectionne le mode et ferme le dialogue.
        """
        self.selected_mode = mode
        logger.info(f"Mode sélectionné : {mode}")
        self.accept()
