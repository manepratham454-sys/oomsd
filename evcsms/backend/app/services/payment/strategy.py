"""
Strategy Pattern for Payment Processing
SOLID Principles Applied:
- Open-Closed Principle (OCP): New payment methods (e.g., CryptoPayment, NetBankingPayment)
  can be added by extending PaymentMethod without altering existing payment processing code.
- Liskov Substitution Principle (LSP): Subclasses UPIPayment, CardPayment, and WalletPayment
  can seamlessly substitute PaymentMethod without breaking the client contract.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import uuid

class PaymentMethod(ABC):
    """
    Abstract Base Strategy for Payment Methods (OCP / LSP).
    All concrete strategies must implement process_transaction.
    """
    @abstractmethod
    def process_transaction(self, amount: float, details: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Executes mock transaction.
        Returns:
            Tuple[success: bool, transaction_id: str, message: str]
        """
        pass

    @property
    @abstractmethod
    def mode_name(self) -> str:
        """Returns the identifier name of the payment mode."""
        pass


class UPIPayment(PaymentMethod):
    """
    Concrete Strategy: UPI Payment (Unified Payments Interface)
    LSP: Drop-in replacement for PaymentMethod.
    """
    @property
    def mode_name(self) -> str:
        return "UPI"

    def process_transaction(self, amount: float, details: Dict[str, Any]) -> Tuple[bool, str, str]:
        upi_id = details.get("upi_id", "user@upi")
        txn_id = f"UPI-{uuid.uuid4().hex[:8].upper()}"
        # Simulate gateway success (or failure if explicitly specified)
        if "fail" in str(upi_id).lower():
            return False, txn_id, "UPI transaction rejected by issuing bank."
        return True, txn_id, f"UPI payment of ₹{amount:.2f} successful via {upi_id}."


class CardPayment(PaymentMethod):
    """
    Concrete Strategy: Credit / Debit Card Payment
    LSP: Drop-in replacement for PaymentMethod.
    """
    @property
    def mode_name(self) -> str:
        return "Card"

    def process_transaction(self, amount: float, details: Dict[str, Any]) -> Tuple[bool, str, str]:
        card_no = details.get("card_number", "4111222233334444")
        masked_card = f"****-****-****-{str(card_no)[-4:]}"
        txn_id = f"CARD-{uuid.uuid4().hex[:8].upper()}"
        if "0000" in str(card_no):
            return False, txn_id, "Card declined: insufficient funds or invalid card."
        return True, txn_id, f"Card payment of ₹{amount:.2f} approved on card ending in {masked_card}."


class WalletPayment(PaymentMethod):
    """
    Concrete Strategy: Digital Wallet Payment (Paytm, PhonePe, AmazonPay)
    LSP: Drop-in replacement for PaymentMethod.
    """
    @property
    def mode_name(self) -> str:
        return "Wallet"

    def process_transaction(self, amount: float, details: Dict[str, Any]) -> Tuple[bool, str, str]:
        provider = details.get("wallet_provider", "Digital Wallet")
        txn_id = f"WAL-{uuid.uuid4().hex[:8].upper()}"
        if "fail" in str(provider).lower():
            return False, txn_id, "Wallet gateway timeout."
        return True, txn_id, f"Wallet debited ₹{amount:.2f} successfully via {provider}."


class PaymentStrategyFactory:
    """
    Factory creating payment strategies dynamically based on requested mode.
    Enforces OCP and eliminates hardcoded switch statements in business services.
    """
    _strategies: Dict[str, PaymentMethod] = {
        "UPI": UPIPayment(),
        "Card": CardPayment(),
        "Wallet": WalletPayment(),
    }

    @classmethod
    def get_strategy(cls, mode: str) -> PaymentMethod:
        strategy = cls._strategies.get(mode)
        if not strategy:
            raise ValueError(f"Unsupported payment mode '{mode}'. Supported modes: {list(cls._strategies.keys())}")
        return strategy

    @classmethod
    def register_strategy(cls, mode: str, strategy: PaymentMethod):
        """Allows runtime extension of new payment strategies without modifying existing codebase (OCP)."""
        cls._strategies[mode] = strategy
