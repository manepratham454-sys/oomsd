import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import apiClient from '../api/client';
import { useNotifications } from '../context/NotificationContext';
import {
  CreditCard,
  QrCode,
  Wallet,
  CheckCircle2,
  AlertCircle,
  FileText,
  Printer,
  X,
  ShieldCheck,
  Download,
} from 'lucide-react';

export const Payments = () => {
  const location = useLocation();
  const passedSessionId = location.state?.sessionId;
  const { fetchNotifications } = useNotifications();

  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);

  // Payment checkout modal state
  const [payModalOpen, setPayModalOpen] = useState(!!passedSessionId);
  const [sessionId, setSessionId] = useState(passedSessionId || '');
  const [paymentMode, setPaymentMode] = useState('UPI'); // UPI, Card, Wallet
  const [upiId, setUpiId] = useState('rahul@okaxis');
  const [cardNumber, setCardNumber] = useState('4532889922114433');
  const [walletProvider, setWalletProvider] = useState('Paytm');
  const [submitting, setSubmitting] = useState(false);
  const [payError, setPayError] = useState('');

  // Invoice modal state
  const [invoiceModalOpen, setInvoiceModalOpen] = useState(false);
  const [currentInvoice, setCurrentInvoice] = useState(null);

  const fetchPayments = async () => {
    try {
      const res = await apiClient.get('/payments/my');
      setPayments(res.data);
    } catch (err) {
      console.error("Failed to load payments", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleProcessPayment = async (e) => {
    e.preventDefault();
    setPayError('');
    setSubmitting(true);

    try {
      const payload = {
        session_id: parseInt(sessionId),
        payment_mode: paymentMode,
      };
      if (paymentMode === 'UPI') payload.upi_id = upiId;
      if (paymentMode === 'Card') payload.card_number = cardNumber;
      if (paymentMode === 'Wallet') payload.wallet_provider = walletProvider;

      const res = await apiClient.post('/payments', payload);
      setPayModalOpen(false);
      await fetchPayments();
      fetchNotifications();
      // Auto open invoice for completed payment
      handleViewInvoice(res.data.id);
    } catch (err) {
      setPayError(err.response?.data?.detail || "Payment processing failed.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleViewInvoice = async (paymentId) => {
    try {
      const res = await apiClient.get(`/payments/${paymentId}/invoice`);
      setCurrentInvoice(res.data);
      setInvoiceModalOpen(true);
    } catch (err) {
      alert("Failed to retrieve tax invoice.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <CreditCard className="w-6 h-6 text-evgreen-400" /> Billing & Payment Settlements
          </h1>
          <p className="text-slate-400 text-xs mt-1">
            Settlement records, Strategy-based mock gateway payments, and official GST tax invoices.
          </p>
        </div>

        <button
          onClick={() => {
            setPayModalOpen(true);
            setPayError('');
          }}
          className="py-2.5 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green self-start sm:self-auto"
        >
          + Make a Payment
        </button>
      </div>

      {/* Payment History Table */}
      <div className="glass-panel rounded-3xl border border-navy-700 overflow-hidden">
        <div className="p-6 border-b border-navy-800 flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-evgreen-400" /> Transaction Ledger ({payments.length})
          </h2>
          <span className="text-xs text-slate-400">All amounts in INR (₹)</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            Loading billing records...
          </div>
        ) : payments.length === 0 ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            No completed payment transactions on record yet.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-navy-900/80 text-slate-400 uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="py-3.5 px-6">Transaction ID</th>
                  <th className="py-3.5 px-6">Session ID</th>
                  <th className="py-3.5 px-6">Payment Mode</th>
                  <th className="py-3.5 px-6">Amount</th>
                  <th className="py-3.5 px-6">Status</th>
                  <th className="py-3.5 px-6">Settled On</th>
                  <th className="py-3.5 px-6 text-right">Invoice</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy-800/80 text-slate-200">
                {payments.map((p) => (
                  <tr key={p.id} className="hover:bg-navy-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono font-semibold text-white">{p.transaction_id}</td>
                    <td className="py-4 px-6">#{p.session_id}</td>
                    <td className="py-4 px-6">
                      <span className="px-2 py-0.5 rounded bg-navy-800 text-slate-300 border border-navy-700 font-medium">
                        {p.payment_mode}
                      </span>
                    </td>
                    <td className="py-4 px-6 font-bold text-emerald-400">₹{p.amount.toFixed(2)}</td>
                    <td className="py-4 px-6">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                        {p.status}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {new Date(p.created_at).toLocaleDateString()} {new Date(p.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={() => handleViewInvoice(p.id)}
                        className="py-1 px-3 bg-navy-800 hover:bg-navy-700 text-slate-200 rounded-lg text-xs font-semibold inline-flex items-center gap-1 transition-colors"
                      >
                        <FileText className="w-3.5 h-3.5 text-evgreen-400" /> View Tax Invoice
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Payment Gateway Modal (OCP Strategy Selection) */}
      {payModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="glass-panel w-full max-w-md p-6 sm:p-8 rounded-3xl border border-navy-700 shadow-2xl relative">
            <button
              onClick={() => setPayModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 mb-1">
              <ShieldCheck className="w-5 h-5 text-evgreen-400" />
              <h3 className="text-xl font-bold text-white">Payment Gateway</h3>
            </div>
            <p className="text-xs text-slate-400 mb-6">
              Strategy Pattern: Select from interchangeable payment strategies.
            </p>

            {payError && (
              <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-2.5 text-xs text-red-300">
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                <span>{payError}</span>
              </div>
            )}

            <form onSubmit={handleProcessPayment} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Session ID to Settle
                </label>
                <input
                  type="number"
                  required
                  value={sessionId}
                  onChange={(e) => setSessionId(e.target.value)}
                  placeholder="e.g. 1"
                  className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                />
              </div>

              {/* Payment Mode Selection */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Payment Method (Strategy)
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { mode: 'UPI', icon: QrCode, label: 'UPI' },
                    { mode: 'Card', icon: CreditCard, label: 'Card' },
                    { mode: 'Wallet', icon: Wallet, label: 'Wallet' },
                  ].map((m) => {
                    const Icon = m.icon;
                    const selected = paymentMode === m.mode;
                    return (
                      <button
                        type="button"
                        key={m.mode}
                        onClick={() => setPaymentMode(m.mode)}
                        className={`py-3 px-2 rounded-xl border flex flex-col items-center gap-1.5 transition-all ${
                          selected
                            ? 'bg-navy-800 border-evgreen-500 text-evgreen-400 shadow-glow-green'
                            : 'bg-navy-900 border-navy-800 text-slate-400 hover:text-white'
                        }`}
                      >
                        <Icon className="w-5 h-5" />
                        <span className="text-xs font-bold">{m.label}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Strategy Specific Mock Inputs */}
              {paymentMode === 'UPI' && (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    VPA / UPI ID
                  </label>
                  <input
                    type="text"
                    required
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    placeholder="user@upi"
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                  />
                </div>
              )}

              {paymentMode === 'Card' && (
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Card Number
                    </label>
                    <input
                      type="text"
                      required
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      placeholder="4111 2222 3333 4444"
                      className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500 font-mono"
                    />
                  </div>
                </div>
              )}

              {paymentMode === 'Wallet' && (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Digital Wallet Provider
                  </label>
                  <select
                    value={walletProvider}
                    onChange={(e) => setWalletProvider(e.target.value)}
                    className="w-full py-2.5 px-3 bg-navy-900 border border-navy-700 rounded-xl text-white text-xs focus:ring-2 focus:ring-evgreen-500"
                  >
                    <option value="Paytm">Paytm Wallet</option>
                    <option value="PhonePe">PhonePe Wallet</option>
                    <option value="AmazonPay">Amazon Pay</option>
                  </select>
                </div>
              )}

              <button
                type="submit"
                disabled={submitting}
                className="w-full mt-2 py-3 px-4 rounded-xl bg-gradient-to-r from-evgreen-500 to-emerald-600 hover:from-evgreen-400 text-navy-950 font-bold text-xs shadow-glow-green flex items-center justify-center gap-2 transition-transform transform active:scale-95 disabled:opacity-50"
              >
                {submitting ? 'Processing Transaction...' : `Authorize ${paymentMode} Payment`}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Tax Invoice Modal */}
      {invoiceModalOpen && currentInvoice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-navy-950/80 backdrop-blur-md animate-in fade-in">
          <div className="bg-slate-900 w-full max-w-xl p-8 rounded-3xl border border-navy-700 shadow-2xl relative text-slate-100">
            <button
              onClick={() => setInvoiceModalOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Printable Invoice Header */}
            <div className="flex justify-between items-start pb-6 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-lg bg-emerald-500 flex items-center justify-center">
                    <Zap className="w-4 h-4 text-slate-900 fill-slate-900" />
                  </div>
                  <span className="font-black text-lg text-white">EVCSMS TAX INVOICE</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Smart Grid EV Charging Services</p>
              </div>

              <div className="text-right">
                <span className="font-mono text-xs font-bold text-emerald-400 block">{currentInvoice.invoice_number}</span>
                <span className="text-[10px] text-slate-400">Date: {new Date(currentInvoice.created_at).toLocaleDateString()}</span>
              </div>
            </div>

            {/* Billed To & Station Info */}
            <div className="grid grid-cols-2 gap-4 my-6 text-xs">
              <div>
                <span className="text-slate-500 font-semibold uppercase text-[10px] block">Customer Details</span>
                <strong className="text-white block mt-0.5">{currentInvoice.user_name}</strong>
                <span className="text-slate-400">{currentInvoice.user_email}</span>
              </div>
              <div className="text-right">
                <span className="text-slate-500 font-semibold uppercase text-[10px] block">Charging Station</span>
                <strong className="text-white block mt-0.5">{currentInvoice.station_name}</strong>
                <span className="text-slate-400">{currentInvoice.station_address || 'Maharashtra'}</span>
              </div>
            </div>

            {/* Itemized Energy Calculations */}
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between text-slate-400">
                <span>Charger Hardware:</span>
                <strong className="text-slate-200">{currentInvoice.charger_type} ({currentInvoice.power_kw} kW)</strong>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Energy Delivered:</span>
                <strong className="text-white">{currentInvoice.units_consumed} kWh</strong>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Base Tariff Rate:</span>
                <strong className="text-slate-200">₹{currentInvoice.price_per_unit.toFixed(2)} / kWh</strong>
              </div>
              <div className="flex justify-between text-slate-400 pt-2 border-t border-slate-800">
                <span>Taxable Amount (Net):</span>
                <span>₹{currentInvoice.amount.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>GST (18% SGST + CGST):</span>
                <span>₹{currentInvoice.tax_amount.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm font-bold text-white pt-2 border-t border-slate-800">
                <span>Total Paid ({currentInvoice.payment_mode}):</span>
                <span className="text-emerald-400">₹{currentInvoice.total_payable.toFixed(2)}</span>
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between text-[11px] text-slate-400">
              <span>Txn Reference: <strong className="font-mono text-slate-300">{currentInvoice.transaction_id}</strong></span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">PAID</span>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => window.print()}
                className="py-2 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 transition-colors"
              >
                <Printer className="w-3.5 h-3.5" /> Print / Save PDF
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
