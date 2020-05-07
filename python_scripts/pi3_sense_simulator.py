"""
Raspberry Pi 3 Sense Hat board node simulator. https://www.raspberrypi.org/products/sense-hat/

Purpose of script: Take readings from the Sense Hat board on the Pi 3 and send them to a Kafka broker topic as a node simulator.

Usage:
python3 pi3_sense_simulator.py --target 192.168.1.82 --topic topic_name

--target = IP address of the target Kafka broker
--topic = Kafka topic to send message to


Usage Notes
===========

"""

import argparse
import logging
import sys
import traceback
from threading import Timer
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from datetime import datetime
from sense_hat import SenseHat


def sensehat_pressure(sense):
    """Read the current reading from the sense hat board sensor.

        Parameters:
            sense: cleared instance of SenseHat()

        Returns:
            (float): current reading from sense hat sensor

    """
    value = sense.get_pressure()
    return value


def sensehat_temperature(sense):
    """Read the current reading from the sense hat board sensor.

            Parameters:
                sense: cleared instance of SenseHat()

            Returns:
                (float): current reading from sense hat sensor

    """
    value = sense.get_temperature()
    return value


def sensehat_humidity(sense):
    """Read the current reading from the sense hat board sensor.

            Parameters:
                sense: cleared instance of SenseHat()

            Returns:
                (float): current reading from sense hat sensor

    """
    value = sense.get_humidity()
    return value


def read_from_sense_hat():
    """
    Read a set of data from sense hat board.

        Returns: Apache AVRO JSON string containing the Kafka Schema with the current reading.

    """
    print("Acquiring data")

    timestamp = datetime.utcnow().isoformat()

    sense = SenseHat()
    sense.clear()

    value = {
        "SOSAobservedProperty": "http://data.posccaesar.org/rdl/RDS16432325",
        "SOSAhasResult": {
            "numericValue": sensehat_temperature(sense),
            "unit": "http://qudt.org/2.1/vocab/unit#DEG_C",
        },
        "timestamp_clock_sync": {
            "ptp_clock_status": "calibrated, in control, stabilised",
            "ptp_best_master_id": "38eaa7fffe38476b(unknown)/178",
            "ptp_offset_from_master": 0.000000082,
        },
        "SOSAresultTime": timestamp
    }

    # return value
    return value


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def main(argv):
    """The main function runs when the script is called """
    # parser = argparse.ArgumentParser(description="Feed data from Pi 3 Sense Hat board into a Kafka topic.")
    # parser.add_argument("--target",
    #                     help="IP address of target Kafka broker.",
    #                     action="store", dest="target", type=str, required=True)
    # parser.add_argument("--topic", help="Kafka topic name to send message to.", action="store", dest="topic", type=str,
    #                     required=True)
    #
    # args = parser.parse_args()

    # Set up the configured Schema registry Avro schema for the test Kafka topic.
    value_schema_str = """
    {
      "type": "record",
      "name": "base_unprocessed_data",
      "namespace": "push_im_subsystem.im_data",
      "doc": "DRAFT Apache AVRO data value schema for push of real-time unprocessed data from MWCC sub-systems. AIMS UAID used as the Kafka key for each value record. Note this requires all associated sensor data (accuracy, range, etc) to be established from attributes of the AIMS UAID related data",
      "fields": [
        {
          "name": "SOSAobservedProperty",
          "type": "string",
          "doc": "https://www.w3.org/TR/vocab-ssn/#SOSAobservedProperty",
          "default": "SOSAobservedProperty"
        },
        {
          "name": "SOSAhasResult",
          "type": {
            "type": "record",
            "doc": "http://qudt.org/schema/qudt#QuantityValue",
            "name": "QuantityValue",
            "namespace": "qudt",
            "fields": [
              {
                "name": "numericValue",
                "type": "double",
                "doc": "http://qudt.org/schema/qudt#numericValue",
                "default": 0.00
              },
              {
                "name": "unit",
                "type": "string",
                "doc": "http://qudt.org/schema/qudt#unit",
                "default": "http://qudt.org/1.1/vocab/unit#"
              }
            ]
          },
          "doc": "https://www.w3.org/TR/vocab-ssn/#SOSAhasResult"
        },
        {
          "name": "timestamp_clock_sync",
          "type": {
            "name": "ptp_sync_status",
            "type": "record",
            "doc": "The status of the PTP client clock sync",
            "fields": [
              {
                "name": "ptp_clock_status",
                "type": "string",
                "doc": "The PTP client daemon PTP_Clock_status of the clock responsible for the SOSAresultTime",
                "default": "ptp_clock_status"
              },
              {
                "name": "ptp_best_master_id",
                "type": "string",
                "doc": "The PTP client daemon Best_master_ID of the PTP client master clock providing current time sync for the SOSAresultTime",
                "default": "ptp_best_master_id"
              },
              {
                "name": "ptp_offset_from_master",
                "type": "float",
                "doc": "The PTP client daemon Offset_from_Master clock. https://www.w3.org/TR/2017/REC-owl-time-20171019/#time:Duration https://www.w3.org/TR/2017/REC-owl-time-20171019/#time:unitSecond",
                "default": 0.00
              }
            ]
          },
          "doc": "The status of the acquisition system clock responsible for the SOSAresultTime"
        },
        {
          "name": "SOSAresultTime",
          "type": "string",
          "doc": "https://www.w3.org/TR/vocab-ssn/#SOSAresultTime https://www.w3.org/TR/2017/REC-owl-time-20171019/#time:Instant https://www.w3.org/TR/xmlschema11-2/#dateTimeStamp",
          "default": "SOSAresultTime"
        }
      ]
    }    
    """

    key_schema_str = """
    {
      "type": "record",
      "name": "key",
      "namespace": "push_im_subsystem.im_data",
      "fields": [
        {
          "name": "aims_asset_id",
          "type": "string"
        }
      ]
    }
    """
    print("running avro loads on schemas")
    value_schema = avro.loads(value_schema_str)
    key_schema = avro.loads(key_schema_str)

    # Set a example key for the message which controls which partition the message ends up in Kafka.
    key = {"aims_asset_id": "HS2-000024H7L"}

    # Run a scheduled infinite loop to read from sensor.
    def send_to_kafka():
        Timer(10.0, send_to_kafka).start()
        try:
            print("running")
            avro_producer = AvroProducer({
                'bootstrap.servers': 'up01:9092,up02:9092,up03:9092',
                'schema.registry.url': 'http://up04:8081'
            }, default_key_schema=key_schema, default_value_schema=value_schema)

            value = read_from_sense_hat()

            print(value)

            avro_producer.poll(0)

            avro_producer.produce(topic='test_avro_2', value=value, key=key, callback=delivery_report)
            avro_producer.flush()

        except Exception as e:
            logging.error(traceback.format_exc())

    send_to_kafka()


# Run the main function when running file.
if __name__ == "__main__":
    sys.exit(main(sys.argv))
