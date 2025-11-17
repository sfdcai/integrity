#!/usr/bin/env bash
pm2 stop deepguard-backend || true
pm2 stop deepguard-frontend || true
