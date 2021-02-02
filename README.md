etchy
=====

Light weight python tool for reading and writing redis data in json and csv format.


Install
-------

* Get self contained single executable from [Github](https://github.com/mywatch/etchy)
	```
	chmod +x etchy
	```
* Install rpm package from [Github](https://github.com/mywatch/etchy)
    ```
	# This will install under /opt/edis/bin
	sudo yum install <RPM>
    ```


Usage
-----

### Export from Redis

* Command line help
        ```
        ./etchy --help
        ```

* Export from Redis with localhost:6379, and save in data.json using redis key t1
	```
	./etchy export "t1"
	```

* Specify redis host and port
	```
	./etchy export "t1" -h 127.0.0.1 -p 16379
	```

* Specify output file
	```
	./etchy export "t1" -h 127.0.0.1 -p 16379 -f /tmp/data.json
	```

### Import to Redis

* Import from ./data.json
    ```
    ./etchy import
    ```

* Specify filename
    ```
    ./etchy import -f /tmp/data.json
    ```
