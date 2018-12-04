# Implementation of Go-Back N ARQ and Selective Repeat ARQ   
Use python3 and install the necessary libraries
### Go-Back N ARQ  
First run the server side:  
`python Server.py client_ip common_port file_to_write_to probability_of_loss`   
then run the client side:  
`python Client.py server_ip common_port file_to_trasfer N MSS`   
### Selective Repeat ARQ   
First run the server side:  
`python Server-SR.py client_ip common_port file_to_write_to probability_of_loss N`  
then run the client side:   
`python CLient-SR.py server_ip common_port file_to_trasfer N MSS`   
