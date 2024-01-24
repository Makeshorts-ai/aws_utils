import logging


class CloudWatchHandler(logging.StreamHandler):
    def __init__(self, log_group_name, log_stream_name, cloudwatch_logs):
        super().__init__()
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.cloudwatch_logs = cloudwatch_logs

    def emit(self, record):
        try:
            log_message = self.format(record)
            self.cloudwatch_logs.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(record.created * 1000),
                        'message': log_message
                    }
                ]
            )
        except Exception as e:
            print("Credentials not available", e)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger_name': record.name  # Include logger's name in the log record
        }

        # Add extra fields from the record's __dict__ if available
        extra_fields = ['userId', 'videoId', 'request_id', 'component']
        for field in extra_fields:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        return self.jsonify(log_record)

    @staticmethod
    def jsonify(log_record):
        try:
            import json
            return json.dumps(log_record)
        except Exception:
            return str(log_record)


def setup_logging(log_group_name, log_stream_name, cloudwatch_logs):
    # Configure the root logger to send logs to CloudWatch
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # Create or get the CloudWatch log group and stream
    try:
        print(f"Creating log group: {log_group_name}")
        cloudwatch_logs.create_log_group(logGroupName=log_group_name)

    except Exception as e:
        print(e)
        pass

    try:
        print(f"Creating log stream: {log_stream_name}")
        cloudwatch_logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except Exception as e:
        print(e)
        pass

    # Add the CloudWatch handler to the logger
    formatter = JsonFormatter()
    cloudwatch_handler = CloudWatchHandler(log_group_name, log_stream_name, cloudwatch_logs)
    cloudwatch_handler.setFormatter(formatter)

    logger.addHandler(cloudwatch_handler)


def main():
    # Use the logger's name for initialization
    logger = logging.getLogger(__name__)

    # Your application code here
    userId = '123'
    videoId = '456'
    request_id = f'{videoId}_{userId}_aasdas'

    logger.info('Execution startedsadasd',
                extra={
                    'userId': userId,
                    'videoId': videoId,
                    'request_id': request_id,
                    'component': 'lambda-triggerClipWorkflow'
                })


if __name__ == "__main__":
    # Pass the log group name and log stream name when setting up logging
    setup_logging(log_group_name='YourLogGroupName', log_stream_name='YourLogStreamName')
    main()
