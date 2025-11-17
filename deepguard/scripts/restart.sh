#!/usr/bin/env bash
pm2 restart deepguard-backend || true
pm2 restart deepguard-frontend || true
