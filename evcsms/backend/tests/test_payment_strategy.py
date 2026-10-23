import pytest
from app.services.payment.strategy import (
    PaymentMethod,
    UPIPayment,
    CardPayment,
    WalletPayment,
    PaymentStrategyFactory,
)

class MockCryptoPayment(PaymentMethod):
    """
    Demonstrating SOLID OCP:
    A brand new payment strategy added without touching UPIPayment, CardPayment, or WalletPayment code!
    """
    @property
    def mode_name(self) -> str:
        return "Crypto"

    def process_transaction(self, amount: float, details: dict):
        wallet_address = details.get("crypto_address", "0xABC123")
        return True, "CRYPTO-9999", f"Transferred equivalent crypto to {wallet_address}."


def test_payment_strategy_liskov_substitution():
    """
    Test LSP: All strategies conform to the PaymentMethod interface
    and are swappable without client code breaking.
    """
    strategies = [UPIPayment(), CardPayment(), WalletPayment()]
    amount = 450.0

    for strategy in strategies:
        # Every strategy must have mode_name and implement process_transaction
        assert isinstance(strategy.mode_name, str)
        success, txn_id, msg = strategy.process_transaction(amount, {})
        assert success is True
        assert any(txn_id.startswith(prefix) for prefix in ["UPI-", "CARD-", "WAL-"])
        assert f"{amount:.2f}" in msg


def test_payment_strategy_open_closed_extension():
    """
    Test OCP: Register a new strategy into PaymentStrategyFactory at runtime.
    """
    crypto_strat = MockCryptoPayment()
    PaymentStrategyFactory.register_strategy("Crypto", crypto_strat)

    retrieved = PaymentStrategyFactory.get_strategy("Crypto")
    assert retrieved is crypto_strat
    assert retrieved.mode_name == "Crypto"

    success, txn_id, msg = retrieved.process_transaction(100.0, {"crypto_address": "0xDEADBEEF"})
    assert success is True
    assert txn_id == "CRYPTO-9999"


def test_payment_failure_handling():
    """
    Test that invalid card details triggers failure according to strategy contract.
    """
    card_strat = CardPayment()
    # Card numbers containing '0000' simulate gateway decline
    success, txn_id, msg = card_strat.process_transaction(300.0, {"card_number": "4111000011112222"})
    assert success is False
    assert "declined" in msg.lower()
