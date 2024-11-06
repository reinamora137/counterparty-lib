SCENARIO = [
    {
        "title": "Create asset PARENTA",
        "transaction": "issuance",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "PARENTA",
            "quantity": 1000 * 10**8,
            "divisible": True,
            "description": "My super asset PARENTA",
        },
        "controls": [],
    },
    {
        "title": "Create subasset PARENTA",
        "transaction": "issuance",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "PARENTA.SUBASSETA",
            "quantity": 1000 * 10**8,
            "divisible": True,
            "description": "My super subasset SUBASSETA",
        },
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_ISSUANCE",
                "result": [
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_5",
                        "params": {
                            "asset": "A95428960939749879",
                            "asset_events": "creation",
                            "asset_longname": "PARENTA.SUBASSETA",
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0.0,
                            "callable": False,
                            "description": "My super subasset SUBASSETA",
                            "description_locked": False,
                            "divisible": True,
                            "fee_paid": 0,
                            "issuer": "$ADDRESS_8",
                            "locked": False,
                            "quantity": 100000000000,
                            "reset": False,
                            "source": "$ADDRESS_8",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    }
                ],
            }
        ],
    },
    {
        "title": "Create asset PARENTB",
        "transaction": "issuance",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "PARENTB",
            "quantity": 1000 * 10**8,
            "divisible": True,
            "description": "My super asset PARENTB",
        },
        "controls": [],
    },
    {
        "title": "Create subasset PARENTB",
        "transaction": "issuance",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "PARENTB.SUBASSETB",
            "quantity": 1000 * 10**8,
            "divisible": True,
            "description": "My super subasset SUBASSETB",
        },
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_ISSUANCE",
                "result": [
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_5",
                        "params": {
                            "asset": "A95428960545690062",
                            "asset_events": "creation",
                            "asset_longname": "PARENTB.SUBASSETB",
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0.0,
                            "callable": False,
                            "description": "My super subasset SUBASSETB",
                            "description_locked": False,
                            "divisible": True,
                            "fee_paid": 0,
                            "issuer": "$ADDRESS_8",
                            "locked": False,
                            "quantity": 100000000000,
                            "reset": False,
                            "source": "$ADDRESS_8",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    }
                ],
            }
        ],
    },
    {
        "title": "Create fairminter on existing subasset",
        "transaction": "fairminter",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "A95428960939749879",
            "max_mint_per_tx": 100,
        },
        "set_variables": {
            "FREEFAIRMINT_SUBASSET_TX_HASH": "$TX_HASH",
        },
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_ISSUANCE,NEW_FAIRMINTER",
                "result": [
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_4",
                        "params": {
                            "asset": "A95428960939749879",
                            "asset_events": "open_fairminter",
                            "asset_longname": "PARENTA.SUBASSETA",
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0,
                            "callable": False,
                            "description": "My super subasset SUBASSETA",
                            "divisible": True,
                            "fair_minting": True,
                            "fee_paid": 0,
                            "issuer": "$ADDRESS_8",
                            "locked": False,
                            "quantity": 0,
                            "reset": False,
                            "source": "$ADDRESS_8",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                    {
                        "event": "NEW_FAIRMINTER",
                        "event_index": "$EVENT_INDEX_3",
                        "params": {
                            "asset": "A95428960939749879",
                            "asset_longname": "PARENTA.SUBASSETA",
                            "asset_parent": "PARENTA",
                            "block_index": "$BLOCK_INDEX",
                            "burn_payment": False,
                            "description": "My super subasset SUBASSETA",
                            "divisible": True,
                            "end_block": 0,
                            "hard_cap": 0,
                            "lock_description": False,
                            "lock_quantity": False,
                            "max_mint_per_tx": 100,
                            "minted_asset_commission_int": 0,
                            "pre_minted": False,
                            "premint_quantity": 0,
                            "price": 0,
                            "quantity_by_price": 1,
                            "soft_cap": 0,
                            "soft_cap_deadline_block": 0,
                            "source": "$ADDRESS_8",
                            "start_block": 0,
                            "status": "open",
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                ],
            }
        ],
    },
    {
        "title": "Create fairminter on existing subasset 2",
        "transaction": "fairminter",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "SUBASSETA",
            "asset_parent": "PARENTA",
            "max_mint_per_tx": 100,
        },
        "expected_error": ["Fair minter already opened for `PARENTA.SUBASSETA`."],
    },
    {
        "title": "Create fairminter on existing subasset 2",
        "transaction": "fairminter",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "SUBASSETB",
            "asset_parent": "PARENTB",
            "max_mint_per_tx": 100,
        },
        "set_variables": {
            "FREEFAIRMINT_SUBASSET_TX_HASH": "$TX_HASH",
        },
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_ISSUANCE,NEW_FAIRMINTER",
                "result": [
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_7",
                        "params": {
                            "asset": "A95428960545690062",
                            "asset_events": "open_fairminter",
                            "asset_longname": "PARENTB.SUBASSETB",
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0,
                            "callable": False,
                            "description": "My super subasset SUBASSETB",
                            "divisible": True,
                            "fair_minting": True,
                            "fee_paid": 0,
                            "issuer": "$ADDRESS_8",
                            "locked": False,
                            "quantity": 0,
                            "reset": False,
                            "source": "$ADDRESS_8",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                    {
                        "event": "NEW_FAIRMINTER",
                        "event_index": "$EVENT_INDEX_6",
                        "params": {
                            "asset": "A95428960545690062",
                            "asset_longname": "PARENTB.SUBASSETB",
                            "asset_parent": "PARENTB",
                            "block_index": "$BLOCK_INDEX",
                            "burn_payment": False,
                            "description": "My super subasset SUBASSETB",
                            "divisible": True,
                            "end_block": 0,
                            "hard_cap": 0,
                            "lock_description": False,
                            "lock_quantity": False,
                            "max_mint_per_tx": 100,
                            "minted_asset_commission_int": 0,
                            "pre_minted": False,
                            "premint_quantity": 0,
                            "price": 0,
                            "quantity_by_price": 1,
                            "soft_cap": 0,
                            "soft_cap_deadline_block": 0,
                            "source": "$ADDRESS_8",
                            "start_block": 0,
                            "status": "open",
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                ],
            }
        ],
    },
    {
        "title": "Create fairminter on existing subasset 2",
        "transaction": "fairminter",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "A95428960545690062",
            "max_mint_per_tx": 100,
        },
        "expected_error": ["Fair minter already opened for `PARENTB.SUBASSETB`."],
    },
    {
        "title": "Create subasset fairminter on  asset",
        "transaction": "fairminter",
        "source": "$ADDRESS_8",
        "params": {
            "asset": "SUBASSETC",
            "asset_parent": "PARENTB",
            "max_mint_per_tx": 100,
        },
        "set_variables": {
            "FREEFAIRMINT_SUBASSET_TX_HASH": "$TX_HASH",
        },
        "controls": [
            {
                "url": "blocks/$BLOCK_INDEX/events?event_name=ASSET_ISSUANCE,NEW_FAIRMINTER",
                "result": [
                    {
                        "event": "ASSET_ISSUANCE",
                        "event_index": "$EVENT_INDEX_5",
                        "params": {
                            "asset": "A95428960586448133",
                            "asset_events": "open_fairminter",
                            "asset_longname": "PARENTB.SUBASSETC",
                            "block_index": "$BLOCK_INDEX",
                            "call_date": 0,
                            "call_price": 0,
                            "callable": False,
                            "description": "",
                            "divisible": True,
                            "fair_minting": True,
                            "fee_paid": 0,
                            "issuer": "$ADDRESS_8",
                            "locked": False,
                            "quantity": 0,
                            "reset": False,
                            "source": "$ADDRESS_8",
                            "status": "valid",
                            "transfer": False,
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                    {
                        "event": "NEW_FAIRMINTER",
                        "event_index": "$EVENT_INDEX_3",
                        "params": {
                            "asset": "A95428960586448133",
                            "asset_longname": "PARENTB.SUBASSETC",
                            "asset_parent": "PARENTB",
                            "block_index": "$BLOCK_INDEX",
                            "burn_payment": False,
                            "description": "",
                            "divisible": True,
                            "end_block": 0,
                            "hard_cap": 0,
                            "lock_description": False,
                            "lock_quantity": False,
                            "max_mint_per_tx": 100,
                            "minted_asset_commission_int": 0,
                            "pre_minted": False,
                            "premint_quantity": 0,
                            "price": 0,
                            "quantity_by_price": 1,
                            "soft_cap": 0,
                            "soft_cap_deadline_block": 0,
                            "source": "$ADDRESS_8",
                            "start_block": 0,
                            "status": "open",
                            "tx_hash": "$TX_HASH",
                            "tx_index": "$TX_INDEX",
                        },
                        "tx_hash": "$TX_HASH",
                    },
                ],
            }
        ],
    },
]
