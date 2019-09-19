    
class DevicesTable(object):  
    def __init__(self, table_resource):
        self._table = table_resource
      
    def insert_device(self, event):
        """Insert a device into the table."""
        # Return an error if we don't have device_id in the JSON event
        if "device_id" not in event:
            return Exception("Invalid event. Must include key 'device_id'")
        try:
            self._table.put_item(
                Item={
                    'device_id': event.get('device_id', None),
                }
            )
        except Exception as e:
            return e