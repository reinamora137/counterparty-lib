from counterparty_rs import indexer

from counterpartycore.lib import config, util


def deserialize_tx(tx_hex, parse_vouts=False, block_index=None):
    deserializer = indexer.Deserializer(
        {
            "rpc_address": "",
            "rpc_user": "",
            "rpc_password": "",
            "network": config.NETWORK_NAME,
            "db_dir": "",
            "log_file": "",
            "prefix": config.PREFIX,
        }
    )
    current_block_index = block_index or util.CURRENT_BLOCK_INDEX
    return deserializer.parse_transaction(tx_hex, current_block_index, parse_vouts)


def deserialize_block(block_hex, parse_vouts=False, block_index=None):
    deserializer = indexer.Deserializer(
        {
            "rpc_address": "",
            "rpc_user": "",
            "rpc_password": "",
            "network": config.NETWORK_NAME,
            "db_dir": "",
            "log_file": "",
            "prefix": config.PREFIX,
        }
    )
    current_block_index = block_index or util.CURRENT_BLOCK_INDEX
    return deserializer.parse_block(block_hex, current_block_index, parse_vouts)
