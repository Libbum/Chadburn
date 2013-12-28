#!/bin/bash
#Gracefully Shutdown the socket server

ps ax | grep './[s]erver.py' | awk '{print $1}' | xargs kill -2
