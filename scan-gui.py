#!/usr/bin/env python

"""
Name of the script

General script documentation...

Project:        Classwork
Filename:       scan-gui.py
Author:         YOUR_NAME <-- change to your name.
Created:        11/12/2019
Version:        
Finished:       DD/MM/YY <--- When code completed, type in the date completed.

"""

# Import required modules
import ipaddress

import PySimpleGUI as sg
import socket

# Constants
progress_max = 1000


# Module Functions
def doScan(target, port, timeout=1.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        host = f"{ipaddress.IPv4Address(target)}"
        con = s.connect((host, port))
        s.close()
        return True
    except:
        return False


def setupGUI():
    print('set up GUI')


# Main method
def main():
    """
    Main method documentation here
    """
    sg.change_look_and_feel('Material2')

    group_ip = [
        [
            sg.Text('Start IP:', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.InputText(key="start_ip", default_text="127.0.0.1")
        ],
        [
            sg.Text('End IP:', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.InputText(key="end_ip", default_text="127.0.0.1")
        ]
    ]
    group_port = [
        [
            sg.Text('Start Port:', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.Input(key="start_port", default_text="1")
        ],
        [
            sg.Text('End Port:', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.Input(key="end_port", default_text="65535")
        ],
    ]
    group_timeout = [
        [
            sg.Text('Timeout (s):', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.Input(key="timeout", default_text="0.01")
        ],
    ]
    group_threads = [
        [
            sg.Text('Threads:', size=(10, 1), auto_size_text=False,
                    justification='right'),
            sg.Input(key="threads", default_text="1")
        ],
    ]
    group_save_load = [
        [
            sg.Button('Save'),
            sg.Button('Load')
        ],
    ]

    group_quit = [
        [
            sg.Button('Quit')
        ],
    ]
    group_scan = [
        [
            sg.Button('Scan', size=(10, 1))
        ],
    ]

    layout_left = [
        [sg.Text('Port Scan Settings')],

        [sg.Column(group_ip)],
        [sg.Column(group_port)],
        [sg.Column(group_timeout)],
        [sg.Column(group_threads)],
        [
            sg.Column(group_scan),
            sg.ProgressBar(progress_max, orientation='h', size=(27, 20),
                           key='scan_progress',
                           bar_color=("#003399", "#ffffff"))
        ]
    ]
    layout_right = [
        [sg.Text('Scan results')],
        [
            sg.Table(values=[["", ""], ],
                     headings=["IP Address", "Port Number"],
                     size=(40, 12),
                     max_col_width=25,
                     key='results_table',
                     num_rows=10, ),
        ],
        [
            sg.Column(group_save_load),
            sg.Column(group_quit)
        ]
    ]

    layout_status_bar = [
        [
            sg.StatusBar('Ready...',
                         size=(90, 1),
                         auto_size_text=True,
                         relief='sunken',
                         key='status_ready')
        ]
    ]

    layout = [
        [
            sg.Column(layout_left),
            sg.Column(layout_right)
        ],
        [
            sg.Column(layout_status_bar)
        ]
    ]

    window = sg.Window("Port Scanner", layout)

    progress = 0

    while True:
        event, values = window.read(timeout=0.5)
        if event in (None, 'Quit'):
            break

        elif event in ('Save'):
            window['status_ready'].update("Saving data to file...")

        elif event in ('Load'):
            window['status_ready'].update("Reading data from file...")

        elif event in ('Scan'):
            start_host = values['start_ip']
            end_host = values['end_ip']

            start_host_ip = socket.gethostbyname(start_host)
            end_host_ip = socket.gethostbyname(end_host)
            ip_min = ipaddress.IPv4Address(start_host_ip)
            ip_max = ipaddress.IPv4Address(end_host_ip)
            int_ip_min = int(ip_min)
            int_ip_max = int(ip_max)

            port_min = int(values['start_port'])
            port_max = int(values['end_port'])
            num_ports = port_max - port_min + 1
            num_ips = int_ip_max - int_ip_min + 1

            timeout = float(values['timeout'])
            try:
                threads = float(values['threads'])
            except Exception:
                threads = 1

            results = []
            current = 0

            for ip in range(int_ip_min, int_ip_max + 1):
                ip_text = f"{ipaddress.IPv4Address(ip)}"
                window['status_ready'].update("Scanning " + ip_text)
                for port in range(port_min, port_max + 1):
                    current += 1
                    progress = progress_max * (current / (num_ips * num_ports))
                    window['scan_progress'].update_bar(progress)
                    if doScan(ip, port, timeout=timeout):
                        results.append([f"{ip_text}", f"{port}"])
                        window['results_table'].update(results)

            window['status_ready'].update('Scan Complete')
            window['scan_progress'].update_bar(0)

    window.close()


if __name__ == "__main__":
    main()
