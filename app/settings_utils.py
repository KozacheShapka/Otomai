from __future__ import annotations

import os
from datetime import date

from app.logging import Ansi
from app.logging import log


def read_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


def read_list(value: str) -> list[str]:
    return [v.strip() for v in value.split(",")]

import os


def read_backgrounds(value: str) -> list[str]:
    SEASONAL_BGS = os.getenv("SEASONAL_BGS").split(",")
    result = []
    base_url = "https://assets.kozacheshapka.pp.ua/backgrounds/"

    for path in SEASONAL_BGS:
        path = path.strip()
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                image_files = [
                    f for f in files 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
                ]
                for image_file in image_files:
                    relative_path = os.path.relpath(os.path.join(root, image_file), os.path.dirname(path))
                    url_path = os.path.join(os.path.basename(os.path.dirname(path)), relative_path).replace(os.sep, '/')
                    url = base_url + url_path
                    result.append(url)
                    
    return result

def support_deprecated_vars(
    new_name: str,
    deprecated_name: str,
    *,
    until: date,
    allow_empty_string: bool = False,
) -> str:
    val1 = os.getenv(new_name)
    if val1:
        return val1

    val2 = os.getenv(deprecated_name)
    if val2:
        if until < date.today():
            raise ValueError(
                f'The "{deprecated_name}" config option has been deprecated as of {until.isoformat()} and is no longer supported. Use {new_name} instead.',
            )

        log(
            f'The "{deprecated_name}" config option has been deprecated and will be supported until {until.isoformat()}. Use {new_name} instead.',
            Ansi.LYELLOW,
        )
        return val2

    if allow_empty_string:
        if val1 is not None:
            return val1
        if val2 is not None:
            return val2

    raise KeyError(f"{new_name} is not set in the environment")
