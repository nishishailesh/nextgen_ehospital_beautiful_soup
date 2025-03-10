#!/bin/sh
systemctl daemon-reload
systemctl enable /lib/systemd/system/ehospital.service
#rename services and edit lines above
