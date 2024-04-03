import random

# initializing all the necessary variables that we'll need
p = 110101
#p=input('Choose your "p".')
n = 15
mistakes = 0
mistakes_ber = 0
p = [int(x) for x in str(p)]
# we repeat the following part 1000000 times in order to get 1000000 different signals
for j in range(0, 1000000):
    go = True
    # this part of the code is "responsible" for calculating the FCS at the transmitter
    data = ''
    for i in range(0, 10):
        data = data + str(random.randint(0, 1))

    data_ = [int(x) for x in str(data)]
    data = data + '00000'
    data2 = [int(x) for x in str(data)]
    k = 0
    while n - k + 1 > len(p):
        if data2[k] != 0:
            for i in range(0, 6):
                data2[k + i] = data2[k + i] ^ p[i]  # FCS
        k = k + 1

    # this part of the code "changes" the signal using the random method
    # if we get a number smaller that 10**-3 we change the current bit
    for k in range(0, len(data_)):
        go=True
        if random.random() < 0.001:
            go = False
            if data_[k] == 1:
                data_[k] = 0
            else:
                data_[k] = 1
        if not go:
            mistakes_ber = mistakes_ber + 1
    

    r = ''
    for i in range(10, 15):
        r = r + str(data2[i])

    s = ""
    for ele in range(0, 10):
        s = s + str(data_[ele])
    data3 = s + r
    data3 = [int(x) for x in str(data3)]

    # in this part of the code we check for errors (
    k = 0
    while n - k + 1 > len(p):
        if data3[k] != 0:
            for o in range(0, 6):
                data3[k + o] = data3[k + o] ^ p[o]
        k = k + 1

    found = False
    for i in range(0, 15):
        if data3[i] != 0:
            found = True
    if found:
        mistakes = mistakes + 1
print("Mistakes in BER: ", mistakes_ber)
print("Not Accepted: ", mistakes)
print(" ")
print("Percentage of mistakes at the receiver : ", mistakes_ber / 10000)
print("Percentage of signals detected as errors from CRC : ", mistakes / 10000)
print("Percentage of signals that are errors but are not being detected: ", (mistakes_ber - mistakes) / 10000)
