from collections import deque

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static
from textual import events

from Structs import *

class MiniCityApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #main_panels {
        height: 95%;
        layout: horizontal;
    }
    #info_panel {
        height: 5%;
        border: round red;
    }
    #left_panel {
        width: 50%;
        layout: vertical;
    }
    #right_panel {
        width: 50%;
        layout: vertical;
    }
    #messages_scroll {
        height: 70%;
        border: round $accent;
    }
    #questions_panel {
        height: 30%;
        border: round yellow;
    }
    #speaker_description_panel {
        height: 40%;
        border: round green;
    }
    #room_description_panel {
        height: 30%;
        border: round green;
    }
    #commands_panel {
        height: 30%;
        border: round magenta;
    }
    """

# ----------------- Textual hooks below -------------------------

    # allow pressing “z” to quit. [key, action name, description]
    BINDINGS = [("z", "quit", "Quit the app")]

    # this makes our left and right halfs of the screen, divided into component sections. 1st to run
    def compose(self) -> ComposeResult:
        # main split area (95% height)
        yield Vertical(
            # left + right columns
            Vertical(
                Vertical(
                    VerticalScroll(
                        Static("Messages:\n", id="messages_header"),
                        id="messages_scroll"
                    ),
                    Static("", id="questions_panel"),
                    id="left_panel"
                ),
                Vertical(
                    Static("", id="speaker_description_panel"),
                    Static("", id="room_description_panel"),
                    Static("", id="commands_panel"),
                    id="right_panel"
                ),
                id="main_panels"
            ),
            # bottom info panel (5% height)
            Static("Press Z to quit • Use 1–4 or Q–R for actions", id="info_panel")
        )

    # runs before first frame. Pre-setup here. 2nd to run
    def on_mount(self):

        self.messages = deque([], maxlen=50)

        #Check for saved game
        save = load_city()
        if save == "None":
            self.city = City()
            self.first_start()
        else:
            self.city = save
            self.continued_start()

        self.question_index = ["Main",0]
        self.command_index = ["Main",0]

        # separate data sets and index tracking
        self.question_sets = Questions(self.question_index)
        self.command_sets = Commands(self.command_index)

    # called once the UI is mounted. Populates panel content. returns any error to the message pane. Is the 3rd textual hook after first frame render
    def on_ready(self):
        try:
            self.update_message_panel()
            self.update_questions_panel()
            self.update_commands_panel()
            self.update_speaker_description_panel()
            self.update_room_description_panel()
        except Exception as e:
            # If anything fails here, log to the message pane so the app doesn't crash immediately.
            err = str(e).replace("[", "(").replace("]", ")")
            self.messages.append(f"- ERROR initial update: {err}")
            # We try one more time just to show the pane:
            try:
                self.update_message_panel()
            except:
                pass
    
    # called when a non-bound key is pressed
    def on_key(self, event: events.Key) -> None:
        self.Question_and_Command_manager(event)

# ----------------- Custom functions below -------------------------

    # populate the scrollable messages container with up to 50 messages
    def update_message_panel(self):
        scroll = self.query_one("#messages_scroll", VerticalScroll)

        # 1) remove all children after the header
        for child in list(scroll.children)[1:]:
            child.remove()

        # 2) mount messages newest-first so they appear just under the header
        for msg in reversed(self.messages):
            safe = msg.replace("[", "(").replace("]", ")")
            scroll.mount(Static(safe))

    # update the questions list based on the current index.
    def update_questions_panel(self):
        text = "Questions:\n\n" + "\n".join(Questions(self.question_index))
        self.query_one("#questions_panel", Static).update(text)

    # update the commands list based on the current index.
    def update_commands_panel(self):
        text = "Commands:\n\n" + "\n".join(Commands(self.command_index))
        self.query_one("#commands_panel", Static).update(text)

    # updates speaker description panel with latest information about the speaker.
    def update_speaker_description_panel(self):
        text = "Speaker Description:\n\n" + "The head elder is an old man with a robe and glasses. He looks around 70"
        self.query_one("#speaker_description_panel", Static).update(text)

    # updates room description panel with latest information about the room.
    def update_room_description_panel(self):
        text = "Room Description:\n\n" + "The portal room is dark and quiet. The only person here is the head elder."
        self.query_one("#room_description_panel", Static).update(text)

    # handle number presses to append new messages or cycle command sets.
    # currently % by 2 to support a main and alt for each, but probably need to dynamically define the length of each page later
    def Question_and_Command_manager(self, event: events.Key) -> None:
        key = event.key.lower()

        #self.messages.append(f"debug:{self.question_index, key, self.speaker}")

        if key == "5":
            self.question_index[1] = (self.question_index[1] + 1) % 2
            self.update_questions_panel()
        elif key == "t":
            self.command_index[1] = (self.command_index[1] + 1) % 2
            self.update_commands_panel()
        elif key in ["1","2","3","4","q","w","e","r"]:
            self.messages.append(f"{timestamp()} {question_responses(self.question_index, key, self.city)}")
            self.update_message_panel()

    def first_start(self):
        self.messages.appendleft(f"{timestamp()} Hello There! Are you our destined leader")
        self.messages.appendleft(f"{timestamp()} This is the town of Jain. We need your help")
        save_city(self.city)

    def continued_start(self):
        self.messages.appendleft(f"{timestamp()} The head elder approaches the portal")
        self.messages.appendleft(f"{timestamp()} My liege! You return!")

if __name__ == "__main__":
    MiniCityApp().run()