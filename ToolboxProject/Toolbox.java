import javax.swing.*;
import java.awt.*;
import apps.*;

public class Toolbox {
    private final JPanel contentPanel; // The area where tools (apps) will be displayed
    private final JLabel messageBar; // Message bar at the bottom

    public Toolbox() {
        // create the main frame
        JFrame frame = new JFrame("Toolbox");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        frame.setLayout(new BorderLayout());

        // create the left toolbar panel
        JPanel toolbarPanel = new JPanel(new GridLayout(0, 1, 5, 5)); // Vertical list of buttons
        JScrollPane toolbar = new JScrollPane(toolbarPanel); // Make it scrollable
        toolbar.setPreferredSize(new Dimension(200, 600)); // Set width of the toolbar

        // create the right content panel (initially empty)
        contentPanel = new JPanel(new BorderLayout());
        contentPanel.setBackground(Color.LIGHT_GRAY);

        // create the bottom message bar
        messageBar = new JLabel("Welcome to the Toolbox!", SwingConstants.CENTER);
        messageBar.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));

        // add buttons to the toolbar
        addButton(toolbarPanel, "XMLFormatter", new XMLFormatter(messageBar));
        addButton(toolbarPanel, "SQLtoVBSConverter", new SQLtoVBSConverter(messageBar));
        addButton(toolbarPanel, "Translator", new Translator());

        // add components to the main frame
        frame.add(toolbar, BorderLayout.WEST);  // Toolbar on the left
        frame.add(contentPanel, BorderLayout.CENTER); // Active tool area
        frame.add(messageBar, BorderLayout.SOUTH); // Message bar at the bottom

        // make main frame visible
        frame.setVisible(true);
    }

    // adds a button the the toolbar
    private void addButton(JPanel toolbar, String name, JPanel app) {
        JButton button = new JButton(name);
        button.addActionListener(e -> {
            launchApp(app);
            updateMessage("Loaded: " + name);
        });
        toolbar.add(button);
    }

     // launches a JPanel app into the content panel
    private void launchApp(JPanel app) {
        contentPanel.removeAll();
        contentPanel.add(app, BorderLayout.CENTER);
        contentPanel.revalidate();
        contentPanel.repaint();
    }

    // Method to update the message bar text
    public void updateMessage(String message) {
        messageBar.setText(message);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Toolbox::new);
    }
}

// Placeholder Sub-Apps
class Translator extends JPanel {
    public Translator() {
        setLayout(new BorderLayout());
        add(new JLabel("TBD App", SwingConstants.CENTER), BorderLayout.CENTER);
    }
}