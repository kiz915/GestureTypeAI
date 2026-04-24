class VirtualKeyboard:
    """
    Tracks typed text from gestures and manages the virtual keyboard state.
    """

    def __init__(self):
        self.text = ""
        self.history = []
        self.max_history = 50

    def add_letter(self, letter):
        """Add a detected letter/command to the typed text."""
        if letter == "SPACE":
            self.text += " "
            self.history.append(("SPACE", " "))
        elif letter == "BACKSPACE":
            if self.text:
                removed = self.text[-1]
                self.text = self.text[:-1]
                self.history.append(("BACKSPACE", removed))
        elif letter and letter != "?":
            self.text += letter
            self.history.append((letter, letter))

        # Keep history manageable
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return self.text

    def clear(self):
        self.text = ""
        self.history = []

    def get_text(self):
        return self.text

    def get_word_count(self):
        return len(self.text.split()) if self.text.strip() else 0

    def get_char_count(self):
        return len(self.text)
