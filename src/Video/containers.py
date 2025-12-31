from dependency_injector import containers, providers

from Video.adapters.external_services.hikvision_dvr_controller_adapter import (
    HikvisionDvrControllerAdapter,
)
from Video.adapters.external_services.mock_hikvision_dvr_controller_adapter import (
    MockHikvisionDvrControllerAdapter,
)
from Video.adapters.external_services.opencv_video_controller_adapter import (
    OpencvVideoControllerAdapter,
)
from Video.adapters.external_services.pyqt_video_observer_adapter import (
    PyqtVideoObserverAdapter,
)
from Video.adapters.repositories.tinydb_repository_adapter import TinydbRepositoryAdapter
from Video.application.services.session_services import SessionServices
from Video.application.services.video_services import VideoServices


def _register_observer(service, observer):
    service.register_observer(observer)
    return True


class VideoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency()
    video_update_service = providers.Dependency()

    dvr_controller = providers.Singleton(
        HikvisionDvrControllerAdapter,
        url=config.dvr.url,
        user=config.dvr.user,
        password=config.dvr.password,
        dir=config.dvr.dir,
        logger=logger,
    )
    video_controller = providers.Singleton(
        OpencvVideoControllerAdapter,
        rtsp_url=config.rtsp_url,
        logger=logger,
    )

    video_services = providers.Singleton(
        VideoServices,
        video_controller=video_controller,
        logger=logger,
    )

    video_observer = providers.Singleton(
        PyqtVideoObserverAdapter,
        video_update_service=video_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observer,
        service=video_services,
        observer=video_observer,
    )

    repository = providers.Singleton(
        TinydbRepositoryAdapter,
        db_name=config.sessions_db,
        logger=logger,
    )
    session_services = providers.Singleton(
        SessionServices,
        dvr_controller=dvr_controller,
        repository=repository,
        logger=logger,
    )


class VideoMockContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency()
    video_update_service = providers.Dependency()

    dvr_controller = providers.Singleton(
        MockHikvisionDvrControllerAdapter,
        url=config.dvr.url,
        user=config.dvr.user,
        password=config.dvr.password,
        dir=config.dvr.dir,
        logger=logger,
    )
    video_controller = providers.Singleton(
        OpencvVideoControllerAdapter,
        rtsp_url=config.rtsp_url,
        logger=logger,
    )

    video_services = providers.Singleton(
        VideoServices,
        video_controller=video_controller,
        logger=logger,
    )

    video_observer = providers.Singleton(
        PyqtVideoObserverAdapter,
        video_update_service=video_update_service,
        logger=logger,
    )

    wire_observers = providers.Callable(
        _register_observer,
        service=video_services,
        observer=video_observer,
    )

    repository = providers.Singleton(
        TinydbRepositoryAdapter,
        db_name=config.sessions_db,
        logger=logger,
    )
    session_services = providers.Singleton(
        SessionServices,
        dvr_controller=dvr_controller,
        repository=repository,
        logger=logger,
    )
