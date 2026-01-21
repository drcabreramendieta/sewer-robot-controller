class CameraSelectorSignal:
    def __init__(self) -> None:
        self._use_expansion = False

    def set_expansion_mode(self, enabled: bool) -> None:
        self._use_expansion = bool(enabled)

    def selector_key(self) -> str:
        return "b" if self._use_expansion else "a"
