from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


class UserDataPathsTests(unittest.TestCase):
    def test_initialize_user_data_copies_bundled_settings_to_local_app_data(self) -> None:
        from core import paths

        with TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / "template.json"
            template_path.write_text('{"timezone": "America/Mexico_City"}', encoding="utf-8")

            with patch.dict(os.environ, {"LOCALAPPDATA": temp_dir}, clear=False):
                with patch.object(paths, "BUNDLED_CONFIG_PATH", template_path):
                    user_data_dir = paths.initialize_user_data()

            self.assertEqual(user_data_dir, Path(temp_dir) / "PIT ALERT")
            self.assertEqual(
                json.loads((user_data_dir / "settings.json").read_text(encoding="utf-8")),
                {"timezone": "America/Mexico_City"},
            )

    def test_initialize_user_data_preserves_existing_settings(self) -> None:
        from core import paths

        with TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / "template.json"
            template_path.write_text('{"sound_enabled": true}', encoding="utf-8")
            settings_path = Path(temp_dir) / "PIT ALERT" / "settings.json"
            settings_path.parent.mkdir()
            settings_path.write_text('{"sound_enabled": false}', encoding="utf-8")

            with patch.dict(os.environ, {"LOCALAPPDATA": temp_dir}, clear=False):
                with patch.object(paths, "BUNDLED_CONFIG_PATH", template_path):
                    paths.initialize_user_data()

            self.assertEqual(
                json.loads(settings_path.read_text(encoding="utf-8")),
                {"sound_enabled": False},
            )

    def test_initialize_user_data_copies_bundled_cache_once(self) -> None:
        from core import paths

        with TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / "template.json"
            cache_template_path = Path(temp_dir) / "cache.json"
            template_path.write_text("{}", encoding="utf-8")
            cache_template_path.write_text('{"events": []}', encoding="utf-8")

            with patch.dict(os.environ, {"LOCALAPPDATA": temp_dir}, clear=False):
                with patch.object(paths, "BUNDLED_CONFIG_PATH", template_path):
                    with patch.object(paths, "BUNDLED_CACHE_PATH", cache_template_path):
                        paths.initialize_user_data()

            self.assertEqual(
                json.loads(
                    (Path(temp_dir) / "PIT ALERT" / "data" / "cache" / "forexfactory_thisweek.json").read_text(
                        encoding="utf-8"
                    )
                ),
                {"events": []},
            )

    def test_settings_and_cache_paths_are_inside_user_data_directory(self) -> None:
        from core import paths

        with TemporaryDirectory() as temp_dir:
            with patch.dict(os.environ, {"LOCALAPPDATA": temp_dir}, clear=False):
                self.assertEqual(
                    paths.get_settings_path(),
                    Path(temp_dir) / "PIT ALERT" / "settings.json",
                )
                self.assertEqual(
                    paths.get_cache_path(),
                    Path(temp_dir) / "PIT ALERT" / "data" / "cache" / "forexfactory_thisweek.json",
                )


if __name__ == "__main__":
    unittest.main()
