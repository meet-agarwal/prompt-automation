# userInterface.py (improved version)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QMessageBox, QScrollArea,
    QFrame, QGridLayout, QSizePolicy, QSpacerItem,
    QGroupBox, QStackedWidget, QTextEdit, QButtonGroup
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QFontDatabase, QPalette, QColor, QPainter, QBrush, QLinearGradient

class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame#card {
                background: transparent;
                border-radius: 8px;
                border: 1px solid #E0E6ED;
                margin: 5px;
            }
            QFrame#card:hover {
                border: 1px solid #3498DB;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

class ModernButton(QPushButton):
    def __init__(self, text, primary=False, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.primary = primary
        self.setMinimumHeight(40)
        
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 6px;
                    font-weight: bold;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
                QPushButton:pressed {
                    background-color: #21618C;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ECF0F1;
                    color: #2C3E50;
                    padding: 8px 16px;
                    border-radius: 4px;
                    border: 1px solid #BDC3C7;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #D5DBDB;
                }
                QPushButton:pressed {
                    background-color: #AEB6BF;
                }
            """)

class StyleCard(QFrame):
    selected = pyqtSignal(str, str)  # section, style_key
    
    def __init__(self, section, style_key, style_desc, parent=None):
        super().__init__(parent)
        self.section = section
        self.style_key = style_key
        self.is_selected = False
        
        self.setObjectName("styleCard")
        self.setFrameStyle(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Style name
        self.name_label = QLabel(f"Style: {style_key.upper()}")
        self.name_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Description
        self.desc_label = QLabel(style_desc)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("""
            QLabel {
                color: #5D6D7E;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        
        # Selection indicator
        self.indicator = QLabel("✓ Selected")
        self.indicator.setStyleSheet("""
            QLabel {
                color: #27AE60;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        self.indicator.hide()
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.desc_label)
        layout.addWidget(self.indicator, 0, Qt.AlignRight)
        
        self.update_style()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected.emit(self.section, self.style_key)
    
    def set_selected(self, selected):
        self.is_selected = selected
        self.indicator.setVisible(selected)
        self.update_style()
    
    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                QFrame#styleCard {
                    background: #EBF5FF;
                    border: 2px solid #3498DB;
                    border-radius: 8px;
                    margin: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#styleCard {
                    background: transparent;
                    border: 1px solid #E0E6ED;
                    border-radius: 8px;
                    margin: 5px;
                }
                QFrame#styleCard:hover {
                    border: 1px solid #3498DB;
                    background: rgba(52, 152, 219, 0.05);
                }
            """)

class TabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        
    def update_style(self, is_active):
        if is_active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    border-bottom: 3px solid #2980B9;
                    font-weight: bold;
                    font-size: 13px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #7F8C8D;
                    padding: 10px 20px;
                    border: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    border-bottom: 3px solid transparent;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #F8F9FA;
                    color: #2C3E50;
                }
            """)

class PRDGeneratorUI(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("PRD Generator for Ecommerce")
        self.config = config
        self.current_section = None
        self.style_cards = {}  # section -> {style_key: card}
        self.selected_styles = {}  # section -> style_key
        self.tab_buttons = {}
        self._init_ui()
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Initialize first section
        sections = list(self.config.keys())
        if sections:
            self.show_section(sections[0])

    def _init_ui(self):
        # Set application font
        font = QFont("Segoe UI", 9) if "Segoe UI" in QFontDatabase().families() else QFont("Arial", 9)
        self.setFont(font)
        
        # Set window background
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
            }
        """)

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar
        self.create_sidebar(main_layout)
        
        # Create main content area
        self.create_content_area(main_layout)

    def create_sidebar(self, main_layout):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #34495E;
                border: none;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(25, 30, 25, 30)
        sidebar_layout.setSpacing(25)

        # Header
        header = QLabel("PRD Generator")
        header.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 15px;
                border-bottom: 2px solid rgba(255,255,255,0.2);
                background-color: transparent;
            }
        """)
        sidebar_layout.addWidget(header)

        # Description
        desc = QLabel("Create professional product requirement documents for eBay and Etsy by selecting templates for each section.")
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            QLabel {
                color: #BDC3C7;
                font-size: 13px;
                line-height: 1.5;
                background-color: transparent;
            }
        """)
        sidebar_layout.addWidget(desc)

        # Progress section
        progress_label = QLabel("Progress")
        progress_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                background-color: transparent;
            }
        """)
        sidebar_layout.addWidget(progress_label)

        # Progress list
        self.progress_widget = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_widget)
        self.progress_layout.setContentsMargins(0, 10, 0, 0)
        self.progress_layout.setSpacing(8)
        
        for section in self.config.keys():
            progress_item = QLabel(f"• {section.capitalize()}")
            progress_item.setObjectName(f"progress_{section}")
            progress_item.setStyleSheet("""
                QLabel {
                    color: #95A5A6;
                    font-size: 12px;
                    padding: 2px 0;
                    background-color: transparent;
                }
            """)
            self.progress_layout.addWidget(progress_item)
        
        sidebar_layout.addWidget(self.progress_widget)
        sidebar_layout.addStretch()

        # Generate button
        self.generate_btn = ModernButton("Generate PRD", primary=True)
        self.generate_btn.clicked.connect(self.on_generate)
        sidebar_layout.addWidget(self.generate_btn)

        main_layout.addWidget(sidebar)

    def create_content_area(self, main_layout):
        content_area = QFrame()
        content_area.setStyleSheet("""
            QFrame {
                background-color: white;
                border: none;
            }
        """)
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header area
        header_area = QFrame()
        header_area.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #E0E6ED;
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_area)
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(15)

        # Title
        title = QLabel("Customize Your Product Page")
        title.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(title)

        # Tab navigation
        self.create_tab_navigation(header_layout)
        content_layout.addWidget(header_area)

        # Main content with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F8F9FA;
            }
        """)

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)

        scroll_area.setWidget(self.content_widget)
        content_layout.addWidget(scroll_area)

        main_layout.addWidget(content_area)

    def create_tab_navigation(self, parent_layout):
        tab_container = QFrame()
        tab_layout = QHBoxLayout(tab_container)
        tab_layout.setContentsMargins(0, 10, 0, 0)
        tab_layout.setSpacing(0)

        self.tab_group = QButtonGroup()
        
        for i, section in enumerate(self.config.keys()):
            tab_btn = TabButton(section.capitalize())
            tab_btn.clicked.connect(lambda checked, s=section: self.show_section(s))
            
            self.tab_buttons[section] = tab_btn
            self.tab_group.addButton(tab_btn)
            tab_layout.addWidget(tab_btn)
        
        tab_layout.addStretch()
        parent_layout.addWidget(tab_container)

    def show_section(self, section):
        if section == self.current_section:
            return
            
        self.current_section = section
        
        # Update tab buttons
        for sec, btn in self.tab_buttons.items():
            btn.setChecked(sec == section)
            btn.update_style(sec == section)
        
        # Clear current content
        self.clear_content()
        
        # Show section content
        self.show_section_content(section)
        
        # Update progress
        self.update_progress()

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_section_content(self, section):
        # Section description
        desc = QLabel(f"Select a template style for the {section} section:")
        desc.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #5D6D7E;
                font-size: 16px;
                margin-bottom: 10px;
            }
        """)
        self.content_layout.addWidget(desc)

        # Style cards container
        styles_container = QWidget()
        styles_layout = QVBoxLayout(styles_container)
        styles_layout.setSpacing(15)
        styles_layout.setContentsMargins(0, 0, 0, 0)
        
        if section not in self.style_cards:
            self.style_cards[section] = {}
        
        styles = self.config[section]
        for style_key, style_desc in styles.items():
            card = StyleCard(section, style_key, style_desc)
            card.selected.connect(self.on_style_selected)
            
            # Check if this style is already selected
            if section in self.selected_styles and self.selected_styles[section] == style_key:
                card.set_selected(True)
            
            self.style_cards[section][style_key] = card
            styles_layout.addWidget(card)
        
        self.content_layout.addWidget(styles_container)
        self.content_layout.addStretch()

    def on_style_selected(self, section, style_key):
        # Update selection
        self.selected_styles[section] = style_key
        
        # Update visual state of cards
        if section in self.style_cards:
            for key, card in self.style_cards[section].items():
                card.set_selected(key == style_key)
        
        # Update progress
        self.update_progress()

    def update_progress(self):
        for section in self.config.keys():
            progress_item = self.progress_widget.findChild(QLabel, f"progress_{section}")
            if progress_item:
                if section in self.selected_styles:
                    progress_item.setStyleSheet("""
                        QLabel {
                            color: #27AE60;
                            font-size: 12px;
                            font-weight: bold;
                            padding: 2px 0;
                            background-color: transparent;
                        }
                    """)
                    progress_item.setText(f"✓ {section.capitalize()}")
                else:
                    progress_item.setStyleSheet("""
                        QLabel {
                            color: #95A5A6;
                            font-size: 12px;
                            padding: 2px 0;
                            background-color: transparent;
                        }
                    """)
                    progress_item.setText(f"• {section.capitalize()}")

    def on_generate(self):
        if len(self.selected_styles) != len(self.config):
            missing = set(self.config.keys()) - set(self.selected_styles.keys())
            QMessageBox.warning(
                self, 
                "Incomplete Selection", 
                f"Please select styles for: {', '.join(missing)}"
            )
            return
        
        # Create detailed summary
        summary = "<div style='font-family: Arial, sans-serif;'>"
        summary += "<h2 style='color: #2C3E50; margin-bottom: 20px;'>PRD Configuration Summary</h2>"
        summary += "<table style='border-collapse: collapse; width: 100%; border: 1px solid #ddd;'>"
        summary += "<thead><tr style='background-color: #3498DB; color: white;'>"
        summary += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Section</th>"
        summary += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Selected Style</th>"
        summary += "<th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>Description</th>"
        summary += "</tr></thead><tbody>"
        
        for section, style_key in self.selected_styles.items():
            style_desc = self.config[section][style_key]
            summary += f"<tr style='border-bottom: 1px solid #ddd;'>"
            summary += f"<td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>{section.capitalize()}</td>"
            summary += f"<td style='padding: 10px; border: 1px solid #ddd; color: #3498DB;'>{style_key.upper()}</td>"
            summary += f"<td style='padding: 10px; border: 1px solid #ddd;'>{style_desc}</td>"
            summary += "</tr>"
        
        summary += "</tbody></table></div>"
        
        msg = QMessageBox(self)
        msg.setWindowTitle("PRD Generation Complete")
        msg.setTextFormat(Qt.RichText)
        msg.setText(summary)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setFixedSize(700, 400)
        msg.exec_()