from __future__ import annotations

from pathlib import Path

from app.core import status
from app.core.menu import Menu
from app.libraries.adb import ADBController
from app.libraries.opencv import OpenCVImageTools
from app.libraries.ocr import TesseractOCR


def _read_text(prompt: str) -> str:
    return status.info_input(prompt, show_prefix=False).strip()


def _read_int(prompt: str, default: int | None = None) -> int | None:
    raw_value = _read_text(prompt)
    if not raw_value:
        return default

    try:
        return int(raw_value)
    except ValueError:
        status.warning("Please enter a valid number.")
        return default


def _read_serial() -> str:
    return _read_text("Device serial (blank for default): ")


def adb_show_devices() -> None:
    adb = ADBController()
    if not adb.is_available():
        status.warning("ADB is not available. Install platform-tools and ensure adb is on PATH.")
        return

    adb.start_server()
    devices = adb.devices()
    if not devices:
        status.warning("No connected ADB devices found.")
        return

    for device in devices:
        description = f" - {device.description}" if device.description else ""
        status.success(f"{device.serial} [{device.state}]{description}")


def adb_shell_command() -> None:
    adb = ADBController()
    command = _read_text("Shell command: ")
    if not command:
        status.warning("Shell command cannot be empty.")
        return

    serial = _read_serial() or None
    output = adb.shell(command, serial=serial)
    if output:
        status.success(output)
        return

    status.warning("ADB shell returned no output.")


def adb_talk() -> None:
    adb = ADBController()
    text = _read_text("Text to type on the device: ")
    if adb.talk(text, serial=(_read_serial() or None)):
        status.success("Text sent to device.")


def adb_tap() -> None:
    adb = ADBController()
    x = _read_int("Tap X: ")
    y = _read_int("Tap Y: ")
    if x is None or y is None:
        return

    if adb.tap(x, y, serial=(_read_serial() or None)):
        status.success("Tap command sent.")


def adb_press() -> None:
    adb = ADBController()
    keycode = _read_text("Keycode or key name (for example 3, 4, HOME): ")
    if not keycode:
        status.warning("Keycode cannot be empty.")
        return

    if adb.press(keycode, serial=(_read_serial() or None)):
        status.success("Key press sent.")


def adb_hold() -> None:
    adb = ADBController()
    keycode = _read_text("Keycode or key name to hold: ")
    if not keycode:
        status.warning("Keycode cannot be empty.")
        return

    if adb.hold(keycode, serial=(_read_serial() or None)):
        status.success("Long press sent.")


def adb_swipe() -> None:
    adb = ADBController()
    start_x = _read_int("Start X: ")
    start_y = _read_int("Start Y: ")
    end_x = _read_int("End X: ")
    end_y = _read_int("End Y: ")
    duration = _read_int("Duration in ms (default 300): ", default=300)
    if None in {start_x, start_y, end_x, end_y}:
        return

    duration_ms = duration if duration is not None else 300

    if adb.swipe(start_x, start_y, end_x, end_y, duration_ms=duration_ms, serial=(_read_serial() or None)):
        status.success("Swipe command sent.")


def adb_open_app() -> None:
    adb = ADBController()
    package_name = _read_text("App package name: ")
    if not package_name:
        status.warning("Package name cannot be empty.")
        return

    activity_name = _read_text("Activity name (blank to use launcher): ")
    if adb.open_app(package_name, activity_name or None, serial=(_read_serial() or None)):
        status.success("Open app command sent.")


def adb_check_app_running() -> None:
    adb = ADBController()
    package_name = _read_text("App package name: ")
    if not package_name:
        status.warning("Package name cannot be empty.")
        return

    running = adb.is_app_running(package_name, serial=(_read_serial() or None))
    if running:
        status.success(f"{package_name} is running.")
        return

    status.warning(f"{package_name} is not running.")


def adb_running_processes() -> None:
    adb = ADBController()
    processes = adb.running_processes(serial=(_read_serial() or None))
    if not processes:
        status.warning("No running processes were returned.")
        return

    for line in processes[:20]:
        status.info(line)


def adb_foreground_app() -> None:
    adb = ADBController()
    app_name = adb.current_foreground_app(serial=(_read_serial() or None))
    if app_name:
        status.success(app_name)
        return

    status.warning("Could not determine the foreground app.")


def opencv_process_image() -> None:
    tools = OpenCVImageTools()
    if not tools.is_available():
        return

    image_path = _read_text("Image path: ")
    if not image_path:
        status.warning("Image path cannot be empty.")
        return

    image = tools.load_image(image_path)
    if image is None:
        return

    app_root = Path(__file__).resolve().parents[2]
    output_dir = app_root / "tmp" / "opencv_demo"
    output_dir.mkdir(parents=True, exist_ok=True)

    gray = tools.to_grayscale(image)
    blurred = tools.blur(image, kernel_size=7)
    edges = tools.detect_edges(image)

    outputs: list[tuple[str, object | None]] = [
        ("gray.png", gray),
        ("blurred.png", blurred),
        ("edges.png", edges),
    ]
    saved_any = False
    for filename, output_image in outputs:
        if output_image is None:
            continue
        if tools.save_image(str(output_dir / filename), output_image):
            saved_any = True
            status.success(f"Saved {filename}")

    if not saved_any:
        status.warning("OpenCV did not produce any output files.")


def ocr_extract_text() -> None:
    ocr = TesseractOCR()
    if not ocr.is_available():
        status.warning("Tesseract is not available. Install Tesseract OCR and ensure it is on PATH.")
        return

    image_path = _read_text("OCR image path: ")
    if not image_path:
        status.warning("Image path cannot be empty.")
        return

    language = _read_text("Language (blank for default eng): ") or None
    text = ocr.extract_text(image_path, language=language)
    if text:
        status.success(text)
        return

    status.warning("No OCR text detected.")


def ocr_extract_data() -> None:
    ocr = TesseractOCR()
    if not ocr.is_available():
        status.warning("Tesseract is not available. Install Tesseract OCR and ensure it is on PATH.")
        return

    image_path = _read_text("OCR image path: ")
    if not image_path:
        status.warning("Image path cannot be empty.")
        return

    data = ocr.extract_data(image_path)
    if not data:
        status.warning("No OCR data returned.")
        return

    texts = data.get("text", [])
    for value in texts:
        cleaned = str(value).strip()
        if cleaned:
            status.info(cleaned)


def register(menu) -> None:
    submenu = Menu("Device Tools", exit_label="Back", exit_message="")

    adb_menu = Menu("ADB Utilities", exit_label="Back", exit_message="")
    adb_menu.add("List devices", adb_show_devices)
    adb_menu.add("Run shell command", adb_shell_command)
    adb_menu.add("Send text to device", adb_talk)
    adb_menu.add("Tap screen", adb_tap)
    adb_menu.add("Press key", adb_press)
    adb_menu.add("Hold key", adb_hold)
    adb_menu.add("Swipe screen", adb_swipe)
    adb_menu.add("Open app", adb_open_app)
    adb_menu.add("Check app running", adb_check_app_running)
    adb_menu.add("Show running processes", adb_running_processes)
    adb_menu.add("Show foreground app", adb_foreground_app)

    vision_menu = Menu("Vision Tools", exit_label="Back", exit_message="")
    vision_menu.add("OpenCV image processing", opencv_process_image)
    vision_menu.add("Tesseract OCR text extraction", ocr_extract_text)
    vision_menu.add("Tesseract OCR data output", ocr_extract_data)

    submenu.add("ADB Utilities", adb_menu.run)
    submenu.add("Vision Tools", vision_menu.run)
    menu.add("Device Tools", submenu.run)

