SCENARIO = [
    {
        "title": "Create asset CHAINING",
        "transaction": "issuance",
        "source": "$ADDRESS_10",
        "no_confirmation": True,
        "params": {
            "asset": "CHAINING",
            "quantity": 10 * 10**8,
            "divisible": True,
            "description": "My super asset CHAINING",
        },
        "set_variables": {
            "CREATE_CHAINING_TX_HASH": "$TX_HASH",
            "CREATE_CHAINING_TX_INDEX": "$TX_INDEX",
        },
        "controls": [],
    },
    {
        "title": "Attach CHAINING to UTXO",
        "transaction": "attach",
        "source": "$ADDRESS_10",
        "no_confirmation": True,
        "params": {
            "asset": "CHAINING",
            "quantity": 1 * 10**8,
            "validate": False,
            "inputs_set": "$CREATE_CHAINING_TX_HASH:1",
        },
        "set_variables": {
            "ATTACH_CHAINING_TX_HASH": "$TX_HASH",
            "ATTACH_CHAINING_TX_INDEX": "$TX_INDEX",
        },
        "controls": [],
    },
    {
        "title": "Move CHAINING from UTXO to UTXO",
        "transaction": "movetoutxo",
        "source": "$ATTACH_CHAINING_TX_HASH:0",  # second output of attach transaction, first is OP_RETURN
        "no_confirmation": True,
        "dont_wait_mempool": True,
        "params": {
            "destination": "$ADDRESS_8",
            "validate": False,
            "inputs_set": "$ATTACH_CHAINING_TX_HASH:2",
        },
        "set_variables": {
            "MOVETOUTXO_CHAINING_TX_HASH": "$TX_HASH",
            "MOVETOUTXO_CHAINING_TX_INDEX": "$TX_INDEX",
        },
        "controls": [],
    },
    {
        "title": "Detach CHAINING from UTXO",
        "transaction": "detach",
        "source": "$MOVETOUTXO_CHAINING_TX_HASH:0",
        "no_confirmation": True,
        "dont_wait_mempool": True,
        "params": {
            "validate": False,
            "inputs_set": "$MOVETOUTXO_CHAINING_TX_HASH:0,$MOVETOUTXO_CHAINING_TX_HASH:1",
        },
        "set_variables": {
            "DETACH_CHAINING_TX_HASH": "$TX_HASH",
            "DETACH_CHAINING_TX_INDEX": "$TX_INDEX",
        },
        "controls": [],
    },
    {
        "title": "mint empty block to trigger order expiration",
        "transaction": "mine_blocks",
        "params": {"blocks": 1},
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_CREATION,ASSET_ISSUANCE,DEBIT,CREDIT,ATTACH_TO_UTXO,DETACH_FROM_UTXO,UTXO_MOVE,INCREMENT_TRANSACTION_COUNT,TRANSACTION_PARSED",
                "result": [
                    {
                        "event": "TRANSACTION_PARSED",
                        "event_index": "$EVENT_INDEX_23",
                        "params": {
                            "supported": True,
                            "tx_hash": "$DETACH_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$DETACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "DETACH_FROM_UTXO",
                        "event_index": "$EVENT_INDEX_22",
                        "params": {
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "destination": "$ADDRESS_8",
                            "fee_paid": 0,
                            "msg_index": 0,
                            "quantity": 100000000,
                            "source": "$MOVETOUTXO_CHAINING_TX_HASH:0",
                            "status": "valid",
                            "tx_hash": "$DETACH_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$DETACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "CREDIT",
                        "event_index": "$EVENT_INDEX_21",
                        "params": {
                            "address": "$ADDRESS_8",
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "calling_function": "detach from utxo",
                            "event": "$DETACH_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX",
                            "utxo": None,
                            "utxo_address": None,
                        },
                        "tx_hash": "$DETACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "DEBIT",
                        "event_index": "$EVENT_INDEX_20",
                        "params": {
                            "action": "detach from utxo",
                            "address": None,
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "event": "$DETACH_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX",
                            "utxo": "$MOVETOUTXO_CHAINING_TX_HASH:0",
                            "utxo_address": "$ADDRESS_8",
                        },
                        "tx_hash": "$DETACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "TRANSACTION_PARSED",
                        "event_index": "$EVENT_INDEX_19",
                        "params": {
                            "supported": True,
                            "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 1",
                        },
                        "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                    },
                    {
                        "event": "UTXO_MOVE",
                        "event_index": "$EVENT_INDEX_18",
                        "params": {
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "destination": "$MOVETOUTXO_CHAINING_TX_HASH:0",
                            "msg_index": 0,
                            "quantity": 100000000,
                            "source": "$ATTACH_CHAINING_TX_HASH:0",
                            "status": "valid",
                            "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 1",
                        },
                        "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                    },
                    {
                        "event": "CREDIT",
                        "event_index": "$EVENT_INDEX_17",
                        "params": {
                            "address": None,
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "calling_function": "utxo move",
                            "event": "$MOVETOUTXO_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX - 1",
                            "utxo": "$MOVETOUTXO_CHAINING_TX_HASH:0",
                            "utxo_address": "$ADDRESS_8",
                        },
                        "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                    },
                    {
                        "event": "DEBIT",
                        "event_index": "$EVENT_INDEX_16",
                        "params": {
                            "action": "utxo move",
                            "address": None,
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "event": "$MOVETOUTXO_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX - 1",
                            "utxo": "$ATTACH_CHAINING_TX_HASH:0",
                            "utxo_address": "$ADDRESS_10",
                        },
                        "tx_hash": "$MOVETOUTXO_CHAINING_TX_HASH",
                    },
                    {
                        "event": "TRANSACTION_PARSED",
                        "event_index": "$EVENT_INDEX_15",
                        "params": {
                            "supported": True,
                            "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 2",
                        },
                        "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "ATTACH_TO_UTXO",
                        "event_index": "$EVENT_INDEX_14",
                        "params": {
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "destination": "$ATTACH_CHAINING_TX_HASH:0",
                            "fee_paid": 0,
                            "msg_index": 0,
                            "quantity": 100000000,
                            "source": "$ADDRESS_10",
                            "status": "valid",
                            "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 2",
                        },
                        "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "CREDIT",
                        "event_index": "$EVENT_INDEX_13",
                        "params": {
                            "address": None,
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "calling_function": "attach to utxo",
                            "event": "$ATTACH_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX - 2",
                            "utxo": "$ATTACH_CHAINING_TX_HASH:0",
                            "utxo_address": "$ADDRESS_10",
                        },
                        "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "DEBIT",
                        "event_index": "$EVENT_INDEX_12",
                        "params": {
                            "action": "attach to utxo",
                            "address": "$ADDRESS_10",
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "event": "$ATTACH_CHAINING_TX_HASH",
                            "quantity": 100000000,
                            "tx_index": "$TX_INDEX - 2",
                            "utxo": None,
                            "utxo_address": None,
                        },
                        "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "INCREMENT_TRANSACTION_COUNT",
                        "event_index": "$EVENT_INDEX_11",
                        "params": {
                            "block_index": "$BLOCK_INDEX",
                            "count": 1,
                            "transaction_id": 101,
                        },
                        "tx_hash": "$ATTACH_CHAINING_TX_HASH",
                    },
                    {
                        "event": "TRANSACTION_PARSED",
                        "event_index": "$EVENT_INDEX_10",
                        "params": {
                            "supported": True,
                            "tx_hash": "$CREATE_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 3",
                        },
                        "tx_hash": "$CREATE_CHAINING_TX_HASH",
                    },
                    {
                        "event": "CREDIT",
                        "event_index": "$EVENT_INDEX_9",
                        "params": {
                            "address": "$ADDRESS_10",
                            "asset": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                            "calling_function": "issuance",
                            "event": "$CREATE_CHAINING_TX_HASH",
                            "quantity": 1000000000,
                            "tx_index": "$TX_INDEX - 3",
                            "utxo": None,
                            "utxo_address": None,
                        },
                        "tx_hash": "$CREATE_CHAINING_TX_HASH",
                    },
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_8",
                        "params": {
                            "asset": "CHAINING",
                            "asset_events": "creation",
                            "asset_longname": None,
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0.0,
                            "callable": False,
                            "description": "My super asset CHAINING",
                            "description_locked": False,
                            "divisible": True,
                            "fee_paid": 50000000,
                            "issuer": "$ADDRESS_10",
                            "locked": False,
                            "quantity": 1000000000,
                            "reset": False,
                            "source": "$ADDRESS_10",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$CREATE_CHAINING_TX_HASH",
                            "tx_index": "$TX_INDEX - 3",
                        },
                        "tx_hash": "$CREATE_CHAINING_TX_HASH",
                    },
                    {
                        "event": "ASSET_CREATION",
                        "event_index": "$EVENT_INDEX_7",
                        "params": {
                            "asset_id": "18229920832",
                            "asset_longname": None,
                            "asset_name": "CHAINING",
                            "block_index": "$BLOCK_INDEX",
                        },
                        "tx_hash": "$CREATE_CHAINING_TX_HASH",
                    },
                    {
                        "event": "DEBIT",
                        "event_index": "$EVENT_INDEX_6",
                        "params": {
                            "action": "issuance fee",
                            "address": "$ADDRESS_10",
                            "asset": "XCP",
                            "block_index": "$BLOCK_INDEX",
                            "event": "$CREATE_CHAINING_TX_HASH",
                            "quantity": 50000000,
                            "tx_index": "$TX_INDEX - 3",
                            "utxo": None,
                            "utxo_address": None,
                        },
                        "tx_hash": "$CREATE_CHAINING_TX_HASH",
                    },
                ],
            }
        ],
    },
]
