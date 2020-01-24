'''
Created on 19.04.2014
Updated 24.01.2020

@author: Christoph Gerneth, Patrick Gesenhues
'''

from csv import DictReader
import xml.etree.ElementTree as xml
import time
import re

from os.path import expanduser
from optparse import OptionParser

# Provides cli options
op = OptionParser(usage="convert your Contacts to FritzBox-Phonebook xml")
op.add_option("-i", dest="filename_in", help="input file (Outlook CSV format)")
op.add_option("-o", dest="filename_out", help="output file (xml)")
op.add_option("-d", dest="debug", action='store_true', help="debug mode")
(options, args) = op.parse_args()

# validate cli options
if options.filename_in and options.filename_out:
    filename_in = expanduser(options.filename_in)
    filename_out = expanduser(options.filename_out)
else:
    op.error("i need input AND output (-h is for help)")

# relevant phone number types (google -> fritz)
trans_number = {"Home": "home",
                "Mobile": "mobile",
                "Work": "work"
                }
typePattern = re.compile("(Phone )\\d{1,2}( - Type)")

# open csv in reading mode
with open(filename_in, "r") as file:
    reader = DictReader(file)

    # needed by fritz xml
    phonebooks = xml.Element("phonebooks")
    phonebook = xml.SubElement(phonebooks, "phonebook")

    # read linewise
    contact_count = 1
    for row in reader:
        contact = xml.SubElement(phonebook, "contact")
        category = xml.SubElement(contact, "category")
        category.text = "0"
        contact_count += 1

        person = xml.SubElement(contact, "person")
        realName = xml.SubElement(person, "realName")

        # Setup Contact Name
        # todo: Add more than just family name and given name
        realName.text = "%s %s" % (row["Family Name"], row["Given Name"])

        # create telephony xml container to store phone information
        telephony = xml.SubElement(contact, "telephony")
        number_counter = 0

        # filter whole contact information to only contain phone information
        phoneDicts = {
            k: v for k, v in row.items()
            if typePattern.match(k)
        }
        for numberTypeKey, numberType in phoneDicts.items():
            if numberType == "":
                continue

            phonenumber = xml.SubElement(telephony,
                                         "number",
                                         {"id": str(number_counter),
                                          "prio": "0",
                                          "type": numberType,
                                          }
                                         )
            keyList = list(row.keys())
            values = list(row.values())
            phonenumber.text = values[keyList.index(numberTypeKey) + 1]
            number_counter += 1
        telephony.set("nid", str(number_counter + 1))

service = xml.SubElement(contact, "services", {"nid": "1"})
mail = xml.SubElement(service, "email", {"classifier": "private", "id": "0"})
mail.text = ""

xml.SubElement(contact, "setup")

mod_time = xml.SubElement(contact, "mod_time")
mod_time.text = str(int(time.time()))

uid = xml.SubElement(contact, "uniqueid")
uid.text = str(contact_count)
elemTree = xml.ElementTree(element=phonebooks)

if options.debug == True:
    root = elemTree.getroot()
    xml.dump(root)

print("[parsed %i contacts]" % contact_count)
print("[writing to '%s']" % filename_out)
elemTree.write(filename_out)
