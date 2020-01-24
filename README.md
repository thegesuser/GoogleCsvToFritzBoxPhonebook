Google CSV to Fritz!Box Phonebook
======================

Fork of [csv2FritzBox_phonebook](https://github.com/c7h/csv2FritzBox_phonebook).

## Changes made: 
- migrated to python 3.6
- Using "Google CSV" format instead of "Outlook CSV"
- minor small improvements

## Example Usage

1. Export your [Google Contacts](https://contacts.google.com) (Format *Google CSV*) to `contacts.csv`
2. run `python3 convertCsvToXml.py -i contacts.csv -o fritzbox_phonebook.xml`
3. open the "restore phonebook dialogue"
3. upload `fritzbox_phonebook.xml`

## Notes

- [original] tested with Fritz!Box 7312
- [fork] tested with Fritz!Box 7590 Fritz!OS 7.12 
