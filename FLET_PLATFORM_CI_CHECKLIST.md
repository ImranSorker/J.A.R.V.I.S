# JARVIS Windows / Linux / Android Flet CI Checklist

This suite is designed around Flet's real integration-test runner. `flet test`
provisions a Flutter test host and drives the app on the target platform, so
these are device/runtime tests rather than Python-only UI mocks.

## Required gates

### Common
- [ ] Python 3.13 environment created.
- [ ] `uv sync --extra dev` succeeds.
- [ ] `python -m compileall -q .` passes.
- [ ] `pytest -q` passes.
- [ ] `flet doctor` has no blocking errors.
- [ ] `flet test` uses the same Flet version declared by `pyproject.toml`.

### Windows 10/11 x64
- [ ] `uv run flet test windows -v -k "not android"` passes.
- [ ] Chat input accepts text.
- [ ] Send button produces the deterministic UI-test response.
- [ ] Model selector is discoverable and actionable.
- [ ] Persona selector is discoverable and actionable.
- [ ] Refresh is actionable.
- [ ] Chat/Workflow tabs are discoverable.
- [ ] No unhandled exception appears during startup or interaction.
- [ ] `flet build windows` succeeds on a Windows runner before release.

### Linux x64
- [ ] `uv run flet test linux -v -k "not android"` passes.
- [ ] Same interaction gates as Windows pass.
- [ ] Full desktop flavor is used because JARVIS includes audio/video features.
- [ ] `flet build linux` succeeds on a supported Linux distribution before release.
- [ ] Audio/voice smoke test is performed on a machine with real audio hardware.

### Android
- [ ] Android SDK + JDK 17 are available.
- [ ] `flet devices android` reports the intended device/emulator.
- [ ] `uv run flet test android --device-id <id> -v -k android` passes.
- [ ] Mobile mode is visible.
- [ ] API URL field accepts only HTTP(S).
- [ ] API token field is present and masked.
- [ ] Connect action is responsive and displays connection errors without crashing.
- [ ] Model/persona controls remain accessible in the mobile layout.
- [ ] Android golden screenshot passes on the canonical emulator/device.
- [ ] `flet build apk --arch arm64-v8a x86_64 armeabi-v7a` (or the release-equivalent command) succeeds.
- [ ] Release APK/AAB is installed and launched on a physical Android device.
- [ ] Orientation/background/foreground lifecycle is manually checked.
- [ ] Production API uses HTTPS.

## Golden screenshots

Flet supports screenshot goldens for Android/iOS. Goldens are platform- and
device-specific; record and compare them on the same emulator/device model.
Do **not** copy a desktop screenshot into the Android golden directory.

Initial recording:

```bash
uv run flet test android --device-id <canonical-device> -u -k android_golden_home
```

Normal comparison:

```bash
uv run flet test android --device-id <canonical-device> -k android_golden_home
```

The repository should contain:

```text
tests/golden/android/test_flet_platform_matrix/home.png
```

The golden is intentionally not generated in this audit environment because no
Android device/emulator is available; a human/device CI run must record it.

## CI policy

- Pull requests: Linux + Windows UI tests are required.
- Main branch: Linux + Windows + Android emulator tests are required.
- Release tags: all UI tests plus actual platform packaging builds are required.
- Any skipped Flet integration test is a CI failure unless the job explicitly
  documents an unavailable platform/device.
- Golden updates require a reviewed PR and an explicit `--update-goldens` run.
- Never use `JARVIS_UI_TEST_MODE=1` for a production build.

## Commands

```bash
# Static + normal regression suite
uv run python -m compileall -q .
uv run pytest -q

# Desktop
JARVIS_UI_TEST_MODE=1 uv run flet test linux -v -k "not android"
JARVIS_UI_TEST_MODE=1 uv run flet test windows -v -k "not android"

# Android
uv run flet devices android
uv run flet test android --device-id <device-id> -v -k android
```

Flet's current integration testing model supports finding controls by key/text,
tapping, entering text, pumping the UI, and screenshot comparison. The target
app runs through the same build pipeline used for deployment. See the official
Flet integration-testing and `flet test` documentation for the authoritative
CLI/options.
