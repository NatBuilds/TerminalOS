from __future__ import annotations

from pathlib import Path
from typing import Any, cast
import shutil

from app.core import config, status

try:  # pragma: no cover - optional dependency
    import cv2  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore[assignment]

try:  # pragma: no cover - optional dependency
    import pytesseract  # type: ignore
    from pytesseract import Output  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore[assignment]
    Output = None  # type: ignore[assignment]


class TesseractOCR:
    def __init__(
        self,
        tesseract_cmd: str | None = None,
        language: str | None = None,
        psm: int | None = None,
        oem: int | None = None,
        timeout: int | None = None,
    ) -> None:
        get_tesseract_cmd = getattr(config, "get_tesseract_cmd", lambda: "tesseract")
        get_ocr_language = getattr(config, "get_ocr_language", lambda: "eng")
        get_ocr_psm = getattr(config, "get_ocr_psm", lambda: 3)
        get_ocr_oem = getattr(config, "get_ocr_oem", lambda: 3)
        get_ocr_timeout = getattr(config, "get_ocr_timeout", lambda: 30)

        self.tesseract_cmd = (tesseract_cmd or get_tesseract_cmd()).strip() or "tesseract"
        self.language = (language or get_ocr_language()).strip() or "eng"
        self.psm = psm if psm is not None else get_ocr_psm()
        self.oem = oem if oem is not None else get_ocr_oem()
        self.timeout = timeout if timeout is not None else get_ocr_timeout()

        if pytesseract is not None:
            cast(Any, pytesseract).pytesseract.tesseract_cmd = self.tesseract_cmd
        else:
            status.warning("pytesseract is not available. Install pytesseract to enable OCR.")

    @staticmethod
    def _pytesseract_api() -> Any:
        return cast(Any, pytesseract)

    @staticmethod
    def _output_api() -> Any:
        return cast(Any, Output)

    def is_available(self) -> bool:
        if pytesseract is None:
            return False

        if shutil.which(str(self.tesseract_cmd)):
            return True

        cmd_path = Path(self.tesseract_cmd)
        return cmd_path.exists() and cmd_path.is_file()

    def _require_tesseract(self) -> bool:
        if pytesseract is None:
            status.error("pytesseract support is unavailable.")
            return False

        if not self.is_available():
            status.error(f"Tesseract executable not found: {self.tesseract_cmd}")
            return False

        return True

    def ocr_config(self) -> str:
        return f"--oem {int(self.oem)} --psm {int(self.psm)}"

    def _load_image(self, image_or_path: Any) -> Any | str | None:
        if isinstance(image_or_path, (str, Path)):
            image_path = Path(image_or_path).expanduser()
            if not image_path.exists():
                status.error(f"OCR image not found: {image_path}")
                return None

            if cv2 is not None:
                image = cv2.imread(str(image_path))
                if image is not None:
                    return image

            return str(image_path)

        return image_or_path

    def extract_text(self, image_or_path: Any, language: str | None = None) -> str:
        if not self._require_tesseract():
            return ""

        image = self._load_image(image_or_path)
        if image is None:
            return ""

        try:
            return self._pytesseract_api().image_to_string(
                image,
                lang=(language or self.language),
                config=self.ocr_config(),
                timeout=self.timeout,
            ).strip()
        except Exception as exc:  # pragma: no cover - defensive
            status.error(f"OCR text extraction failed: {exc}")
            return ""

    def extract_data(self, image_or_path: Any, language: str | None = None) -> dict[str, Any]:
        if not self._require_tesseract() or Output is None:
            return {}

        image = self._load_image(image_or_path)
        if image is None:
            return {}

        try:
            data = self._pytesseract_api().image_to_data(
                image,
                lang=(language or self.language),
                config=self.ocr_config(),
                timeout=self.timeout,
                output_type=self._output_api().DICT,
            )
        except Exception as exc:  # pragma: no cover - defensive
            status.error(f"OCR data extraction failed: {exc}")
            return {}

        return data if isinstance(data, dict) else {}

    def extract_boxes(self, image_or_path: Any, language: str | None = None) -> str:
        if not self._require_tesseract():
            return ""

        image = self._load_image(image_or_path)
        if image is None:
            return ""

        try:
            return self._pytesseract_api().image_to_boxes(
                image,
                lang=(language or self.language),
                config=self.ocr_config(),
                timeout=self.timeout,
            ).strip()
        except Exception as exc:  # pragma: no cover - defensive
            status.error(f"OCR box extraction failed: {exc}")
            return ""

    def extract_pdf(self, image_or_path: Any, language: str | None = None) -> bytes:
        if not self._require_tesseract():
            return b""

        image = self._load_image(image_or_path)
        if image is None:
            return b""

        try:
            return self._pytesseract_api().image_to_pdf_or_hocr(
                image,
                extension="pdf",
                lang=(language or self.language),
                config=self.ocr_config(),
                timeout=self.timeout,
            )
        except Exception as exc:  # pragma: no cover - defensive
            status.error(f"OCR PDF generation failed: {exc}")
            return b""

    def recognize_file(self, path: str, language: str | None = None) -> str:
        return self.extract_text(path, language=language)

