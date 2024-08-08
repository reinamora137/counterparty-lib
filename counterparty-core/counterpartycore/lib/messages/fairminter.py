import decimal
import logging
import struct

from counterpartycore.lib import config, database, exceptions, ledger

logger = logging.getLogger(config.LOGGER_NAME)
D = decimal.Decimal

ID = 90


def initialise(db):
    cursor = db.cursor()

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS fairminters (
            tx_hash TEXT PRIMARY KEY,
            tx_index INTEGER,
            block_index INTEGER,
            source TEXT,
            asset TEXT,
            asset_parent TEXT,
            asset_longname TEXT,
            description TEXT,
            price INTEGER,
            hard_cap INTEGER,
            burn_payment BOOL,
            max_mint_per_tx INTEGER,
            premint_quantity INTEGER,
            start_block INTEGER,
            end_block INTEGER,
            minted_asset_commission INTEGER,
            soft_cap INTEGER,
            soft_cap_deadline_block INTEGER,
            lock_description BOOL,
            lock_quantity BOOL,
            divisible BOOL,
            status TEXT,
        )
    """
    cursor.execute(create_table_sql)

    database.create_indexes(
        cursor,
        "fairminters",
        [
            ["block_index"],
            ["asset"],
            ["source"],
        ],
    )


def validate(
    db,
    source,
    asset,
    asset_parent="",
    price=0,
    max_mint_per_tx=0,
    hard_cap=0,
    premint_quantity=0,
    start_block=0,
    end_block=0,
    soft_cap=0,
    soft_cap_deadline_block=0,
    minted_asset_commission=0.0,
    burn_payment=False,
    lock_description=False,
    lock_quantity=True,
    divisible=True,
    description="",
):
    problems = []

    # check integer parameters
    for optional_int_param in [
        price,
        max_mint_per_tx,
        hard_cap,
        premint_quantity,
        start_block,
        end_block,
        soft_cap,
        soft_cap_deadline_block,
    ]:
        if optional_int_param is not None:
            if not isinstance(optional_int_param, int):
                problems.append(f"{optional_int_param} must be an integer.")
            elif optional_int_param < 0:
                problems.append(f"{optional_int_param} must be >= 0.")
    # check boolean parameters
    for option_bool_param in [burn_payment, lock_description, lock_quantity, divisible]:
        if not isinstance(option_bool_param, bool):
            problems.append(f"{option_bool_param} must be a boolean.")
    # check minted_asset_commission
    if minted_asset_commission is not None:
        if not isinstance(minted_asset_commission, float):
            problems.append("minted_asset_commission must be a float")
        elif minted_asset_commission < 0 or minted_asset_commission >= 1:
            problems.append("minted_asset_commission must be >=0 and <1")

    try:
        ledger.generate_asset_id(asset)
        if asset_parent != "":
            ledger.generate_asset_id(asset_parent)
    except exceptions.AssetNameError as e:
        problems.append(f"Invalid asset name: {e}")

    asset_name = asset
    if asset_parent != "":
        asset_name = f"{asset_parent}.{asset}"
    existing_asset = ledger.get_asset(db, asset_name)

    # check if existing asset is locked, issued by source, hard cap is reached
    if existing_asset:
        if existing_asset["locked"]:
            problems.append(f"Asset {asset_name} is locked.")
        if existing_asset["issuer"] != source:
            problems.append(f"Asset {asset_name} is not issued by {source}.")
        if description != "" and existing_asset["description_locked"]:
            problems.append(f"Description of asset {asset_name} is locked.")
        if hard_cap and existing_asset["supply"] >= hard_cap:
            problems.append(f"Hard cap of asset {asset_name} is already reached.")

    if price == 0 and max_mint_per_tx == 0:
        problems.append("Price or max_mint_per_tx must be > 0.")

    if premint_quantity > 0 and premint_quantity >= hard_cap:
        problems.append("Premint quantity must be < hard cap.")

    if end_block < 0:
        problems.append("End block must be >= 0.")
    if start_block > 0 and end_block > 0 and start_block >= end_block:
        problems.append("Start block must be < end block.")

    if hard_cap > 0 and soft_cap >= hard_cap:
        problems.append("Soft cap must be < hard cap.")
    if soft_cap > 0:
        if not soft_cap_deadline_block:
            problems.append("Soft cap deadline block must be specified if soft cap is specified.")
        elif end_block > 0 and soft_cap_deadline_block >= end_block:
            problems.append("Soft cap deadline block must be < end block.")

    return problems


def compose(
    db,
    source,
    asset,
    asset_parent="",
    price=0,
    max_mint_per_tx=0,
    hard_cap=0,
    premint_quantity=0,
    start_block=0,
    end_block=0,
    soft_cap=0,
    soft_cap_deadline_block=0,
    minted_asset_commission=0.0,
    burn_payment=False,
    lock_description=False,
    lock_quantity=True,
    divisible=True,
    description="",
):
    # validate parameters
    problems = validate(
        db,
        source,
        asset,
        asset_parent,
        price,
        max_mint_per_tx,
        hard_cap,
        premint_quantity,
        start_block,
        end_block,
        soft_cap,
        soft_cap_deadline_block,
        minted_asset_commission,
        burn_payment,
        lock_description,
        lock_quantity,
        divisible,
        description,
    )
    if len(problems) > 0:
        raise exceptions.ComposeError(problems)

    minted_asset_commission_int = int((minted_asset_commission or 0) * 1e8)

    # create message
    data = struct.pack(config.SHORT_TXTYPE_FORMAT, ID)
    data_content = "|".join(
        [
            asset,
            asset_parent,
            price,
            max_mint_per_tx,
            hard_cap,
            premint_quantity,
            start_block,
            end_block,
            soft_cap,
            soft_cap_deadline_block,
            minted_asset_commission_int,
            burn_payment,
            lock_description,
            lock_quantity,
            divisible,
            description,
        ]
    )
    data += struct.pack(f">{len(data_content)}s", data_content)
    return (source, [], data)


def unpack(message, return_dict=False):
    try:
        data_content = struct.unpack(f">{len(message)}s", message)[0].decode("utf-8").split("|")
        (
            asset,
            asset_parent,
            price,
            max_mint_per_tx,
            hard_cap,
            premint_quantity,
            start_block,
            end_block,
            soft_cap,
            soft_cap_deadline_block,
            minted_asset_commission_int,
            burn_payment,
            lock_description,
            lock_quantity,
            divisible,
        ) = data_content[0:15]
        description = "|".join(data_content[15:]) if len(data_content) > 15 else ""

        minted_asset_commission = D(minted_asset_commission_int) / D(1e8)

        if return_dict:
            return {
                "asset": asset,
                "asset_parent": asset_parent,
                "price": int(price),
                "max_mint_per_tx": int(max_mint_per_tx),
                "hard_cap": int(hard_cap),
                "premint_quantity": int(premint_quantity),
                "start_block": int(start_block),
                "end_block": int(end_block),
                "soft_cap": int(soft_cap),
                "soft_cap_deadline_block": int(soft_cap_deadline_block),
                "minted_asset_commission": int(minted_asset_commission),
                "burn_payment": bool(burn_payment),
                "lock_description": bool(lock_description),
                "lock_quantity": bool(lock_quantity),
                "divisible": bool(divisible),
                "description": description,
            }
        else:
            return (
                asset,
                asset_parent,
                int(price),
                int(max_mint_per_tx),
                int(hard_cap),
                int(premint_quantity),
                int(start_block),
                int(end_block),
                int(soft_cap),
                int(soft_cap_deadline_block),
                int(minted_asset_commission),
                bool(burn_payment),
                bool(lock_description),
                bool(lock_quantity),
                bool(divisible),
                description,
            )
    except Exception as e:
        raise exceptions.UnpackError(f"Cannot unpack fair minter message: {e}") from e


def parse(db, tx, message):
    (
        asset,
        asset_parent,
        price,
        max_mint_per_tx,
        hard_cap,
        premint_quantity,
        start_block,
        end_block,
        soft_cap,
        soft_cap_deadline_block,
        minted_asset_commission,
        burn_payment,
        lock_description,
        lock_quantity,
        divisible,
        description,
    ) = unpack(message)

    problems = validate(
        db,
        tx["source"],
        asset,
        asset_parent,
        price,
        max_mint_per_tx,
        hard_cap,
        premint_quantity,
        start_block,
        end_block,
        soft_cap,
        soft_cap_deadline_block,
        minted_asset_commission,
        burn_payment,
        lock_description,
        lock_quantity,
        divisible,
        description,
    )

    status = "pending"
    if problems:
        status = "invalid: " + "; ".join(problems)
    else:
        if start_block == 0 or tx["block_index"] >= start_block:
            status = "open"
        if end_block > 0 and tx["block_index"] > end_block:
            status = "closed"

    asset_longname = ""
    if asset_parent == "":
        asset_longname = f"{asset_parent}.{asset}"

    bindings = {
        "tx_hash": tx["tx_hash"],
        "tx_index": tx["tx_index"],
        "block_index": tx["block_index"],
        "source": tx["source"],
        "asset": asset,
        "asset_parent": asset_parent,
        "asset_longname": asset_longname,
        "description": description,
        "price": price,
        "hard_cap": hard_cap,
        "burn_payment": burn_payment,
        "max_mint_per_tx": max_mint_per_tx,
        "premint_quantity": premint_quantity,
        "start_block": start_block,
        "end_block": end_block,
        "minted_asset_commission": minted_asset_commission,
        "soft_cap": soft_cap,
        "soft_cap_deadline_block": soft_cap_deadline_block,
        "lock_description": lock_description,
        "lock_quantity": lock_quantity,
        "divisible": divisible,
        "status": status,
    }
    ledger.insert_record(db, "fairminters", bindings, "NEW_FAIRMINTER")

    if len(problems) == 0:
        # calculate fee
        fee = 0
        if asset_parent == "" and not asset.startswith("A"):
            # named asset
            fee = 0.5

        quantity = premint_quantity

        bindings = {
            "tx_index": tx["tx_index"],
            "tx_hash": tx["tx_hash"],
            "block_index": tx["block_index"],
            "asset": asset,
            "quantity": quantity,
            "divisible": divisible,
            "source": tx["source"],
            "issuer": tx["source"],
            "transfer": False,
            "callable": False,
            "call_date": 0,
            "call_price": 0,
            "description": description,
            "fee_paid": fee,
            "locked": False,
            "reset": False,
            "status": "valid",
            "asset_longname": asset_longname,
        }
        ledger.insert_record(db, "issuances", bindings, "ASSET_ISSUANCE")
