"""
    A time series example from Cisco Devnet
    source: https://github.com/CiscoDevNet/intersight-python-utils
"""

import logging
from pprint import pformat
import traceback
from datetime import datetime, timedelta
import intersight.authentication
import intersight.api.telemetry_api
import intersight.model.telemetry_druid_data_source
import intersight.model.telemetry_druid_period_granularity
import intersight.model.telemetry_druid_query_context
import intersight.model.telemetry_druid_time_series_request
import os

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')

def format_time(dt):
    s = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    return f"{s[:-3]}Z"

def get_time_interval(num_days=5):
    current_time = datetime.now()
    end_time = format_time(current_time)
    start_time = format_time(current_time - timedelta(days=num_days))
    interval_str = start_time + '/' + end_time
    return interval_str

def get_time_series(api_client):
    """Query Druid time series"""

    # Create an instance of the API telemetry service.
    api_instance = intersight.api.telemetry_api.TelemetryApi(api_client)
    
    print("")
    logger.info("Query 'device_connector' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="device_connector",
        ),
        intervals=[
            get_time_interval(),
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="device_connector-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))

    ##########################
    print("")
    logger.info("Query 'ucs_ether_port_stat' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        aggregations=[
            intersight.model.telemetry_druid_aggregator.TelemetryDruidAggregator(
                field_name="sumBytesTx",
                type="longSum",
                name="traffic",
                field_names=["sumBytesTx"]
            ),
        ],
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="ucs_ether_port_stat",
        ),
        intervals=[
            get_time_interval(),
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="ucs_ether_port_stat-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))

    ##########################
    print("")
    logger.info("Query 'PSU stat' time series")
    req = intersight.model.telemetry_druid_time_series_request.TelemetryDruidTimeSeriesRequest(
        aggregations=[
            intersight.model.telemetry_druid_aggregator.TelemetryDruidAggregator(
                field_name="sumEnergyConsumed",
                type="doubleSum",
                name="energyConsumed",
                field_names=["sumEnergyConsumed"]
            ),
        ],
        query_type="timeseries",
        data_source=intersight.model.telemetry_druid_data_source.TelemetryDruidDataSource(
            type="table",
            name="psu_stat",
        ),
        intervals=[
            get_time_interval(),
        ],
        granularity=intersight.model.telemetry_druid_period_granularity.TelemetryDruidPeriodGranularity(
            type="period",
            period="P1D",
        ),
        context=intersight.model.telemetry_druid_query_context.TelemetryDruidQueryContext(
            timeout=30,
            query_id="psu_stat-QueryIdentifier",
        ),
    )
    api_response = api_instance.query_telemetry_time_series(
        telemetry_druid_time_series_request=req,
    )
    logger.info(pformat(api_response))


def main():
    # Configure API key settings for authentication
    API_KEY_ID = os.getenv("METRIC_API_KEY_ID_V3")
    PRIVATE_KEY_FILE = os.getenv("METRIC_API_PRIVATE_KEY_V3")
    client = intersight.authentication.get_api_client(api_key_id=API_KEY_ID, api_secret_file=PRIVATE_KEY_FILE, endpoint="https://intersight.com")

    try:
        # Get example time series data
        get_time_series(client)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()

if __name__ == "__main__":
    main()