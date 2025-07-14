#controller.py
#Module that connects the GUI to the StatisticsHelper library. Uses all helper functions from statisticsHelp.py.
#Written by David Dueiri
# 7/9/2025

from User_Libraries.statisticsHelp import (SimpleStatisticsHelper,
                                            advancedStatisticsHelper)


#import necessary GUI components directly from statsGui
from PyQt6.QtWidgets import (
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QTimer


class controller:
    
    helper = SimpleStatisticsHelper()
    advHelper = advancedStatisticsHelper()


    def open_advanced_stats(self):
        """Open the Advanced Statistics dialog."""
        from GUI_Control.statsGui import AdvancedStatsDialog
        dialog = AdvancedStatsDialog(self).exec()

    def open_extra_stats(self):
        """Open the Extra Statistics dialog."""
        from GUI_Control.statsGui import ExtraStatsDialog
        ExtraStatsDialog(self).exec()

    #run function in statisticshelp.py
    def show_frequency(self):
        text = self.freq_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter a dataset.")
            return
        try:
            # lowest_class_limit and class_width are spinboxes declared in statsGui.py
            data = self.helper.datasetToList(text)
            lowest = self.lowest_class_limit.value()
            width = self.class_width.value()
            import io
            import contextlib

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.advHelper.frequencyDistribution(data, lowest, width)
            self.freq_output.setText(buf.getvalue())
        except Exception as e: #avoid crashing the GUI
            QMessageBox.warning(self, "Error", str(e))

    def show_stemleaf_to_list(self):
        text = self.stemleaf_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(
                self, "Input Error", "Please enter a stem-and-leaf plot."
            )
            return
        try:
            result = self.advHelper.stemLeafToList(text)
            self.stemleaf_output.setText(f"List: {result}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def get_data_list(self):
        if self.tokenized_data is not None:
            return self.tokenized_data
        text = self.dataset_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter a dataset.")
            return None
        try:
            return self.helper.datasetToList(text)
        except Exception as e:
            QMessageBox.warning(self, "Input Error", f"Invalid dataset: {e}")
            return None

    def show_mean(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.mean(data)
            self.output_box.setText(f"Mean: {result}")

    def show_median(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.median(data)
            self.output_box.setText(f"Median: {result}")

    def show_mode(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.mode(data)
            if result is None:
                self.output_box.setText("Mode: No mode found (all values are unique)")
            else:
                self.output_box.setText(f"Mode: {result}")

    def show_range(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.range(data)
            self.output_box.setText(f"Range: {result}")

    def show_population_std(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.populationStandardDeviation(data)
            self.output_box.setText(f"Population Standard Deviation: {result}")

    def show_sample_std(self):
        data = self.get_data_list()
        if data is not None:
            result = self.helper.sampleStandardDeviation(data)
            self.output_box.setText(f"Sample Standard Deviation: {result}")

    def show_quartiles(self):
        data = self.get_data_list()
        if data is not None:
            q1, q2, q3, q4, iqr, lowerBound, upperBound, outliers = (
                self.helper.findQuartiles(data)
            )
            self.output_box.setText(
                f"Q1: {q1}\nQ2 (Median): {q2}\nQ3: {q3}\nQ4 (Max): {q4}\nIQR: {iqr}\nLower Bound: {lowerBound}\nUpper Bound: {upperBound}\nOutliers: {outliers}"
            )

    def handle_tokenize(self, dataset):
        self.tokenized_data = None
        dataset.setEnabled(False)  # Disable the input widget during processing
        idx = self.tokenizer_type_combo.currentIndex()
        alphaOrNum = 3 if idx == 0 else (1 if idx == 1 else 2)
        self.tokenized_type = alphaOrNum

        def finish_tokenize():
            text = dataset.text().strip()
            if not text:
                QMessageBox.warning(self, "Input Error", "Please enter a dataset.")
                dataset.setEnabled(True)
                return
            try:
                tokens = self.helper.tokenize(text, alphaOrNum)
                self.tokenized_data = tokens
                dataset.setText(", ".join(str(t) for t in tokens))  # Update the correct widget
            except Exception as e:
                QMessageBox.warning(self, "Tokenization Error", str(e))
                self.tokenized_data = None
            dataset.setEnabled(True)  # Re-enable the input widget

        QTimer.singleShot(500, finish_tokenize)  # Delay to avoid UI freeze

    def save_data_output(self): #Todo: make function dynamic to save any data and output
        dataset = self.dataset_input.text().strip()
        output = self.output_box.toPlainText().strip()
        if not dataset or not output:
            QMessageBox.warning(
                self, "Save Error", "Both dataset and output must be present."
            )
            return
        fname, _ = QFileDialog.getSaveFileName(
            self, "Save Data and Output", "", "Text Files (*.txt)"
        )
        if fname:
            try:
                with open(fname, "w", encoding="utf-8") as f:
                    f.write("Dataset:\n")
                    f.write(dataset + "\n\n")
                    f.write("Output:\n")
                    f.write(output + "\n")
                QMessageBox.information(
                    self, "Saved", f"Data and output saved to {fname}"
                )
            except Exception as e:
                QMessageBox.warning(self, "Save Error", str(e))

    def show_z_score(self):
        """Calculate and display z-score for a value in a dataset."""
        dataset_text = self.zscore_dataset_input.text().strip()
        value_text = self.zscore_value_input.text().strip()
        
        if not dataset_text or not value_text:
            QMessageBox.warning(self, "Input Error", "Please enter both dataset and value.")
            return
        
        try:
            data = self.helper.datasetToList(dataset_text)
            value = float(value_text)
            z_score = self.advHelper.zScore(data, value)
            
            if z_score is None:
                self.zscore_output.setText("Cannot calculate z-score (standard deviation is 0)")
            else:
                self.zscore_output.setText(f"Z-Score: {z_score:.4f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_quartiles_advanced(self):
        """Calculate and display quartiles in the advanced stats dialog."""
        text = self.quartiles_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter a dataset.")
            return
        try:
            data = self.helper.datasetToList(text)
            q1, q2, q3, q4, iqr, lowerBound, upperBound, outliers = (
                self.advHelper.findQuartiles(data)
            )
            self.quartiles_output.setText(
                f"Q1: {q1}\nQ2 (Median): {q2}\nQ3: {q3}\nQ4 (Max): {q4}\nIQR: {iqr}\nLower Bound: {lowerBound}\nUpper Bound: {upperBound}\nOutliers: {outliers}"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
