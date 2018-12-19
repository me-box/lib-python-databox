import pythonzestclient
import unittest

zestEndpoint="tcp://127.0.0.1:5555"
zestDealerEndpoint="tcp://127.0.0.1:5556"
CORE_STORE_KEY="vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<"
tokenString=b"secrete"

class WriteReadTestCase(unittest.TestCase):
    def setUp(self):
        self.zc = pythonzestclient.PyZestClient(CORE_STORE_KEY,zestEndpoint,zestDealerEndpoint)

    def tearDown(self):
        print("Tearing Down")

    def testKVWrite(self):
        payLoad='{"name":"testuser", "age":37}'
        path='/kv/test/key1'
        contentFormat='JSON'
        response = self.zc.post(path, payLoad, contentFormat,tokenString)
        self.assertEqual(response,None)

    def testKVRead(self):
        expected='{"name":"testuser", "age":37}'
        path='/kv/test/key1'
        contentFormat='JSON'
        response = self.zc.get(path, contentFormat,tokenString)
        print("ReadTestCase:: response=" + str(response))
        self.assertEqual(response,expected)

if __name__ == '__main__':
    unittest.main()