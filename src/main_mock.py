import argparse
import sys

from PyQt6.QtWidgets import QApplication

from containers_hex_mock import DEFAULT_CONFIG_PATH, build_container


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run sewer robot controller (mock).")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to YAML configuration file.",
    )
    return parser.parse_args()


def run() -> None:
    args = _parse_args()
    app = QApplication(sys.argv)
    container = build_container(args.config)

    telemetry_services = container.communication.telemetry_services()
    video_services = container.video.video_services()
    panel_services = container.panel_and_feeder.panel_services()
    feeder_services = container.panel_and_feeder.feeder_services()

    telemetry_services.start_listening()
    video_services.start_listening()
    panel_services.start_listening()
    feeder_services.start_listening()

    main_window = container.inspection.main_window()
    main_window.show()

    exit_code = 0
    try:
        exit_code = app.exec()
    finally:
        logger = container.logger()
        for service in (feeder_services, panel_services, video_services, telemetry_services):
            try:
                service.stop_listening()
            except Exception as exc:
                logger.error("Failed to stop service: %s", exc, exc_info=True)

    sys.exit(exit_code)


if __name__ == "__main__":
    run()
