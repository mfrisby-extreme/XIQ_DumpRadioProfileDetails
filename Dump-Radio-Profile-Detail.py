import argparse
import logging
import getpass
import pandas as pd
import csv

from lib.xiq_api import XIQ, logger


script_name = "Dump-Radio-Profile-Detail"
logger.setLevel(logging.DEBUG)

field_names = [
    "id",
    "create_time",
    "update_time",
    "name",
    "predefined",
    "description",
    "transmission_power",
    "max_transmit_power",
    "transmission_power_floor",
    "transmission_power_max_drop",
    "max_clients",
    "enable_client_transmission_power",
    "client_transmission_power",
    "enable_ofdma",
    "radio_mode",
    "neighborhood_analysis_id",
    "channel_selection_id",
    "radio_usage_optimization_id",
    "miscellaneous_settings_id",
    "presence_server_settings_id",
    "sensor_scan_settings_id",
    "enable_dynamic_channel_switching",
    "channel_width",
    "enable_dynamic_frequency_selection",
    "enable_static_channel",
    "enable_zero_wait_dfs",
    "enable_use_last_selection",
    "exclude_channels",
    "exclude_channels_width",
    "channel",
    "enable_limit_channel_selection",
    "channel_region",
    "channel_model",
    "channels",
    "enable_channel_auto_selection",
    "channel_selection_start_time",
    "channel_selection_end_time",
    "enable_avoid_switch_channel_if_clients_connected",
    "channel_selection_max_clients",
    "enable_switch_channel_if_exceed_threshold",
    "rf_interference_threshold",
    "crc_error_threshold",
    "preamble",
    "beacon_period",
    "enable_frame_burst",
    "enable_smart_antenna",
    "enable_backhaul_failover",
    "wireless_backhaul_switch_trigger_time",
    "wired_backhaul_revert_hold_time",
    "enable_band_steering",
    "band_steering_mode",
    "ignore_initial_client_connection_number",
    "enable_client_load_balancing",
    "load_balancing_mode",
    "crc_error_rate_per_device",
    "rf_interference_per_device",
    "average_airtime_per_client",
    "anchor_period",
    "neighbor_query_interval",
    "enable_weak_signal_probe_request_suppression",
    "weak_snr_threshold",
    "enable_safety_net",
    "safety_net_period",
    "enable_high_density",
    "management_frame_basic_data_rate",
    "enable_suppress_successive_probe_request",
    "probe_response_reduction_option",
    "suppression_limit",
    "enable_radio_balance",
    "enable_ampdu",
    "enable_mu_mimo",
    "enable_ofdma_down_link",
    "enable_ofdma_up_link",
    "bss_coloring",
    "enable_target_weak_time",
    "mac_ouis",
    "ratio_for_5g_clients",

]


XIQ_API_token = ''
# pageSize = 100

parser = argparse.ArgumentParser()
parser.add_argument('--external',action="store_true", help="Optional - adds External Account selection, to use an external VIQ")
parser.add_argument('--csv_file', default='radio_profiles.csv', help='name of csv file to create')
args = parser.parse_args()

csv_file = args.csv_file

## XIQ API Setup
if XIQ_API_token:
    x = XIQ(token=XIQ_API_token)
else:
    print("Enter your XIQ login credentials")
    username = input("Email: ")
    password = getpass.getpass("Password: ")
    x = XIQ(user_name=username,password = password)
#OPTIONAL - use externally managed XIQ account
if args.external:
    accounts, viqName = x.selectManagedAccount()
    if accounts == 1:
        validResponse = False
        while validResponse != True:
            response = input("No External accounts found. Would you like to import data to your network?")
            if response == 'y':
                validResponse = True
            elif response =='n':
                logging.warning("script is exiting....\n")
                raise SystemExit
    elif accounts:
        validResponse = False
        while validResponse != True:
            print("\nWhich VIQ would you like to connect to?")
            accounts_df = pd.DataFrame(accounts)
            count = 0
            for df_id, viq_info in accounts_df.iterrows():
                print(f"   {df_id}. {viq_info['name']}")
                count = df_id
            print(f"   {count+1}. {viqName} (This is Your main account)\n")
            selection = input(f"Please enter 0 - {count+1}: ")
            try:
                selection = int(selection)
            except:
                logging.warning("Please enter a valid response!!")
                continue
            if 0 <= selection <= count+1:
                validResponse = True
                if selection != count+1:
                    newViqID = (accounts_df.loc[int(selection),'id'])
                    newViqName = (accounts_df.loc[int(selection),'name'])
                    x.switchAccount(newViqID, newViqName)


def main():

    response = x.getRadioProfiles(page=1, limit=10)
    logging.debug(f"Got Page 1 response: {response}")
    total_pages = response.get("total_pages", 1)
    data_list = response.get("data", [])

    if total_pages > 1:
        for pg in range(2, total_pages+1):
            response = x.getRadioProfiles(page=pg, limit=10)
            logging.debug(f"Got Page {pg} response: {response}")
            data_list.extend(response.get("data", []))

    # get Radio Profile Channel Selection for each record
    for data_record in data_list:
        rp_name = data_record.get("name")
        cs_id = data_record.get("channel_selection_id")
        ru_id = data_record.get("radio_usage_optimization_id")
        if cs_id is not None:
            logging.info(f"Getting Channel Selection ID :{cs_id} for Radio Profile: {rp_name}")
            cs_data = x.getRPChannelSelection(cs_id)
            if cs_data is not None:
                cs_data.pop("id")
                cs_data.pop("create_time")
                cs_data.pop("update_time")
                logging.info(f"Adding channel selection data to radio profile record:{rp_name}")
                data_record.update(cs_data)
            print("\n")
        if ru_id is not None:
            logging.info(f"Getting Radio Optimization ID :{ru_id} for Radio Profile: {rp_name}")
            ru_data = x.getRPRadioUsageOpt(ru_id)
            if ru_data is not None:
                ru_data.pop("id")
                ru_data.pop("create_time")
                ru_data.pop("update_time")
                logging.info(f"Adding radio utilization data to radio profile record:{rp_name}")
                data_record.update(ru_data)
            print("\n")


    # Specify the CSV column headers (field names)
    # unique_field_names = set()

    # Collect unique field names from all dictionaries in data_list
    # for data in data_list:
    #     unique_field_names.update(data.keys())

    # Convert the set to a list to maintain order (if needed)
    # field_names = list(unique_field_names)



    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for data in data_list:
            writer.writerow(data)


if __name__ == '__main__':
    main()
