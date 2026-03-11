using System.Runtime.InteropServices;

// main program container for the tray-based autotab application
static class Program
{
    // imports the native windows function that simulates keyboard input
    [DllImport("user32.dll")]
    private static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);

    // virtual key codes used to simulate alt+tab
    private const byte VK_ALT = 0x12;       // alt key
    private const byte VK_TAB = 0x09;        // tab key
    private const uint KEY_RELEASE = 0x0002; // flag indicating key release

    // background timer that triggers the alt+tab simulation
    private static System.Threading.Timer altTabTimer;

    // system tray icon displayed in the notification area
    private static NotifyIcon trayIcon;

    // tracks whether the autotab behavior is currently paused
    private static bool isPaused = false;

    // cached icons used to visually indicate running (green) or paused (red) state
    private static Icon greenIcon = CreateDotIcon(Color.LimeGreen);
    private static Icon redIcon = CreateDotIcon(Color.Red);

    // interval between alt+tab switches (4 minutes)
    private static readonly int intervalMs = 240000;

    // stores the next scheduled execution time for countdown display
    private static DateTime nextRunTime;

    // menu items that need to be dynamically enabled/disabled
    private static ToolStripMenuItem pauseItem;
    private static ToolStripMenuItem resumeItem;
    private static ToolStripMenuItem countdownItem;

    // ui timer used to update the countdown text once per second
    private static System.Windows.Forms.Timer uiTimer;

    // application entry point; initializes tray icon, menu, and timers
    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);

        // create tray icon and set initial state
        trayIcon = new NotifyIcon
        {
            Icon = greenIcon,
            Text = "AutoTab (running)",
            Visible = true
        };

        // attach left-click handler for quick pause/resume toggle
        trayIcon.MouseClick += TrayIcon_MouseClick;

        // build tray context menu
        var menu = new ContextMenuStrip();

        // countdown display item (read-only)
        countdownItem = new ToolStripMenuItem("Next switch: --:--");
        countdownItem.Enabled = false;

        // pause/resume menu actions using lambda event handlers
        pauseItem = new ToolStripMenuItem("Pause", null, (_, _) => Pause());
        resumeItem = new ToolStripMenuItem("Resume", null, (_, _) => Resume());

        menu.Items.Add(countdownItem);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add(pauseItem);
        menu.Items.Add(resumeItem);
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add("Exit", null, (_, _) => Exit());

        // hook into menu open/close events to start/stop countdown updates
        menu.Opening += Menu_Opening;
        menu.Closing += Menu_Closing;

        trayIcon.ContextMenuStrip = menu;

        // since program starts running, resume is disabled initially
        resumeItem.Enabled = false;

        // ui timer updates countdown text every second while menu is open
        uiTimer = new System.Windows.Forms.Timer();
        uiTimer.Interval = 1000;
        uiTimer.Tick += (_, _) => UpdateCountdownText();

        // initialize next execution time and start background timer
        nextRunTime = DateTime.Now.AddMilliseconds(intervalMs);
        altTabTimer = new System.Threading.Timer(AltTabSimulation, null, intervalMs, intervalMs);

        Application.Run();
    }

    // pauses the background switching behavior and updates ui state
    private static void Pause()
    {
        if (isPaused) return;

        pauseItem.Enabled = false;
        resumeItem.Enabled = true;

        altTabTimer.Change(Timeout.Infinite, Timeout.Infinite);

        trayIcon.Text = "AutoTab (paused)";
        trayIcon.Icon = redIcon;

        isPaused = true;
    }

    // resumes the background switching behavior and updates ui state
    private static void Resume()
    {
        if (!isPaused) return;

        pauseItem.Enabled = true;
        resumeItem.Enabled = false;

        nextRunTime = DateTime.Now.AddMilliseconds(intervalMs);
        altTabTimer.Change(0, intervalMs);

        trayIcon.Text = "AutoTab (running)";
        trayIcon.Icon = greenIcon;

        isPaused = false;
    }

    // cleanly shuts down the application and disposes of resources
    private static void Exit()
    {
        trayIcon.Visible = false;

        altTabTimer.Dispose();
        greenIcon.Dispose();
        redIcon.Dispose();

        Application.Exit();
    }

    // called by background timer; performs two quick alt+tab presses
    private static void AltTabSimulation(object? state)
    {
        DoAltTab();
        Thread.Sleep(100);
        DoAltTab();

        nextRunTime = DateTime.Now.AddMilliseconds(intervalMs);
    }

    // simulates pressing and releasing alt+tab using native windows api
    private static void DoAltTab()
    {
        keybd_event(VK_ALT, 0, 0, UIntPtr.Zero);
        keybd_event(VK_TAB, 0, 0, UIntPtr.Zero);
        keybd_event(VK_TAB, 0, KEY_RELEASE, UIntPtr.Zero);
        keybd_event(VK_ALT, 0, KEY_RELEASE, UIntPtr.Zero);
    }

    // creates a small 16x16 circular icon of the specified color
    private static Icon CreateDotIcon(Color color)
    {
        Bitmap bmp = new Bitmap(16, 16);

        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.Clear(Color.Transparent);

            using (Brush brush = new SolidBrush(color))
            {
                // draws a centered 12x12 circle inside the 16x16 bitmap
                g.FillEllipse(brush, 2, 2, 12, 12);
            }
        }

        // clone icon to prevent handle lifetime issues
        Icon icon = Icon.FromHandle(bmp.GetHicon());
        return (Icon)icon.Clone();
    }

    // handles tray icon mouse clicks and toggles pause on left click
    private static void TrayIcon_MouseClick(object? sender, MouseEventArgs e)
    {
        if (e.Button == MouseButtons.Left)
        {
            TogglePause();
        }
    }

    // switches between paused and running states
    private static void TogglePause()
    {
        if (isPaused)
            Resume();
        else
            Pause();
    }

    // triggered when context menu opens; refreshes countdown and starts ui timer
    private static void Menu_Opening(object? sender, System.ComponentModel.CancelEventArgs e)
    {
        UpdateCountdownText();
        uiTimer.Start();
    }

    // triggered when context menu closes; stops ui timer updates
    private static void Menu_Closing(object? sender, ToolStripDropDownClosingEventArgs e)
    {
        uiTimer.Stop();
    }

    // updates the countdown display text based on remaining time
    private static void UpdateCountdownText()
    {
        if (isPaused)
        {
            countdownItem.Text = "Paused";
            return;
        }

        var remaining = nextRunTime - DateTime.Now;

        if (remaining.TotalSeconds < 0)
            remaining = TimeSpan.Zero;

        countdownItem.Text = $"Next Alt-Tab: {remaining.Minutes:D2}:{remaining.Seconds:D2}";
    }
}
