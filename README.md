# BlockChainPy
**_Academic project for the university.
It consists of the creation of a blockchain network for the use of smart contracts in a work proposal._**

## How to use
Install the requirements and run the MeineAPI file which is the blockchain node.
```py
pip3 install -r requirements.txt
python3 MeineAPI.py
```

_I use the Thunder Client extension in VS Code for testing, you may find it useful for not having to use postman._

## Transaction format

```json
{
    "type":"Contract/Payment", //any of then, only are an example
    "company":"MDPM",
    "client":"Z",
    "taskcode":"MDPM-010",
    "deadline":"2022-05-26 00:00:00",  //recomend use datetime equivalent in the client
    "amountr":5000,
    "currency":"P"
}
```

## Files
There are only 2 files, the Blockchain class and the API (Node) implementation
### Blockchain.py
_It's a simple implementation of a blockchain, the important things are:_
- Every method and argument of the class has their respective data type
- The code are separated by region to make it easier to read
- The hashing algorithm is SHA3-512
### MeineAPI
- Every method has their respective data type
- The code are separated by region to make it easier to read
- It needs to always have the Blockchain class in the path to be executed as it is its main dependency.
