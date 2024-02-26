# Network monitoring using SNMP in python using easysnmp API.
This main goal of the project is to probing devices and monitoring
You need to do an extended version of the 'Simple Service Performance' assignment. Described, below. 

The assignment is the same, but you need to augment your solution to support two additional types; GAUGE and OCTET_STR. 

A Gauge assumes values between 0 and 2^32-1, an OCTET_STRING is just a sequence of characters. A Gauge can assume higher, similar or lower values between 'samples'. An OCTET_STRING can change between samples. 

Your solution should handle COUNTER32, COUNTER64, GAUGE, and OCTET_STR. 

You should treat the COUNTERxy as before.

A GAUGE type should show the current value + the relative change compared to the previously successfully read value. 

1504083911  | 72 (+50) | 819027 (-10000) | 0 (+-0) | 281761  (+1023)  ##Example of four Gauge's. 

The OCTET_STRING should just be printed. 

1636556717  | Hello | Jump | ## Examples of two OCTET_STR
1636556718  | ello H| ump J| ## Examples of two OCTET_STR

Of course, your solution should handle ALL types at the same time. 

1504083911  | 2124 | 72 (+50) | Hello | 281761 
1504083912  | 2471 | 90 (+18) | ello H| 450782 
1504083913  | 1904 | 10 (-80) | llo He | 325448 

If you have questions, reach out to me via Teams (ET2598 channel). 

 

1.3.6.1.4.1.4171.40.{1...} gives Counters
1.3.6.1.4.1.4171.50.{4,5,6} gives strings
1.3.6.1.4.1.4171.60.{1...} gives Gauges.

To test your solution, direct your requests to 13.48.17.69:1613, the community is public.

 ----------------------------------------------------------------------

 

Write a script to probe an SNMP agent and find the rate of change for several counters between successive probes/ samples. The rate calculated for each counter/OID should be displayed on the console, one line for each calculated rate, the output format will be described in detail in 'output format'. Furthermore, as the only requirement on the OIDs is that they are of the type COUNTER, this means that there are both 32 and 64 bit versions of counters. Your solution should handle both counter types, and in the case that a counter wraps (ie goes from a high number to a low number), your solution should address/rectify (if its possible). The solution needs also to handle that an SNMP agent restarts (i.e. the sysUpTime OID becomes less than it was before, ie. it starts counting from zero), and timeouts, i.e. the device does not respond to your request in time. It will be tested that your solution maintains the requested sampling frequency (i.e. the requests from your solution should be sent so that the sampling frequency is maintained, irrespectively if the device has responded or not). 

The script will be invoked as follows:

prober <Agent IP:port:community> <sample frequency> <samples> <OID1> <OID2> …….. <OIDn>

where,

IP, port and community are agent details,

OIDn are the OIDs to be probed (they are absolute, cf. IF-MIB::ifInOctets.2 for interface 2, or 1.3.6.1.2.1.2.2.1.10.2 [1]) 

Sample frequency  (Fs) is the sampling frequency expressed in Hz, you should handle between 10 and 0.1 Hz. 

Samples (N) is the number of successful samples the solution should do before terminating, hence the value should be greater or equal to 2. If the value is -1 that means run forever (until CTRL-C is pressed, or the app is terminated in someway). 

 

Following are the files to be submitted:  Note: The file has to be submitted with ".txt" extension so that plagiarism control will work.

prober.txt         	
Script that probes the agent, may be written in any language (perl, python,etc.), make use of the SHEBANG to handle what language interpreter that execute the script. 

If you use a complied language, make sure that the compiler outputs the correct filename on the executable. 

 

Whatever language you choose to implement the solution in, make sure that you use a proper API for the SNMP communication, i.e. using system commands is not the way to do it. The aim is to train API interaction. 

Output format

The output from the script _MUST_ be as follows:

Sample time | ROID1 | ROID2 | .... | ROIDn

 

Sample time: Timestamp of the last sample, in UNIX time (seconds). 

ROID*: Rate of OID* between the last two successful samples

 

As an example:

1504083911  | 2124 | 819 | 0 | 281761 
1504083912  | 2471 | 819 | 110 | 450782 
1504083913  | 1904 | 819 | 2000 | 325448 
 

--Technical Testing--: 

Your solution will be tested against a simulated/real SNMP agent, where the behavior is known.

 

I'll use https://github.com/patrikarlos/anm, A2 for the evaluation. 

 

A test script will be launch your solution and validate the results against the known results. The script will check:

- that the solution generates the correct number of samples, as requested, at the requested sample frequency. 

- that the solution sends the snmp request at the required sampling frequency, will be tested by packet tracing. 

- that the SNMP request contain all the requested OIDs, by packet tracing

- that the solution handles non-responsive SNMP agents, ie. timeouts. Ie the inter-sample time presented in the console would be n/Fs where Fs is sample frequency and n=1,2,3,... 

- that the solution handles that the SNMP agent restarts/reboots

- that the output from the solution matches the configuration of the agent

- that the solution handles counters that wrap around, both 32 and 64-bit counters. 

 

Use SysUpTime[2] to detect device reboots and to obtain the device time when calculating rates. 

Development testing

As the access to SNMP devices can be limited, I've provided access to TWO simulators. They are reachable via 18.219.51.6 port 1611 and port 1612. The one on port 1611, is behaving a bit better than the one in 1612. Their community strings are 'public'. Furthermore, both serve values from two separate configuration files, the 1611's config is public, so you can view and verify what you should get. Access to this file is via 

curl http://18.219.51.6/counters.conf

The information in the file should be read that the first column contains the interface-id-1, the second column contains the 'capacity' (Cx) that that interface has. In this list the base OID is also shown (1.3.6.1.4.1.4171.40.), this is a 'special' OID, so no 'string' version is available. 

1.3.6.1.4.1.4171.40.1 Value of (counter32) device time in seconds.  This is an integer version of Ty, in calculations by the system a high-resolution version is used. 
1.3.6.1.4.1.4171.40.2 Value of (counter32) 1, i.e. y1=C1*Ty 
1.3.6.1.4.1.4171.40.3 Value of (counter32) 2, i.e. y2=C2*Ty
....
1.3.6.1.4.1.4171.40.16 Value of (counter32) 15, i.e. y15=C15*Ty
1.3.6.1.4.1.4171.40.17 Value of (counter64) 16, i.e. y16=C16*Ty
1.3.6.1.4.1.4171.40.18 Value of (counter32) 17, i.e. y17=C17*Ty, however, behaves badly, and randomized when it answers (delay 750ms +rand(1000)*500). 
1.3.6.1.4.1.4171.40.19 Value of (counter64) 2, i.e. y18=C18*Ty, however, behaves really badly, and randomly ignore to respond (50%).  
1.3.6.1.4.1.4171.40.3 Value of (counter64) 3, i.e. y3=C3*Ty 
The service on 1612 uses 64bit counters for all values (1611 alternates between 32 and 64-bit versions). 


 
