import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QDesktopWidget, QFileDialog, QLineEdit, QDialog, QInputDialog, QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import subprocess
import os
from Z_lift_change import insert_gcode_above_tool_change, remove_g1_z_lines, write_tool_change, remove_consecutive_duplicates_inplace

class StyledApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Revo Optimization')
        self.setGeometry(0, 0, 900, 700)
        centerPoint = QDesktopWidget().availableGeometry().center()

        # Use move method to set the top-left corner of the window
        self.move(centerPoint.x() - self.width() // 2, centerPoint.y() - self.height() // 2)
        self.setStyleSheet('background-color: #FFFFFF;')

        # Create a QLabel to display the logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(os.path.abspath('RevoLogo.png'))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Create a QStackedWidget to manage different pages
        self.stacked_widget = QStackedWidget(self)

        # Create three pages as QWidgets
        page1 = QWidget(self)
        page2 = QWidget(self)
        page3 = QWidget(self)

        # Add labels to each page
        layout1 = QVBoxLayout(page1)
        layout1.addWidget(QLabel('G-Code Optimizer Content'))

        layout2 = QVBoxLayout(page2)
        layout2.addWidget(QLabel('E Deleter Content'))

        layout3 = QVBoxLayout(page3)
        layout3.addWidget(QLabel('Coming Soon Content'))

        # Add pages to the QStackedWidget
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)

        # Create buttons
        button1 = QPushButton('G-Code Optimizer', self)
        button_e_deleter = QPushButton('E Deleter', self)
        button3 = QPushButton('Z Lift Change', self)

        # Connect button clicks to change pages
        button1.clicked.connect(lambda: self.change_page(0))
        button_e_deleter.clicked.connect(lambda: self.choose_file_e_deleter())  # Connect to choose_file_e_deleter method
        button3.clicked.connect(lambda: self.choose_file_z_lift_change())
        


        # Apply styles to the buttons
        button_style = 'QPushButton { background-color: #ECECEC; color: black; padding: 10px; text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px; }'
        button1.setStyleSheet(button_style)
        button_e_deleter.setStyleSheet(button_style)
        button3.setStyleSheet(button_style)

        # Set cursor style for buttons
        button1.setCursor(Qt.PointingHandCursor)
        button_e_deleter.setCursor(Qt.PointingHandCursor)
        button3.setCursor(Qt.PointingHandCursor)

        # Set font style for buttons
        font = QFont('Arial')
        font.setPointSize(16)
        font.setBold(True)
        button1.setFont(font)
        button_e_deleter.setFont(font)
        button3.setFont(font)

        # Create a vertical layout for the main window
        layout = QVBoxLayout(self)

        # Add widgets to the main layout
        self.choose_file_button = QPushButton('Choose File', self)
        self.choose_file_button.clicked.connect(self.choose_file)
        self.choose_file_button.setStyleSheet(button_style)  # Use the same style as other buttons
        page_e_deleter = QWidget(self)
        layout_e_deleter = QVBoxLayout(page_e_deleter)
        layout_e_deleter.addWidget(QLabel('E Deleter Content'))
        self.stacked_widget.addWidget(page_e_deleter)
        layout.addWidget(logo_label)
        layout.addWidget(button1)
        layout.addWidget(button_e_deleter)
        layout.addWidget(button3)
        layout.addWidget(self.choose_file_button)  # Add the button to the layout
        layout.addWidget(self.stacked_widget)

        # Create Proceed button
        self.proceed_button = QPushButton('Proceed', self)
        self.proceed_button.clicked.connect(self.proceed_action)
        self.proceed_button.setStyleSheet(button_style)  # Use the same style as other buttons
        self.proceed_button.setVisible(False)  # Initially set to not visible
        layout.addWidget(self.proceed_button)

        # Center the widgets within the layout
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Attribute to store the current page index
        self.current_page_index = 0

    def choose_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose G-code File", "", "G-code Files (*.gcode);;All Files (*)", options=options)
        if file_name:
            print(f"Selected file: {file_name}")

            # Ask the user for the desired output file name
            custom_name, ok = QInputDialog.getText(self, 'Output File Name', 'Enter a name for the output file:')
            if ok and custom_name:
                print(f"Custom name for the output file: {custom_name}")

                # Ask the user for the directory to save the output file
                output_directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Output File")
                if output_directory:
                    # Construct the full file path for the output file
                    output_file_path = os.path.join(output_directory, custom_name + "_output.gcode")

                    # Print debugging information
                    print(f"Input File: {file_name}")
                    print(f"Output File: {output_file_path}")

                    # Call your optimization algorithm using subprocess
                    try:
                        # Use absolute paths for the subprocess
                        main_script_path = os.path.abspath("main.py")

                        # Pass input file, custom name, and output directory as arguments
                        subprocess.run(["python", main_script_path, file_name, custom_name, output_directory], check=True)
                        print("Optimization completed successfully.")

                        # Update the label of the Choose File button with the selected file name
                        self.choose_file_button.setText(f'Input File: {file_name}\nOutput File: {output_file_path}')

                        # Show the Proceed button after successful optimization
                        self.proceed_button.setVisible(True)

                    except subprocess.CalledProcessError as e:
                        print(f"Error during optimization: {e}")

    def choose_file_z_lift_change(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File for Z Lift Change", "", "G-code Files (*.gcode);;All Files (*)", options=options)
        if file_name:
            print(f"Selected file for Z Lift Change: {file_name}")
            # Update the label of the button with the selected file name
            self.choose_file_button.setText(f'File: {file_name}')

            # Call the Z Lift Change algorithm script here, passing the chosen file_name
            self.run_z_lift_change(file_name)

    def run_z_lift_change(self, file_path):
        # Create a dialog window to prompt the user for input
        dialog = QDialog(self)
        dialog.setWindowTitle('Z Lift Change Input')
        dialog.resize(300, 200)

        # Create labels and input fields for Z Height and Subtract Value
        z_height_label = QLabel('Z Height:', dialog)
        self.z_height_input = QSpinBox(dialog)
        self.z_height_input.setMinimum(1)
        subtract_value_label = QLabel('Subtract Value:', dialog)
        self.subtract_value_input = QDoubleSpinBox(dialog)
        self.subtract_value_input.setMinimum(0)

        # Create a button to confirm the input
        confirm_button = QPushButton('Confirm', dialog)
        confirm_button.clicked.connect(lambda: self.on_confirm_z_lift_change(file_path, dialog))

        # Create a layout for the dialog window
        layout = QVBoxLayout(dialog)
        layout.addWidget(z_height_label)
        layout.addWidget(self.z_height_input)
        layout.addWidget(subtract_value_label)
        layout.addWidget(self.subtract_value_input)
        layout.addWidget(confirm_button)

        # Display the dialog window
        dialog.exec_()

    def on_confirm_z_lift_change(self, file_path, dialog):
        # Get the values entered by the user
        z_height = float(self.z_height_input.text())  # Convert text to float
        subtract_value = float(self.subtract_value_input.text())  # Convert text to float
        remove_g1_z_lines(file_path)
        write_tool_change(file_path)
        remove_consecutive_duplicates_inplace(file_path)
        # Call the modified insert_gcode_above_tool_change function with the user input values
        insert_gcode_above_tool_change(file_path, z_height, subtract_value)

        # Close the dialog window
        dialog.close()


    def change_page(self, index):
        # Change the current page of the stacked widget
        self.stacked_widget.setCurrentIndex(index)
        
        # Set the current page index attribute
        self.current_page_index = index

        # Reset the style of all buttons to default
        for button in self.findChildren(QPushButton):
            button.setStyleSheet('background-color: #ECECEC; color: black; padding: 10px; text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px;')
        
        for button_e_deleter in self.findChildren(QPushButton):
            button_e_deleter.setStyleSheet('background-color: #ECECEC; color: black; padding: 10px; text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px;')

        # Reset the label of the "Choose File" button
        self.choose_file_button.setText('Choose File')

        # Hide the Proceed button when switching pages
        self.proceed_button.setVisible(False)

        # Get the button that triggered the event
        sender = self.sender()

        # Apply a different style to the clicked button
        sender.setStyleSheet('background-color: #B3B3B3; color: black; padding: 10px; text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px;')

    def proceed_action(self):
        # Check if a file has been chosen
        if self.choose_file_button.text() == 'Choose File':
            print("Please choose a file before proceeding.")
            return

        # Extract the file name from the button's text
        file_name = self.choose_file_button.text().replace('File: ', '')

        # Construct the file path (adjust this based on your file structure)
        file_path = f"{file_name}"

        print(f"Proceed button clicked for page {self.current_page_index}")

        # Call your optimization algorithm using subprocess
        try:
            subprocess.run(["python", os.path.abspath("main.py"), file_path], check=True)
            print("Optimization completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during optimization: {e}")

    def choose_file_e_deleter(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File for E Deleter", "", "G-code Files (*.gcode);;All Files (*)", options=options)
        if file_name:
            print(f"Selected file for E Deleter: {file_name}")
            # Update the label of the button with the selected file name
            self.choose_file_button.setText(f'File: {file_name}')

            # Call the E Deleter algorithm script here, passing the chosen file_name
            self.run_e_deleter(file_name)

    def run_e_deleter(self, file_path):
        # Assuming your E Deleter script is named "E_deleter.py" and is in the same directory as the main script
        e_deleter_script_path = os.path.abspath("E_deleter.py")

        # Ask the user for the directory to save the E Deleter output file
        output_directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save E Deleter Output File")
        if not output_directory:
            print("Output directory not selected. E Deleter operation aborted.")
            return

        # Ask the user for the desired output file name
        custom_name, ok = QInputDialog.getText(self, 'Output File Name', 'Enter a name for the E Deleter output file:')
        if not ok or not custom_name:
            print("Invalid output file name. E Deleter operation aborted.")
            return

        # Construct the full input and output file paths
        input_file_path = file_path
        output_file_path = os.path.join(output_directory, f"{custom_name}.gcode")

        print(f"Running E Deleter algorithm for file: {input_file_path}")

        try:
            # Modify this line to run your E Deleter script
            subprocess.run(["python", e_deleter_script_path, input_file_path, custom_name, output_directory], check=True)
            print("E Deleter completed successfully.")

            # Update the label of the Choose File button with the selected file name
            self.choose_file_button.setText(f'Input File: {input_file_path}\nE Deleter Output: {output_file_path}')

            # Show the Proceed button after successful E Deleter operation
            self.proceed_button.setVisible(True)

        except subprocess.CalledProcessError as e:
            print(f"Error during E Deleter: {e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    styled_app = StyledApp()
    styled_app.show()
    sys.exit(app.exec_())

