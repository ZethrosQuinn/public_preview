package apps;

import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class XMLFormatter extends JPanel {
    private final JTextArea inputTextArea; // where users enter XML or file path
    private final JTextArea outputTextArea; // formatted XML output
    private final JTextField filePathField; // field to input file path
    private final JButton formatButton; // button to format text
    private final JButton browseButton; // button to browse files
    private final JLabel messageBar; // reference to Toolbox's message bar

    public XMLFormatter(JLabel messageBar) {
        this.messageBar = messageBar; // use Toolbox's message bar

        setLayout(new BorderLayout(10, 10));

        // instruction label
        JLabel instructionLabel = new JLabel("Enter XML text below or provide a file path:");
        add(instructionLabel, BorderLayout.NORTH);

        // main panel for input/output
        JPanel mainPanel = new JPanel(new GridLayout(2, 1, 5, 5));
        add(mainPanel, BorderLayout.CENTER);

        // input area (text + file selection)
        JPanel inputPanel = new JPanel(new BorderLayout(5, 5));
        JPanel filePanel = new JPanel(new FlowLayout(FlowLayout.LEFT));

        inputTextArea = new JTextArea(5, 40);
        filePathField = new JTextField(30);
        browseButton = new JButton("Browse");
        formatButton = new JButton("Format XML");

        inputPanel.add(new JScrollPane(inputTextArea), BorderLayout.CENTER);
        filePanel.add(new JLabel("File path:"));
        filePanel.add(filePathField);
        filePanel.add(browseButton);
        filePanel.add(formatButton);
        inputPanel.add(filePanel, BorderLayout.SOUTH);
        mainPanel.add(inputPanel);

        // output area
        outputTextArea = new JTextArea(5, 40);
        outputTextArea.setEditable(false);
        mainPanel.add(new JScrollPane(outputTextArea));

        // button actions
        formatButton.addActionListener(e -> formatXml());
        browseButton.addActionListener(e -> selectFile());
    }

    // method to format XML from input
    private void formatXml() {
        String input = inputTextArea.getText().trim();
        String filePath = filePathField.getText().trim();

        if (!filePath.isEmpty()) {
            try {
                input = Files.readString(Paths.get(filePath));
            } catch (IOException e) {
                showMessage("Error reading file: " + e.getMessage());
                return;
            }
        }

        if (input.isEmpty()) {
            showMessage("Please enter XML text or select a file.");
            return;
        }

        String formattedXml = formatXmlString(input);
        outputTextArea.setText(formattedXml);
        showMessage("Formatting complete!");
    }

    // method to select a file
    private void selectFile() {
        JFileChooser fileChooser = new JFileChooser();
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            filePathField.setText(fileChooser.getSelectedFile().getAbsolutePath());
        }
    }

    // method to format XML text
    private static String formatXmlString(String input) {
        StringBuilder formattedXml = new StringBuilder();
        int indentLevel = 0;
        String indentSpace = "    "; // 4 spaces per indentation level

        input = input.replaceAll(">\\s*<", ">\n<"); // ensure newlines between tags

        String[] lines = input.split("\n");
        for (String line : lines) {
            line = line.trim();

            if (line.startsWith("</")) {
                // closing tag -> decrease indent before appending
                indentLevel--;
            }

            // append indent and line
            formattedXml.append(indentSpace.repeat(Math.max(0, indentLevel))).append(line).append("\n");

            if (line.startsWith("<") && !line.startsWith("</") && !line.endsWith("/>")) {
                // opening tag -> increase indent after appending
                indentLevel++;
            }
        }

        return formattedXml.toString().trim();
    }

    // method to update Toolbox's message bar
    private void showMessage(String message) {
        messageBar.setText(message);
    }
}
