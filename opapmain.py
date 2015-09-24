#!/usr/bin/python2.7

__author__ = 'nassos'

import os
import sys
#import urllib.request
import http.client
import json
import csv
import time
from progmenu import ProgramMenu

# OPAP REST Services
# {game} proto
# {extension} json
# http://applications.opap.gr/DrawsRestServices/{game}/last.{extension}
# http://applications.opap.gr/DrawsRestServices/{game}/{draw_number}.{extension}

def draw_json_data_to_tuple(draw_json_data):
    return (draw_json_data['draw']['drawNo'],
            draw_json_data['draw']['drawTime'],
            draw_json_data['draw']['results'])

def print_proto_draw(draw_request_response):
    print(draw_request_response['draw']['drawTime'])
    print(draw_request_response['draw']['drawNo'])
    print(draw_request_response['draw']['results'])

def fetch_proto_last_draw():
    conn = http.client.HTTPConnection("applications.opap.gr")
    request_str = "/DrawsRestServices/{0}/last.{1}".format("proto","json")
    conn.request("GET",request_str,None,{"Accept":"text\json"})
    last_draw_response = conn.getresponse()
    last_draw_data = last_draw_response.read().decode('utf-8')
    lastdraw_json_data = json.loads(last_draw_data)
    conn.close()
    return lastdraw_json_data
    # http_request = urllib.request.Request("http://applications.opap.gr/DrawsRestServices/{0}/last.{1}".format("proto", "json"))
    # http_request.add_header('Pragma', 'no-cache')
    # response = urllib.request.urlopen(http_request)
    # urllib.request.urlcleanup()
    # lastdraw_text_data = response.read().decode('utf-8')
    # lastdraw_json_data = json.loads(lastdraw_text_data)
    # return lastdraw_json_data

def fetch_proto_draw(draw_number):
    print(draw_number)
    conn = http.client.HTTPConnection("applications.opap.gr")
    request_str = "/DrawsRestServices/proto/{0}.json".format(draw_number)
    conn.request("GET",request_str,None,{"Accept":"text\json"})
    last_draw_response = conn.getresponse()
    last_draw_data = last_draw_response.read().decode('utf-8')
    lastdraw_json_data = json.loads(last_draw_data)
    conn.close()
    return lastdraw_json_data
    # print(draw_number)
    # http_request = "http://applications.opap.gr/DrawsRestServices/proto/{0}.json".format(draw_number)
    # response = urllib.request.urlopen(http_request)
    # print(response)
    # draw_text_data = response.read().decode('utf-8')
    # draw_json_data = json.loads(draw_text_data)
    # return draw_json_data

def create_drawsdata_file():
    try:
        fh = open("protodraws.csv","w")
        return fh
    except IOError:
        return None

if __name__ == "__main__":
    try:
        print("OPAP PROTO PROGRAM")
        progMenu = ProgramMenu()
        progMenu.print_menu()
        option_selected = input('Select an option: ')

        if progMenu.validate_option(option_selected):
            action_str = progMenu.get_action_str(option_selected)
            action_num = progMenu.get_action_num(option_selected)
            print(action_str)
            if action_num == 1:
                lastdraw_json_data = fetch_proto_last_draw()
                print_proto_draw( lastdraw_json_data )
            elif action_num == 2:
                lastdraw_json_data = fetch_proto_last_draw()
                print("Last 'Proto' Draw Number: ", lastdraw_json_data['draw']['drawNo'])
                drawdat_fh = None

                try:
                    drawdat_fh = open("protodraws.csv","r+b")
                except IOError:
                    print("'PROTO' draws' data CSV file does not exist.")
                    drawsfile_exists = False

                    # Create the CSV file.
                    drawdat_fh = create_drawsdata_file()
                    if drawdat_fh == None:
                        raise SystemExit
                reader = csv.reader(drawdat_fh)
                draw_data = []

                if reader.line_num > 0:
                    for line in reader:
                        draw_data.append(line)

                if drawdat_fh != None:
                    drawdat_fh.close()
                    drawdat_fh = open("protodraws.csv","a")
                    writer = csv.writer(drawdat_fh)

                    print("Available 'PROTO' draws: {0}".format(len(draw_data)))

                    # tmp_counter = 0
                    #
                    # for a_draw_num in range(1,1000):
                    #     draw_json_data = fetch_proto_draw(a_draw_num)
                    #     writer.writerow( draw_json_data_to_tuple(draw_json_data))
                    #     tmp_counter += 1
                    #
                    #     if tmp_counter == 250:
                    #         tmp_counter = 0
                    #         print("Sleeping for 5 seconds...")
                    #         time.sleep(5)

                    tmp_counter = 0

                    for a_draw_num in range(-715,1,1):
                        draw_json_data = fetch_proto_draw(a_draw_num)
                        writer.writerow( draw_json_data_to_tuple(draw_json_data))
                        tmp_counter += 1
                        if tmp_counter == 250:
                            time.sleep(5)
                            tmp_counter = 0

                    start_draw_num = len(draw_data) + 1
                    end_draw_num   = lastdraw_json_data['draw']['drawNo']

                    tmp_counter = 0

                    for a_draw_num in range(1,end_draw_num+1,1):
                        draw_json_data = fetch_proto_draw(a_draw_num)
                        writer.writerow( draw_json_data_to_tuple(draw_json_data))
                        tmp_counter += 1
                        if tmp_counter == 250:
                            time.sleep(5)
                            tmp_counter = 0

                    drawdat_fh.close()
            else:
                print("SANITY CHECK ERROR")
    except SystemExit:
        print("Exiting script...")
        sys.exit()