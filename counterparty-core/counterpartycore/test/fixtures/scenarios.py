"""
This file defines the fixtures used for unit testing and integration testing scenarios. The fixtures are required to test the
full range of functionality. They are also used in integration testing, with additional scenarios to test different signing types.
The folder `test/fixtures/scenarios` contains the expected output (.json, .log and .sql) for each scenario. The integration suite
tests if the outputs of all scenarios are identical. It also tests the similarity between the output of a scenario and its base
scenario (for instance `simplesig` scenario is the base scenario for all mutlisig scenarios).

To add (or update) a transaction in a scenario, or add a scenario, just update `scenarios.py` and run `py.test --skiptestbook=all --savescenarios`
This command will generates new outputs for each scenario (.new.json, .new.sql and .new.log), if you are satisfied with the new output just rename them (remove the .new).
You need to do this every time you update UNITTEST_FIXTURE.

```
mv counterpartycore/test/fixtures/scenarios/unittest_fixture.new.json counterpartycore/test/fixtures/scenarios/unittest_fixture.json
mv counterpartycore/test/fixtures/scenarios/unittest_fixture.new.sql counterpartycore/test/fixtures/scenarios/unittest_fixture.sql
mv counterpartycore/test/fixtures/scenarios/unittest_fixture.new.log counterpartycore/test/fixtures/scenarios/unittest_fixture.log
```

Before every entry in UNITTEST_FIXTURE is executed a block is inserted first, so each of them has a +1 block_index.
The `create_next_block` that appears a few times bumps the height to a fixed number to keep things easier to test against.
When you add more fixtures, add before 310490, that won't affect any of other vector (for a while).

Some functions' output depends on scenarios staying the same (for instance, function returning the last message).
Here's a list of unit tests that will fail and need to be updated:
- blocks.get_next_tx_index
- blocks.parse_block
- util.last_message
- util.get_balance
"""

from .params import ADDR, MULTISIGADDR, P2SH_ADDR, P2WPKH_ADDR
from .params import DEFAULT_PARAMS as DP

UNITTEST_FIXTURE = [
    ["burn", (ADDR[0], DP["burn_quantity"]), {"encoding": "multisig"}],  # 310000
    [
        "issuance",
        (ADDR[0], "DIVISIBLE", DP["quantity"] * 1000, None, True, None, None, "Divisible asset"),
        {"encoding": "multisig"},
    ],
    [
        "issuance",
        (ADDR[0], "NODIVISIBLE", 1000, None, False, None, None, "No divisible asset"),
        {"encoding": "multisig"},
    ],
    [
        "issuance",
        (ADDR[0], "CALLABLE", 1000, None, True, None, None, "Callable asset"),
        {"encoding": "multisig"},
    ],
    [
        "issuance",
        (ADDR[0], "LOCKED", 1000, None, True, None, None, "Locked asset"),
        {"encoding": "multisig"},
    ],
    ["issuance", (ADDR[0], "LOCKED", 0, None, True, None, None, "LOCK"), {"encoding": "multisig"}],
    [
        "order",
        (ADDR[0], "XCP", DP["quantity"], "DIVISIBLE", DP["quantity"], 2000, 0),
        {"encoding": "multisig"},
    ],
    ["send", (ADDR[0], ADDR[1], "DIVISIBLE", DP["quantity"]), {"encoding": "multisig"}, None],
    ["send", (ADDR[0], ADDR[1], "XCP", DP["quantity"]), {"encoding": "multisig"}, None],
    [
        "order",
        (ADDR[0], "XCP", DP["quantity"], "DIVISIBLE", DP["quantity"], 2000, 0),
        {"encoding": "multisig"},
    ],
    [
        "order",
        (
            ADDR[0],
            "XCP",
            DP["quantity"],
            "BTC",
            round(DP["quantity"] / 100),
            2000,
            DP["fee_required"],
        ),
        {"encoding": "multisig"},
    ],
    [
        "order",
        (ADDR[0], "BTC", round(DP["quantity"] / 150), "XCP", DP["quantity"], 2000, 0),
        {"encoding": "multisig", "fee_provided": DP["fee_provided"]},
    ],
    ["send", (ADDR[0], MULTISIGADDR[0], "XCP", DP["quantity"] * 3), {"encoding": "multisig"}, None],
    [
        "send",
        (ADDR[0], MULTISIGADDR[0], "DIVISIBLE", DP["quantity"] * 10),
        {"encoding": "multisig"},
        None,
    ],
    ["send", (ADDR[0], ADDR[1], "NODIVISIBLE", 5), {"encoding": "multisig"}, None],
    ["send", (ADDR[0], MULTISIGADDR[0], "NODIVISIBLE", 10), {"encoding": "multisig"}, None],
    [
        "issuance",
        (ADDR[0], "MAXI", 2**63 - 1, None, True, None, None, "Maximum quantity"),
        {"encoding": "multisig"},
    ],
    [
        "broadcast",
        (ADDR[0], 1388000000, 1, DP["fee_multiplier"], "Unit Test"),
        {"encoding": "multisig"},
    ],
    ["broadcast", (ADDR[2], 1288000000, 1, 0.0, "lock"), {"encoding": "multisig"}],
    ["bet", (ADDR[0], ADDR[0], 1, 1388000001, 9, 9, 0.0, 5040, 100), {"encoding": "multisig"}],
    ["bet", (ADDR[1], ADDR[0], 0, 1388000001, 9, 9, 0.0, 5040, 100), {"encoding": "multisig"}],
    ["create_next_block", 100],  # 310100
    ["bet", (ADDR[1], ADDR[0], 3, 1388000200, 10, 10, 0.0, 5040, 1000), {"encoding": "multisig"}],
    [
        "broadcast",
        (ADDR[0], 1388000002, 1, DP["fee_multiplier"], "Unit Test"),
        {"encoding": "multisig"},
    ],
    ["burn", (ADDR[4], DP["burn_quantity"]), {"encoding": "multisig"}],
    ["burn", (ADDR[5], DP["burn_quantity"]), {"encoding": "multisig"}],
    ["burn", (ADDR[6], DP["burn_quantity"]), {"encoding": "multisig"}],
    ["burn", (ADDR[8], DP["burn_verysmall_quantity"]), {"encoding": "multisig"}],
    ["dispenser", (ADDR[5], "XCP", 100, 100, 100, 0), {"encoding": "opreturn"}],
    ["burn", (P2SH_ADDR[0], int(DP["burn_quantity"] / 2)), {"encoding": "opreturn"}],
    [
        "issuance",
        (P2SH_ADDR[0], "PAYTOSCRIPT", 1000, None, False, None, None, "PSH issued asset"),
        {"encoding": "multisig", "multisig_pubkey": DP["pubkey"][ADDR[0]]},
    ],
    [
        "send",
        (ADDR[0], P2SH_ADDR[0], "DIVISIBLE", DP["quantity"]),
        {"encoding": "multisig", "multisig_pubkey": DP["pubkey"][ADDR[0]]},
        None,
    ],
    [
        "broadcast",
        (P2SH_ADDR[0], 1388000002, 1, DP["fee_multiplier"], "Unit Test"),
        {"encoding": "opreturn"},
    ],
    [
        "bet",
        (P2SH_ADDR[0], P2SH_ADDR[0], 3, 1388000200, 10, 10, 0.0, 5040, 1000),
        {"encoding": "opreturn"},
    ],
    # locked with an issuance after lock
    [
        "issuance",
        (ADDR[6], "LOCKEDPREV", 1000, None, True, None, None, "Locked asset"),
        {"encoding": "multisig"},
    ],
    [
        "issuance",
        (ADDR[6], "LOCKEDPREV", 0, None, True, None, None, "LOCK"),
        {"encoding": "multisig"},
    ],
    [
        "issuance",
        (ADDR[6], "LOCKEDPREV", 0, None, True, None, None, "changed"),
        {"encoding": "multisig"},
    ],
    ["burn", (P2WPKH_ADDR[0], DP["burn_quantity"]), {"encoding": "opreturn"}],
    ["create_next_block", 480],
    # force 2 enhanced sends
    [
        "send",
        (ADDR[0], ADDR[1], "XCP", DP["quantity"], "hello", False, True),
        {"encoding": "opreturn"},
        {"enhanced_sends": True},
    ],
    [
        "send",
        (ADDR[1], ADDR[0], "XCP", DP["quantity"], "fade0001", True, True),
        {"encoding": "opreturn"},
        {"enhanced_sends": True},
    ],
    ["create_next_block", 485],
    [
        "broadcast",
        (ADDR[4], 1388000000, 1, DP["fee_multiplier"], "Unit Test"),
        {"encoding": "multisig"},
    ],
    ["bet", (ADDR[4], ADDR[4], 1, 1388000001, 9, 9, 0.0, 5040, 100), {"encoding": "multisig"}],
    # To test REQUIRE_MEMO
    [
        "broadcast",
        (ADDR[4], 1388000002, 1, 0.0, "options 0"),
        {"encoding": "multisig"},
        {"options_require_memo": True},
    ],
    ["broadcast", (ADDR[4], 1388000003, 1, 0.0, "lock"), {"encoding": "multisig"}],
    # To test REQUIRE_MEMO
    [
        "broadcast",
        (ADDR[6], 1388000004, 1, 0.0, "options 1"),
        {"encoding": "multisig"},
        {"options_require_memo": True},
    ],
    # ['create_next_block', 490],
    [
        "order",
        (
            ADDR[0],
            "XCP",
            DP["quantity"],
            "BTC",
            round(DP["quantity"] / 125),
            2000,
            DP["fee_required"],
        ),
        {"encoding": "multisig"},
    ],
    [
        "order",
        (ADDR[1], "BTC", round(DP["quantity"] / 125), "XCP", DP["quantity"], 2000, 0),
        {"encoding": "multisig", "exact_fee": DP["fee_provided"]},
    ],
    ["burn", (ADDR[2], DP["burn_quantity"]), {"encoding": "multisig"}],
    [
        "issuance",
        (ADDR[2], "DIVIDEND", 100, None, True, "Test dividend", None, None),
        {"encoding": "multisig"},
    ],
    ["send", (ADDR[2], ADDR[3], "DIVIDEND", 10), {"encoding": "multisig"}, None],
    ["send", (ADDR[2], ADDR[3], "XCP", 92945878046), {"encoding": "multisig"}, None],
    [
        "issuance",
        (ADDR[0], "PARENT", DP["quantity"] * 1, None, True, None, None, "Parent asset"),
        {"encoding": "opreturn"},
    ],
    [
        "issuance",
        (
            ADDR[0],
            "PARENT.already.issued",
            DP["quantity"] * 1,
            None,
            True,
            None,
            None,
            "Child of parent",
        ),
        {"encoding": "opreturn"},
    ],
    [
        "fairminter",
        (ADDR[0], "FREEFAIRMIN", "", 0, 1, 10),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairminter",
        (ADDR[0], "PAIDFAIRMIN", "", 10, 1, 0),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairmint",
        (ADDR[0], "FREEFAIRMIN", 0),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairminter",
        (
            ADDR[0],  # source
            "RAIDFAIRMIN",  # asset
            "",  # asset_parent
            10,  # price
            1,  # quantity_by_price
            10,  # max_mint_per_tx
            30,  # hard_cap
            20,  # premint_quantity
        ),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairminter",
        (
            ADDR[0],  # source
            "QAIDFAIRMIN",  # asset
            "",  # asset_parent,
            10,  # price=0,
            1,  # quantity_by_price
            0,  # max_mint_per_tx,
            50,  # hard_cap=0,
            20,  # premint_quantity=0,
            0,  # start_block=0,
            0,  # end_block=0,
            20,  # soft_cap=0,
            400000,  # soft_cap_deadline_block=0,
            0.5,  # minted_asset_commission=0.0,
        ),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairminter",
        (
            ADDR[1],  # source
            "A160361285792733729",  # asset
            "",  # asset_parent,
            10,  # price=0,
            1,  # quantity_by_price
            0,  # max_mint_per_tx,
            50,  # hard_cap=0,
            20,  # premint_quantity=0,
            0,  # start_block=0,
            0,  # end_block=0,
            20,  # soft_cap=0,
            310520,  # soft_cap_deadline_block=0,
            0.3,  # minted_asset_commission=0.0,
            False,  # burn_payment=False,
            True,  # lock_description=False,
            True,  # lock_quantity
            True,  # divisible
            "softcap description",
        ),
        {"encoding": "multisig"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairmint",
        (ADDR[1], "A160361285792733729", 10),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "fairmint",
        (ADDR[1], "A160361285792733729", 20),
        {"encoding": "opreturn"},
        {"short_tx_type_id": True, "fairminter": True},
    ],
    [
        "attach",
        (ADDR[0], "XCP", 100),
        {"encoding": "multisig"},
        {"short_tx_type_id": True, "utxo_support": True, "spend_utxo_to_detach": True},
    ],
    [
        "attach",
        (
            ADDR[0],
            "DIVISIBLE",
            1,
        ),
        {"encoding": "multisig"},
        {"short_tx_type_id": True, "utxo_support": True, "spend_utxo_to_detach": True},
    ],
    [
        "issuance",
        (ADDR[5], "TESTDISP", 1000, None, False, None, None, "Test dispensers asset"),
        {"encoding": "multisig"},
    ],
    ["dispenser", (ADDR[5], "TESTDISP", 100, 100, 100, 0), {"encoding": "opreturn"}],
    ["create_next_block", 703],
]

PARSEBLOCKS_FIXTURE = UNITTEST_FIXTURE + [
    ["create_next_block", 704, False]  # parse_block=False so we can unittest blocks.parse_block
]


def generate_standard_scenario(address1, address2, order_matches):
    """Return a predefined set of transactions to test different types of signing."""
    return [
        ["burn", (address1, int(0.62 * DP["quantity"])), {"encoding": "multisig"}],
        ["send", (address1, address2, "XCP", DP["small"]), {"encoding": "multisig"}, None],
        [
            "order",
            (address1, "BTC", DP["small"], "XCP", DP["small"] * 2, DP["expiration"], 0),
            {"encoding": "multisig", "exact_fee": DP["fee_provided"]},
        ],
        [
            "order",
            (
                address1,
                "XCP",
                round(DP["small"] * 2.1),
                "BTC",
                DP["small"],
                DP["expiration"],
                DP["fee_required"],
            ),
            {"encoding": "multisig"},
        ],
        ["btcpay", (address1, order_matches[0]), {"encoding": "multisig"}],
        [
            "issuance",
            (address1, "BBBB", DP["quantity"] * 10, None, True, None, None, ""),
            {"encoding": "multisig"},
        ],
        [
            "issuance",
            (address1, "BBBC", round(DP["quantity"] / 1000), None, False, None, None, "foobar"),
            {"encoding": "multisig"},
        ],
        [
            "send",
            (address1, address2, "BBBB", round(DP["quantity"] / 25)),
            {"encoding": "multisig"},
            None,
        ],
        [
            "send",
            (address1, address2, "BBBC", round(DP["quantity"] / 190000)),
            {"encoding": "multisig"},
            None,
        ],
        ["dividend", (address1, 600, "BBBB", "XCP"), {"encoding": "multisig"}],
        ["dividend", (address1, 800, "BBBC", "XCP"), {"encoding": "multisig"}],
        [
            "broadcast",
            (address1, 1388000000, 100, 0.99999999, "Unit Test"),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                0,
                1388000100,
                DP["small"],
                round(DP["small"] / 2),
                0.0,
                15120,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                1,
                1388000100,
                round(DP["small"] / 2),
                round(DP["small"] * 0.83),
                0.0,
                15120,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                0,
                1388000100,
                DP["small"] * 3,
                DP["small"] * 7,
                0.0,
                5040,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                1,
                1388000100,
                DP["small"] * 7,
                DP["small"] * 3,
                0.0,
                5040,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                2,
                1388000200,
                DP["small"] * 15,
                DP["small"] * 13,
                1,
                5040,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "bet",
            (
                address1,
                address1,
                3,
                1388000200,
                DP["small"] * 13,
                DP["small"] * 15,
                1,
                5040,
                DP["expiration"],
            ),
            {"encoding": "multisig"},
        ],
        [
            "broadcast",
            (
                address1,
                1388000050,
                round(100 - (0.415 / 3) - 0.00001, 5),
                DP["fee_multiplier"],
                "Unit Test",
            ),
            {"encoding": "multisig"},
        ],
        [
            "broadcast",
            (address1, 1388000101, 100.343, DP["fee_multiplier"], "Unit Test"),
            {"encoding": "multisig"},
        ],
        [
            "broadcast",
            (address1, 1388000201, 2, DP["fee_multiplier"], "Unit Test"),
            {"encoding": "multisig"},
        ],
        [
            "order",
            (address1, "BBBB", DP["small"], "XCP", DP["small"], DP["expiration"], 0),
            {"encoding": "multisig"},
        ],
        [
            "burn",
            (address1, (1 * DP["quantity"]), True),
            {"encoding": "multisig"},
        ],  # Try to burn a whole 'nother BTC.
        ["send", (address1, address2, "BBBC", 10000), {"encoding": "multisig"}, None],
        ["create_next_block", 101],
    ]


standard_scenarios_params = {
    "simplesig": {
        "address1": ADDR[0],
        "address2": ADDR[1],
        "order_matches": [
            "af8c1bec82dec4f7ddb77eafb129e3f8e47e95e283ce7224d4c28e6ee69aabab_ef249bd74fcfea725635e02e49e9c792f4b4109c1f3378c5a18a2395ef2d7504"
        ],
    },
    "multisig_1_of_2": {
        "address1": MULTISIGADDR[0],
        "address2": MULTISIGADDR[1],
        "order_matches": [
            "5f2272489b2c35bb58a1e014004bb730bc9bcd8e6386587c75a97536570e897b_a5c22744b12848286d77e68c8ecc073e779d78c056948e3f190a031cf491ade5"
        ],
    },
    "multisig_2_of_2": {
        "address1": MULTISIGADDR[3],
        "address2": MULTISIGADDR[4],
        "order_matches": [
            "8e5917ea002c66ff984539a110f9a309361b591e6b19d19b7d3f51862b06cb24_1a4653caf52308d72ed7d0328fe3016722e282b62bfccefb8e9bf76f6dbb6aea"
        ],
    },
    "multisig_1_of_3": {
        "address1": MULTISIGADDR[5],
        "address2": MULTISIGADDR[6],
        "order_matches": [
            "9f5de4ea5b89249f8588efd7f086d25be1ba35bc71f6a98a67a854c1ad90ab70_f392f7180c4e71a8de800832be946a2d9e86cedf73937031f8d92815ed06ab42"
        ],
    },
    "multisig_2_of_3": {
        "address1": MULTISIGADDR[7],
        "address2": MULTISIGADDR[8],
        "order_matches": [
            "0882dc106624f7c8b29f7ab0d44a9e13a154967e45a03d132dd6e057b3de0d42_6540319330edbb4531739bd1b335ce95e7c8b2788e7e8ac32a07321ec4cd51e5"
        ],
    },
    "multisig_3_of_3": {
        "address1": MULTISIGADDR[9],
        "address2": MULTISIGADDR[10],
        "order_matches": [
            "adef5785d2d981123ac83691a8c5bef53b9f87901f9fa01939da3733bb0ade8a_d0dd774649ef223b690cc4592e691e70e3058aa748a83511cbed124169063994"
        ],
    },
}

INTEGRATION_SCENARIOS = {
    "unittest_fixture": (UNITTEST_FIXTURE, "unittest_fixture"),
    "parseblock_unittest_fixture": (PARSEBLOCKS_FIXTURE, "parseblock_unittest_fixture"),
}
# Generate special tests for simplesig, multisig2 and multisig3 using standard scenario.
for scenario_name, params in standard_scenarios_params.items():
    INTEGRATION_SCENARIOS[scenario_name] = (
        generate_standard_scenario(**params),
        scenario_name,
    )
