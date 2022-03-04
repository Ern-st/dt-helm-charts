import unittest
import os
from datetime import datetime, timezone
from unittest.mock import Mock, patch

from app.kafka_topic_replicator import calculate_delay_sec, get_input

class TestCalculateDelayMs(unittest.TestCase):
    
    def setUp(self):
        # Mock Consumer record
        consumer_record_mock = Mock()
        consumer_record_mock.timestamp = 1000 # Kafka timestamps are in miliseconds 
        self.consumer_record = consumer_record_mock

    @patch('app.kafka_topic_replicator.get_current_time')    
    def test_should_return_non_zero_when_record_is_no_older_than_delay(self, mock_timestamp_now):
        mock_timestamp_now.return_value = datetime.fromtimestamp(2, tz=timezone.utc)
        # Act
        sleep_delay_sec = calculate_delay_sec(self.consumer_record, delay_ms=4000)
        
        # Inspect
        self.assertEquals(sleep_delay_sec,3)


    @patch('app.kafka_topic_replicator.get_current_time')    
    def test_should_return_zero_when_record_is_older_than_delay(self, mock_timestamp_now):
        mock_timestamp_now.return_value = datetime.fromtimestamp(6, tz=timezone.utc)
        # Act
        sleep_delay_sec = calculate_delay_sec(self.consumer_record, delay_ms=4000)
        
        # Inspect
        self.assertEquals(sleep_delay_sec,0)

    @patch('app.kafka_topic_replicator.get_current_time')    
    def test_should_return_zero_when_record_as_old_as_delay(self, mock_timestamp_now):
        mock_timestamp_now.return_value = datetime.fromtimestamp(5, tz=timezone.utc)
        # Act
        sleep_delay_sec = calculate_delay_sec(self.consumer_record, delay_ms=4000)
        
        # Inspect
        self.assertEquals(sleep_delay_sec,0)

class TestGetInput(unittest.TestCase):
    def setUp(self):
        os.environ["KAFKA_BROKER_ENDPOINT"] = "test"
        os.environ["INPUT_TOPIC"] = "test"
        os.environ["OUTPUT_TOPIC"] = "test"
        os.environ["DELAY_MS"] = "1000"

    def tearDown(self):
        os.environ.pop("KAFKA_BROKER_ENDPOINT")
        os.environ.pop("INPUT_TOPIC")
        os.environ.pop("OUTPUT_TOPIC")
        os.environ.pop("DELAY_MS")

    def test_input_should_be_type_cast(self):
        kafka_broker_endpoint, input_topic, output_topic, delay_ms = get_input()

        self.assertEqual(type(kafka_broker_endpoint),str)
        self.assertEqual(type(input_topic),str)
        self.assertEqual(type(output_topic),str)
        self.assertEqual(type(delay_ms),int)

if __name__ == '__main__':
    unittest.main()
