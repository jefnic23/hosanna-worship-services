from datetime import date
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Static


class DateSelector(Static):
    '''A date selector.'''

    def compose(self):
        yield date.today()


class HosannaWorshipServices(App):
    '''Textual interface for creating worship services.'''
    
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode')]
    
    def compose(self) -> ComposeResult:
        '''Compose the main view.'''
        yield Header()
        yield Footer()
        yield Container(DateSelector())
        
    def action_toggle_dark(self) -> None:
        '''Toggle dark mode.'''
        self.dark = not self.dark