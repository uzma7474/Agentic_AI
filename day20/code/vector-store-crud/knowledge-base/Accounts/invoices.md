# Invoice Processing Policy

## Purpose

This document describes how invoices are received, validated, approved, and paid
by the Accounts department.

## Submission Channels

Vendors may submit invoices through one of the following channels:

- The Finance Portal at https://finance.example.com/invoices (preferred)
- Email to invoices@example.com with the invoice as a PDF attachment
- Physical mail to the Accounts Payable desk (only for amounts above USD 50,000)

Invoices submitted by any other channel will be rejected and returned to the sender.

## Required Fields

Every invoice must contain:

- Vendor legal name and tax identifier
- Unique invoice number
- Invoice date and due date
- Line items with quantity, unit price, and total
- Purchase Order (PO) number if the amount exceeds USD 5,000
- Bank account details matching the vendor master record

Invoices missing any of these fields are placed in the "On Hold" queue.

## Approval Workflow

Invoices are routed based on amount:

- Up to USD 1,000: automatic approval if the PO matches
- USD 1,001 – USD 10,000: line manager approval
- USD 10,001 – USD 50,000: department head approval
- Above USD 50,000: CFO approval

Approvers receive a daily digest email at 9:00 AM local time.

## Payment Terms

Standard payment terms are Net 30 from the invoice date. Early payment discounts
of 2% are applied automatically when the vendor offers Net 10 terms.

## Common Rejection Reasons

- Invoice number already used (duplicate)
- PO number does not match any open purchase order
- Bank details differ from the vendor master record
- Tax identifier is invalid or expired

## Contact

For questions, contact accounts-payable@example.com.
