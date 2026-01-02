import uuid
import random
from apps.payment.models import Payment

PREMIUM_PRICE = 40000


class PaymentService:
    @staticmethod
    def process_payment(user, provider, force_fail=False):
        """
        Simulates a payment via PayPal or bank sandbox.
        Always returns success for testing.
        """
        transaction_id = str(uuid.uuid4())

        if force_fail:
            status = "FAILED"
        else:
            status = "SUCCESS"

        # Save payment record
        payment = Payment.objects.create(
            user=user,
            provider=provider,
            amount=PREMIUM_PRICE,
            status=status,
            transaction_id=transaction_id
        )

        return payment, status
