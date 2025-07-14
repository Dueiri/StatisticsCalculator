#statsGui.py
#module that handles the GUI for the statistics helper application
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

class AdvancedStatsDialog(QDialog, controller):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Statistics")
        self.resize(500, 400)

        # create the main layout and tabs
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.quartiles_tab = QWidget()
        self.zscore_tab = QWidget()
    
        # Quartiles Tab
        quartiles_layout = QFormLayout()
        self.quartiles_input = QLineEdit()
        self.quartiles_input.setPlaceholderText("Enter numbers separated by commas")
        quartiles_layout.addRow("Dataset:", self.quartiles_input)
        
        # Tokenizer type dropdown for quartiles
        self.quartiles_tokenizer_combo = QComboBox()
        self.quartiles_tokenizer_combo.addItems(
            ["Both (Default)", "Alphabetical Data", "Numerical Data"]
        )
        quartiles_layout.addRow("Tokenization Type:", self.quartiles_tokenizer_combo)

        # Tokenize button for quartiles
        self.quartiles_tokenize_btn = QPushButton("Tokenize")
        self.quartiles_tokenize_btn.clicked.connect(lambda: self.handle_tokenize(self.quartiles_input))
        quartiles_layout.addRow(self.quartiles_tokenize_btn)
        
        self.quartiles_output = QTextEdit()
        self.quartiles_output.setReadOnly(True)
        quartiles_layout.addRow(self.quartiles_output)
        
        # Button to calculate quartiles
        quartiles_btn = QPushButton("Calculate Quartiles")
        quartiles_btn.clicked.connect(self.show_quartiles_advanced)
        quartiles_layout.addRow(quartiles_btn)
        self.quartiles_tab.setLayout(quartiles_layout)
        
        # Z-Score Tab
        zscore_layout = QFormLayout()
        self.zscore_dataset_input = QLineEdit()
        self.zscore_dataset_input.setPlaceholderText("Enter numbers separated by commas")
        zscore_layout.addRow("Dataset:", self.zscore_dataset_input)
        
        # Tokenizer type dropdown for z-score
        self.zscore_tokenizer_combo = QComboBox()
        self.zscore_tokenizer_combo.addItems(
            ["Both (Default)", "Alphabetical Data", "Numerical Data"]
        )
        zscore_layout.addRow("Tokenization Type:", self.zscore_tokenizer_combo)

        # Tokenize button for z-score
        self.zscore_tokenize_btn = QPushButton("Tokenize")
        self.zscore_tokenize_btn.clicked.connect(lambda: self.handle_tokenize(self.zscore_dataset_input))
        zscore_layout.addRow(self.zscore_tokenize_btn)
        
        self.zscore_value_input = QLineEdit()
        self.zscore_value_input.setPlaceholderText("Enter the value to calculate z-score for")
        zscore_layout.addRow("Value:", self.zscore_value_input)
        
        self.zscore_output = QTextEdit()
        self.zscore_output.setReadOnly(True)
        zscore_layout.addRow(self.zscore_output)
        
        # Button to calculate z-score
        zscore_btn = QPushButton("Calculate Z-Score")
        zscore_btn.clicked.connect(self.show_z_score)
        zscore_layout.addRow(zscore_btn)
        self.zscore_tab.setLayout(zscore_layout)

        # Add tabs to the main layout
        self.tabs.addTab(self.quartiles_tab, "Quartiles & IQR")
        self.tabs.addTab(self.zscore_tab, "Z-Score")

        layout.addWidget(self.tabs)
        self.setLayout(layout)


class ExtraStatsDialog(QDialog, controller):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.tokenize_btn.clicked.connect(lambda: self.handle_tokenize(self.freq_input))
        freq_layout.addRow(self.tokenize_btn)


        freq_layout.addRow(QLabel("Frequency Distribution Options:"))
        self.lowest_class_limit = QSpinBox()
        self.lowest_class_limit.setRange(-100000, 100000)
        self.lowest_class_limit.setValue(0)

        # Set the default value for lowest class limit
        freq_layout.addRow("Lowest Class Limit:", self.lowest_class_limit)
        self.class_width = QSpinBox()
        self.class_width.setRange(1, 100000)
        self.class_width.setValue(5)

        #set the default value for class width
        freq_layout.addRow("Class Width:", self.class_width)
        self.freq_output = QTextEdit()
        self.freq_output.setReadOnly(True)
        freq_layout.addRow(self.freq_output)

        # Button to show frequency table
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

        # Add tabs to the main layout
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
        self.tokenize_btn.clicked.connect(lambda: self.handle_tokenize(self.dataset_input))
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

        # Advanced Statistics (opens dialog)
        advanced_stats = QPushButton("Advanced Statistics")
        advanced_stats.clicked.connect(self.open_advanced_stats)
        iqr_ops_layout.addWidget(advanced_stats)

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


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = StatsApp()
    window.show()
    sys.exit(app.exec())
