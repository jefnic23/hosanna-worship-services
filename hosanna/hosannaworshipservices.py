from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class HosannaWorshipServices(App):
    '''Textual interface for creating worship services.'''
    
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]
    
    def compose(self) -> ComposeResult:
        '''Compose the main view.'''
        yield Header()
        yield Footer()
        
    def action_toggle_dark(self) -> None:
        '''Toggle dark mode.'''
        self.dark = not self.dark