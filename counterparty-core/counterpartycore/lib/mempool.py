import logging
import time

from counterpartycore.lib import blocks, config, exceptions, ledger

logger = logging.getLogger(config.LOGGER_NAME)


def parse_mempool_transaction(db, decoded_tx):
    logger.debug("Parsing mempool transaction: %s" % decoded_tx["tx_hash"])
    now = time.time()
    transaction_events = []
    try:
        with db:
            cursor = db.cursor()
            # insert fake block
            cursor.execute(
                """INSERT INTO blocks(
                                block_index,
                                block_hash,
                                block_time) VALUES(?,?,?)""",
                (config.MEMPOOL_BLOCK_INDEX, config.MEMPOOL_BLOCK_HASH, now),
            )
            # list_tx
            cursor.execute("SELECT tx_index FROM transactions ORDER BY tx_index DESC LIMIT 1")
            mempool_tx_index = cursor.fetchone()["tx_index"]
            blocks.list_tx(
                db,
                config.MEMPOOL_BLOCK_HASH,
                config.MEMPOOL_BLOCK_INDEX,
                now,
                decoded_tx["tx_hash"],
                tx_index=mempool_tx_index,
                decoded_tx=decoded_tx,
            )
            # parse fake block
            blocks.parse_block(db, config.MEMPOOL_BLOCK_INDEX, now)
            # get messages generated by the transaction
            cursor.execute(
                """SELECT * FROM messages WHERE block_index = ?""",
                (config.MEMPOOL_BLOCK_INDEX,),
            )
            # save the events in memory
            transaction_events = cursor.fetchall()
            # we raise an exception to rollback the transaction
            raise exceptions.MempoolError("Mempool transaction parsed successfully")
    except exceptions.MempoolError:
        # save events in the mempool table
        for event in transaction_events:
            bindings = event | {"tx_hash": decoded_tx["tx_hash"]}
            cursor.execute(
                """INSERT INTO mempool VALUES(:tx_hash, :command, :category, :bindings, :timestamp, :event)""",
                bindings,
            )


def clean_transaction_events(db, tx_hash):
    cursor = db.cursor()
    cursor.execute("DELETE FROM mempool WHERE tx_hash = ?", (tx_hash,))


def clean_mempool(db):
    logger.debug("Cleaning mempool...")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mempool")
    mempool_events = cursor.fetchall()
    for event in mempool_events:
        tx = ledger.get_transaction(db, event["tx_hash"])
        if tx:
            clean_transaction_events(db, event["tx_hash"])
