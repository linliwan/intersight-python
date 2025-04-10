"""
    Use the Intersight Telemetry API to query the energy consumption of a specific server over the past 24 hours
    Author: Linlin Wang
"""

import os
from datetime import datetime, timedelta
import intersight.authentication
from intersight.apis import ComputeApi, TelemetryApi
from intersight.model.telemetry_druid_time_series_request import TelemetryDruidTimeSeriesRequest
from intersight.model.telemetry_druid_table_data_source import TelemetryDruidTableDataSource
from intersight.model.telemetry_druid_period_granularity import TelemetryDruidPeriodGranularity
from intersight.model.telemetry_druid_query_context import TelemetryDruidQueryContext
from intersight.model.telemetry_druid_in_filter import TelemetryDruidInFilter
from intersight.model.telemetry_druid_selector_filter import TelemetryDruidSelectorFilter
from intersight.model.telemetry_druid_and_filter import TelemetryDruidAndFilter
from intersight.model.telemetry_druid_aggregator import TelemetryDruidAggregator
from intersight.model.telemetry_druid_expression_post_aggregator import TelemetryDruidExpressionPostAggregator
from datetime import datetime, timedelta

# initial client
client = intersight.authentication.get_api_client(
    api_key_id=os.getenv("METRIC_API_KEY_ID_V3"),
    api_secret_file=os.getenv("METRIC_API_PRIVATE_KEY_V3"),
    endpoint="https://intersight.com"
)

compute = ComputeApi(api_client=client)
telemetry = TelemetryApi(api_client=client)

# Get the MoID for a specific server (by serial number)
server = compute.get_compute_blade_list(filter="Serial eq 'FCH264477D7'").results
server_moid = server[0].moid
server_dn = server[0].name
print(f"Target server MoID: {server_moid}")

# Time range settings
now = datetime.now()
start_time = now - timedelta(hours=24)
interval = f"{start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z/{now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"

# Construct the request body. 
# You can generate the query code in the Intersight GUI and then give it to ChatGPT to assist in the conversion.
req = TelemetryDruidTimeSeriesRequest(
    query_type="groupBy",
    data_source=TelemetryDruidTableDataSource(type="table", name="PhysicalEntities"),
    granularity=TelemetryDruidPeriodGranularity(
        type="period",
        period="PT1H",
        time_zone="Asia/Shanghai",
        origin=start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
    ),
    intervals=[interval],
    dimensions=[],
    filter=TelemetryDruidAndFilter(
        type="and",
        fields=[
            TelemetryDruidInFilter(
                type="in",
                dimension="host.id",
                values=[f"/api/v1/compute/Blades/{server_moid}"]
            ),
            TelemetryDruidSelectorFilter(
                type="selector",
                dimension="host.name",
                value=server_dn
            ),
            TelemetryDruidSelectorFilter(
                type="selector",
                dimension="instrument.name",
                value="hw.host"
            )
        ]
    ),
    aggregations=[
        TelemetryDruidAggregator(
            type="doubleSum",
            name="hw.host.energy_duration-Sum",
            field_name="hw.host.energy_duration"
        ),
        TelemetryDruidAggregator(
            type="doubleSum",
            name="hw.host.energy-SumAg",
            field_name="hw.host.energy"
        ),
        TelemetryDruidAggregator(
            type="thetaSketch",
            name="endpoint_count",
            field_name="host.id"
        )
    ],
    post_aggregations=[
        TelemetryDruidExpressionPostAggregator(
            type="expression",
            name="hw-host-energy-Sum",
            expression='(("hw.host.energy-SumAg" * 3600) / "hw.host.energy_duration-Sum")'
        )
    ],
    context=TelemetryDruidQueryContext(
        timeout=30,
        query_id="host_energy_query"
    )
)
# Run a query
results = telemetry.query_telemetry_time_series(telemetry_druid_time_series_request=req)

# format output
print(f"\nHourly Energy Consumption for server {server_dn} (past 24h):\n")
print("{:<20} {:>15} {:>15} {:>15} {:>10}".format(
    "Timestamp", "Energy (kJ)", "Energy (Wh)", "Raw Energy", "Dur(s)"
))
print("=" * 80)

for r in results:
    ts = r["timestamp"].astimezone().strftime("%Y-%m-%d %H:%M")
    event = r["event"]
    energy_kj = event.get("hw-host-energy-Sum", 0) / 1000
    energy_wh = energy_kj / 3.6  # 因为 1 Wh = 3600 J = 3.6 kJ
    energy_raw = event.get("hw.host.energy-SumAg", 0)
    duration = event.get("hw.host.energy_duration-Sum", 0)

    print("{:<20} {:>15.2f} {:>15.2f} {:>15.2f} {:>10.0f}".format(
        ts, energy_kj, energy_wh, energy_raw, duration
    ))


# Target server MoID: 67ee693b617675330133e43f

# Hourly Energy Consumption for server lon-ai1-pod1-1-7 (past 24h):

# Timestamp                Energy (kJ)     Energy (Wh)      Raw Energy     Dur(s)
# ================================================================================
# 2025-04-06 06:37             1360.72          377.98      1360718.26       3600
# 2025-04-06 07:37             1337.38          371.50      1337383.97       3600
# 2025-04-06 08:37             1348.86          374.68      1348864.67       3600
# 2025-04-06 09:37             1359.37          377.60      1359371.75       3600
# 2025-04-06 10:37             1346.58          374.05      1346579.01       3600
# 2025-04-06 11:37             1354.44          376.23      1354440.50       3600
# 2025-04-06 12:37             1356.83          376.90      1356825.13       3600
# 2025-04-06 13:37             1368.60          380.17      1368596.59       3600
# 2025-04-06 14:37             1358.58          377.38      1358584.53       3600
# 2025-04-06 15:37             1349.30          374.81      1349303.29       3600
# 2025-04-06 16:37             1348.30          374.53      1348297.75       3600
# 2025-04-06 17:37             1386.21          385.06      1386209.89       3600
# 2025-04-06 18:37             1351.21          375.34      1351214.12       3600
# 2025-04-06 19:37             1368.93          380.26      1368933.49       3600
# 2025-04-06 20:37             1349.00          374.72      1349003.66       3600
# 2025-04-06 21:37             1363.61          378.78      1363609.66       3600