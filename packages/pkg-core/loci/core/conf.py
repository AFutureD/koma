from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URI: str


class LazySettings(Settings):
    _wrapped: None | Settings = None

    def __getattr__(self, item):
        if self._wrapped is None:
            raise RuntimeError("Settings not configured")

        return getattr(self._wrapped, item)

    def configure(self, value: Settings):
        self._wrapped = value


settings = LazySettings()
