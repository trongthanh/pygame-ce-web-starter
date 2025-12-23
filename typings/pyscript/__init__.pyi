"""Type stubs for PyScript runtime APIs."""
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

def when(event_type: str, selector: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to bind a Python function to a DOM event.

    Args:
        event_type: The type of event (e.g., 'click', 'input', 'change')
        selector: CSS selector for the target element(s)

    Returns:
        Decorator function
    """
    ...

class Window:
    """Represents the browser window object."""
    def alert(self, message: str) -> None: ...
    def confirm(self, message: str) -> bool: ...
    def prompt(self, message: str, default: str = "") -> str | None: ...

window: Window

class Document:
    """Represents the browser document object."""
    def getElementById(self, id: str) -> Any: ...
    def querySelector(self, selector: str) -> Any: ...
    def querySelectorAll(self, selector: str) -> list[Any]: ...
    def createElement(self, tag: str) -> Any: ...

document: Document

def fetch(url: str, **kwargs: Any) -> Any:
    """Fetch a resource from the network."""
    ...

class RUNNING:
    """PyScript running state."""
    ...

class COMPLETE:
    """PyScript complete state."""
    ...

__version__: str
