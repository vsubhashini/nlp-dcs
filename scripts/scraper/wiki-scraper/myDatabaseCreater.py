#!/usr/bin/python

import my_wp_info as wi

xmldump = open('test','r').read();

info_scraper = wi.my_wp_info();
info_scraper.infobox(xmldump.split("\n"));
infobox_List = info_scraper.info;

for infobox in infobox_List:
    #print infobox;
    info_list = infobox.split("\n\n|");
    parsedData={};
    for item in info_list:
        data=item.split("\n");
        if "=" in data[0]:
            columns=data[0].split("=");
            parsedData[columns[0].strip()]=columns[1].strip();
    #print parsedData;
    #need to make db from parsed data dictionary
