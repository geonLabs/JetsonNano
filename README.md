# JetsonNano
## 1. WSL Ubuntu 18.04.6 설치
Windows powershell에서 `wsl --list --online` 로 배포판 확인 후 `wsl --install -d Ubuntu-18.04`로 18.04 설치 Jetson nano의 경우 18.04에서 설치 가능

## 2. WSL USB연결
https://github.com/dorssel/usbipd-win/releases 에 들어가 usbipd-win_4.3.0.msi 설치
powershell 관리자 권한으로 실행
 
```
usbipd list # 연결된 usb port 확인
usbipd bind -b 1-6 # 필자의 경우 1-6으로 확인됨
usbipd attach --wsl --busid 1-6 --auto-attach
```

## 3. 기본 라이브러리 설치
```
sudo apt-get update
sudo apt-get install nautilus x11-apps firefox ubuntu-desktop -y
```

## 4. dpkg설치 오류
```
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo apt install -y binfmt-support qemu-user-static

sudo update-binfmts \
 --package qemu-user \
 --install qemu-aarch64 /usr/bin/qemu-aarch64-static \
 --magic '\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00' \
 --mask '\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'

wget https://github.com/qemu/qemu/raw/master/scripts/qemu-binfmt-conf.sh
chmod +x qemu-binfmt-conf.sh
sudo ./qemu-binfmt-conf.sh --qemu-path /usr/bin --qemu-suffix -static --debian
sudo update-binfmts --import qemu-aarch64
```

## 5. L4T Driver Package(BSP), Sample Root Filesystem 설치
```
wget [https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/jetson-210_linux_r32.7.1_aarch64.tbz2](https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/jetson-210_linux_r32.7.1_aarch64.tbz2)
wget [https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2](https://developer.nvidia.com/embedded/l4t/r32_release_v7.1/t210/tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2)

sudo tar xfp jetson-210_ #tab 치세요
sudo tar xfp tegra_linux_sample-root-filesystem_r32.7.1_aarch64.tbz2 -C Linux_for_Tegra/rootfs
sudo ./Linux_for_Tegra/apply_binaries.sh

cd Linux_for_Tegra
sudo ./flash.sh jetson-nano-devkit-emmc mmcblk0p1
```
