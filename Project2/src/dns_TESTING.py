def open_dns():
    dns_file = open("PROJ2-DNSTS2.txt", "r")
    dns = {}
    
    for line in dns_file:
        line = line.strip()
        word = line.split(' ')
        dns[word[0]] = line

    dns_file.close()

    print(dns)
    

open_dns()