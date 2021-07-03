'''
Description
'''
import sys
import json
import hashlib
from time import time

class Blockchain:
    '''
    Description
    '''
    def __init__ ( self, blockchain_file ) :
        '''
        Description
        '''
        self.blockchain_file = blockchain_file
        self.blockchain = []
        self.block = []

    def get_blockchain (self) :
        '''
        Description
        '''
        with open( self.blockchain_file, 'r' ) as blockchain_json:
            blockchain_json = blockchain_json.read()
            self.blockchain = json.loads( blockchain_json )

        return self.blockchain

    def get_last_block ( self ) :
        '''
        Pega o último bloco
        '''
        return self.blockchain[0]

    def set_hash ( self, data, index, previous_hash, timestamp ) :
        '''
        Cria o hash do bloco
        '''
        string = str( data ) + str( index ) + str( previous_hash ) + str( timestamp )
        block_hash = hashlib.sha512( string.encode( 'utf-8' ) ).hexdigest()
        return block_hash

    def set_block ( self, data ) :
        '''
        Cria um novo bloco
        '''
        data = data.encode( 'utf-8' ).hex()
        block_timestamp = time()
        last_block = self.get_last_block()
        index = last_block['index'] + 1
        previous_hash = self.set_hash(
           last_block['data'],
           last_block['index'],
           last_block['previous_hash'],
           last_block['timestamp']
        )
        self.block = {
            'data': data,
            'index': index,
            'hash': self.set_hash( data, index, previous_hash, block_timestamp ),
            'previous_hash': previous_hash,
            'timestamp': block_timestamp,
        }
        return self.block

    def set_blockchain ( self ) :
        '''
        Adiciona o novo bloco na blockchain
        '''
        self.blockchain.insert( 0, self.block )
        with open( self.blockchain_file, 'w' ) as outfile:
            json.dump( self.blockchain, outfile )

        return self.blockchain

    def check_blockchain ( self ) :
        '''
        Verifica a blockchain
        '''
        i = 0
        while i < len( self.blockchain ) :
            if self.blockchain[i]['index'] <= 1 :
                return False

            previous_block = self.blockchain[ i + 1 ]
            previous_hash = self.set_hash (
                previous_block['data'],
                previous_block['index'],
                previous_block['previous_hash'],
                previous_block['timestamp']
            )
            if self.blockchain[i]['previous_hash'] !=  previous_hash :
                return  self.blockchain[i]['hash']

            i = i + 1
        return False

if __name__ == '__main__':
    block = Blockchain( 'blockchain.json' )
    block.get_blockchain()
    check = block.check_blockchain()
    if check :
        print( 'Error block : ' + check )
        sys.exit()

    print( 'Type data' )
    input_data = input()
    new_block = block.set_block( input_data )
    block.set_blockchain()
    print( new_block )
