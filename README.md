# Shape Security Bot Detection

Starbucks uses Shape Security for bot detection. This script is to pass that bot detection for any website using Shape Security, like Starbucks or Chipotle for example

Shape Security uses a custom VM in their javascript to execute bytecodes which makes the javascript pretty unreadable. But its still not very hard to decompile the bytecodoes to a proper javascript. For the purpose of this script, I am not going to post the script that can decompile the bytecodes.

## Details of the Bot Detection

The sensor data is first encoded using superpack encoding. Its a custom encoding that Shape Security came up with and they have a github repo for it as well. Then the encoded data is encrypted using a custom encryption function. The encryption function uses two randomized sets of data as seed, let's call them seed1 and seed2. Then the encrypted data is base64 encoded where the standard base64 alphabets are shuffled.

Each time you load a webpage that has Shape Security js enabled, it loads a randomized value for encryption seed1, seed2, the custom alphabet set. And the whole thing is identified with a uuid token which is visibly present in the main javascript and also a bundle seed which is hidden in the bytecodes. I assume Shape Security can calculate and verify the bundle seed, encryption seed1, seed2 and the custom alphabet set value from the uuid token and if you use the same uuid token too many times, they will block it.

So its essential to extract the bundle seed, encryption seeds and the custom alphabet set from the javascript directly which is done in the processrawscript function in sensordata.py

The details of the sensor data generating is also mentioned in sensordata.py

A set of sensor data headers look like this:-

```
X-DQ7Hy5L1-d: ...
X-DQ7Hy5L1-f: ................................................
X-DQ7Hy5L1-a: ................................................
X-DQ7Hy5L1-c: ................................................
X-DQ7Hy5L1-b: .......
```

The ``X-DQ7Hy5L1-`` is a header name prefix which is also hidden in the script but its always the same for the same website, so I didn't write any methods to extract that. It can be found by checking any request from the webpage that has the sensor data headers.

``X-DQ7Hy5L1-d`` is the version header, a constant.

``X-DQ7Hy5L1-f`` is the uuid token header

``X-DQ7Hy5L1-a`` is the main payload containing the sensor data

``X-DQ7Hy5L1-c`` is the bundle seed value

``X-DQ7Hy5L1-b`` is a checksum calculated from the sensor data and the uuid token

The main payload header can be decoded for inspection using the decode function in sensordata.py script. I haven't uploaded a superpack decoder in python yet, but I plan to soon.
