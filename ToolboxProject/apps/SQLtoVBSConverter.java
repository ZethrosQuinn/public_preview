package apps;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.regex.Pattern;

public class SQLtoVBSConverter extends JPanel {
    private final JTextArea inputTextArea; // where users enter SQL or VBS
    private final JTextArea outputTextArea; // converted output
    private final JButton convertButton; // button to start conversion
    private final JLabel messageBar; // reference to Toolbox's message bar

    // keywords for formatting
    private static final String[] NEWLINE_KEYWORDS = {"FROM", "JOIN", "WHERE", "AND", "ORDER BY", "WHEN", "CASE", "GROUP BY", "INTO", " END ", "DECLARE", "FORMAT"};
    private static final String[] INLINE_KEYWORDS = {" DESC", " ASC", "SELECT", "(NOLOCK)", " ON ", " IN ", " WITH ", "MIN", "MAX", " THEN ", " CONVERT", " CAST", " COALESCE", " ELSE ", " DISTINCT", " TOP ", " INSERT", " UPDATE", " AS ", "GETDATE(", " UNION ", "DATEDIFF("};

    public SQLtoVBSConverter(JLabel messageBar) {
        this.messageBar = messageBar; // use Toolbox's message bar
        setLayout(new BorderLayout(10, 10));

        // instruction label
        JLabel instructionLabel = new JLabel("Enter SQL or VBS code below:");
        add(instructionLabel, BorderLayout.NORTH);

        // main panel for input/output
        JPanel mainPanel = new JPanel(new GridLayout(2, 1, 5, 5));
        add(mainPanel, BorderLayout.CENTER);

        // input area
        inputTextArea = new JTextArea(5, 40);
        mainPanel.add(new JScrollPane(inputTextArea));

        // output area
        outputTextArea = new JTextArea(5, 40);
        outputTextArea.setEditable(false);
        mainPanel.add(new JScrollPane(outputTextArea));

        // button panel
        JPanel buttonPanel = new JPanel();
        convertButton = new JButton("Convert");
        buttonPanel.add(convertButton);
        add(buttonPanel, BorderLayout.SOUTH);

        // button action
        convertButton.addActionListener(e -> convertInput());
    }

    // method to process input and determine conversion type
    private void convertInput() {
        String input = inputTextArea.getText().trim();

        if (input.isEmpty()) {
            showMessage("Please enter SQL or VBS code to convert.");
            return;
        }

        char firstChar = input.charAt(0);
        String result = (firstChar == '"') ? vbsToSql(input) : sqlToVbs(input);

        outputTextArea.setText(result);
        showMessage("Conversion complete!");
    }

    // method to convert VBS to SQL
    private String vbsToSql(String input) {
        input = input.replace("\"", "").replace("& _", "").replace("&_", "").replace("&", "").replace("vbcrlf", "");

        // special replacement for joins
        input = input.replace("left join", "LEFT JOIN").replace("LEFT JOIN", "\nLEFT JOTINGER")
                     .replace("inner join", "INNER JOIN").replace("INNER JOIN", "\nINNER JOTINGER")
                     .replace("full outer join", "FULL OUTER JOIN").replace("FULL OUTER JOIN", "\nFULL OUTER JOTINGER")
                     .replace("right join", "RIGHT JOIN").replace("RIGHT JOIN", "\nRIGHT JOTINGER");

        input = input.replaceAll("\\s+", " "); // remove extra spaces

        // format new lines and capitalization
        for (String s : NEWLINE_KEYWORDS) {
            input = input.replace(s.toLowerCase(), s).replace(s, "\n" + s);
        }

        for (String s : INLINE_KEYWORDS) {
            input = input.replace(s.toLowerCase(), s);
        }

        // restore join keywords
        input = input.replace("JOTINGER", "JOIN");

        return input;
    }

    // method to convert SQL to VBS
    private String sqlToVbs(String input) {
        // special replacement for joins
        input = input.replace("left join", "\" & _ \n\"LEFT JOTINGER")
                     .replace("inner join", "\" & _ \n\"INNER JOTINGER")
                     .replace("full outer join", "\" & _ \n\"FULL OUTER JOTINGER")
                     .replace("right join", "\" & _ \n\"RIGHT JOTINGER");

        // format new lines and capitalization
        for (String s : NEWLINE_KEYWORDS) {
            input = input.replace(s.toLowerCase(), s).replace(s, "\" & _ \n\"" + s);
        }

        for (String s : INLINE_KEYWORDS) {
            input = input.replace(s.toLowerCase(), s);
        }

        // restore join keywords
        input = input.replace("JOTINGER", "JOIN");

        // enclose statement in quotes
        return "\"" + input + "\"";
    }

    // method to update Toolbox's message bar
    private void showMessage(String message) {
        messageBar.setText(message);
    }
}
