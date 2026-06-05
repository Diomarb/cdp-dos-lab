# cdp-dos-lab
Lab ataque DoS mediante protocolo CDP

# CDP DoS Lab — Seguridad de Redes
**Matrícula:** 2024-1185

---
Playlist: https://www.youtube.com/playlist?list=PLedgCpC2B7oUOUOG7D6VLYsRR7i7bySIM

Enlace del video: https://youtu.be/RI4xwDZU1qc?si=rYKOYqE5mTRvvCYF


## Descripción

Script Python que realiza un ataque de **Denegación de Servicio (DoS)** mediante el protocolo **CDP (Cisco Discovery Protocol)**. El ataque consiste en inundar la tabla CDP de un switch Cisco con miles de paquetes falsos, cada uno simulando un dispositivo Cisco diferente, provocando agotamiento de memoria y CPU.

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Linux (probado en Linux2024 / Debian) |
| Python | 3.x |
| Librería | Scapy (`pip3 install scapy`) |
| Privilegios | root (sudo) |
| Simulador | GNS3 con IOU Cisco |

---

## Instalación

```bash
pip3 install scapy
```

---

## Uso

```bash
sudo python3 cdp_dos.py -i <interfaz> [opciones]
```

### Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-i` / `--interface` | Interfaz de red | `-i eth0` |
| `-c` / `--count` | Número de paquetes (0=infinito) | `-c 500` |
| `-d` / `--delay` | Delay entre paquetes en segundos | `-d 0.01` |
| `-v` / `--verbose` | Mostrar cada paquete enviado | `--verbose` |

### Ejemplos

```bash
# Enviar 500 paquetes con output detallado
sudo python3 cdp_dos.py -i eth0 -c 500 -v

# Ataque continuo (Ctrl+C para detener)
sudo python3 cdp_dos.py -i eth0

# Con delay de 10ms entre paquetes
sudo python3 cdp_dos.py -i eth0 -c 1000 -d 0.01
```

---

## Topología

```
IOU1 (Router — 192.168.1.1)
      |  Ethernet0/0
    IOU2 (Switch — Víctima CDP)
      |  Ethernet0/3
Linux2024 (Atacante — 192.168.1.30)
```
<img width="703" height="298" alt="image" src="https://github.com/user-attachments/assets/8cb1dd5c-8f55-45bf-9dfd-9d79594d507b" />

### Tabla de Direccionamiento

| Dispositivo | Interfaz | IP | Máscara | Rol |
|-------------|----------|----|---------|-----|
| IOU1 | Ethernet0/0 | 192.168.1.1 | /24 | Router |
| IOU2 | Ethernet0/0 | — | — | Switch Capa 2 |
| Linux2024 | eth0 | 192.168.1.30 | /24 | Atacante |

---

## Verificación del Ataque

En el switch víctima (IOU2):

```
show cdp neighbors
show cdp neighbors detail
show processes cpu
show memory statistics
```
<img width="975" height="791" alt="image" src="https://github.com/user-attachments/assets/3643af44-1d6b-4274-aed2-99cd0ef88722" />

<img width="916" height="558" alt="image" src="https://github.com/user-attachments/assets/f818fd21-679d-44e6-b39f-e8651a4b4f89" />

---

## Contramedida

```bash
# En IOU2 — deshabilitar CDP en el puerto del atacante
conf t
interface Ethernet0/3
 no cdp enable
end
wr
```
<img width="476" height="228" alt="image" src="https://github.com/user-attachments/assets/9e4a7644-c2df-48ff-a0b8-3ea4f9a149a0" />

<img width="416" height="164" alt="image" src="https://github.com/user-attachments/assets/2889f3ca-a1d1-4b9e-8e35-602c5e19964b" />

```bash
# Verificar
show cdp interface
show cdp neighbors
```
<img width="424" height="102" alt="image" src="https://github.com/user-attachments/assets/aeb9799e-7a5f-4c13-92a6-de41a4e52379" />

---

## Video

> Enlace al video de demostración: (https://youtu.be/RI4xwDZU1qc?si=rYKOYqE5mTRvvCYF)

---

## Documentación

Ver archivo `CDP_DoS_Documentacion.pdf` incluido en este repositorio.
