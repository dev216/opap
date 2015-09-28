#!/usr/bin/python2.7

__author__ = 'nassos'

import os
import sys
#import urllib.request
import http.client
import json
import csv
import time
import random
from progmenu import ProgramMenu
from collections import OrderedDict

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

def print_statistics(winning_columns):

    winning_columns_4digit_parts_dict = OrderedDict()
    not_winning_columns_4digit_parts = []

    for a_winning_column in winning_columns:
        head_part = a_winning_column[0:4]
        tail_part = a_winning_column[-4:]
        if head_part in winning_columns_4digit_parts_dict.keys():
            winning_columns_4digit_parts_dict[head_part] += 1
        else:
            winning_columns_4digit_parts_dict[head_part] = 1

        if tail_part in winning_columns_4digit_parts_dict.keys():
            winning_columns_4digit_parts_dict[tail_part] += 1
        else:
            winning_columns_4digit_parts_dict[head_part] = 1

    for a_num in range(1,10000):
        four_digit_str = "{0:04d}".format(a_num)
        if four_digit_str not in winning_columns_4digit_parts_dict.keys():
            not_winning_columns_4digit_parts.append(four_digit_str)

    print_not_winning_columns_4digit_parts(not_winning_columns_4digit_parts,4)

    # winning_columns_statistics_len = len(winning_columns_4digit_parts_dict.keys())
    # remaining = winning_columns_statistics_len % 8
    # full = int( ( winning_columns_statistics_len - remaining ) / 8 )
    # lines_to_print = 0
    # if remaining == 0:
    #     if winning_columns_statistics_len > 0:
    #         lines_to_print = full
    # else:
    #     lines_to_print = full + 1
    #
    # row_element_counter = 0
    # line_counter = 0
    # line_str_to_print = ""
    # for a_key in winning_columns_4digit_parts_dict.keys():
    #     line_str_to_print += "{0}:{1}".format(a_key,winning_columns_4digit_parts_dict[a_key])
    #     row_element_counter += 1
    #     if row_element_counter == 8:
    #         row_element_counter = 0
    #         line_str_to_print += "\n"
    #         line_counter += 1
    #     else:
    #         line_str_to_print += "\t"
    #
    #     if line_counter == 10:
    #         print(line_str_to_print)
    #         line_str_to_print = ""
    #         row_element_counter = 0
    #         line_counter = 0
    #         next_page_prompt = input("Press any key for the next page...")
    #
    # if len( line_str_to_print ) > 0:
    #     print(line_str_to_print)

def print_not_winning_columns_4digit_parts(not_winning_columns_4digit_parts,numbers_to_generate):
    print(not_winning_columns_4digit_parts)
    tmplen = len(not_winning_columns_4digit_parts)
    generated_numbers = []
    generated_numbers_parts = []
    if numbers_to_generate >= 1 and numbers_to_generate <= 10:
        while len(generated_numbers) < numbers_to_generate:
            index = random.randint(0,tmplen-1)
            head_part = not_winning_columns_4digit_parts[index]
            head_part_last_char = head_part[-1]
            if head_part not in generated_numbers_parts:
                generated_numbers_parts.append(head_part)
                tail_part_found = False
                while tail_part_found == False:
                    index = random.randint(0,tmplen-1)
                    tail_part = not_winning_columns_4digit_parts[index]
                    if tail_part in generated_numbers_parts:
                        continue
                    else:
                        tail_part_first_char = tail_part[0]
                        if head_part_last_char == tail_part_first_char:
                            generated_numbers_parts.append(tail_part)
                            generated_numbers.append("{0}{1}{2}".format(head_part[0:3],head_part_last_char,tail_part[-3:]))
                            tail_part_found = True
                        else:
                            continue
            else:
                continue
    print(generated_numbers)
    return generated_numbers

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

            elif action_num == 3:
                drawdat_fh = open("protodraws.csv","r")
                reader = csv.reader(drawdat_fh)
                winning_columns = []
                for draw_line_row in reader:
                    # print(draw_line_row)
                    winning_column_digits_list_str = draw_line_row[2]
                    winning_column_str = ""
                    for a_char in winning_column_digits_list_str:
                        if a_char.isdigit():
                            winning_column_str += a_char
                    if winning_column_str not in winning_columns:
                        winning_columns.append(winning_column_str)
                    # else:
                    #     print(draw_line_row[0:2])
                    #     print(winning_column_str)
                drawdat_fh.close()
                print(len(winning_columns))
                print_statistics(winning_columns)

            else:
                print("SANITY CHECK ERROR")
    except SystemExit:
        print("Exiting script...")
        sys.exit()