
# Real-Time Fraud Analytics for Credit Card Transaction 🚀   
Built using Python Streamlit

To run this code , you need to setup launch.json inside .vscode folder. No need to checkin this folder

launch.json
```
{

    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "debug streamlit",
            "type": "python",
            "request": "launch",
            "program": "/usr/local/bin/streamlit",  
            "args": [
                "run",
                "Streamlit_app.py"
            ]
        }
    ]
}
```

For streamlit confidential credentials 

Create a folder .streamlit and a file secrets.toml

secrets.toml
```
[default]
"bootstrap.servers"="pkc-lgwgm.eastus2.azure.confluent.cloud:9092"
"security.protocol"="SASL_SSL"
"sasl.mechanisms"="PLAIN"
"sasl.username"="******"
"sasl.password"="******"

[consumer]
"group.id"="python_example_group_2"
# 'auto.offset.reset=earliest' to start reading from the beginning of
# the topic if no committed offsets exist.
"auto.offset.reset"="earliest"

[telegram]
"BOT_API_KEY" = "******"
```
To get Confulent server credential
bootstrap.servers 

To get Telegram bot token
BOT_API_KEY

## Get Started  
To debug in local mode

Run the following command in shell 
```
/usr/local/bin/streamlit run Streamlit_app.py
```

Deploy the code using git integration with Streamlit portal 

Push some sample data via Kafka producer
    

