"""
ADB Screenshot Analysis Module
================================

This module demonstrates how to use all three new libraries together:
1. ADB Controller - to capture a device screenshot
2. OpenCV Image Tools - to analyze and process the image
3. Tesseract OCR - to extract text from the screenshot

This is a practical example showing best practices for combining
device automation with computer vision and OCR workflows.
"""

from __future__ import annotations

from pathlib import Path

from app.core import status
from app.core.menu import Menu
from app.libraries.adb import ADBController
from app.libraries.opencv import OpenCVImageTools
from app.libraries.ocr import TesseractOCR


def adb_screenshot_and_read() -> None:
    """
    Main handler: Capture device screenshot and analyze it comprehensively.

    Workflow:
    1. Connect to ADB device
    2. Capture screenshot
    3. Process with OpenCV (grayscale, edges, etc.)
    4. Extract text with Tesseract OCR
    5. Display results
    """

    # ============================================================================
    # STEP 1: Initialize ADB Controller
    # ============================================================================
    # Why: We need a controller instance to interact with the connected device.
    # The constructor automatically loads config values for:
    # - adb_executable: path to adb binary (default: "adb")
    # - device_serial: target device (empty = first device)
    # - timeout: command timeout in seconds (default: 30)
    #
    adb = ADBController()

    # Verify ADB is available on the system
    if not adb.is_available():
        status.error("ADB is not available. Ensure platform-tools is installed.")
        return

    status.info("ADB is available")

    # ============================================================================
    # STEP 2: List devices and select target (or use default)
    # ============================================================================
    # Why: Useful for users with multiple devices to understand what's available
    # and optionally choose a specific device.
    #
    devices = adb.devices()
    if not devices:
        status.warning("No ADB devices connected.")
        return

    status.success(f"Found {len(devices)} device(s)")
    for device in devices:
        status.info(f"  - {device.serial} [{device.state}]")

    # For this demo, we use the first device (or config default)
    # In a real scenario, you might prompt the user to choose
    target_serial = devices[0].serial if devices else None

    # ============================================================================
    # STEP 3: Create output directory for screenshots
    # ============================================================================
    # Why: Organize outputs in a dedicated folder for easy access and cleanup
    # Use Path() for cross-platform compatibility (Windows/Linux/macOS)
    #
    app_root = Path(__file__).resolve().parents[2]  # Navigate to app root
    screenshots_dir = app_root / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    status.debug(f"Screenshots directory: {screenshots_dir}")

    # ============================================================================
    # STEP 4: Capture screenshot via ADB
    # ============================================================================
    # Why: ADBController.screenshot() handles the entire workflow:
    # - Executes 'screencap' on device
    # - Pulls image via 'adb pull'
    # - Cleans up temp file on device
    # - Saves to local path
    #
    screenshot_path = screenshots_dir / "device_screenshot.png"
    status.info("Capturing screenshot from device...")

    if not adb.screenshot(str(screenshot_path), serial=target_serial):
        status.error("Failed to capture screenshot from device.")
        return

    if not screenshot_path.exists():
        status.error(f"Screenshot was not saved to {screenshot_path}")
        return

    status.success(f"Screenshot saved: {screenshot_path}")

    # ============================================================================
    # STEP 5: Initialize OpenCV for image processing
    # ============================================================================
    # Why: OpenCV provides low-level image operations
    # - Preprocessing (blur, threshold) improves OCR accuracy
    # - Edge detection reveals UI structure
    # - Grayscale conversion reduces data and improves analysis speed
    #
    cv = OpenCVImageTools()

    if not cv.is_available():
        status.warning("OpenCV not available. Skipping image processing.")
        cv = None
    else:
        status.info("OpenCV initialized")

    # ============================================================================
    # STEP 6: Load and process the screenshot with OpenCV
    # ============================================================================
    # Why: Different transformations serve different purposes:
    # - Grayscale: Reduces complexity, needed for Tesseract
    # - Blur: Reduces noise, improves OCR accuracy
    # - Edges: Reveals UI boundaries and structural elements
    # - These can be saved for visual debugging
    #
    if cv is not None:
        status.info("Processing image with OpenCV...")

        # Load the screenshot
        image = cv.load_image(str(screenshot_path))
        if image is None:
            status.error("Failed to load screenshot with OpenCV")
            cv = None
        else:
            # Create grayscale version (better for OCR)
            gray_image = cv.to_grayscale(image)
            if gray_image is not None:
                cv.save_image(str(screenshots_dir / "processed_grayscale.png"), gray_image)
                status.debug("Saved grayscale version")

            # Create blurred version (reduces noise)
            blurred_image = cv.blur(image, kernel_size=5)
            if blurred_image is not None:
                cv.save_image(str(screenshots_dir / "processed_blurred.png"), blurred_image)
                status.debug("Saved blurred version")

            # Detect edges (reveals UI structure)
            edges_image = cv.detect_edges(image, lower=50, upper=150)
            if edges_image is not None:
                cv.save_image(str(screenshots_dir / "processed_edges.png"), edges_image)
                status.debug("Saved edge detection")
                status.info("Image processing complete")

    # ============================================================================
    # STEP 7: Initialize Tesseract OCR
    # ============================================================================
    # Why: Tesseract is the industry-standard open-source OCR engine
    # It can:
    # - Extract text with high accuracy
    # - Work with preprocessed images
    # - Support multiple languages
    # - Return confidence scores and bounding boxes
    #
    ocr = TesseractOCR()
    ocr_data = None

    if not ocr.is_available():
        status.warning("Tesseract OCR not available. Skipping OCR.")
        ocr = None
    else:
        status.info("Tesseract OCR initialized")

    # ============================================================================
    # STEP 8: Extract text from screenshot with OCR
    # ============================================================================
    # Why: OCR converts visual text to machine-readable text
    # This enables:
    # - UI automation based on text content
    # - Screen reading/accessibility
    # - Automated testing of app text
    #
    if ocr is not None:
        status.info("Extracting text with Tesseract...")

        # Extract plain text
        extracted_text = ocr.extract_text(str(screenshot_path))

        if extracted_text:
            status.success("OCR Text Extraction Result:")
            # Display in chunks for readability
            for line in extracted_text.split("\n")[:20]:  # First 20 lines
                if line.strip():
                    status.info(f"  {line}")
            if len(extracted_text.split('\n')) > 20:
                status.info("  ... (more text)")
        else:
            status.warning("No text detected on screen")

        # Extract detailed data (positions, confidence scores)
        # Why: Knowing WHERE text is helps with UI automation and analysis
        status.info("Extracting detailed OCR data...")
        ocr_data = ocr.extract_data(str(screenshot_path))

        if ocr_data:
            # Parse the data dictionary
            texts = ocr_data.get("text", [])
            confidences = ocr_data.get("conf", [])

            # Filter out empty results and show high-confidence detections
            detected_items = [
                (text, conf)
                for text, conf in zip(texts, confidences)
                if text.strip() and float(conf) > 50  # Confidence > 50%
            ]

            if detected_items:
                status.success(f"Detected {len(detected_items)} high-confidence text items:")
                for text, conf in detected_items[:15]:  # Show top 15
                    status.info(f"  '{text}' (confidence: {conf}%)")
                if len(detected_items) > 15:
                    status.info(f"  ... and {len(detected_items) - 15} more items")
            else:
                status.warning("No high-confidence text detected")
        else:
            status.warning("Could not extract detailed OCR data")

    # ============================================================================
    # STEP 9: Display analysis summary
    # ============================================================================
    # Why: Users need to know what was accomplished and what the results mean
    #
    status.success("\n=== Analysis Summary ===")
    status.info(f"Screenshot: {screenshot_path}")
    status.info(f"Processed Images:")
    status.info(f"  - Grayscale: {screenshots_dir / 'processed_grayscale.png'}")
    status.info(f"  - Blurred: {screenshots_dir / 'processed_blurred.png'}")
    status.info(f"  - Edges: {screenshots_dir / 'processed_edges.png'}")

    if ocr_data and "text" in ocr_data:
        status.info(f"OCR Results: {len([t for t in ocr_data['text'] if t.strip()])} text elements found")

    status.info("All files saved to: " + str(screenshots_dir))


def demo_adb_screenshot_menu() -> None:
    """
    Creates a submenu showing different screenshot analysis options.
    This demonstrates how to organize related functionality.
    """
    submenu = Menu("Screenshot Analysis", exit_label="Back", exit_message="")
    submenu.add("Capture and Analyze", adb_screenshot_and_read)

    # In a real application, you might have options like:
    # submenu.add("Analyze existing screenshot", analyze_existing_screenshot)
    # submenu.add("Batch process screenshots", batch_process_screenshots)
    # submenu.add("Compare screenshots", compare_screenshots)

    submenu.run()


def register(menu) -> None:
    """
    Register the screenshot analysis module with the main menu.

    This function is called automatically by app/main.py when discovering
    modules. It should add items to the provided menu object.
    """
    menu.add("ADB Screenshot and read", demo_adb_screenshot_menu)

