class EventProcessor:
    def __init__(self, **kwargs):
        # Unpack Kwargs
        self.logger = kwargs.get('LOGGER')
        self.env = kwargs.get('ENV')
        self.redis_con = kwargs.get('REDIS_CON')

    def _submit_event_to_stream(self, formatted_event):
        # Get home id and generate key
        stream_key = '<user_key>'

        try:
            response = self.redis_con.add_entry_to_stream(
                                stream_key, formatted_event)
        except Exception as e:
            self.logger.error(f'Error submitting event to stream',
                              extra={'formatted_event': formatted_event,
                                     'e': e})
            return None

        return response

    def process_event(self, event):
        self.logger.debug(f'Processing event',
                                  extra={'event': event})
        # Submit to redis stream
        redis_response = self._submit_event_to_stream(event)
        self.logger.debug(f'Redis response {redis_response}')
