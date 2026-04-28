from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from app.core import status

try:  # pragma: no cover - optional dependency
    import cv2  # type: ignore
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore[assignment]
    np = None  # type: ignore[assignment]


class OpenCVImageTools:
    def __init__(self) -> None:
        self.available = cv2 is not None and np is not None
        if not self.available:
            status.warning("OpenCV is not available. Install opencv-python to enable image tools.")

    def is_available(self) -> bool:
        return self.available

    def _require_cv2(self) -> bool:
        if self.available:
            return True
        status.error("OpenCV support is unavailable.")
        return False

    @staticmethod
    def _cv2_api() -> Any:
        return cast(Any, cv2)

    @staticmethod
    def _np_api() -> Any:
        return cast(Any, np)

    def load_image(self, path: str, flags: int | None = None) -> Any | None:
        if not self._require_cv2():
            return None

        image_path = Path(path).expanduser()
        if not image_path.exists():
            status.error(f"Image not found: {image_path}")
            return None

        cv2_api = self._cv2_api()
        image = cv2_api.imread(str(image_path), cv2_api.IMREAD_COLOR if flags is None else flags)
        if image is None:
            status.error(f"Failed to load image: {image_path}")
        return image

    def save_image(self, path: str, image: Any) -> bool:
        if not self._require_cv2():
            return False

        output_path = Path(path).expanduser()
        if not output_path.parent.exists():
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                status.error(f"Failed to create output folder '{output_path.parent}': {exc}")
                return False

        try:
            return bool(self._cv2_api().imwrite(str(output_path), image))
        except Exception as exc:  # pragma: no cover - defensive
            status.error(f"Failed to save image '{output_path}': {exc}")
            return False

    def create_blank(self, width: int, height: int, color: tuple[int, int, int] = (0, 0, 0)) -> Any | None:
        if not self._require_cv2():
            return None

        np_api = self._np_api()
        return np_api.full((max(1, int(height)), max(1, int(width)), 3), color, dtype=np_api.uint8)

    def to_grayscale(self, image: Any) -> Any | None:
        if not self._require_cv2():
            return None
        cv2_api = self._cv2_api()
        return cv2_api.cvtColor(image, cv2_api.COLOR_BGR2GRAY)

    def blur(self, image: Any, kernel_size: int = 5) -> Any | None:
        if not self._require_cv2():
            return None

        size = max(1, int(kernel_size))
        if size % 2 == 0:
            size += 1
        return self._cv2_api().GaussianBlur(image, (size, size), 0)

    def median_blur(self, image: Any, kernel_size: int = 5) -> Any | None:
        if not self._require_cv2():
            return None

        size = max(1, int(kernel_size))
        if size % 2 == 0:
            size += 1
        return self._cv2_api().medianBlur(image, size)

    def threshold(
        self,
        image: Any,
        threshold_value: int = 127,
        max_value: int = 255,
        threshold_type: int | None = None,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        cv2_api = self._cv2_api()
        mode = threshold_type if threshold_type is not None else cv2_api.THRESH_BINARY
        grayscale = image if len(image.shape) == 2 else self.to_grayscale(image)
        if grayscale is None:
            return None
        _, thresholded = cv2_api.threshold(grayscale, int(threshold_value), int(max_value), mode)
        return thresholded

    def resize(
        self,
        image: Any,
        width: int | None = None,
        height: int | None = None,
        interpolation: int | None = None,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        if width is None and height is None:
            return image

        original_height, original_width = image.shape[:2]
        if width is None:
            scale = int(height) / float(original_height)
            width = int(original_width * scale)
        elif height is None:
            scale = int(width) / float(original_width)
            height = int(original_height * scale)

        cv2_api = self._cv2_api()
        method = interpolation if interpolation is not None else cv2_api.INTER_AREA
        return cv2_api.resize(image, (max(1, int(width)), max(1, int(height))), interpolation=method)

    def rotate(
        self,
        image: Any,
        angle: float,
        center: tuple[int, int] | None = None,
        scale: float = 1.0,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        (height, width) = image.shape[:2]
        rotation_center = center if center is not None else (width // 2, height // 2)
        cv2_api = self._cv2_api()
        matrix = cv2_api.getRotationMatrix2D(rotation_center, float(angle), float(scale))
        return cv2_api.warpAffine(image, matrix, (width, height))

    def crop(self, image: Any, left: int, top: int, width: int, height: int) -> Any | None:
        if not self._require_cv2():
            return None

        x1 = max(0, int(left))
        y1 = max(0, int(top))
        x2 = max(x1, x1 + max(0, int(width)))
        y2 = max(y1, y1 + max(0, int(height)))
        return image[y1:y2, x1:x2]

    def detect_edges(self, image: Any, lower: int = 50, upper: int = 150) -> Any | None:
        if not self._require_cv2():
            return None

        grayscale = image if len(image.shape) == 2 else self.to_grayscale(image)
        if grayscale is None:
            return None
        return self._cv2_api().Canny(grayscale, int(lower), int(upper))

    def draw_text(
        self,
        image: Any,
        text: str,
        position: tuple[int, int] = (10, 30),
        color: tuple[int, int, int] = (0, 255, 0),
        font_scale: float = 1.0,
        thickness: int = 2,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        cv2_api = self._cv2_api()
        return cv2_api.putText(
            image,
            str(text),
            (int(position[0]), int(position[1])),
            cv2_api.FONT_HERSHEY_SIMPLEX,
            float(font_scale),
            color,
            max(1, int(thickness)),
            cv2_api.LINE_AA,
        )

    def draw_rectangle(
        self,
        image: Any,
        top_left: tuple[int, int],
        bottom_right: tuple[int, int],
        color: tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        return self._cv2_api().rectangle(
            image,
            (int(top_left[0]), int(top_left[1])),
            (int(bottom_right[0]), int(bottom_right[1])),
            color,
            max(1, int(thickness)),
        )

    def draw_circle(
        self,
        image: Any,
        center: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        return self._cv2_api().circle(
            image,
            (int(center[0]), int(center[1])),
            max(1, int(radius)),
            color,
            max(1, int(thickness)),
        )

    def normalize_brightness(self, image: Any) -> Any | None:
        if not self._require_cv2():
            return None

        grayscale = image if len(image.shape) == 2 else self.to_grayscale(image)
        if grayscale is None:
            return None
        return self._cv2_api().equalizeHist(grayscale)

    def annotate_box(
        self,
        image: Any,
        left: int,
        top: int,
        width: int,
        height: int,
        label: str,
    ) -> Any | None:
        if not self._require_cv2():
            return None

        annotated = self.draw_rectangle(
            image,
            (left, top),
            (left + width, top + height),
        )
        if annotated is None:
            return None
        return self.draw_text(annotated, label, position=(left, max(0, top - 10)))

