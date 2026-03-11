using System.Runtime.InteropServices;

class Program {
    [DllImport("user32.dll")]
    private static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);

    private const byte VK_MENU = 0x12;
    private const byte VK_TAB = 0x09;
    private const uint KEYEVENTF_KEYUP = 0x0002;

    static void Main() {
        Console.WriteLine("Space to Exit");
        // Set up a timer to call the AltTabSimulation method every 4 minutes (120000 X 2 milliseconds)
        Timer altTabTimer = new(AltTabSimulation, null, 0, 240000);

        while (true) {
            // Check if a key is pressed
            if (Console.KeyAvailable) {
                // Read the key
                var key = Console.ReadKey(true);
                // Exit if the space key is pressed
                if (key.Key == ConsoleKey.Spacebar) {
                    break;
                }
            }
            // Small sleep to prevent high CPU usage
            Thread.Sleep(100);
        }
        System.Environment.Exit(1);
    }

    private static void AltTabSimulation(object? state) {
        // Press Alt key
        keybd_event(VK_MENU, 0, 0, UIntPtr.Zero);
        // Press Tab key
        keybd_event(VK_TAB, 0, 0, UIntPtr.Zero);
        // Release Tab key
        keybd_event(VK_TAB, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        // Release Alt key
        keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);

        // Do whole thing twice with a pause so it goes back to the first tab
        Thread.Sleep(100);

        // Press Alt key
        keybd_event(VK_MENU, 0, 0, UIntPtr.Zero);
        // Press Tab key
        keybd_event(VK_TAB, 0, 0, UIntPtr.Zero);
        // Release Tab key
        keybd_event(VK_TAB, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
        // Release Alt key
        keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, UIntPtr.Zero);
    }
}