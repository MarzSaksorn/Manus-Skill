---
name: uti120m-thermal-companion
description: Build or extend an Android companion app for the UNI-T UTi120M USB thermal camera. Use when connecting the camera to phones or tablets, implementing the USB bridge, rendering local thermal previews, adding calibrated capture, or handing thermal records to a web app.
---

# UNI-T UTi120M companion workflow

Use this skill to implement a native Android bridge between the UNI-T UTi120M and a clinical or industrial web app. Treat the camera as a custom USB sensor, not as a webcam.

## Non-negotiable safety boundary

- Keep raw sensor counts visibly labeled as **raw** and **not Celsius** until shutter/NUC correction and factory calibration conversion are implemented and verified on real hardware.
- Never call raw-count or colorized JPEG output a temperature measurement.
- Keep automated results labeled **Decision Support**, not diagnosis.
- Do not send patient-identifiable data to external AI services.
- Do not delete clinical records or change production schemas without explicit confirmation.
- Validate the companion with a physical camera before claiming end-to-end support.

## Workflow

1. **Inspect the host project and target devices.**
   - Identify whether the companion is native Android, Expo, Capacitor, or another shell.
   - Prefer native Android USB host APIs for the first hardware path.
   - Confirm the target phone/tablet has USB host/OTG support and a data-capable cable.
   - Keep the existing web app separate from the hardware layer.

2. **Research the official app and protocol.**
   - Check UNI-T's official Thermal Mobile app and product documentation first.
   - Treat Thermal Mobile as a closed end-user viewer unless UNI-T documents an SDK, service, export contract, or live-data API.
   - Do not scrape or control the official app as the production bridge.
   - If needed, inspect the maintained reverse-engineering reference in `references/uti120m-protocol.md` and validate assumptions against the camera.

3. **Create the native USB foundation.**
   - Declare `android.hardware.usb.host` in the manifest.
   - Add an attachment filter for VID `0x5656` and PID `0x1201`.
   - Discover devices with `UsbManager`, request permission with a user-visible action, open with `openDevice`, and claim the camera interfaces.
   - Keep USB I/O off the main thread. Use a single serialized I/O executor.
   - Release interfaces, stop streaming, and close the connection on disconnect and activity teardown.

4. **Implement raw frame transport.**
   - Enter image-upload mode only after the device is claimed.
   - Request frames with the documented command and read the complete 25,600-byte packet.
   - Validate frame magic and dimensions before exposing a frame to UI code.
   - Parse the 120 × 90 Y16 pixel plane and header values into an immutable frame model.
   - Report transfer errors and incomplete packets. Do not silently turn partial frames into images.

5. **Add local real-time preview.**
   - Render frames locally in a custom Android `View`, `Bitmap`, or equivalent efficient surface.
   - Preserve the 4:3 sensor aspect ratio and avoid allocating a new bitmap per frame.
   - Use a clearly labeled false-color palette for raw-count visibility.
   - Show a placeholder before connection and clear the preview after disconnect.
   - Include connection state, frame counter, dimensions, and raw-count range.
   - Keep the page scroll-safe on small phones.
   - Do not display a Celsius legend until calibrated conversion exists.

6. **Add calibration before measurement.**
   - Implement device calibration-package reads, shutter/NUC correction, bad-pixel and gain correction, lens/FPA compensation, emissivity, and temperature conversion as a separate layer.
   - Test warm-up, shutter refresh, low/high range switching, reconnects, and malformed frames.
   - Store calibration version and capture metadata with every calibrated capture.

7. **Bridge captures to the web app.**
   - Prefer authenticated HTTPS upload from the companion directly to the web backend.
   - Send the false-color preview plus the original calibrated temperature matrix and metadata.
   - Use a dedicated thermal-capture contract; do not silently route thermal data through an RGB wound-inference endpoint.
   - Bind captures to a patient and wound assessment only after showing a confirmation step.
   - Store image bytes and matrix artifacts in protected object storage. Keep searchable metadata and derived statistics in the database.
   - Record clinician, device serial, calibration version, timestamp, emissivity, ambient temperature, distance, and audit event.

8. **Validate and deliver.**
   - Run the Android debug build, parser smoke tests, XML checks, and `git diff --check`.
   - Install the APK on a real OTG-capable Android device and verify the physical camera path.
   - Capture logs for permission denial, missing device, endpoint failure, disconnect, reconnect, and partial frames.
   - Update README with the exact hardware-test boundary.
   - Commit with a focused message, push to the authenticated GitHub remote, and save a project checkpoint.

## Preferred architecture

```text
UTi120M → Android native USB layer → calibrated thermal model
                                      ├─ local preview
                                      └─ authenticated HTTPS upload
                                                ↓
                                      web app + protected storage
```

Keep the browser responsible for patient records, review, assignment, audit history, and web workflows. Keep the Android companion responsible for USB access, frame acquisition, calibration, and local preview.

## Implementation contract

Use a dedicated thermal capture payload with fields equivalent to:

```ts
{
  patientId,
  woundAssessmentId,
  capturedAt,
  previewImage,
  temperatureMap,
  width: 120,
  height: 90,
  unit: "C",
  emissivity,
  ambientTemperatureC,
  distanceM,
  fpaTemperatureC,
  shutterTemperatureC,
  lensTemperatureC,
  frameCounter,
  deviceSerial,
  calibrationVersion,
  bridgeVersion,
}
```

Reject a calibrated capture when the matrix dimensions, unit, calibration version, or required metadata are missing. Keep a separate raw-preview path for hardware validation.

## Testing checklist

### Source-level

- Parser accepts a valid 25,600-byte frame with `0xAA55` magic.
- Parser rejects incomplete frames, invalid magic, and unexpected width.
- Unsigned 16-bit pixel values remain within `0..65535`.
- Preview maps low and high raw values to visibly different colors.
- Preview clears after disconnect.
- Main-thread UI never performs USB reads.

### Hardware-level

- Android asks for USB permission.
- Camera is detected by VID/PID.
- Both interfaces and expected endpoints are claimed.
- Frames arrive repeatedly without blocking the UI.
- Device disconnect produces a readable error and releases resources.
- Reconnect can start a fresh session.
- Calibrated output is compared against Thermal Mobile or a trusted reference before clinical use.

Use `scripts/validate_companion.sh` for repeatable source/build checks when the companion follows the standard Gradle layout.

## What not to do

- Do not use `getUserMedia()` for the UTi120M.
- Do not assume a Thermal Mobile JPEG contains a radiometric temperature matrix.
- Do not make WebUSB the production foundation without a browser/device support decision.
- Do not run the existing RGB YOLO model on thermal imagery unless it was trained and validated for that input domain.
- Do not claim hardware support based only on a successful APK build.
