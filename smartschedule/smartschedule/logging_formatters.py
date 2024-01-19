from datetime import datetime
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        log_record['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['level'] = record.levelname.upper()
        log_record['function_name'] = record.funcName

        if hasattr(record, 'user'):
            log_record['user'] = record.user
        if hasattr(record, 'response_code'):
            log_record['response_code'] = record.response_code
        if hasattr(record, 'execution_time'):
            log_record['execution_time'] = record.execution_time
            
        log_record['logger_name'] = record.name


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(user)s %(message)s %(response_code)s')


