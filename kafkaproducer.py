#!/usr/bin/env python

import sys
import os , json
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer
import pandas as pd
import streamlit as st
from datetime import datetime

print(st.secrets["default"]["bootstrap.servers"])

if __name__ == '__main__':


    conf = {
        'bootstrap.servers': st.secrets["default"]["bootstrap.servers"],
        'sasl.username': st.secrets["default"]["sasl.username"],
        'sasl.password': st.secrets["default"]["sasl.password"],
        'security.protocol': st.secrets["default"]["security.protocol"],
        'sasl.mechanisms': st.secrets["default"]["sasl.mechanisms"]
    }




    # Create Producer instance
    producer = Producer(conf)

    # Produce data by selecting random values from these lists.
    topic = "topic_0"
    df_test = pd.read_csv(r"./data/fraudTest01.csv")
    df_test.drop(df_test.columns[0], axis=1, inplace=True)
    # Select a record randomly
    json=df_test.sample(1).to_json(orient="records")

    #print(json)
    print("Message sent...")

    producer.produce(topic, value=json)

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()