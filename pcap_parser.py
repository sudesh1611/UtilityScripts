#!/usr/bin/python3
import os
import sys
import subprocess
from subprocess import PIPE
import argparse
import json

All_Packets = []
All_Summary = {}
_Duplicate_found = 0
_Duplicate_resolved = 0



def pcap_summary():
    #return True
    global All_Summary
    for packet in All_Packets:
        if "ip" in packet["_source"]["layers"]:
            ip_info = packet["_source"]["layers"]["ip"]
            from_to_ip = f'{ip_info["ip.src"]}_{ip_info["ip.dst"]}'
            if from_to_ip not in All_Summary:
                All_Summary[from_to_ip] = {}
                All_Summary[from_to_ip]["Total_Packets"] = 0
                All_Summary[from_to_ip]["Handshakes"] = {}
                for handshake_type in [(0, "Hello_Request"), (1, "Client_Hello"), (2,"Server_Hello"), (4, "New_Session_Ticket"), (8, "Encrypted_Extensions"), (11, "Certificate"), (12, "Server_Key_Exchange"), (13, "Certificate_Request"), (14, "Server_Hello_Done"), (15, "Certificate_Verify"), (16, "Client_Key_Exchange"), (20, "Finished")]:
                    All_Summary[from_to_ip]["Handshakes"][str(handshake_type[0])] = {
                        "Name":handshake_type[1],
                        "Count":0
                    }
            All_Summary[from_to_ip]["Total_Packets"] +=1
            if "tls" in packet["_source"]["layers"]:
                tls_main_packet = packet["_source"]["layers"]["tls"]
                for extra in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                    TLS_RECORD = "tls.record" + extra
                    if TLS_RECORD in tls_main_packet:
                        if TLS_RECORD != "tls.record":
                            print(TLS_RECORD)
                            print("----------------------------")
                            print("----------------------------")
                            print(json.dumps(tls_main_packet, indent=2))
                            print("----------------------------")
                            print("----------------------------")
                        tls_info = tls_main_packet
                        if "tls.record.content_type" in tls_info[TLS_RECORD] and tls_info[TLS_RECORD]["tls.record.content_type"] == "22" and "tls.handshake" in tls_info[TLS_RECORD] and "tls.handshake.type" in tls_info[TLS_RECORD]["tls.handshake"]:
                            All_Summary[from_to_ip]["Handshakes"][tls_info[TLS_RECORD]["tls.handshake"]["tls.handshake.type"]]["Count"] +=1

    print("From\t\tTo\t\tCount")
    for key, data in All_Summary.items():
        ip_printed = False
        for i in range(20):
            if str(i) in data["Handshakes"] and data["Handshakes"][str(i)]["Count"] > 0:
                if ip_printed == False:
                    print(key.split("_")[0] + "\t" + key.split("_")[1] + "\t" + f'{data["Handshakes"][str(i)]["Name"]}({data["Handshakes"][str(i)]["Count"]})', end=", ")
                    ip_printed = True
                else:
                    print(f'{data["Handshakes"][str(i)]["Name"]}({data["Handshakes"][str(i)]["Count"]})', end=", ")
        if ip_printed == True:
            print("")



def dict_add_keys_on_duplicates(ordered_pairs):
    """Parse and load duplicate keys"""
    global _Duplicate_found
    global _Duplicate_resolved
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            _Duplicate_found += 1
            for extra in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                temp_key = k+extra
                if temp_key not in d:
                    d[temp_key] = v
                    _Duplicate_resolved +=1
                    break
        else:
           d[k] = v
    return d



def pcap_timeline():
    pass



def pcap_to_json(pcap_path):
    global All_Packets
    cmd = f"tshark -r {pcap_path} -V -T json"
    x = ""
    try:
        x = subprocess.run(cmd, stdout=PIPE, stderr=PIPE, encoding="UTF-8")
    except Exception as ex:
        print(f"Error: Exception ({ex}) occured while parsing pcap.")
        return False
    All_Packets = json.loads(x.stdout, object_pairs_hook=dict_add_keys_on_duplicates)
    #print(json.dumps(All_Packets[-5:], indent=4))
    print(f"DEBUG: {_Duplicate_found - _Duplicate_resolved} duplicate keys were not resolved")
    return True



def main():
    cmd_line_arg_parser = argparse.ArgumentParser( description="A script to get summary out of pcap file")
    cmd_line_arg_parser.add_argument('pcap_file_path', metavar="pcap_file_path", type=str, help="path of the pcap file")
    cmd_line_arg_parser.add_argument('--summary', action='store_true', help="summarize different TLS handshake types")
    cmd_line_arg_parser.add_argument('--timeline', action='store_true', help="timeline of TLS handshakes")
    cmd_line_args = cmd_line_arg_parser.parse_args()
    pcapPath = os.path.abspath(cmd_line_args.pcap_file_path)
    if not os.path.exists(pcapPath):
        print(f"{pcapPath} doesn't exist!")
        sys.exit(1)
    pcap_to_json(pcapPath)
    if cmd_line_args.summary == False and cmd_line_args.timeline == False:
        cmd_line_args.summary = True
    if cmd_line_args.timeline == True:
        pcap_timeline()
    if cmd_line_args.summary == True:
        pcap_summary()


if __name__ == "__main__":
    main()