#!/usr/bin/env py
import configpath as cfgpath
from configparser import ConfigParser
import json
import csv
import time


def load_config(configpath, section):
    '''
    Use configparser to load the .ini file with the header information
    '''
    parser = ConfigParser()  # Create parser
    parser.read(configpath)  # Read config ini file
    config = {}  # Create empty dictionary for config
    if parser.has_section(section):  # Look for section in config ini file
        params = parser.items(section)  # Parse config ini file
        for param in params:  # Loop through parameters
            config[param[0]] = param[1]  # Set key-value pair for parameter in dictionary
    else:  # Raise exception if the section can't be found
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, configpath))
    config['header'] = config['header'].split(',')  # Convert header string into list
    config['rename_from'] = config['rename_from'].split(',')  # Convert rename_from string into list
    config['rename_to'] = config['rename_to'].split(',')  # Convert rename_to string into list
    config['split_from'] = config['split_from'].split(',')  # Convert split_from string into list
    config['split_to'] = config['split_to'].split(';')  # Convert split_to string into list
    config['splitter'] = config['splitter'].split(',')  # Convert splitter string into list
    return config


def load_json(config):
    '''
    Load the json file with the input data
    '''
    with open(config['datapath'], 'r') as f:  # Open from datapath in config
        jsondat = json.load(f)  # Load json file
    if config['subset'] != '':
        jsondat = jsondat['locations']  # Extract subset key
    return jsondat


def create_writer(config):
    '''
    Open output csv file and create csvwriter object
    '''
    csvout = open(config['outputpath'], 'w', newline='')  # Open csv output writer
    csvwriter = csv.writer(csvout)  # Create csv writer object
    return csvout, csvwriter


def rename_var(config, loc):
    '''
    Rename variables in config['rename_from'] to config['rename_to']
    '''
    for r in range(len(config['rename_from'])):
        loc[config['rename_to'][r]] = loc.pop(config['rename_from'][r])
    return loc


def split_var(config, loc):
    '''
    Split variables from config['split_from'] to config['split_to']
    '''
    for s in range(len(config['split_from'])):
        if config['splitter'][s] != '':  # Get rid of newline, split the variable into a list of two
            splitvar = loc.pop(config['split_from'][s]).replace('\n', '').split(config['splitter'][s])
        else:  # Use an empty splitter
            splitvar = loc.pop(config['split_from'][s]).replace('\n', '').split()
        splitto = config['split_to'][s].split(',')  # Subset the split variables
        while splitto:  # Insert split variable into loc until all have been reinserted
            if len(splitvar) >= 1:
                loc[splitto.pop()] = splitvar.pop()
            else:
                loc[splitto.pop()] = ''
    return loc


def remove_vars(config, loc):
    '''
    Remove variables not in config header
    '''
    to_delete = set(loc.keys()).difference(config['header'])
    for d in to_delete:
        del loc[d]
    return loc


def library_write(csvwriter, loc):
    '''
    Write cleaned row of data to csv
    '''
    csvwriter.writerow(loc)  # Write to csv


def library_clean(config, jsondat, csvwriter):
    '''
    Clean and transform data before writing to csv
    '''
    for loc in jsondat:  # Loop through rows
        if config['rowkey'] != '':
            loc = loc[config['rowkey']]  # Extract from row key

        if config['rename_from'] != '':
            loc = rename_var(config, loc)  # Rename pre-determined variables

        if config['split_from'] != '':
            loc = split_var(config, loc)  # Split pre-determined variables

        loc['processing_date'] = time.strftime('%d-%m-%Y')  # add processing_date to row

        loc = remove_vars(config, loc)  # Remove variables not in config header

        loc = [loc[k] for k in config['header']]  # Sort dictionary by header before writing to csv
        library_write(csvwriter, loc)  # Write to csv


if __name__ == '__main__':
    config = load_config(cfgpath.configpath, 'config')  # Load config file from configpath
    jsondat = load_json(config)  # Load json input file
    csvout, csvwriter = create_writer(config)  # Open output file and create csvwriter
    csvwriter.writerow(config['header'])  # Write header to csv
    library_clean(config, jsondat, csvwriter)  # Clean and write data to csv
    csvout.close()  # Close output file
