# UTi120M protocol reference

This reference summarizes the reverse-engineered transport used by the companion workflow. Treat it as an implementation aid, not a substitute for hardware validation.

## USB identity and endpoints

- Vendor ID: `0x5656`
- Product ID: `0x1201`
- Frame interface: interface `0`, bulk IN endpoint commonly `0x82`
- Command interface: interface `1`, interrupt/bulk OUT commonly `0x01`, IN commonly `0x81`

Endpoint addresses and transfer types must be confirmed from the connected device. Enumerate endpoints instead of hard-coding an endpoint when possible.

## Raw frame

- Packet size: `25,600` bytes
- Pixel plane: `10,800` little-endian 16-bit values
- Sensor dimensions: `120 × 90`
- Pixel plane begins after a `360`-short header offset in the reference implementation.
- Header includes magic, frame counter, dimensions, shutter/lens/FPA values, and status fields.
- Raw pixels are sensor counts. They are not Celsius.

## Initial transport sequence

1. Open and claim the required interfaces.
2. Read device information and calibration data as required by the implementation.
3. Write run status `2` to enter image-upload mode.
4. Send frame request byte `0x81`.
5. Read the complete 25,600-byte packet.
6. Validate magic and dimensions before parsing.
7. Repeat on a serialized I/O worker.
8. Write idle run status during best-effort teardown.

## Calibration pipeline

A calibrated temperature map requires more than frame parsing:

1. Capture a shutter/dark reference.
2. Apply per-pixel gain and bad-pixel correction.
3. Correct lens and shutter/FPA drift.
4. Apply the device calibration curves.
5. Apply emissivity and relevant environmental corrections.
6. Emit a radiometric matrix plus calibration metadata.

Do not expose a Celsius UI until this pipeline is implemented and compared with a trusted reference.

## Sources

- https://github.com/diegosainz/uni-t-thermal-uti120
- https://thermal.uni-trend.com/product/uti120m/
- https://play.google.com/store/apps/details?id=com.unitrend.thermal_mobile_721
