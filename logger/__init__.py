__author__ = 'hzhigeng'

import logging

_logger = logging.getLogger(__name__)
_formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
_file_handler = logging.FileHandler('run.log')
_file_handler.setFormatter(_formatter)
_logger.addHandler(_file_handler)
_logger.setLevel(logging.DEBUG)


def _log_generator(min_log_level):
    def internal_log(log_level, *args, **kwargs):
        print(log_level, min_log_level)
        if log_level >= min_log_level:
            # print(log_level, min_log_level, args)
            _logger.log(log_level, *args, **kwargs)

    return internal_log

log_fatal = _log_generator(logging.FATAL)
log_error = _log_generator(logging.ERROR)
log_warn = _log_generator(logging.WARN)
log_info = _log_generator(logging.INFO)
log_debug = _log_generator(logging.DEBUG)

FATAL = logging.FATAL
ERROR = logging.ERROR
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG


if __name__ == '__main__':
    log = log_fatal
    log(logging.FATAL, 'fatal')
    log(logging.WARN, 'warn')
    log(logging.DEBUG, 'debug')
    log(logging.FATAL, '=========')
    log = log_warn
    log(logging.FATAL, 'fatal')
    log(logging.WARN, 'warn')
    log(logging.DEBUG, 'debug')
    log(logging.FATAL, '=========')
    log = log_debug
    log(logging.FATAL, 'fatal')
    log(logging.WARN, 'warn')
    log(logging.DEBUG, 'debug')
    log(logging.FATAL, '=========')
