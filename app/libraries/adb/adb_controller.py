from __future__ import annotations

from dataclasses import dataclass
import subprocess
from pathlib import Path

from app.core import config, status


@dataclass(slots=True)
class ADBDeviceInfo:
    serial: str
    state: str = "unknown"
    description: str = ""


class ADBController:
    def __init__(
        self,
        adb_executable: str | None = None,
        device_serial: str | None = None,
        timeout: int | None = None,
    ) -> None:
        get_adb_executable = getattr(config, "get_adb_executable", lambda: "adb")
        get_adb_device_serial = getattr(config, "get_adb_device_serial", lambda: "")
        get_adb_timeout = getattr(config, "get_adb_timeout", lambda: 30)

        self.adb_executable = (adb_executable or get_adb_executable()).strip() or "adb"
        self.device_serial = (device_serial if device_serial is not None else get_adb_device_serial()).strip()
        self.timeout = timeout if timeout is not None else get_adb_timeout()

    def _resolve_serial(self, serial: str | None = None) -> str:
        return (serial if serial is not None else self.device_serial).strip()

    def _base_command(self, serial: str | None = None) -> list[str]:
        command = [self.adb_executable]
        resolved_serial = self._resolve_serial(serial)
        if resolved_serial:
            command.extend(["-s", resolved_serial])
        return command

    def _run(
        self,
        *args: str,
        serial: str | None = None,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str] | None:
        command = self._base_command(serial)
        command.extend(str(arg) for arg in args)
        status.debug(f"ADB command: {' '.join(command)}")

        try:
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                check=check,
            )
        except FileNotFoundError:
            status.error(f"ADB executable not found: {self.adb_executable}")
        except subprocess.TimeoutExpired:
            status.error(f"ADB command timed out after {self.timeout} seconds.")
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or exc.stdout or str(exc)).strip()
            status.error(f"ADB command failed: {stderr}")
        except OSError as exc:
            status.error(f"ADB command failed: {exc}")
        return None

    @staticmethod
    def _clean_output(output: str | None) -> str:
        return (output or "").strip()

    def is_available(self) -> bool:
        result = self._run("version")
        return bool(result and result.returncode == 0)

    def start_server(self) -> bool:
        result = self._run("start-server")
        return bool(result and result.returncode == 0)

    def kill_server(self) -> bool:
        result = self._run("kill-server")
        return bool(result and result.returncode == 0)

    def devices(self) -> list[ADBDeviceInfo]:
        result = self._run("devices", "-l")
        if result is None:
            return []

        devices: list[ADBDeviceInfo] = []
        for raw_line in self._clean_output(result.stdout).splitlines():
            line = raw_line.strip()
            if not line or line.startswith("List of devices attached"):
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            serial = parts[0]
            state = parts[1]
            description = " ".join(parts[2:]) if len(parts) > 2 else ""
            devices.append(ADBDeviceInfo(serial=serial, state=state, description=description))

        return devices

    def connect(self, host: str, port: int = 5555) -> bool:
        endpoint = host.strip()
        if not endpoint:
            status.warning("ADB connect requires a host.")
            return False

        result = self._run("connect", f"{endpoint}:{port}")
        return bool(result and result.returncode == 0)

    def disconnect(self, serial: str | None = None) -> bool:
        resolved_serial = self._resolve_serial(serial)
        if resolved_serial:
            result = self._run("disconnect", resolved_serial)
        else:
            result = self._run("disconnect")
        return bool(result and result.returncode == 0)

    def shell(self, command: str, serial: str | None = None) -> str:
        shell_command = (command or "").strip()
        if not shell_command:
            return ""

        result = self._run("shell", shell_command, serial=serial)
        if result is None:
            return ""

        if result.returncode != 0:
            stderr = self._clean_output(result.stderr) or self._clean_output(result.stdout)
            if stderr:
                status.error(stderr)
            return ""

        return self._clean_output(result.stdout)

    def talk(self, text: str, serial: str | None = None) -> bool:
        content = (text or "").strip()
        if not content:
            status.warning("ADB talk requires text.")
            return False

        sanitized = content.replace(" ", "%s")
        result = self._run("shell", "input", "text", sanitized, serial=serial)
        return bool(result and result.returncode == 0)

    def tap(self, x: int, y: int, serial: str | None = None) -> bool:
        result = self._run("shell", "input", "tap", str(int(x)), str(int(y)), serial=serial)
        return bool(result and result.returncode == 0)

    def press(self, keycode: str | int, serial: str | None = None) -> bool:
        result = self._run("shell", "input", "keyevent", str(keycode), serial=serial)
        return bool(result and result.returncode == 0)

    def hold(self, keycode: str | int, serial: str | None = None) -> bool:
        result = self._run("shell", "input", "keyevent", "--longpress", str(keycode), serial=serial)
        if result and result.returncode == 0:
            return True
        return self.press(keycode, serial=serial)

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int = 300,
        serial: str | None = None,
    ) -> bool:
        result = self._run(
            "shell",
            "input",
            "swipe",
            str(int(start_x)),
            str(int(start_y)),
            str(int(end_x)),
            str(int(end_y)),
            str(max(0, int(duration_ms))),
            serial=serial,
        )
        return bool(result and result.returncode == 0)

    def open_app(
        self,
        package_name: str,
        activity_name: str | None = None,
        serial: str | None = None,
    ) -> bool:
        package = package_name.strip()
        if not package:
            status.warning("ADB open_app requires a package name.")
            return False

        if activity_name and activity_name.strip():
            component = f"{package}/{activity_name.strip()}"
            result = self._run("shell", "am", "start", "-n", component, serial=serial)
        else:
            result = self._run(
                "shell",
                "monkey",
                "-p",
                package,
                "-c",
                "android.intent.category.LAUNCHER",
                "1",
                serial=serial,
            )

        return bool(result and result.returncode == 0)

    def is_app_running(self, package_name: str, serial: str | None = None) -> bool:
        package = package_name.strip()
        if not package:
            return False

        pidof_output = self.shell(f"pidof {package}", serial=serial)
        if pidof_output:
            return True

        ps_output = self.shell(f"ps -A | grep {package}", serial=serial)
        return bool(ps_output)

    def running_processes(self, serial: str | None = None) -> list[str]:
        result = self.shell("ps -A", serial=serial)
        if not result:
            result = self.shell("ps", serial=serial)
        return [line for line in result.splitlines() if line.strip()]

    def current_foreground_app(self, serial: str | None = None) -> str:
        output = self.shell("dumpsys activity activities | grep mResumedActivity", serial=serial)
        if not output:
            output = self.shell("dumpsys window windows | grep mCurrentFocus", serial=serial)

        if not output:
            return ""

        tokens = output.replace("=", " ").replace("/", " ").split()
        for token in tokens:
            if "." in token and "/" not in token:
                return token.strip()
        return output.strip()

    def screenshot(self, output_path: str, serial: str | None = None) -> bool:
        destination = Path(output_path).expanduser()
        if not destination.parent.exists():
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                status.error(f"Failed to prepare screenshot folder '{destination.parent}': {exc}")
                return False

        remote_path = "/sdcard/__terminalos_screenshot.png"

        # Execute screencap on device
        status.debug(f"Executing: screencap -p {remote_path}")
        screencap_output = self.shell(f"screencap -p {remote_path}", serial=serial)
        # screencap returns empty output on success, so check if it didn't error
        # (shell() would log an error if command failed)

        # Verify file was created on device
        status.debug(f"Verifying screenshot exists on device...")
        verify_output = self.shell(f"test -f {remote_path} && echo SUCCESS", serial=serial)
        if "SUCCESS" not in verify_output:
            status.error(f"Screenshot was not created on device at {remote_path}")
            status.debug(f"Verify result: '{verify_output}'")
            return False

        # Pull the file from device
        status.debug(f"Pulling screenshot from {remote_path} to {destination}")
        pulled = self._run("pull", remote_path, str(destination), serial=serial)
        if not pulled or pulled.returncode != 0:
            stderr = (pulled.stderr or "").strip() if pulled else "Unknown error"
            status.error(f"Failed to pull screenshot: {stderr}")
            status.debug(f"Pull command returned: {pulled.returncode if pulled else 'None'}")
            return False

        # Verify file was saved locally
        if not destination.exists():
            status.error(f"Screenshot file was not saved to {destination}")
            return False

        file_size = destination.stat().st_size
        status.debug(f"Screenshot saved successfully ({file_size} bytes)")

        # Clean up device file
        self.shell(f"rm {remote_path}", serial=serial)
        return True

    def install(self, apk_path: str, serial: str | None = None) -> bool:
        path = Path(apk_path).expanduser()
        if not path.exists():
            status.warning(f"APK not found: {path}")
            return False

        result = self._run("install", str(path), serial=serial)
        return bool(result and result.returncode == 0)

    def uninstall(self, package_name: str, keep_data: bool = False, serial: str | None = None) -> bool:
        package = package_name.strip()
        if not package:
            return False

        args = ["uninstall"]
        if keep_data:
            args.append("-k")
        args.append(package)
        result = self._run(*args, serial=serial)
        return bool(result and result.returncode == 0)

    def reboot(self, mode: str | None = None, serial: str | None = None) -> bool:
        args = ["reboot"]
        if mode and mode.strip():
            args.append(mode.strip())
        result = self._run(*args, serial=serial)
        return bool(result and result.returncode == 0)

    def pull(self, remote_path: str, local_path: str, serial: str | None = None) -> bool:
        result = self._run("pull", remote_path, local_path, serial=serial)
        return bool(result and result.returncode == 0)

    def push(self, local_path: str, remote_path: str, serial: str | None = None) -> bool:
        result = self._run("push", local_path, remote_path, serial=serial)
        return bool(result and result.returncode == 0)

    def format_devices(self) -> str:
        devices = self.devices()
        if not devices:
            return "No devices found."

        lines = [f"{device.serial} [{device.state}] {device.description}".strip() for device in devices]
        return "\n".join(lines)

