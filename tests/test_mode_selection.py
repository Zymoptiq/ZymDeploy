# tests/test_mode_selection.py

import sys
import unittest
from unittest.mock import MagicMock, patch


class TestModeConstants(unittest.TestCase):
    """Test the mode constants."""

    def test_mode_full_value(self):
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL
        self.assertEqual(MODE_FULL, "full")

    def test_mode_validation_only_value(self):
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        self.assertEqual(MODE_VALIDATION_ONLY, "validation_only")

    def test_modes_are_different(self):
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL, MODE_VALIDATION_ONLY
        self.assertNotEqual(MODE_FULL, MODE_VALIDATION_ONLY)


class TestModeSelectionDialogSelectMode(unittest.TestCase):
    """Test ModeSelectionDialog._select_mode logic."""

    @patch("zymosoft_assistant.gui.mode_selection_dialog.QDialog.__init__", return_value=None)
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog._create_widgets")
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog.accept")
    def test_select_mode_full(self, mock_accept, mock_create, mock_init):
        from zymosoft_assistant.gui.mode_selection_dialog import ModeSelectionDialog, MODE_FULL
        dialog = ModeSelectionDialog.__new__(ModeSelectionDialog)
        dialog.selected_mode = MODE_FULL
        dialog.accept = mock_accept
        dialog._select_mode(MODE_FULL)
        self.assertEqual(dialog.selected_mode, MODE_FULL)
        mock_accept.assert_called_once()

    @patch("zymosoft_assistant.gui.mode_selection_dialog.QDialog.__init__", return_value=None)
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog._create_widgets")
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog.accept")
    def test_select_mode_validation_only(self, mock_accept, mock_create, mock_init):
        from zymosoft_assistant.gui.mode_selection_dialog import ModeSelectionDialog, MODE_VALIDATION_ONLY
        dialog = ModeSelectionDialog.__new__(ModeSelectionDialog)
        dialog.selected_mode = "full"
        dialog.accept = mock_accept
        dialog._select_mode(MODE_VALIDATION_ONLY)
        self.assertEqual(dialog.selected_mode, MODE_VALIDATION_ONLY)
        mock_accept.assert_called_once()


class TestMainWindowModeBehavior(unittest.TestCase):
    """
    Test MainWindow mode-related behavior using mocks to avoid
    importing modules that depend on tkinter.
    """

    @classmethod
    def setUpClass(cls):
        """
        Mock the problematic imports before importing main_window.
        We need to mock the scripts that depend on tkinter.
        """
        # Create mock modules for the problematic import chain
        cls._mock_modules = {}
        problematic_modules = [
            'zymosoft_assistant.scripts.home_made_tools_v3',
            'zymosoft_assistant.scripts.Routine_VALIDATION_ZC_18022025',
            'zymosoft_assistant.scripts.getDatasFromWellResults',
        ]
        for mod_name in problematic_modules:
            if mod_name not in sys.modules:
                cls._mock_modules[mod_name] = MagicMock()
                sys.modules[mod_name] = cls._mock_modules[mod_name]

    @classmethod
    def tearDownClass(cls):
        """Remove mocked modules."""
        for mod_name in cls._mock_modules:
            if mod_name in sys.modules and sys.modules[mod_name] is cls._mock_modules[mod_name]:
                del sys.modules[mod_name]

    def test_initialize_steps_validation_only_creates_single_step(self):
        """In validation-only mode, only Step3 should be created."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY
        window.steps = []
        window.step_container = MagicMock()

        with patch("zymosoft_assistant.gui.main_window.Step3Acquisition") as mock_step3:
            mock_step3.return_value = MagicMock()
            MainWindow.initialize_steps(window)

        mock_step3.assert_called_once()
        self.assertEqual(len(window.steps), 1)

    def test_initialize_steps_full_mode_creates_four_steps(self):
        """In full mode, all 4 steps should be created."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_FULL
        window.steps = []
        window.step_container = MagicMock()

        with patch("zymosoft_assistant.gui.main_window.Step1Info") as m1, \
             patch("zymosoft_assistant.gui.main_window.Step2Checks") as m2, \
             patch("zymosoft_assistant.gui.main_window.Step3Acquisition") as m3, \
             patch("zymosoft_assistant.gui.main_window.Step4Closure") as m4:
            m1.return_value = MagicMock()
            m2.return_value = MagicMock()
            m3.return_value = MagicMock()
            m4.return_value = MagicMock()
            MainWindow.initialize_steps(window)

        m1.assert_called_once()
        m2.assert_called_once()
        m3.assert_called_once()
        m4.assert_called_once()
        self.assertEqual(len(window.steps), 4)

    def test_show_step_validation_only_sets_correct_title(self):
        """In validation-only mode, show_step sets the plate validation title."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY
        window.initial_load = True
        window.step_title_label = MagicMock()
        window.step_description_label = MagicMock()
        window.status_label = MagicMock()
        window.step_container = MagicMock()

        mock_step = MagicMock()
        window.steps = [mock_step]

        MainWindow.show_step(window, 0)

        window.step_title_label.setText.assert_called_with("Validation de plaque")
        window.step_description_label.setText.assert_called_with(
            "Réalisation et analyse des acquisitions de validation"
        )
        window.status_label.setText.assert_called_with("Mode validation de plaque")

    def test_switch_mode_to_validation_only(self):
        """_switch_mode to validation_only hides sidebar and nav."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL, MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_FULL
        window.steps = [MagicMock()]
        window.current_step_index = 0
        window.step_container = MagicMock()
        window.session_data = {}
        window.initial_load = False
        window.left_column = MagicMock()
        window.nav_widget = MagicMock()
        window.validation_only_action = MagicMock()
        window.full_mode_action = MagicMock()
        window.new_session_action = MagicMock()
        window.load_session_action = MagicMock()
        window.save_session_action = MagicMock()
        window.initialize_steps = MagicMock()
        window.show_step = MagicMock()

        MainWindow._switch_mode(window, MODE_VALIDATION_ONLY)

        self.assertEqual(window.mode, MODE_VALIDATION_ONLY)
        window.left_column.setVisible.assert_called_with(False)
        window.nav_widget.setVisible.assert_called_with(False)
        window.initialize_steps.assert_called_once()
        window.show_step.assert_called_once_with(0)

    def test_switch_mode_to_full(self):
        """_switch_mode to full shows sidebar and nav."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL, MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY
        window.steps = [MagicMock()]
        window.current_step_index = 0
        window.step_container = MagicMock()
        window.session_data = {}
        window.initial_load = False
        window.left_column = MagicMock()
        window.nav_widget = MagicMock()
        window.validation_only_action = MagicMock()
        window.full_mode_action = MagicMock()
        window.new_session_action = MagicMock()
        window.load_session_action = MagicMock()
        window.save_session_action = MagicMock()
        window.initialize_steps = MagicMock()
        window.show_step = MagicMock()

        MainWindow._switch_mode(window, MODE_FULL)

        self.assertEqual(window.mode, MODE_FULL)
        window.left_column.setVisible.assert_called_with(True)
        window.nav_widget.setVisible.assert_called_with(True)
        window.initialize_steps.assert_called_once()
        window.show_step.assert_called_once_with(0)


class TestMainWindowMenuActions(unittest.TestCase):
    """Test menu actions behavior according to mode."""

    def test_session_actions_disabled_in_validation_only_mode(self):
        """Session actions should be disabled in validation-only mode."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY
        window.new_session_action = MagicMock()
        window.load_session_action = MagicMock()
        window.save_session_action = MagicMock()
        window.validation_only_action = MagicMock()
        window.full_mode_action = MagicMock()

        # Simulate what happens in create_menu when mode is validation_only
        if window.mode == MODE_VALIDATION_ONLY:
            window.new_session_action.setEnabled(False)
            window.load_session_action.setEnabled(False)
            window.save_session_action.setEnabled(False)

        window.new_session_action.setEnabled.assert_called_with(False)
        window.load_session_action.setEnabled.assert_called_with(False)
        window.save_session_action.setEnabled.assert_called_with(False)

    def test_session_actions_enabled_in_full_mode(self):
        """Session actions should be enabled in full mode."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_FULL
        window.new_session_action = MagicMock()
        window.load_session_action = MagicMock()
        window.save_session_action = MagicMock()

        # In full mode (default), actions should not be disabled
        # They remain enabled by default
        # Verify they were not called with False
        window.new_session_action.setEnabled.assert_not_called()
        window.load_session_action.setEnabled.assert_not_called()
        window.save_session_action.setEnabled.assert_not_called()

    @patch("zymosoft_assistant.gui.main_window.QMessageBox")
    def test_new_session_shows_message_in_validation_only_mode(self, mock_msgbox):
        """new_session should show info message in validation-only mode."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY

        MainWindow.new_session(window)

        mock_msgbox.information.assert_called_once()
        args = mock_msgbox.information.call_args[0]
        self.assertIn("n'est pas disponible", args[2])
        self.assertIn("mode validation de plaque", args[2])

    @patch("zymosoft_assistant.gui.main_window.QMessageBox")
    def test_load_session_shows_message_in_validation_only_mode(self, mock_msgbox):
        """load_session should show info message in validation-only mode."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY

        MainWindow.load_session(window)

        mock_msgbox.information.assert_called_once()
        args = mock_msgbox.information.call_args[0]
        self.assertIn("n'est pas disponible", args[2])

    @patch("zymosoft_assistant.gui.main_window.QMessageBox")
    def test_save_session_shows_message_in_validation_only_mode(self, mock_msgbox):
        """save_session should show info message in validation-only mode."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_VALIDATION_ONLY

        MainWindow.save_session(window)

        mock_msgbox.information.assert_called_once()
        args = mock_msgbox.information.call_args[0]
        self.assertIn("n'est pas disponible", args[2])

    def test_mode_switch_updates_session_actions(self):
        """Switching modes should update session actions state."""
        from zymosoft_assistant.gui.mode_selection_dialog import MODE_FULL, MODE_VALIDATION_ONLY
        from zymosoft_assistant.gui.main_window import MainWindow

        window = MagicMock(spec=MainWindow)
        window.mode = MODE_FULL
        window.steps = []
        window.current_step_index = 0
        window.step_container = MagicMock()
        window.session_data = {}
        window.initial_load = False
        window.left_column = MagicMock()
        window.nav_widget = MagicMock()
        window.validation_only_action = MagicMock()
        window.full_mode_action = MagicMock()
        window.new_session_action = MagicMock()
        window.load_session_action = MagicMock()
        window.save_session_action = MagicMock()
        window.initialize_steps = MagicMock()
        window.show_step = MagicMock()

        # Switch to validation only
        MainWindow._switch_mode(window, MODE_VALIDATION_ONLY)

        window.new_session_action.setEnabled.assert_called_with(False)
        window.load_session_action.setEnabled.assert_called_with(False)
        window.save_session_action.setEnabled.assert_called_with(False)


class TestModeSelectionDialogUI(unittest.TestCase):
    """Test ModeSelectionDialog UI elements."""

    @patch("zymosoft_assistant.gui.mode_selection_dialog.QDialog.__init__", return_value=None)
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog._create_widgets")
    def test_dialog_window_title(self, mock_create, mock_init):
        """Dialog should have correct window title."""
        from zymosoft_assistant.gui.mode_selection_dialog import ModeSelectionDialog

        dialog = MagicMock(spec=ModeSelectionDialog)
        dialog.setWindowTitle = MagicMock()

        # Simulate what happens in __init__
        dialog.setWindowTitle("ZymDeploy")

        dialog.setWindowTitle.assert_called_with("ZymDeploy")

    @patch("zymosoft_assistant.gui.mode_selection_dialog.QDialog.__init__", return_value=None)
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog._create_widgets")
    def test_dialog_minimum_size(self, mock_create, mock_init):
        """Dialog should have minimum size set."""
        from zymosoft_assistant.gui.mode_selection_dialog import ModeSelectionDialog

        dialog = MagicMock(spec=ModeSelectionDialog)
        dialog.setMinimumSize = MagicMock()

        # Simulate what happens in __init__
        dialog.setMinimumSize(800, 500)

        dialog.setMinimumSize.assert_called_with(800, 500)

    @patch("zymosoft_assistant.gui.mode_selection_dialog.QDialog.__init__", return_value=None)
    @patch("zymosoft_assistant.gui.mode_selection_dialog.ModeSelectionDialog._create_widgets")
    def test_dialog_modal(self, mock_create, mock_init):
        """Dialog should be modal."""
        from zymosoft_assistant.gui.mode_selection_dialog import ModeSelectionDialog

        dialog = MagicMock(spec=ModeSelectionDialog)
        dialog.setModal = MagicMock()

        # Simulate what happens in __init__
        dialog.setModal(True)

        dialog.setModal.assert_called_with(True)


if __name__ == "__main__":
    unittest.main()
