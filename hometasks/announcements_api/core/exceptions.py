class ServiceException(Exception):
    pass


class DatabaseException(ServiceException):
    pass


class NotFoundException(ServiceException):
    pass
