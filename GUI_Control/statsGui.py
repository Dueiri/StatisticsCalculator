#statsGui.py
#handles the GUI for the statistics helper application
#Written by David Dueiri
# 7/9/2025

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QFormLayout,
    QSpinBox,
    QDialog,
    QTabWidget,
)
from GUI_Control.controller import controller

class ExtraStatsDialog(QDialog, controller):
    def __init__(self, helper, parent=None):
        super().__init__(parent)
        self.helper = helper
        self.setWindowTitle("Extra Statistics")
        self.resize(500, 400)

        # create the main layout and tabs
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.freq_tab = QWidget()
        self.stemleaf_tab = QWidget()

        # Frequency Distribution Tab
        freq_layout = QFormLayout()
        self.freq_input = QLineEdit()
        self.freq_input.setPlaceholderText("Enter numbers and tokenize them")
        freq_layout.addRow("Dataset:", self.freq_input)

        # Tokenizer type dropdown
        self.tokenizer_type_combo = QComboBox()
        self.tokenizer_type_combo.addItems(
            ["Both (Default)", "Alphabetical Data", "Numerical Data"]
        )
        freq_layout.addRow("Tokenization Type:", self.tokenizer_type_combo)

        # Tokenize button
        self.tokenize_btn = QPushButton("Tokenize")
        self.tokenize_btn.clicked.connect(self.handle_tokenize)
        freq_layout.addRow(self.tokenize_btn)



        freq_layout.addRow(QLabel("Frequency Distribution Options:"))
        self.lowest_class_limit = QSpinBox()
        self.lowest_class_limit.setRange(-100000, 100000)
        self.lowest_class_limit.setValue(0)
        freq_layout.addRow("Lowest Class Limit:", self.lowest_class_limit)
        self.class_width = QSpinBox()
        self.class_width.setRange(1, 100000)
        self.class_width.setValue(5)
        freq_layout.addRow("Class Width:", self.class_width)
        self.freq_output = QTextEdit()
        self.freq_output.setReadOnly(True)
        freq_layout.addRow(self.freq_output)
        freq_btn = QPushButton("Show Frequency Table")
        freq_btn.clicked.connect(self.show_frequency)
        freq_layout.addRow(freq_btn)
        self.freq_tab.setLayout(freq_layout)

        # Stem-and-Leaf Tab
        stem_layout = QFormLayout()
        self.stemleaf_input = QTextEdit()
        self.stemleaf_input.setPlaceholderText("Enter stem-and-leaf plot")
        stem_layout.addRow("Stem-and-Leaf:", self.stemleaf_input)
        self.stemleaf_output = QTextEdit()
        self.stemleaf_output.setReadOnly(True)
        stem_layout.addRow(self.stemleaf_output)
        stem_btn = QPushButton("Convert to List")
        stem_btn.clicked.connect(self.show_stemleaf_to_list)
        stem_layout.addRow(stem_btn)
        self.stemleaf_tab.setLayout(stem_layout)

        self.tabs.addTab(self.freq_tab, "Frequency Table")
        self.tabs.addTab(self.stemleaf_tab, "Stem-and-Leaf")

        layout.addWidget(self.tabs)
        self.setLayout(layout)



class StatsApp(QWidget, controller):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistics Helper GUI")
        self.resize(700, 540)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Dataset input
        self.dataset_input = QLineEdit()
        self.dataset_input.setPlaceholderText(
            "Enter numbers separated by commas (e.g. 1,2,3,4)"
        )
        form_layout.addRow("Dataset:", self.dataset_input)

        # Tokenizer type dropdown
        self.tokenizer_type_combo = QComboBox()
        self.tokenizer_type_combo.addItems(
            ["Both (Default)", "Alphabetical Data", "Numerical Data"]
        )
        form_layout.addRow("Tokenization Type:", self.tokenizer_type_combo)

        # Tokenize button
        self.tokenize_btn = QPushButton("Tokenize")
        self.tokenize_btn.clicked.connect(self.handle_tokenize)
        form_layout.addRow(self.tokenize_btn)

        # Output box
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setMinimumHeight(120)

        # Button categories
        num_ops_layout = QHBoxLayout()
        iqr_ops_layout = QHBoxLayout()

        # Numerical Operations
        btn_mean = QPushButton("Mean")
        btn_mean.clicked.connect(self.show_mean)
        num_ops_layout.addWidget(btn_mean)

        btn_median = QPushButton("Median")
        btn_median.clicked.connect(self.show_median)
        num_ops_layout.addWidget(btn_median)

        btn_mode = QPushButton("Mode")
        btn_mode.clicked.connect(self.show_mode)
        num_ops_layout.addWidget(btn_mode)

        btn_range = QPushButton("Range")
        btn_range.clicked.connect(self.show_range)
        num_ops_layout.addWidget(btn_range)

        btn_pop_std = QPushButton("Population Std Dev")
        btn_pop_std.clicked.connect(self.show_population_std)
        num_ops_layout.addWidget(btn_pop_std)

        btn_sample_std = QPushButton("Sample Std Dev")
        btn_sample_std.clicked.connect(self.show_sample_std)
        num_ops_layout.addWidget(btn_sample_std)

        # IQR & Outlier Operations
        btn_quartiles = QPushButton("Quartiles & IQR")
        btn_quartiles.clicked.connect(self.show_quartiles)
        iqr_ops_layout.addWidget(btn_quartiles)

        # Extra stats (opens dialog)
        btn_extra = QPushButton("Extra Stats (Tables, Stem-Leaf conversion)")
        btn_extra.clicked.connect(self.open_extra_stats)
        iqr_ops_layout.addWidget(btn_extra)


        # Save Data Button
        btn_save = QPushButton("Save Data & Output")
        btn_save.clicked.connect(self.save_data_output)
        iqr_ops_layout.addWidget(btn_save)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(QLabel("Numerical Operations:"))
        main_layout.addLayout(num_ops_layout)
        main_layout.addWidget(QLabel("Other Operations:"))
        main_layout.addLayout(iqr_ops_layout)
        main_layout.addWidget(QLabel("Output:"))
        main_layout.addWidget(self.output_box)
        self.setLayout(main_layout)

        # Internal state
        self.tokenized_data = None
        self.tokenized_type = 3  # 3 = both, 1 = alpha, 2 = num

